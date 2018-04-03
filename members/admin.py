from django.contrib import admin

# Register your models here.

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'avatar', 'bio', 'location', 'uploadQuota', 'dailyCount', 'curator')


admin.site.register(Profile, ProfileAdmin)