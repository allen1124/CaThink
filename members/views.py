from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from ImageX.forms import UserForm, ProfileForm
from django.http import HttpResponse
from django.contrib import messages
from members.models import Profile


def profile_detail(request, id = None):
	profile = get_object_or_404(Profile, id=id)
	user = profile.user
	context = {
		"profile": profile,
		"user_": user,
	}
	return render(request, "profile_detail.html", context)


@login_required
@transaction.atomic
def profile_edit(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST or None, instance=request.user)
		profile_form = ProfileForm(request.POST or None, instance=request.user.profile, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('profile_detail', request.user.id)
		else:
			return HttpResponse("<h1>Error</h1>")
	else:
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)
		return render(request, 'profile_form.html', {
			'user_form': user_form,
			'profile_form': profile_form
			})
