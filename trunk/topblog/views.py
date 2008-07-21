# Create your views here.
from google.appengine.api import users
from google.appengine.ext import db
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from top.blog import models
from top.blog import forms

def admin(request):
  user = users.get_current_user()
  if not user: return HttpResponseRedirect(users.create_login_url('/admin'))
  if not users.is_current_user_admin(): return HttpResponseRedirect('/')

  if request.method == 'GET':
    form = forms.BlogForm()
  elif request.method == 'POST':
    params = request.POST
    form = forms.BlogForm(params)
    if form.is_valid():
      def txn():
        blog = models.Blog.get_by_key_name(params['name'])
        if blog is None:
          blog = models.Blog(key_name=params['name'], name=params['name'], owner=user, title=params['title'])
          blog.put()
          return HttpResponseRedirect(blog.get_absolute_url())
        else:
          return render_to_response('error.html', dict(message='%s has already been used.' % params['name']))
      return db.run_in_transaction(txn)
  return render_to_response('admin.html', dict(form=form))
  
def index(request):
  return render_to_response('index.html', dict(logout_url=users.create_logout_url('')))

