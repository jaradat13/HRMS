from django.contrib.auth.decorators import login_required
from django.views.generic import View
from payroll.models import PayPeriod, Payroll
from .models import EmployeeSSPercentage, CompanySSPercentage
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from openpyxl import Workbook
from decimal import Decimal
from .models import SocialSecurityDeductions
from django.shortcuts import render, redirect
from .forms import EmployeeSSPercentageForm, CompanySSPercentageForm


@login_required
def list_ss_percentages(request):
    employee_percentage = EmployeeSSPercentage.objects.first()
    company_percentage = CompanySSPercentage.objects.first()
    context = {
        'employee_percentage': employee_percentage,
        'company_percentage': company_percentage,
    }
    return render(request, 'socialsecurity/ss_percentage_list.html', context)


@login_required
def set_ss_percentage(request):
    if request.method == 'POST':
        employee_form = EmployeeSSPercentageForm(request.POST, prefix='employee')
        company_form = CompanySSPercentageForm(request.POST, prefix='company')
        if employee_form.is_valid() and company_form.is_valid():
            employee_form.save()
            company_form.save()
            return redirect('list_ss_percentages')  # Redirect to success page after successful form submission
    else:
        employee_form = EmployeeSSPercentageForm(prefix='employee')
        company_form = CompanySSPercentageForm(prefix='company')
    return render(request, 'socialsecurity/ss_percentage_form.html',
                  {'employee_form': employee_form, 'company_form': company_form})


@login_required
def edit_ss_percentage(request, employee_id, company_id):
    employee_instance = get_object_or_404(EmployeeSSPercentage, pk=employee_id)
    company_instance = get_object_or_404(CompanySSPercentage, pk=company_id)

    if request.method == 'POST':
        employee_form = EmployeeSSPercentageForm(request.POST, instance=employee_instance, prefix='employee')
        company_form = CompanySSPercentageForm(request.POST, instance=company_instance, prefix='company')

        if employee_form.is_valid() and company_form.is_valid():
            employee_form.save()
            company_form.save()
            return redirect('list_ss_percentages')  # Redirect to a success page
    else:
        employee_form = EmployeeSSPercentageForm(instance=employee_instance, prefix='employee')
        company_form = CompanySSPercentageForm(instance=company_instance, prefix='company')

    return render(request, 'socialsecurity/ss_percentage_form.html', {
        'employee_form': employee_form,
        'company_form': company_form
    })


@login_required
def calculate_ss_deductions(pay_period_id):
    try:
        pay_period = get_object_or_404(PayPeriod, id=pay_period_id)
        payrolls = Payroll.objects.filter(pay_period=pay_period)

        # Retrieve employee_ss_deduction_percentage, set to 0 if not found
        employee_ss_percentage_object = EmployeeSSPercentage.objects.first()
        if employee_ss_percentage_object:
            employee_ss_deduction_percentage = employee_ss_percentage_object.percentage
        else:
            employee_ss_deduction_percentage = 0

        company_ss_percentage_object = CompanySSPercentage.objects.first()

        # Set company_ss_deduction_percentage to 0 if not found
        if company_ss_percentage_object:
            company_ss_deduction_percentage = company_ss_percentage_object.percentage
        else:
            company_ss_deduction_percentage = 0

        ss_deductions_data = []
        total_employee_ss_deduction = Decimal('0')
        total_company_ss_deduction = Decimal('0')
        for payroll in payrolls:
            employee = payroll.employee
            basic_salary = payroll.basic_salary

            # Sum up allowance amounts for the current payroll
            allowance_amount = sum(allowance.amount for allowance in payroll.employee.allowances.all())

            total_salary = basic_salary + allowance_amount

            # Check if employee's hire date meets the condition
            if employee.hire_date.day >= 15 and employee.hire_date.month == pay_period.month:
                employee_ss_deduction = Decimal('0')
                company_ss_deduction = Decimal('0')
            else:
                employee_ss_deduction = employee_ss_deduction_percentage * total_salary / 100
                company_ss_deduction = company_ss_deduction_percentage * total_salary / 100

            total_employee_ss_deduction += employee_ss_deduction
            total_company_ss_deduction += company_ss_deduction

            ss_deductions_data.append({
                'employee_name': f"{payroll.employee.first_name} {payroll.employee.last_name}",
                'hire_date': employee.hire_date,
                'position': employee.job_title,
                'basic_salary': basic_salary,
                'allowance': allowance_amount,
                'ssn_number': employee.social_security_number,
                'employee_ss_deduction': employee_ss_deduction,
                'company_ss_deduction': company_ss_deduction
            })
        total_ss_deduction = total_employee_ss_deduction + total_company_ss_deduction

        return {
            'ss_deductions_data': ss_deductions_data,
            'total_employee_ss_deduction': total_employee_ss_deduction,
            'total_company_ss_deduction': total_company_ss_deduction,
            'total_ss_deduction': total_ss_deduction
        }
    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {e}")


@login_required
def calculate_and_show_ss_deductions(request, pay_period_id):
    try:
        ss_data = calculate_ss_deductions(pay_period_id)
        pay_period = get_object_or_404(PayPeriod, id=pay_period_id)
        context = {'pay_period': pay_period, **ss_data}
        return render(request, 'socialsecurity/ss_sheet.html', context)
    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {e}")


@login_required
class ExportSocialSecurityDeductionsView(View):
    def get(self, request, pay_period_id, *args, **kwargs):
        try:
            pay_period = PayPeriod.objects.get(id=pay_period_id)
        except PayPeriod.DoesNotExist:
            return HttpResponse("Pay period does not exist", status=404)

        payrolls = Payroll.objects.filter(pay_period=pay_period)
        workbook = Workbook()
        worksheet = workbook.active
        headers = [
            'Employee ID', 'Employee Name', 'Basic Salary', 'Total Allowances', 'Net Salary',
            'Social Security Number', 'Employee Share', 'Company Share'
        ]
        worksheet.append(headers)

        for payroll in payrolls:
            # Calculate the social security deductions here
            employee_ss_deduction = payroll.employee_ss_deduction
            company_ss_deduction = payroll.company_ss_deduction

            # Create SocialSecurityDeduction instance
            social_security_deduction = SocialSecurityDeductions.objects.create(
                employee=payroll.employee,
                pay_period=pay_period,
                employee_ss_deduction=employee_ss_deduction,
                company_ss_deduction=company_ss_deduction
            )

            # Append payroll data to the Excel worksheet
            payroll_data = [
                str(payroll.employee.pk),
                f"{payroll.employee.first_name} {payroll.employee.last_name}",
                payroll.basic_salary,
                payroll.total_allowance,
                payroll.net_salary,
                payroll.employee.social_security_number,
                payroll.employee_ss_deduction,
                payroll.company_ss_deduction
            ]
            worksheet.append(payroll_data)

        # Save the workbook to the response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response[
            'Content-Disposition'] = f'attachment; filename="{pay_period.year}_{pay_period.month}_SS_deductions.xlsx"'
        workbook.save(response)
        return response
