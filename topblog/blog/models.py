from google.appengine.ext import db
import re

def check_pattern(pattern):
  def check_pattern_func(val):
    if not re.compile(pattern).match(val): 
      raise db.BadValueError('Property must be consist of alphabets and numbers.')
    val
  return check_pattern_func

# Create your models here.
class Tag(db.Model):
  name = db.CategoryProperty()
  count = db.IntegerProperty(default=0)

class Blog(db.Model):
  entry_count = db.IntegerProperty(required=True, default=0)
  name = db.StringProperty(required=True, validator=check_pattern(r'^\w+$'))
  #owner = db.UserProperty(required=True)
  owner = db.UserProperty()
  title = db.StringProperty(required=True)
  created_on = db.DateTimeProperty(auto_now_add=True)

  def __str__(self):
    return '"%s" written by %s' % [self.title, self.owner.nickname()]

  def get_absolute_url(self):
    return '/blog/%s' % self.name

  def create_new_entry_url(self):
    return '/blog/%s/new' % self.name

class Entry(db.Model):
  index = db.IntegerProperty(required=True, default=0)
  #owner = db.UserProperty(required=True)
  owner = db.UserProperty()
  title = db.StringProperty(required=True)
  body = db.TextProperty(required=True)
  #name = db.StringProperty(required=True, validator=check_pattern(r'^\w+$'))
  tags = db.ListProperty(unicode)
  date = db.DateTimeProperty()
  created_on = db.DateTimeProperty(auto_now_add=True)

  def month(self):
    return ['', 'Jan', 'Feb', 'Mar', 'Apl', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][self.date.month]

  def day(self):
    return self.date.day

  def time(self):
    return '%2d:%2d' % (self.date.hour, self.date.minute)

  def create_edit_url(self):
    return '/blog/%s/edit/%d' % (self.parent().name, self.index)

  @classmethod
  def first_for(cls, blog):
    return cls.all().ancestor(blog).order('-date').order('-index').get()

  @classmethod
  def last_for(cls, blog):
    return cls.all().ancestor(blog).order('date').order('index').get()

