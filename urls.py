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
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),
    ('^admin/', include(admin.site.urls)),
    (r'^bookForm/$', 'books.views.addBook'),
    url(r'^books/$', 'books.views.listBook', name="books"),
    url(r'^index/$', TemplateView.as_view(template_name='index.html'), name="index"),
    url(r'^account/$', TemplateView.as_view(template_name='account.html'), name="account"),
    (r'^contactForm/$', 'books.views.addContact'),
    url(r'^contacts/$', 'books.views.listContacts', name="contacts"),
    url(r'^books/(?P<bookId>\d+)/addItem/$', 'books.views.addItem', name="addItem"),
    url(r'^books/(?P<bookId>\d+)/addItem_aa/$', 'books.views.addItem_aa', name="addItem_aa"),
    url(r'^books/(?P<bookId>\d+)/$', 'books.views.bookDetail', name="book_detail"),
    url(r'^books/(?P<bookId>\d+)/balance/$', 'books.views.balance', name="book_balance"),
    (r'^deleteBooks/$', 'books.views.deleteBooks'),
    (r'^deleteContacts/$', 'books.views.deleteContacts'),   
    (r'^books/(?P<bookId>\d+)/deleteItems/$', 'books.views.deleteItems'),
    (r'^register/$', 'books.views.register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^qqLogin/$', 'books.views.qqLogin', name="qqLogin"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',name="logout"),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'), 
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'), 
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
'django.contrib.auth.views.password_reset_confirm', 
name='password_reset_confirm'), 
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'), 
    (r'^bookTypeForm/$', 'books.views.addBookType'),
    (r'^bookTypes/$', 'books.views.listBookTypes'),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root':settings.STATIC_URL }),
)
