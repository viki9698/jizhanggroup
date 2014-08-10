from django.conf.urls.defaults import *
from django.contrib import admin
import dbindexer
from django.views.generic import TemplateView
import settings
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
    url(r'^books/$', 'books.views.listBook', name="books"),
    (r'^contactForm/$', 'books.views.addContact'),
    url(r'^contacts/$', 'books.views.listContacts', name="contacts"),
    url(r'^books/(?P<bookId>\d+)/addItem/$', 'books.views.addItem', name="addItem"),
    url(r'^books/(?P<bookId>\d+)/$', 'books.views.bookDetail', name="book_detail"),
    (r'^deleteBooks/$', 'books.views.deleteBooks'),
    (r'^deleteContacts/$', 'books.views.deleteContacts'),   
    (r'^books/(?P<bookId>\d+)/deleteItems/$', 'books.views.deleteItems'),
    (r'^register/$', 'books.views.register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',name="logout"),
    (r'^bookTypeForm/$', 'books.views.addBookType'),
    (r'^bookTypes/$', 'books.views.listBookTypes'),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                            { 'document_root':settings.STATIC_URL }),
)
