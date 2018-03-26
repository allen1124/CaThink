from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageForm
from .models import Image


def image_home(request):
	return HttpResponse("<h1>It is Image Homepage </h1>")

def image_create(request):
	form = ImageForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		image = form.save(commit=False)
		image.save()
	context = {
		"form": form
	}
	return render(request, "image_form.html", context)