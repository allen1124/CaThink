from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

# Create your models here.


class Image(models.Model):

	title = models.CharField(max_length=120)
	image = models.ImageField(null=True, blank=False)
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

