from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from .models import Image


def image_search(request):
	queryset_list = Image.objects.all()
	query = request.GET.get("q")
	category = request.GET.get("cat")
	if query:
		queryset_list = queryset_list.filter(Q(tag=query))
	if category:
		queryset_list = queryset_list.filter(Q(category=category))
	context = {
		"imagesList": queryset_list,
	}
	return render(request, "images.html", context)


def image_detail(request):
	return HttpResponse("<h1>It is Image Detail page </h1>")


@login_required
def image_upload(request):
	form = ImageForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		image = form.save(commit=False)
		image.user = request.user
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