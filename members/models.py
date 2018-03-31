from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
	bio = models.TextField(max_length=500, default='', blank=True)
	location = models.CharField(max_length=100, default='', blank=True)
	no_of_images = models.IntegerField(default=0, blank=True)
	no_of_uploads = models.IntegerField(default=0, blank=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()
