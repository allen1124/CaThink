from django.contrib import admin

# Register your models here.

from .models import Image, Gallery

class ImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'user', 'category', 'tag')

class GalleryAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'user', 'category', 'tag')

admin.site.register(Image, ImageAdmin)
admin.site.register(Gallery, GalleryAdmin)
