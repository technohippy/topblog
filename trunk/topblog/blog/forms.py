from django import newforms as forms
from google.appengine.ext.db import djangoforms
import models
import time
import widgets

class BlogForm(djangoforms.ModelForm):
	class Meta:
		model = models.Blog
		exclude = ['owner', 'created_on', 'entry_count']

class EntryForm(djangoforms.ModelForm):
  class Meta:
    model = models.Entry
    #exclude = ['owner', 'created_on', 'tags', 'index']
    exclude = ['owner', 'date', 'created_on', 'tags', 'index']
  date = forms.DateField(widget=widgets.CalendarWidget, initial=time.strftime('%Y-%m-%d'))
