from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.views.generic import View
from openpyxl.workbook import Workbook
from employee.models import Employee
from incometax.models import IncomeTaxPercentage, IncomeTaxDeductions
from socialsecurity.models import EmployeeSSPercentage, CompanySSPercentage, SocialSecurityDeductions
from .models import PayPeriod, Payroll
from .forms import PayPeriodForm, PayrollForm
from django.shortcuts import redirect, reverse, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from allowance.models import AllowancePayments


@login_required
def pay_period_list_view(request):
    pay_periods = PayPeriod.objects.all()
    return render(request, 'payroll/pay_period_list.html', {'pay_periods': pay_periods})


@login_required
def pay_period_detail_view(request, pk):
    pay_period = get_object_or_404(PayPeriod, pk=pk)
    return render(request, 'payroll/pay_period_detail.html', {'pay_period': pay_period})


@login_required
def pay_period_create_view(request):
    form = PayPeriodForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('pay-period-list')
    return render(request, 'payroll/pay_period_form.html', {'form': form})


@login_required
def pay_period_update_view(request, pk):
    pay_period = get_object_or_404(PayPeriod, pk=pk)
    form = PayPeriodForm(request.POST or None, instance=pay_period)
    if form.is_valid():
        form.save()
        return redirect('pay-period-list')
    return render(request, 'payroll/pay_period_form.html', {'form': form})


@login_required
def pay_period_delete_view(request, pk):
    pay_period = get_object_or_404(PayPeriod, pk=pk)
    if request.method == 'POST':
        pay_period.delete()
        return redirect('pay-period-list')
    return render(request, 'payroll/pay_period_confirm_delete.html', {'pay_period': pay_period})


@login_required
def payroll_list_view(request, month, year):
    payrolls = Payroll.objects.filter(pay_period__month=month, pay_period__year=year).order_by('id')
    month_names = {
        "January": 1,
        "February": 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
    }
    month = month_names.get(month)

    # Calculate totals
    totals = payrolls.aggregate(
        total_basic_salary=Sum('basic_salary'),
        total_mobile_allowance=Sum('mobile_allowance'),
        total_travel_allowance=Sum('travel_allowance'),
        total_housing_allowance=Sum('housing_allowance'),
        total_medical_allowance=Sum('medical_allowance'),
        total_uniform_allowance=Sum('uniform_allowance'),
        total_other_allowance=Sum('other_allowance'),
        total_total_deductions=Sum('total_deductions'),
        total_total_allowance=Sum('total_allowance'),
        total_employee_ss_deduction=Sum('employee_ss_deduction'),
        total_income_tax_deduction=Sum('income_tax_deduction'),
        total_gross_salary=Sum('gross_salary'),
        total_other_deductions=Sum('other_deductions'),
        total_employee_total_deduction=Sum('employee_total_deduction'),
        total_net_salary=Sum('net_salary'),
    )

    paginator = Paginator(payrolls, 20)
    page_number = request.GET.get('page')
    try:
        payrolls = paginator.page(page_number)
    except PageNotAnInteger:
        payrolls = paginator.page(1)
    except EmptyPage:
        payrolls = paginator.page(paginator.num_pages)
    selected_month = timezone.datetime(year, month, 1).strftime('%B %Y')

    return render(request, 'payroll/payroll_list.html', {
        'payrolls': payrolls,
        'selected_month': selected_month,
        'totals': totals,
        'is_last_page': payrolls.number == paginator.num_pages
    })


