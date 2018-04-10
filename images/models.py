from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tagging.fields import TagField
import os


# Create your models here.
CategoryList = (('Abstract', 'Abstract'),
					('Aerial', 'Aerial'),
					('Animals', 'Animals'),
					('Architecture', 'Architecture'),
					('Black and White', 'Black and White'),
					('Family', 'Family'),
					('Fashion', 'Fashion'),
					('Fine Art', 'Fine Art'),
					('Food', 'Food'),
					('Journalism', 'Journalism'),
					('Landscape', 'Landscape'),
					('Macro', 'Macro'),
					('Nature', 'Nature'),
					('Night', 'Night'),
					('People', 'People'),
					('Performing Arts', 'Performing Arts'),
					('Sport', 'Sport'),
					('Still Life', 'Still Life'),
					('Street, and Travel', 'Street, and Travel'))

class Image(models.Model):
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	title = models.CharField(max_length=120, blank=True)
	tag = TagField(blank=True)
	category = models.CharField(max_length=120, choices=CategoryList, null=True, blank=True)
	image = models.ImageField(null=True, blank=False, height_field="heightField", width_field="WidthField")
	heightField = models.IntegerField(default=0)
	WidthField = models.IntegerField(default=0)
	description = models.TextField(blank=True)
	download_count = models.IntegerField(default=0, blank=True)
	likes = models.ManyToManyField(User, blank=True, related_name="image_likes")
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("image_detail", kwargs={"id": self.id})

	def get_api_like_url(self):
		return reverse("like-api-toggle", kwargs={"id": self.id})

	def filename(self):
		return os.path.basename(self.image.name)

	def get_popularity(self):
		return self.likes.count() + self.download_count



class Gallery(models.Model):
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	title = models.CharField(max_length=120, blank=True)
	category = models.CharField(max_length=120, choices=CategoryList, null=True, blank=True)
	tag = TagField(blank=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
