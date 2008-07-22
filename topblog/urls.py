from django.conf.urls.defaults import *

urlpatterns = \
patterns('top.blog.views',
    (r'^blog/?$', 'index'),
    (r'^blog/(?P<blogname>[^/]+)/?$', 'list'),
    (r'^blog/(?P<blogname>[^/]+)/(?P<year>\d{4})/?$', 'list_yearly'),
    (r'^blog/(?P<blogname>[^/]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/?$', 'list_monthly'),
    (r'^blog/(?P<blogname>[^/]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/?$', 'list_daily'),
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
