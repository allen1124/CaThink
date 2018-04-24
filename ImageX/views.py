from django.shortcuts import render
from django.contrib.auth.models import User
from images.models import Image
from django.db.models import F, Count
from django.core.files.images import ImageFile


def index(request):
    if not Image.objects.filter(pk=1).exists():
        image_ = Image.objects.create(user=get_object_or_404(User, id=1))
        image_.image = ImageFile(open("static/img/bg-masthead.jpg", "rb"))
        image_.save()
    liked_images = None
    queryset_list = Image.objects.all().exclude(id=1).annotate(
        popularity=(F('download_count')+Count('likes'))).order_by('-popularity') [:10]
    if request.user.is_authenticated:
        liked_images = Image.objects.filter(likes=request.user)
    context = {
        "imagesList": queryset_list,
        "likedImages": liked_images,
    }
    return render(request, "index.html", context)

