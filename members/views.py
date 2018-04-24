from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from ImageX.forms import UserForm, ProfileForm
from django.contrib.auth import update_session_auth_hash
from members.models import Profile
from django.db.models import Q
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from ImageX.forms import SignupForm, InvitationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ImageX.tokens import registration_token
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages
from images.models import Image

def profile_detail(request, id=None):
    profile = get_object_or_404(Profile, id=id)
    user = profile.user
    images_list = Image.objects.filter(Q(user=profile.user))
    images_list = images_list.exclude(id=1)
    context = {
        "profile": profile,
        "user_": user,
        "imagesList": images_list,
    }
    return render(request, "profile_detail.html", context)


@login_required
@transaction.atomic
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, instance=request.user) #firstname, lastname, email
        profile_form = ProfileForm(request.POST or None, instance=request.user.profile, files=request.FILES) #avatar, bio, location
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile_detail', request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'profile_form.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your Password was successfully updated!')
            return redirect('profile_detail', request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile_change_password.html', {
        'form': form
    })

def invitation(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)
            mail_subject = 'Invitation to ImageX '
            message = render_to_string('InvitationEmail.html', {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(request.user.pk)).decode(),
                'token': registration_token.make_token(request.user),
                'email': form.cleaned_data.get('email')
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Your Invitation has been sent!')
            return redirect('profile_detail', request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = InvitationForm()
    return render(request, 'invitation.html', {'form': form})


def register(request, uidb64, token, email):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and registration_token.check_token(user, token):
            new_user = form.save(commit=False)
            new_user.email = email
            new_user.save()
            auth.login(request, new_user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Activation link is invalid!')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

