from django.contrib import admin

# Register your models here.

from .models import Image

class ImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'user', 'category', 'tag')

admin.site.register(Image, ImageAdmin)
