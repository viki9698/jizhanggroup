# Create your views here.
from books.forms import BookForm, BookTypeForm, ItemForm, ContactForm
from books.models import Book, Book_Type, Contact, Contact_Book
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from common import getHost
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(getHost(request) + "/books/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form,}, context_instance=RequestContext(request))
'''
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(getHost(request) + "/books/")

    else:
        form = AuthenticationForm()
    return render_to_response("registration/login.html", {'form': form,}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return render_to_response("registration/login.html", context_instance=RequestContext(request))
'''
def addBook(request):
    if request.method == 'POST' :
        form = BookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = Book(name=cd['name'], description=cd['description'], book_type=cd['book_type'])
            g.create_by = request.user
            g.save()
            for contactId in request.POST['contacts'].split(","):
                Contact_Book(contact=Contact(id=contactId), book=g).save()
            return HttpResponseRedirect(getHost(request) + "/books/")
    else:
        form = BookForm()
    contacts = Contact.objects.filter(create_by=request.user)
    return  render_to_response('books/book_form.html', {'form':form, 'contacts':contacts},context_instance=RequestContext(request))

def listBook(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)    
    l = Book.objects.filter(create_by=request.user)
    return render_to_response('books/books.html', {'forms':l})
    
def addContact(request):
    if request.method == 'POST' :
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = Contact(name=cd['name'], description=cd['description'], user=cd['user'])
            g.create_by = request.user
            g.save()
            return HttpResponseRedirect(getHost(request) + "/contacts/")
    else:
        form = ContactForm()
    return  render_to_response('books/contact_form.html', {'form':form},context_instance=RequestContext(request))

def listContacts(request):
    l = Contact.objects.filter(create_by=request.user)
    return render_to_response('books/contacts.html', {'forms':l})

    
def bookDetail(request, bookId):
    if request.session.get('userId', None) is None:
        return login(request)
    userId = request.session['userId']
    book = Book.objects.get(id=bookId)
    return render_to_response('books/book_form.html', {'forms':book})
    
def deleteBooks(request):
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/books/")

def deleteContacts(request):
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Contact.objects.get(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/contacts/")
    
def addItem(request, bookId):
    if request.session.get('userId', None) is None:
        return login(request)
    userId = request.session['userId']
    if request.method == 'POST' :
        form = BookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = Book(name=cd['name'], description=cd['description'], book_type=cd['book_type'])
            g.save()
            return HttpResponseRedirect(getHost(request) + "/books/")
    else:
        form = ItemForm()
    return  render_to_response('books/item_form.html', {'form':form})
    
def addBookType(request):
    if request.session.get('userId', None) is None:
        return login(request)
    userId = request.session['userId']
    if request.method == 'POST' :
        form = BookTypeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = Book_Type(name=cd['name'], description=cd['description'])
            g.save()
            return HttpResponseRedirect(getHost(request) + "/bookTypes/")
    else:
        form = BookTypeForm()
    return  render_to_response('books/book_type_form.html', {'form':form})
    
def listBookTypes(request):
    if request.session.get('userId', None) is None:
        return login(request)
    userId = request.session['userId']
    l = Book_Type.objects.all()
    return render_to_response('books/book_types.html', {'forms':l})
    
def deleteBookTypes(request):
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book_Type.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/bookTypes/")
