from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from openpyxl.workbook import Workbook
from employee.models import Employee
from .forms import CompanyForm, DepartmentForm, SectionForm, JobTitleForm
from .models import Company, Department, Section, JobTitle
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def department_list_view(request):
    departments = Department.objects.annotate(num_employees=Count('employees'))
    return render(request, 'core/department_list.html', {'departments': departments})


@login_required
def department_detail_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department_head = Employee.objects.filter(department=department, is_department_head=True).first()
    return render(request, 'core/department_detail.html',
                  {'department': department, 'department_head': department_head})


@login_required
def department_create_view(request):
    form = DepartmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('department-list')
    return render(request, 'core/department_form.html', {'form': form})


@login_required
def department_update_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, request.FILES or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('department-list')
    return render(request, 'core/department_form.html', {'form': form})


@login_required
def department_delete_view(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department-list')
    return render(request, 'core/department_confirm_delete.html', {'department': department})


@login_required
def company_list_view(request):
    companies = Company.objects.all()
    return render(request, 'core/company_list.html', {'companies': companies})


@login_required
def company_detail_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'core/company_detail.html', {'company': company})


@login_required
def company_create_view(request):
    form = CompanyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('company-list')
    return render(request, 'core/company_form.html', {'form': form})


@login_required
def company_update_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)
    if form.is_valid():
        form.save()
        return redirect('company-list')
    return render(request, 'core/company_form.html', {'form': form})


@login_required
def company_delete_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('company-list')
    return render(request, 'core/company_confirm_delete.html', {'company': company})


@login_required
# Views for Section
def section_list_view(request):
    sections = Section.objects.all()
    return render(request, 'core/section_list.html', {'sections': sections})


@login_required
def section_detail_view(request, pk):
    section = get_object_or_404(Section, pk=pk)
    return render(request, 'core/section_detail.html', {'section': section})


@login_required
def section_create_view(request):
    form = SectionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/section_form.html', {'form': form})


@login_required
def section_update_view(request, pk):
    section = get_object_or_404(Section, pk=pk)
    form = SectionForm(request.POST or None, request.FILES or None, instance=section)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/section_form.html', {'form': form})


@login_required
def section_delete_view(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        return redirect('section-list')
    return render(request, 'core/section_confirm_delete.html', {'section': section})


@login_required
def jobtitle_list_view(request):
    jobtitles = JobTitle.objects.all()
    return render(request, 'core/jobtitle_list.html', {'jobtitles': jobtitles})


@login_required
def jobtitle_detail_view(request, pk):
    jobtitle = get_object_or_404(JobTitle, pk=pk)
    return render(request, 'core/jobtitle_detail.html', {'jobtitle': jobtitle})


@login_required
def jobtitle_create_view(request):
    form = JobTitleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/jobtitle_form.html', {'form': form})


@login_required
def jobtitle_update_view(request, pk):
    jobtitle = get_object_or_404(JobTitle, pk=pk)
    form = JobTitleForm(request.POST or None, request.FILES or None, instance=jobtitle)
    if form.is_valid():
        form.save()
        return redirect('section-list')
    return render(request, 'core/jobtitle_form.html', {'form': form})


@login_required
def jobtitle_delete_view(request, pk):
    jobtitle = get_object_or_404(JobTitle, pk=pk)
    if request.method == 'POST':
        jobtitle.delete()
        return redirect('jobtitle-list')
    return render(request, 'core/jobtitle_confirm_delete.html', {'jobtitle': jobtitle})


@login_required
def export_department_employees_to_excel(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    employees = department.employees.all()

    # Create a new Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(['Name', 'Section', 'Job Title'])
    for employee in employees:
        ws.append([f"{employee.first_name} {employee.last_name}", employee.section.name, employee.job_title.name])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{department.name}_employees.xlsx"'
    wb.save(response)
    return response


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
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
