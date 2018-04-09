from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'tag', 'category', 'description', 'image')

class ImageEditForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'tag', 'category', 'description')
