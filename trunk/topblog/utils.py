from django.shortcuts import render_to_response
def render_error(message):
  return render_to_response('error.html', dict(message=message))
