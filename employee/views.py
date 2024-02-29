from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from allowance.models import HousingAllowance, UniformAllowance, MedicalAllowance, \
    OtherAllowance
from allowance.models import TravelAllowance, MobileAllowance
from core.models import JobTitle, Department, Section
from .forms import EmployeeForm, EmployeeImportForm
import pandas as pd
from django.http import HttpResponse
from django.views.generic import View
from openpyxl import Workbook
from django.shortcuts import render, get_object_or_404
from .models import Employee



def employee_list_view(request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee_list.html', {'employees': employees})


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


def employee_delete_view(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee-list')
    return render(request, 'employee/employee_confirm_delete.html', {'employee': employee})


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
    @staticmethod
    def get(self, request, *args, **kwargs):
        # Query all employees
        employees = Employee.objects.all()

        # Create a new Excel workbook and select the active worksheet
        workbook = Workbook()
        worksheet = workbook.active

        # Define column headers
        headers = ['ID Number', 'First Name', 'Second Name', 'Last Name', 'Date of Birth',
                   'Nationality', 'National ID Number', 'ID Expiry Date', 'Gender', 'Marital Status',
                   'Phone Number', 'Email', 'Address', 'Emergency Contact Name', 'Emergency Contact Phone',
                   'Number of Dependents', 'Department', 'Section', 'Job Title', 'Employment Type', 'Hire Date',
                   'Contract Expiry Date', 'Degrees', 'Certifications', 'Social Security Number',
                   'Tax identification Number', 'Bank Name', 'Bank Branch', 'Bank Account Number',
                   'Basic Salary', 'Mobile Allowance', 'Housing Allowance', 'Travel Allowance', 'Uniform Allowance',
                   'Medical Allowance', 'Other Allowance']

        worksheet.append(headers)

        # Add employee data to the worksheet
        for employee in employees:
            # Serialize allowances
            allowances = [
                employee.mobile_allowance.amount,
                employee.housing_allowance.amount,
                employee.travel_allowance.amount,
                employee.uniform_allowance.amount,
                employee.medical_allowance.amount,
                employee.other_allowance.amount
            ]

            row_data = [
                employee.employee_id, employee.first_name, employee.second_name, employee.last_name,
                employee.date_of_birth, employee.nationality, employee.national_id_number,
                employee.id_expiry_date, employee.gender, employee.marital_status,
                employee.phone_number, employee.email, employee.address,
                employee.emergency_contact_name, employee.emergency_contact_phone,
                employee.number_of_dependents, employee.department.name,
                employee.section.name, employee.job_title.name,
                employee.employment_type, employee.hire_date,
                employee.contract_expiry_date, employee.degrees,
                employee.certifications, employee.social_security_number,
                employee.tax_identification_number, employee.bank_name,
                employee.bank_branch, employee.bank_account_number,
                employee.basic_salary, *allowances
            ]

            worksheet.append(row_data)

        # Create a response object
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'

        # Save the workbook content to the response
        workbook.save(response)

        return response


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

                section_name = row.get('Section', 'Default Section')

                try:
                    section = Section.objects.get(name=section_name, department=department)
                except Section.DoesNotExist:
                    section = Section.objects.create(name=section_name, department=department)

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
                    nationality=row['Nationality'],
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
                    employment_type=row['Employment Type'],
                    hire_date=row['Hire Date'],
                    contract_expiry_date=row['Contract Expiry Date'],
                    degrees=row['Degrees'],
                    certifications=row['Certifications'],
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




@login_required
def employee_history(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    history = employee.employeehistory_set.all()
    # Access history via the related name

    # Pass the authenticated user to the signal handler
    user = request.user

    return render(request, 'employee/employee_history.html', {
        'employee': employee,
        'history': history,
        'user': user  # Pass the authenticated user to the template context
    })