from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from allowance.models import (HousingAllowance, UniformAllowance, MedicalAllowance, OtherAllowance, TravelAllowance,
                              MobileAllowance)
from core.models import JobTitle, Department, Section
from employee.forms import EmployeeForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from openpyxl import Workbook
from employee.models import Nationality, EmploymentType, Degree, Certification
from django.db import transaction
from .models import Employee
from .forms import EmployeeImportForm
import pandas as pd


@login_required
def employee_list_view(request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee_list.html', {'employees': employees})


@login_required
def employee_detail_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee/employee_detail.html', {'employee': employee})


@login_required
def employee_create_view(request):
    form = EmployeeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('employee-list')
    return render(request, 'employee/employee_form.html', {'form': form})


@login_required
def employee_update_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, request.FILES or None, instance=employee)
    if form.is_valid():
        employee = form.save(commit=False)
        if request.user.is_authenticated:  # Check if user is authenticated
            employee.edited_by = request.user  # Set the user making the change
        else:
            # Handle the case where user is not authenticated
            pass
        employee.save()
        form.save_m2m()
        return redirect('employee-list')
    return render(request, 'employee/employee_form.html', {'form': form})


@login_required
def employee_delete_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee-list')
    return render(request, 'employee/employee_confirm_delete.html', {'employee': employee})


@login_required
def employee_search(request):
    # Get the query string from the URL parameters
    query = request.GET.get('q')

    # Initialize the results variable
    results = []

    # Check if a query string exists
    if query:
        # Perform the search query using Q object
        results = Employee.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(employee_id__icontains=query)
        )

    # Render the template with the search results
    return render(request, 'employee/employee_search.html', {'results': results, 'query': query})


class ExportEmployeesExcelView(View):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        workbook = Workbook()
        worksheet = workbook.active

        headers = ['ID Number', 'First Name', 'Second Name', 'Last Name', 'Date of Birth',
                   'Nationality', 'National ID Number', 'ID Expiry Date', 'Gender', 'Marital Status',
                   'Phone Number', 'Email', 'Address', 'Emergency Contact Name', 'Emergency Contact Phone',
                   'Number of Dependents', 'Department', 'Section', 'Job Title', 'EmploymentType', 'Hire Date',
                   'Contract Expiry Date', 'Degree', 'Certification', 'Social Security Number',
                   'Tax identification Number', 'Bank Name', 'Bank Branch', 'Bank Account Number',
                   'Basic Salary', 'Mobile Allowance', 'Housing Allowance', 'Travel Allowance', 'Uniform Allowance',
                   'Medical Allowance', 'Other Allowance']
        worksheet.append(headers)

        for employee in employees:
            allowances = [
                employee.mobile_allowance.amount if employee.mobile_allowance else None,
                employee.housing_allowance.amount if employee.housing_allowance else None,
                employee.travel_allowance.amount if employee.travel_allowance else None,
                employee.uniform_allowance.amount if employee.uniform_allowance else None,
                employee.medical_allowance.amount if employee.medical_allowance else None,
                employee.other_allowance.amount if employee.other_allowance else None
            ]

            row_data = [
                employee.employee_id, employee.first_name, employee.second_name, employee.last_name,
                employee.date_of_birth, employee.nationality.name, employee.national_id_number,
                employee.id_expiry_date, employee.gender, employee.marital_status,
                employee.phone_number, employee.email, employee.address,
                employee.emergency_contact_name, employee.emergency_contact_phone,
                employee.number_of_dependents, employee.department.name,
                employee.section.name, employee.job_title.name,
                employee.employment_type.name, employee.hire_date,
                employee.contract_expiry_date, employee.degree.name,
                employee.certification.name, employee.social_security_number,
                employee.tax_identification_number, employee.bank_name,
                employee.bank_branch, employee.bank_account_number,
                employee.basic_salary, *allowances
            ]

            worksheet.append(row_data)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
        workbook.save(response)
        return response


