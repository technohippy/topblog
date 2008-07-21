from google.appengine.ext import db
import re

# Create your models here.
class TopAccount(db.Model):
  user = db.UserProperty()
  image = db.BlobProperty()
  introduction = db.StringProperty()

  def nickname():
    return self.user.nickname

  def get_absolute_url(self):
    return '/profile/%s' % self.nickname()
