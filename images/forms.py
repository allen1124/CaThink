from django import forms

from .models import Image

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = [
			"title",
			"tag",
			"category",
			"description",
			"image",
		]

		# CategoryList = (('Abstract', 'Abstract'),
		# 				('Aerial', 'Aerial'),
		# 				('Animals', 'Animals'),
		# 				('Architecture', 'Architecture'),
		# 				('Black and White', 'Black and White'),
		# 				('Family', 'Family'),
		# 				('Fashion', 'Fashion'),
		# 				('Fine Art', 'Fine Art'),
		# 				('Food', 'Food'),
		# 				('Journalism', 'Journalism'),
		# 				('Landscape', 'Landscape'),
		# 				('Macro', 'Macro'),
		# 				('Nature', 'Nature'),
		# 				('Night', 'Night'),
		# 				('People', 'People'),
		# 				('Performing Arts', 'Performing Arts'),
		# 				('Sport', 'Sport'),
		# 				('Still Life', 'Still Life'),
		# 				('Street, and Travel', 'Street, and Travel'))
		# Image.category = forms.ChoiceField(choices=CategoryList)
