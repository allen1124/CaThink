from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import ImageForm
from .models import Image


def image_home(request):
	querysetList = Image.objects.all()
	query = request.GET.get("q")
	if query:
		querysetList = querysetList.filter(Q(tag__contains=query))
	context = {
		"imagesList": querysetList,
	}
	return render(request, "images.html", context)

def image_detail(request):
	return HttpResponse("<h1>It is Image Detail page </h1>")

def image_create(request):
	form = ImageForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		image = form.save(commit=False)
		image.username = request.user.username
		image.save()
		return redirect('images')
	context = {
		"form": form
	}
	return render(request, "image_form.html", context)

def image_update(request):
	return HttpResponse("<h1>It is Image Update page </h1>")

def image_delete(request):
	return HttpResponse("<h1>It is Image Delete page </h1>")