@login_required
@transaction.atomic
def import_employees(request):
    if request.method == 'POST':
        form = EmployeeImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                employee_id = row.get('ID Number')
                # Check if an employee with the same unique identifier exists
                if Employee.objects.filter(employee_id=employee_id).exists():
                    continue  # Skip importing this row

                # Fetch or create department, section, and job title for each row
                department_name = row.get('Department', 'Default Department')
                department, _ = Department.objects.get_or_create(name=department_name)

                nationality_name = row.get('Nationality', 'Default')
                nationality, _ = Nationality.objects.get_or_create(name=nationality_name)

                employment_type_name = row.get('EmploymentType', 'Default')
                employment_type, _ = EmploymentType.objects.get_or_create(name=employment_type_name)

                degree_name = row.get('Degree', 'Default')
                degree, _ = Degree.objects.get_or_create(name=degree_name)

                certification_name = row.get('Certification', 'Default')
                certification, _ = Certification.objects.get_or_create(name=certification_name)

                section_name = row.get('Section', 'Default Section')
                section, _ = Section.objects.get_or_create(name=section_name, department=department)

                job_title_name = row.get('Job Title', 'Default Job Title')
                job_title, _ = JobTitle.objects.get_or_create(name=job_title_name, department=department)

                # Fetch or create related allowances for each row
                travel_allowance_amount = row.get('Travel Allowance', 'Default Travel Allowance')
                travel_allowance_instance, _ = TravelAllowance.objects.get_or_create(amount=travel_allowance_amount)

                mobile_allowance_amount = row.get('Mobile Allowance', 'Default Mobile Allowance')
                mobile_allowance_instance, _ = MobileAllowance.objects.get_or_create(amount=mobile_allowance_amount)

                housing_allowance_amount = row.get('Housing Allowance', 'Default Housing Allowance')
                housing_allowance_instance, _ = HousingAllowance.objects.get_or_create(amount=housing_allowance_amount)

                medical_allowance_amount = row.get('Medical Allowance', 'Default Medical Allowance')
                medical_allowance_instance, _ = MedicalAllowance.objects.get_or_create(amount=medical_allowance_amount)

                uniform_allowance_amount = row.get('Uniform Allowance', 'Default Uniform Allowance')
                uniform_allowance_instance, _ = UniformAllowance.objects.get_or_create(amount=uniform_allowance_amount)

                other_allowance_amount = row.get('Other Allowance', 'Default Other Allowance')
                other_allowance_instance, _ = OtherAllowance.objects.get_or_create(amount=other_allowance_amount)

                # Create employee object for each row
                employee = Employee(
                    employee_id=row['ID Number'],
                    first_name=row['First Name'],
                    second_name=row['Second Name'],
                    last_name=row['Last Name'],
                    date_of_birth=row['Date of Birth'],
                    nationality=nationality,
                    national_id_number=row['National ID Number'],
                    id_expiry_date=row['ID Expiry Date'],
                    gender=row['Gender'],
                    marital_status=row['Marital Status'],
                    phone_number=row['Phone Number'],
                    email=row['Email'],
                    address=row['Address'],
                    emergency_contact_name=row['Emergency Contact Name'],
                    emergency_contact_phone=row['Emergency Contact Phone'],
                    number_of_dependents=row['Number of Dependents'],
                    employment_type=employment_type,
                    hire_date=row['Hire Date'],
                    contract_expiry_date=row['Contract Expiry Date'],
                    degree=degree,
                    certification=certification,
                    social_security_number=row['Social Security Number'],
                    tax_identification_number=row['Tax identification Number'],
                    bank_name=row['Bank Name'],
                    bank_branch=row['Bank Branch'],
                    bank_account_number=row['Bank Account Number'],
                    basic_salary=row['Basic Salary'],
                    department=department,
                    section=section,
                    job_title=job_title,
                    mobile_allowance=mobile_allowance_instance,
                    housing_allowance=housing_allowance_instance,
                    travel_allowance=travel_allowance_instance,
                    medical_allowance=medical_allowance_instance,
                    uniform_allowance=uniform_allowance_instance,
                    other_allowance=other_allowance_instance,
                    # Map other fields accordingly
                )
                employee.save()

            return render(request, 'employee/employee_list.html')
    else:
        form = EmployeeImportForm()
    return render(request, 'employee/import_employees.html', {'form': form})
