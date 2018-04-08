from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import SignupForm, InvitationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import registration_token
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    return render(request, "index.html")


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
            return HttpResponse('Your Invitation has been sent')
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
