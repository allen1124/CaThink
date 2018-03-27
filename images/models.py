from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):

	title = models.CharField(max_length=120)
	username = models.CharField(max_length=120, null=False, blank=False)
	tag = models.CharField(max_length=120, null=True, blank=True)
	category = models.CharField(max_length=120, null=True, blank=False)
	image = models.ImageField(null=True, blank=False, height_field="heightField", width_field="WidthField")
	heightField = models.IntegerField(default=0)
	WidthField = models.IntegerField(default=0)
	description = models.TextField(blank=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("images:detail", kwargs={"id": self.id})

	class Meta:
		ordering = ["-timestamp", "-updated"]

