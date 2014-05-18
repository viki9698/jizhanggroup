from django.conf.urls.defaults import *
from django.contrib import admin
import dbindexer
from django.views.generic import TemplateView

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', TemplateView.as_view(template_name="index.html")),
    ('^admin/', include(admin.site.urls)),
    (r'^groupForm/$', 'groups.views.addGroup'),
    (r'^groups/$', 'groups.views.listGroup'),
    (r'^deleteGroups/$', 'groups.views.deleteGroups'),
)
