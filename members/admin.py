from django.contrib import admin

# Register your models here.

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'avatar', 'bio', 'location', 'remaining_quota', 'daily_upload_count', 'curator', 'last_upload_time')


admin.site.register(Profile, ProfileAdmin)