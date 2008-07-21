import logging
from google.appengine.api import users
from google.appengine.ext import db
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from top.utils import *
from top.blog import models
from top.blog import forms

PER_PAGE = 1

# Create your views here.
def index(request):
  user = users.get_current_user()
  context = dict(user=user)
  if user:
    context['logout_url'] = users.create_logout_url('/')
  else:
    context['login_url'] = users.create_login_url('/')
  context['blogs'] = models.Blog.all().order('-created_on')
  if context['blogs'].count() == 0:
    context['blogs'] = [models.Blog(name='noblog', title='No Blog')]
  return render_to_response('blog/index.html', context)

def list(request, blogname):
  page = int(request.GET.get('p', '0'))
  user = users.get_current_user()
  blog = models.Blog.get_by_key_name(blogname)
  if blog is None:
    return render_error("The blog named `%s' does not exist." % blogname)
  context = context_with_login_status(user, blog)
  #context['entries'] = models.Entry.all().ancestor(blog).filter('index <= ', from_index).order('-index').fetch(PER_PAGE, PER_PAGE * page)
  context['entries'] = models.Entry.all().ancestor(blog).order('-index').fetch(PER_PAGE, PER_PAGE * page)
  if len(context['entries']) == 0:
    context['entries'] = [models.Entry(title='No Entry', body='Comming soon...')]
    context['editable'] = False
  else:
    context['editable'] = context['page_owner']
    if 0 < page:
      context['prev_page'] = str(page - 1)
    if context['entries'][-1].index != models.Entry.last_for(blog).index:
      context['next_page'] = str(page + 1)
  return render_to_response('blog/list.html', context)

def new(request, blogname):
  user = users.get_current_user()
  blog = models.Blog.get_by_key_name(blogname)
  context = context_with_login_status(user, blog)
  if request.method == 'GET':
    context['form'] = forms.EntryForm()
    context['form_title'] = 'New Entry'
  elif request.method == 'POST':
    return post_entry(request.POST, blogname, user)
  return render_to_response('blog/edit_entry.html', context)

def edit(request, blogname, index):
  user = users.get_current_user()
  blog = models.Blog.get_by_key_name(blogname)
  context = context_with_login_status(user, blog)
  entry = models.Entry.get_by_key_name(blogname + index, blog)
  if entry is None:
    return render_to_response('error.html', dict(message='%s%s does not exist' % (blogname, index)))
  if request.method == 'GET':
    context['form'] = forms.EntryForm({'title':entry.title, 'body':entry.body})
    context['form_title'] = 'Edit Entry'
    context['tagnames'] = ''
    for tagname in entry.tags:
      context['tagnames'] += (tagname + ' ')
  elif request.method == 'POST':
    params = request.POST
    entry.title = params['title']
    entry.body = params['body']
    return post_entry(params, blogname, user, entry)
  return render_to_response('blog/edit_entry.html', context)

def post_entry(params, blogname, user, entry=None):
  def txn():
    local_entry = entry
    form = forms.EntryForm(params)
    if not form.is_valid(): return None

    blog = models.Blog.get_by_key_name(blogname)
    if local_entry is None: # new
      entry_count = blog.entry_count
      blog.entry_count += 1
      blog.put()
      local_entry = models.Entry(blog, blogname+str(entry_count),
          owner=user, index=entry_count, title=params['title'], body=params['body'])
    else: # edit
      for tag in local_entry.tags:
        tag.count -=1
        tag.put()
      local_entry.tags = []

    for tagname in params['tags'].split(' '):
      if tagname:
        tag = models.Tag.get_by_key_name(tagname, blog)
        if tag is None:
          tag = models.Tag(blog, tagname, name=db.Category(tagname))
        tag.count += 1
        tag.put()
        local_entry.tags.append(tagname)
    local_entry.put()
    return HttpResponseRedirect(blog.get_absolute_url())
  return db.run_in_transaction(txn)

### followings are private functions. ###
def context_with_login_status(user, blog):
  context = dict(title=blog.title, user=user, blog=blog, page_owner=False)
  context['tags'] = models.Tag.all().ancestor(blog)
  if user:
    context['logout_url'] = users.create_logout_url('/')
    if blog.owner == user:
      context['page_owner'] = True
      context['new_entry_url'] = blog.create_new_entry_url()
  else:
    context['login_url'] = users.create_login_url('/')
  return context

