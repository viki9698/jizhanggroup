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
    (r'^contactForm/$', 'books.views.addContact'),
    (r'^contacts/$', 'books.views.listContacts'),
    url(r'^books/(?P<bookId>\d+)/addItem/$', 'books.views.addItem', name="book_index"),
    url(r'^books/(?P<bookId>\d+)/$', 'books.views.bookDetail', name="book_detail"),
    (r'^deleteBooks/$', 'books.views.deleteBooks'),
    (r'^deleteContacts/$', 'books.views.deleteContacts'),
    (r'^register/$', 'books.views.register'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^bookTypeForm/$', 'books.views.addBookType'),
    (r'^bookTypes/$', 'books.views.listBookTypes'),
)
