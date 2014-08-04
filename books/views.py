# Create your views here.
from books.forms import BookForm
from books.models import Book
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
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(getHost(request) + "/books/")
        else:
            # Show an error page
            return HttpResponseRedirect("/account/invalid/")

    else:
        form = AuthenticationForm()
    return render_to_response("registration/login.html", {'form': form,})    

def addBook(request):
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
    l = Book.objects.all()
    return render_to_response('books/books.html', {'forms':l});

def deleteBooks(request):
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/books/")