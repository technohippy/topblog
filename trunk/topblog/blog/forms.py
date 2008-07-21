from django import newforms as forms
from google.appengine.ext.db import djangoforms
import models

class BlogForm(djangoforms.ModelForm):
	class Meta:
		model = models.Blog
		exclude = ['owner', 'created_on', 'entry_count']

class EntryForm(djangoforms.ModelForm):
  class Meta:
    model = models.Entry
    exclude = ['owner', 'created_on', 'tags', 'index']
