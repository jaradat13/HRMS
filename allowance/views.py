from django.shortcuts import get_object_or_404, redirect, render

from allowance.forms import MobileAllowanceForm, TravelAllowanceForm, MedicalAllowanceForm, HousingAllowanceForm, \
    UniformAllowanceForm, OtherAllowanceForm
from allowance.models import MobileAllowance, TravelAllowance, HousingAllowance, MedicalAllowance, OtherAllowance, \
    UniformAllowance


def allowance_list(request):
    mobile_allowances = MobileAllowance.objects.all()
    travel_allowances = TravelAllowance.objects.all()
    housing_allowances = HousingAllowance.objects.all()
    uniform_allowances = UniformAllowance.objects.all()
    medical_allowances = MedicalAllowance.objects.all()
    other_allowances = OtherAllowance.objects.all()
    return render(request, 'allowance/allowance_list.html', {'mobile_allowances': mobile_allowances,
                                                             'travel_allowances': travel_allowances,
                                                             'housing_allowances': housing_allowances,
                                                             'uniform_allowances': uniform_allowances,
                                                             'medical_allowances': medical_allowances,
                                                             'other_allowances': other_allowances})


def mobile_allowance_create(request):
    if request.method == 'POST':
        form = MobileAllowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = MobileAllowanceForm()
    return render(request, 'allowance/allowances_form.html', {'form': form})


def mobile_allowance_update(request, pk):
    allowance = get_object_or_404(MobileAllowance, pk=pk)
    if request.method == 'POST':
        form = MobileAllowanceForm(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = MobileAllowanceForm(instance=allowance)
    return render(request, 'allowance/allowances_form.html', {'form': form})


def mobile_allowance_delete(request, pk):
    allowance = get_object_or_404(MobileAllowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('allowance_list')
    return render(request, 'allowance/allowances_confirm_delete.html', {'allowance': allowance})


def travel_allowance_create(request):
    if request.method == 'POST':
        form = TravelAllowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = TravelAllowanceForm()
    return render(request, 'allowance/allowances_form.html', {'form': form})


def travel_allowance_update(request, pk):
    allowance = get_object_or_404(TravelAllowance, pk=pk)
    if request.method == 'POST':
        form = TravelAllowanceForm(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = TravelAllowanceForm(instance=allowance)
    return render(request, 'allowance/allowances_form.html', {'form': form})


def travel_allowance_delete(request, pk):
    allowance = get_object_or_404(TravelAllowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('allowance_list')
    return render(request, 'allowance/allowances_confirm_delete.html', {'allowance': allowance})


def medical_allowance_create(request):
    if request.method == 'POST':
        form = MedicalAllowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = MedicalAllowanceForm()
    return render(request, 'allowance/allowances_form.html', {'form': form})


def medical_allowance_update(request, pk):
    allowance = get_object_or_404(MedicalAllowance, pk=pk)
    if request.method == 'POST':
        form = MedicalAllowanceForm(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = MedicalAllowanceForm(instance=allowance)
    return render(request, 'allowance/allowances_form.html', {'form': form})


def medical_allowance_delete(request, pk):
    allowance = get_object_or_404(MedicalAllowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('allowance_list')
    return render(request, 'allowance/allowances_confirm_delete.html', {'allowance': allowance})


def housing_allowance_create(request):
    if request.method == 'POST':
        form = MedicalAllowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = MedicalAllowanceForm()
    return render(request, 'allowance/allowances_form.html', {'form': form})


def housing_allowance_update(request, pk):
    allowance = get_object_or_404(HousingAllowance, pk=pk)
    if request.method == 'POST':
        form = HousingAllowanceForm(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = HousingAllowanceForm(instance=allowance)
    return render(request, 'allowance/allowances_form.html', {'form': form})


def housing_allowance_delete(request, pk):
    allowance = get_object_or_404(HousingAllowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('allowance_list')
    return render(request, 'allowance/allowances_confirm_delete.html', {'allowance': allowance})


def uniform_allowance_create(request):
    if request.method == 'POST':
        form = UniformAllowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = UniformAllowanceForm()
    return render(request, 'allowance/allowances_form.html', {'form': form})


def uniform_allowance_update(request, pk):
    allowance = get_object_or_404(UniformAllowance, pk=pk)
    if request.method == 'POST':
        form = UniformAllowanceForm(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = UniformAllowanceForm(instance=allowance)
    return render(request, 'allowance/allowances_form.html', {'form': form})


def uniform_allowance_delete(request, pk):
    allowance = get_object_or_404(UniformAllowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('allowance_list')
    return render(request, 'allowance/allowances_confirm_delete.html', {'allowance': allowance})


def other_allowance_create(request):
    if request.method == 'POST':
        form = OtherAllowanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = OtherAllowanceForm()
    return render(request, 'allowance/allowances_form.html', {'form': form})


def other_allowance_update(request, pk):
    allowance = get_object_or_404(OtherAllowance, pk=pk)
    if request.method == 'POST':
        form = OtherAllowanceForm(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            return redirect('allowance_list')
    else:
        form = OtherAllowanceForm(instance=allowance)
    return render(request, 'allowance/allowances_form.html', {'form': form})


def other_allowance_delete(request, pk):
    allowance = get_object_or_404(OtherAllowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('allowance_list')
    return render(request, 'allowance/allowances_confirm_delete.html', {'allowance': allowance})


from django.shortcuts import render
from .models import AllowancePayments


def allowance_payments_view(request):
    # Retrieve all allowance payments
    allowance_payments = AllowancePayments.objects.all()

    # You can perform additional filtering, ordering, or any other processing here

    # Render the template with the data
    return render(request, 'allowance/allowance_payments.html', {'allowance_payments': allowance_payments})
