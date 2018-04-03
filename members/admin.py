from django.contrib import admin

# Register your models here.

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'avatar', 'bio', 'location', 'no_of_images', 'no_of_uploads', 'curator')


admin.site.register(Profile, ProfileAdmin)