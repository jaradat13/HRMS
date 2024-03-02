from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl.workbook import Workbook
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from employee.models import Employee
from .forms import CompanyForm, DepartmentForm, SectionForm, JobTitleForm, LoginForm
from .models import Company, Department, Section, JobTitle

@login_required
def home(request):
    return render(request, 'home.html')


# Views for Department

def department_list_view(request):
    departments = Department.objects.annotate(num_employees=Count('employees'))
    return render(request, 'core/department_list.html', {'departments': departments})


def department_detail_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department_head = Employee.objects.filter(department=department, is_department_head=True).first()
    return render(request, 'core/department_detail.html',
                  {'department': department, 'department_head': department_head})


def department_create_view(request):
    form = DepartmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('department-list')
    return render(request, 'core/department_form.html', {'form': form})


def department_update_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, request.FILES or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('department-list')
    return render(request, 'core/department_form.html', {'form': form})


def department_delete_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department-list')
    return render(request, 'core/department_confirm_delete.html', {'department': department})


# Views for Company

def company_list_view(request):
    companies = Company.objects.all()
    return render(request, 'core/company_list.html', {'companies': companies})


def company_detail_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'core/company_detail.html', {'company': company})


def company_create_view(request):
    form = CompanyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('company-list')
    return render(request, 'core/company_form.html', {'form': form})


def company_update_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)
    if form.is_valid():
        form.save()
        return redirect('company-list')
    return render(request, 'core/company_form.html', {'form': form})


def company_delete_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('company-list')
    return render(request, 'core/company_confirm_delete.html', {'company': company})


# Views for Section
def section_list_view(request):
    sections = Section.objects.all()
    return render(request, 'core/section_list.html', {'sections': sections})


def section_detail_view(request, pk):
    section = get_object_or_404(Section, pk=pk)
    return render(request, 'core/section_detail.html', {'section': section})


def section_create_view(request):
    form = SectionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/section_form.html', {'form': form})


def section_update_view(request, pk):
    section = get_object_or_404(Section, pk=pk)
    form = SectionForm(request.POST or None, request.FILES or None, instance=section)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/section_form.html', {'form': form})


def section_delete_view(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        return redirect('section-list')
    return render(request, 'core/section_confirm_delete.html', {'section': section})


# Views for JobTitle
def jobtitle_list_view(request):
    jobtitles = JobTitle.objects.all()
    return render(request, 'core/jobtitle_list.html', {'jobtitles': jobtitles})


def jobtitle_detail_view(request, pk):
    jobtitle = get_object_or_404(JobTitle, pk=pk)
    return render(request, 'core/jobtitle_detail.html', {'jobtitle': jobtitle})


def jobtitle_create_view(request):
    form = JobTitleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/jobtitle_form.html', {'form': form})


def jobtitle_update_view(request, pk):
    jobtitle = get_object_or_404(JobTitle, pk=pk)
    form = JobTitleForm(request.POST or None, request.FILES or None, instance=jobtitle)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/jobtitle_form.html', {'form': form})


def jobtitle_delete_view(request, pk):
    jobtitle = get_object_or_404(JobTitle, pk=pk)
    if request.method == 'POST':
        jobtitle.delete()
        return redirect('jobtitle-list')
    return render(request, 'core/jobtitle_confirm_delete.html', {'jobtitle': jobtitle})


def export_department_employees_to_excel(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    employees = department.employees.all()

    # Create a new Workbook
    wb = Workbook()
    ws = wb.active

    # Add headers
    ws.append(['Name', 'Section', 'Job Title'])

    # Add employee data
    for employee in employees:
        ws.append([f"{employee.first_name} {employee.last_name}", employee.section.name, employee.job_title.name])

    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{department.name}_employees.xlsx"'

    # Save workbook to response
    wb.save(response)

    return response


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm  # Import the LoginForm class from forms.py
from django.contrib.auth import logout


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authentication Logic
        user = authenticate(request, username=username, password=password)

        if user is not None:  # Successful authentication
            login(request, user)
            return redirect('home')  # Redirect after successful login
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'core/login.html')
    else:
        return render(request, 'core/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')
