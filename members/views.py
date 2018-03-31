from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from ImageX.forms import UserForm, ProfileForm
from django.http import HttpResponse


@login_required
@transaction.atomic
def edit_profile(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return render(request, 'profile_form.html', {
				'user_form': user_form,
				'profile_form': profile_form
			})
		else:
			return HttpResponse("<h1>Error</h1>")
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
		return render(request, 'profile_form.html', {
			'user_form': user_form,
			'profile_form': profile_form
			})
