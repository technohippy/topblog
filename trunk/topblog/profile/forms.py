from django import newforms as forms
from google.appengine.ext.db import djangoforms
import models

class TopAccountForm(djangoforms.ModelForm):
	class Meta:
		model = models.TopAccount
		exclude = ['user']
