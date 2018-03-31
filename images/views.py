from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import ImageForm
from .models import Image


def image_home(request):
	queryset_list = Image.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(Q(tag=query))
	context = {
		"imagesList": queryset_list,
	}
	return render(request, "images.html", context)


def image_detail(request):
	return HttpResponse("<h1>It is Image Detail page </h1>")


def image_upload(request):
	form = ImageForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		image = form.save(commit=False)
		image.userID = request.user.id
		image.save()
		return redirect('images')
	context = {
		"form": form
	}
	return render(request, "image_form.html", context)


def image_edit(request):
	return HttpResponse("<h1>It is Image Update page </h1>")


def image_delete(request):
	return HttpResponse("<h1>It is Image Delete page </h1>")