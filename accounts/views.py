from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import UserProfileForm


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('update_profile')  # Redirect to a success page
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/profile_update.html', {'form': form})
