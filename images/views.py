from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from .models import Image
from members.models import Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib import messages
from tagging.models import Tag, TaggedItem
import re


def normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def image_search(request):
	queryset_list = Image.objects.all().order_by("-timestamp")
	query_string_q = request.GET.get("q")
	query_string_p = request.GET.get("p")
	query_category = request.GET.get("cat")
	query = Q(pk__in=[])
	if query_string_q:
		terms = normalize_query(query_string_q.lower())
		queryset_list = TaggedItem.objects.get_union_by_model(Image, terms)
	elif query_string_p:
		terms_p = normalize_query(query_string_p)
		for term in terms_p:
			try:
				user = User.objects.get(username=term)
			except User.DoesNotExist:
				pass
			else:
				query = query | Q(user=user)
		queryset_list = queryset_list.filter(query)
<<<<<<< HEAD
	paginator = Paginator(queryset_list, 10)
=======
	if query_category:
		queryset_list = queryset_list.filter(Q(category=query_category))
	paginator = Paginator(queryset_list, 12)
>>>>>>> ed59430219e3df1b5d2e28bfb8b9f785940f1361
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
		messages.warning(request, "Sorry, you have reached the upload limit. Please delete your images or upload later.")
		return redirect('images')
	context = {
		"form": form
	}
	return render(request, "image_form.html", context)


def image_edit(request, id=None):
	image = get_object_or_404(Image, id=id)
	form = ImageForm(request.POST or None, instance=image)
	if form.is_valid():
		image = form.save(commit=False)
		image.save()
		messages.success(request, "Image has been updated.")
		return HttpResponseRedirect(image.get_absolute_url())
	context = {
		"image": image,
		"form": form,
	}
	return render(request, "image_edit.html", context)


def image_delete(request, id=None):
	image = get_object_or_404(Image, id=id)
	user_profile = get_object_or_404(Profile, user=image.user)
	user_profile.remaining_quota += 1
	user_profile.save()
	image.delete()
	messages.success(request, "Image has been deleted.")
	return redirect('images')