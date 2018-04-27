from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ImageForm, ImageEditForm
from .models import Image
from members.models import Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib import messages
from tagging.models import TaggedItem, Tag
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.core.files.images import ImageFile
import re


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def image_search(request):
    queryset_list = Image.objects.all().exclude(id=1)
    query_string_q = request.GET.get("q")
    query_string_p = request.GET.get("p")
    query_category = request.GET.get("cat")
    ordering = request.GET.get("order")
    if not Image.objects.filter(pk=1).exists():
        image_ = Image.objects.create(user=get_object_or_404(User, id=1))
        image_.image = ImageFile(open("static/img/bg-masthead.jpg", "rb"))
        image_.save()
    query = Q(pk__in=[])
    if query_string_q:
        image_ = get_object_or_404(Image, id=1)
        Tag.objects.update_tags(image_, None)
        Tag.objects.update_tags(image_, query_string_q.lower())
        queryset_list = TaggedItem.objects.get_related(image_, Image)
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
    if query_category:
        if query_string_q:
            queryset_list = [x for x in queryset_list if x.category == query_category]
        else:
            queryset_list = queryset_list.filter(Q(category=query_category))
    if ordering is "2":
        queryset_list = sorted(queryset_list, key=lambda x: x.get_popularity(), reverse=True)
    elif ordering is "1":
        queryset_list = sorted(queryset_list, key=lambda x: x.timestamp, reverse=True)
    paginator = Paginator(queryset_list, 12)
    page = request.GET.get('page')
    queryset_list = paginator.get_page(page)
    liked_images = None
    if request.user.is_authenticated:
        liked_images = Image.objects.filter(likes=request.user)
    context = {
        "imagesList": queryset_list,
        "likedImages": liked_images,
    }
    return render(request, "images.html", context)


def image_detail(request, id=None):
    image = get_object_or_404(Image, id=id)
    context = {
        "image": image,
        "likedUsers": image.likes.all()
    }
    return render(request, "image_detail.html", context)

def image_download(request, id=None):
    image = get_object_or_404(Image, id=id)
    image.download_count += 1
    image.save()
    response = HttpResponse(image.image, content_type='image/jpg')
    if image.title:
        response['Content-Disposition'] = 'attachment;filename="%s.jpg"' % image.title
    else:
        response['Content-Disposition'] = 'attachment;filename="%s"' % image.filename()
    return response

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
            if form.cleaned_data['tag'] is not None:
                if len(normalize_query(form.cleaned_data['tag'])) > 10:
                    messages.warning(request, "Sorry, you have added too many tags in a image")
                    context = {
                        "form": form
                    }
                    return render(request, "image_form.html", context)
            if not (str(form.cleaned_data['image'].content_type).endswith("jpeg") or str(
                    form.cleaned_data['image'].content_type).endswith("jpg")):
                messages.warning(request, "Sorry, imageX supports only the JPEG file format.")
                context = {
                    "form": form
                }
                return render(request, "image_form.html", context)
            image.user = request.user
            image.save()
            user_profile.daily_upload_count += 1
            user_profile.remaining_quota -= 1
            user_profile.last_upload_time = datetime.now()
            user_profile.save()
            return redirect('images')
    else:
        messages.warning(request,
                         "Sorry, you have reached the upload limit. Please delete your images or upload later.")
        return redirect('images')
    context = {
        "form": form
    }
    return render(request, "image_form.html", context)

@login_required
def image_edit(request, id=None):
    image = get_object_or_404(Image, id=id)
    if image.user == request.user:
        form = ImageEditForm(request.POST or None, instance=image)
        if form.is_valid():
            image = form.save(commit=False)
            if form.cleaned_data['tag'] is not None:
                if len(normalize_query(form.cleaned_data['tag'])) > 10:
                    messages.warning(request, "Sorry, you have added too many tags in a image")
                    context = {
                        "form": form
                    }
                    return render(request, "image_edit.html", context)
            image.save()
            messages.success(request, "Image has been updated.")
            return HttpResponseRedirect(image.get_absolute_url())
        context = {
            "image": image,
            "form": form,
        }
        return render(request, "image_edit.html", context)
    else:
        return HttpResponse('Sorry, you don\'t have the permission to do so')

@login_required
def image_delete(request, id=None):
    image = get_object_or_404(Image, id=id)
    if image.user == request.user:
        user_profile = get_object_or_404(Profile, user=image.user)
        user_profile.remaining_quota += 1
        user_profile.save()
        image.delete()
        messages.success(request, "Image has been deleted.")
        return redirect('images')
    else:
        return HttpResponse('Sorry, you don\'t have the permission to do so')

class ImageLikesAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, id=None):
        image = get_object_or_404(Image, id=id)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in image.likes.all():
                liked = False
                image.likes.remove(user)
            else:
                liked = True
                image.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)
