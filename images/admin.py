from django.contrib import admin

# Register your models here.

from .models import Image

class ImageAdmin(admin.ModelAdmin):
	list_display = ('title', 'username', 'category', 'tag')

admin.site.register(Image, ImageAdmin)
