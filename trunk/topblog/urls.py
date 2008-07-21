from django.conf.urls.defaults import *

urlpatterns = \
patterns('top.blog.views',
    (r'^blog/?$', 'index'),
    (r'^blog/(?P<blogname>[^/]+)/?$', 'list'),
    (r'^blog/(?P<blogname>[^/]+)/new/?$', 'new'),
    (r'^blog/(?P<blogname>[^/]+)/edit/(?P<index>\d+)/?$', 'edit'),
) + \
patterns('top.profile.views',
    (r'^profile/?$', 'index'),
    (r'^profile/(?P<name>[^/]+)/?$', 'show'),
    (r'^profile/(?P<name>[^/]+/edit)/?$', 'edit'),
) + \
patterns('top.views',
    (r'^admin/', 'admin'),
    (r'^$', 'index'),
)
