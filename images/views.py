from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from .models import Image
from members.models import Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from wsgiref.util import FileWrapper
import mimetypes, os

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
			query = Q(pk__in=[])
		else:
			query = Q(user=user)
	if query_category:
		if query is not None:
			query = query & Q(category=query_category)
		else:
			query = Q(category=query_category)
	if query:
		queryset_list = queryset_list.filter(query)
	paginator = Paginator(queryset_list, 12)
	page = request.GET.get('page')
	queryset_list = paginator.get_page(page)
	context = {
		"imagesList": queryset_list,
	}
	return render(request, "images.html", context)


def image_detail(request, id=None):
	image = get_object_or_404(Image, id=id)
	context = {
		"image": image,
	}
	return render(request, "image_detail.html", context)


@login_required
def image_upload(request):
	user_profile = get_object_or_404(Profile, user=request.user)
	form = ImageForm(request.POST or None, request.FILES or None)
	if datetime.now().day > user_profile.last_upload_time.day:
		user_profile.daily_upload_count = 0
		user_profile.save()
	if user_profile.daily_upload_count < 4 and user_profile.remaining_quota >= 1:
		if form.is_valid():
			image = form.save(commit=False)
			image.user = request.user
			image.save()
			user_profile.daily_upload_count += 1
			user_profile.remaining_quota -= 1
			user_profile.last_upload_time = datetime.now()
			user_profile.save()
			return redirect('images')
	else:
		return HttpResponse("<h1>Sorry, You have reached the upload limit. Please delete your images and upload on next day.</h1>")
	context = {
		"form": form
	}
	return render(request, "image_form.html", context)


def image_download(request, id):
	img = Image.objects.get(id=id)
	wrapper = FileWrapper(open(img.image.file.get))
	content_type = mimetypes.guess_type(img.image.name)[0]
	response = HttpResponse(wrapper, content_type=content_type)
	response['Content-Length'] = os.path.getsize(img.image.file)
	response['Content-Disposition'] = "attachment; filename=%s" % img.title
	return response


def image_edit(request):
	return HttpResponse("<h1>It is Image Update page </h1>")


def image_delete(request):
	return HttpResponse("<h1>It is Image Delete page </h1>")