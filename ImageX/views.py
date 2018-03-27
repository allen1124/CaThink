from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from images.models import Image



def index(request):
    query = request.GET.get("q")
    if query:
        querysetList = Image.objects.all()
        querysetList = querysetList.filter(Q(tag__contains=query))
        context = {
            "imagesList": querysetList,
        }
        return render(request, "images.html", context)
    return render(request, 'index.html')

def login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/index/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})