@login_required
def payroll_detail_view(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    return render(request, 'payroll/payroll_detail.html', {'payroll': payroll})


def payroll_create_view(request):
    form = PayrollForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payroll-list')
    return render(request, 'payroll/payroll_form.html', {'form': form})


@login_required
def payroll_update_view(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    form = PayrollForm(request.POST or None, instance=payroll)
    if form.is_valid():
        form.save()
        return redirect('payroll-list')
    return render(request, 'payroll/payroll_form.html', {'form': form})


@login_required
def payroll_delete_view(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        payroll.delete()
        return redirect('payroll-list')
    return render(request, 'payroll/payroll_confirm_delete.html', {'payroll': payroll})


@login_required
@transaction.atomic
def generate_payroll(request):
    if request.method == 'POST':
        try:
            current_pay_period = PayPeriod.objects.get(is_closed=False)
        except PayPeriod.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No open pay period found.'})

        if Payroll.objects.filter(pay_period=current_pay_period).exists():
            return JsonResponse({'success': False, 'message': 'Payroll for this period already exists.'})

        employees = Employee.objects.filter(is_active=True)

        # Retrieve percentages or set to 0 if not found
        employee_ss_percentage = EmployeeSSPercentage.objects.first()
        employee_ss_percentage = employee_ss_percentage.percentage if employee_ss_percentage else 0

        company_ss_percentage = CompanySSPercentage.objects.first()
        company_ss_percentage = company_ss_percentage.percentage if company_ss_percentage else 0

        income_tax_percentage = IncomeTaxPercentage.objects.first()
        income_tax_percentage = income_tax_percentage.percentage if income_tax_percentage else 0

        payroll_records = []
        social_security_deductions = []
        allowance_payments = []  # Renamed from AllowancePayments
        income_tax_deductions = []

        for employee in employees:
            # Get fixed amount allowances
            mobile_allowance = Decimal(employee.mobile_allowance.amount) if employee.mobile_allowance else 0
            travel_allowance = Decimal(employee.travel_allowance.amount) if employee.travel_allowance else 0
            housing_allowance = Decimal(employee.housing_allowance.amount) if employee.housing_allowance else 0
            medical_allowance = Decimal(employee.medical_allowance.amount) if employee.medical_allowance else 0
            uniform_allowance = Decimal(employee.uniform_allowance.amount) if employee.uniform_allowance else 0
            other_deductions = Decimal(employee.other_deductions.amount) if employee.other_deductions else 0
            other_allowance = Decimal(employee.other_allowance.amount) if employee.other_allowance else 0

            # Calculate total allowance for the employee
            total_allowance = Decimal(
                mobile_allowance + travel_allowance + housing_allowance + medical_allowance + uniform_allowance +
                other_allowance)

            # Calculate gross salary including allowances
            gross_salary = Decimal(employee.basic_salary + total_allowance - other_deductions)

            # Calculate deductions
            employee_ss_deduction = Decimal(employee_ss_percentage * Decimal(
                gross_salary) / 100) if employee_ss_percentage != 0 else 0
            company_ss_deduction = Decimal(company_ss_percentage * Decimal(
                gross_salary) / 100) if company_ss_percentage != 0 else 0
            income_tax_deduction = Decimal(income_tax_percentage * Decimal(
                gross_salary) / 100) if income_tax_percentage != 0 else 0
            employee_total_deduction = Decimal(employee_ss_deduction + income_tax_deduction + other_deductions)

            total_deductions = Decimal(employee_ss_deduction) + Decimal(company_ss_deduction) + Decimal(
                income_tax_deduction) + Decimal(other_deductions)

            # Calculate net salary
            net_salary = Decimal(gross_salary) - Decimal(employee_total_deduction)

            # Create Payroll object
            payroll = Payroll(
                pay_period=current_pay_period,
                employee=employee,
                basic_salary=employee.basic_salary,
                employee_ss_deduction=employee_ss_deduction,
                company_ss_deduction=company_ss_deduction,
                income_tax_deduction=income_tax_deduction,
                gross_salary=gross_salary,
                net_salary=net_salary,
                total_allowance=total_allowance,
                total_deductions=total_deductions,
                mobile_allowance=mobile_allowance,
                travel_allowance=travel_allowance,
                housing_allowance=housing_allowance,
                medical_allowance=medical_allowance,
                uniform_allowance=uniform_allowance,
                other_allowance=other_allowance,
                other_deductions=other_deductions,
                employee_total_deduction=employee_total_deduction,
            )
            payroll_records.append(payroll)

            allowance_payment = AllowancePayments(
                employee=employee,
                pay_period=current_pay_period,
                mobile_allowance_payment=mobile_allowance,
                travel_allowance_payment=travel_allowance,
                housing_allowance_payment=housing_allowance,
                medical_allowance_payment=medical_allowance,
                uniform_allowance_payment=uniform_allowance,
                other_allowance_payment=other_allowance,
                total_allowance_payment=total_allowance,
            )
            allowance_payments.append(allowance_payment)

            # Create SocialSecurityDeductions object
            social_security_deduction = SocialSecurityDeductions(
                employee=employee,
                pay_period=current_pay_period,
                employee_ss_deduction=employee_ss_deduction,
                company_ss_deduction=company_ss_deduction
            )
            social_security_deductions.append(social_security_deduction)

            # Create IncomeTaxDeductions object
            income_tax_deduction = IncomeTaxDeductions(
                employee=employee,
                pay_period=current_pay_period,
                income_tax_deduction=income_tax_deduction
            )
            income_tax_deductions.append(income_tax_deduction)

        # Bulk create records
        Payroll.objects.bulk_create(payroll_records)
        SocialSecurityDeductions.objects.bulk_create(social_security_deductions)
        IncomeTaxDeductions.objects.bulk_create(income_tax_deductions)
        AllowancePayments.objects.bulk_create(allowance_payments)  # Save AllowancePayments instances

        return JsonResponse({'success': True, 'message': 'Payroll generated successfully.'})

    return HttpResponseBadRequest('Invalid request method. This operation requires a POST request.')


@login_required
def close_payroll_period(request, period_id):
    period = get_object_or_404(PayPeriod, pk=period_id)
    period.is_closed = True
    period.save()
    return redirect(reverse('pay-period-list'))


@login_required
class ExportPayrollExcelView(View):
    @staticmethod
    def get(request, pay_period_id, *args, **kwargs):
        pay_period = PayPeriod.objects.get(id=pay_period_id)
        payrolls = Payroll.objects.filter(pay_period=pay_period)
        workbook = Workbook()
        worksheet = workbook.active
        headers = [
            'Employee ID', 'Employee Name', 'Basic Salary', 'Mobile Allowance', 'Travel Allowance', 'Medical Allowance',
            'Housing Allowance', 'Uniform Allowance', 'Other Allowance', 'Total Allowances', 'Income Tax Deduction',
            'Employee SS Deduction',
            'Other Deductions', 'Employee Total Deductions', 'Net Salary'
        ]
        worksheet.append(headers)
        for payroll in payrolls:
            payroll_data = [
                payroll.employee.employee_id,
                f"{payroll.employee.first_name} {payroll.employee.last_name}",
                payroll.basic_salary,
                payroll.mobile_allowance,
                payroll.travel_allowance,
                payroll.medical_allowance,
                payroll.housing_allowance,
                payroll.uniform_allowance,
                payroll.other_allowance,
                payroll.total_allowance,
                payroll.income_tax_deduction,
                payroll.employee_ss_deduction,
                payroll.other_deductions,
                payroll.employee_total_deduction,
                payroll.net_salary,
            ]
            worksheet.append(payroll_data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{pay_period.year}_{pay_period.month}_payroll.xlsx"'
        workbook.save(response)
        return response


@login_required
def search_employee_payroll_view(request):
    if 'q' in request.GET:
        search_term = request.GET['q']
        by_name = Payroll.objects.filter(
            employee__first_name__icontains=search_term
        ) | Payroll.objects.filter(
            employee__last_name__icontains=search_term
        )
        by_id = Payroll.objects.filter(
            employee__employee_id__icontains=search_term
        )
        payrolls = by_name.union(by_id)
    else:
        payrolls = Payroll.objects.none()
    return render(request, 'payroll/payroll_search.html', {'payrolls': payrolls})
