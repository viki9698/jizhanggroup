# Create your views here.
from books.forms import BookForm, BookTypeForm, ItemForm
from books.models import Book, Book_Type
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from common import getHost
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import auth

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(getHost(request) + "/books/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form,})
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            request.session['userId'] = username
            # Redirect to a success page.
            return HttpResponseRedirect(getHost(request) + "/books/")

    else:
        form = AuthenticationForm()
    return render_to_response("registration/login.html", {'form': form,})    

def addBook(request):
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
        form = BookForm()
    return  render_to_response('books/book_form.html', {'form':form})

def listBook(request):
    if request.session.get('userId', None) is None:
        return login(request)
    userId = request.session['userId']
    l = Book.objects.all()
    return render_to_response('books/books.html', {'forms':l})

def deleteBooks(request):
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/books/")
    
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
