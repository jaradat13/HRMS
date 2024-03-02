from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from openpyxl.workbook import Workbook

from payroll.models import PayPeriod, Payroll
from .models import IncomeTaxPercentage, IncomeTaxDeductions
from .forms import IncomeTaxPercentageForm


@login_required
def income_tax_percentage_list_view(request):
    income_tax_percentages = IncomeTaxPercentage.objects.all()
    return render(request, 'income_tax/income_tax_percentage_list.html',
                  {'income_tax_percentages': income_tax_percentages})


@login_required
def income_tax_percentage_detail_view(request, pk):
    income_tax_percentage = get_object_or_404(IncomeTaxPercentage, pk=pk)
    return render(request, 'income_tax/income_tax_percentage_detail.html',
                  {'income_tax_percentage': income_tax_percentage})


@login_required
def income_tax_percentage_create_view(request):
    form = IncomeTaxPercentageForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('income-tax-percentage-list')
    return render(request, 'income_tax/income_tax_percentage_form.html', {'form': form})


@login_required
def income_tax_percentage_update_view(request, pk):
    income_tax_percentage = get_object_or_404(IncomeTaxPercentage, pk=pk)
    form = IncomeTaxPercentageForm(request.POST or None, instance=income_tax_percentage)
    if form.is_valid():
        form.save()
        return redirect('income-tax-percentage-list')
    return render(request, 'income_tax/income_tax_percentage_form.html', {'form': form})


@login_required
def income_tax_percentage_delete_view(request, pk):
    income_tax_percentage = get_object_or_404(IncomeTaxPercentage, pk=pk)
    if request.method == 'POST':
        income_tax_percentage.delete()
        return redirect('income-tax-percentage-list')
    return render(request, 'income_tax/income_tax_percentage_confirm_delete.html',
                  {'income_tax_percentage': income_tax_percentage})


class IncomeTaxDeductionsExport(View):
    def get(self, request, pay_period_id, *args, **kwargs):
        try:
            pay_period = PayPeriod.objects.get(id=pay_period_id)
        except PayPeriod.DoesNotExist:
            return HttpResponse("Pay period does not exist", status=404)

        payrolls = Payroll.objects.filter(pay_period=pay_period)
        workbook = Workbook()
        worksheet = workbook.active
        headers = [
            'Employee ID', 'Employee Name', 'Basic Salary', 'Total Allowances', 'Net Salary', 'Income Tax',
        ]
        worksheet.append(headers)

        income_tax_deductions_instances = []

        for payroll in payrolls:
            # Calculate the income tax deductions here
            income_tax_deduction = payroll.income_tax_deduction

            # Append payroll data to the Excel worksheet
            payroll_data = [
                str(payroll.employee.pk),
                f"{payroll.employee.first_name} {payroll.employee.last_name}",
                payroll.basic_salary,
                payroll.total_allowance,
                payroll.net_salary,
                income_tax_deduction,
            ]
            worksheet.append(payroll_data)

            # Create IncomeTaxDeductions instances for all payrolls
            income_tax_deductions_instances.append(IncomeTaxDeductions(
                employee=payroll.employee,
                pay_period=pay_period,
                income_tax_deduction=income_tax_deduction,
            ))

        # Bulk create all IncomeTaxDeductions instances
        IncomeTaxDeductions.objects.bulk_create(income_tax_deductions_instances)

        # Save the workbook to the response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response[
            'Content-Disposition'] = (f'attachment; filename="{pay_period.year}_{pay_period.month}'
                                      f'_Income_tax_deductions.xlsx"')
        workbook.save(response)
        return response
