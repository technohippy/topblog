# Create your views here.
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from top.profile import models
from top.profile import forms

def index(request):
  user = users.get_current_user()
  context = dict(user=user)
  if user:
    context['login_url'] = users.create_login_url('/')
  else:
    context['logout_url'] = users.create_logout_url('/')
  return render_to_response('profile/index.html', context)

def show(request, name):
  user = users.User('test@example.com')
  #user = users.User('%s@gmail.com' % name)
  #account = models.TopAccount.get().filter('user =', user)
  accounts = models.TopAccount.all().filter('user =', user)
  if accounts.count() == 0:
    account = models.TopAccount(user=user)
  else:
    account = acconts[0]
  context = dict(account=account, title=user.nickname())
  return render_to_response('profile/show.html', context)

def edit(request, name):
  user = users.User('test@example.com')
  #user = users.User('%s@gmail.com' % name)
  #account = models.TopAccount.get().filter('user =', user)
  accounts = models.TopAccount.all().filter('user =', user)
  if accounts.count() == 0:
    account = models.TopAccount(user=user)
  else:
    account = acconts[0]
  context = dict(account=account, title=user.nickname())
  if request.method == 'GET':
    context['form'] = forms.TopAccountForm()
  elif request.method == 'POST':
    context['form'] = forms.TopAccountForm() # TODO: dummy
  return render_to_response('profile/edit.html', context)
