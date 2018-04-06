from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from .models import Image
from django.contrib.auth.models import User


def image_search(request):
	queryset_list = Image.objects.all()
	query_string_q = request.GET.get("q")
	query_string_p = request.GET.get("p")
	query_category = request.GET.get("cat")
	query = None
	if query_string_q:
		query = Q(tag=query_string_q)
	elif query_string_p:
		try:
			user = User.objects.get(username=query_string_p)
		except User.DoesNotExist:
			pass
		query = Q(user=user)
	if query_category:
		query = query & Q(category=query_category)
	if query:
		queryset_list = queryset_list.filter(query)
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