import re
from django import template
from textile.textile import textile

register = template.Library()

def textile_filter(value):
  return textile(str(value))

def sanitize_filter(value):
  return re.compile(r'<(script|button|input|a|form|font)(\s|>)', re.I).sub(r'&lt;\1\2', value)

def taglevel_filter(value):
  if value < 5:
    return str(value) # 1..4
  elif value < 20:
    return str(value // 5 + 5) # 5..8
  elif value < 50:
    return str(value // 10 + 8) # 9..12
  else:
    return str(13)

register.filter('sanitize', sanitize_filter)
register.filter('textile', textile_filter)
register.filter('taglevel', taglevel_filter)
