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
    ('^$', 'books.views.listBook'),
    ('^admin/', include(admin.site.urls)),
    (r'^bookForm/$', 'books.views.addBook'),
    (r'^books/$', 'books.views.listBook'),
    url(r'^books/(?P<bookId>\d+)/addItem/$', 'books.views.addItem', name="book_index"),
    (r'^deleteBooks/$', 'books.views.deleteBooks'),
    (r'^register/$', 'books.views.register'),
    (r'^login/$', 'books.views.login'),
    (r'^bookTypeForm/$', 'books.views.addBookType'),
    (r'^bookTypes/$', 'books.views.listBookTypes'),
)
