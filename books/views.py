# Create your views here.
from books.forms import BookForm
from books.models import Book,User_Book
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
            request.session['user'] = user
            # Redirect to a success page.
            return HttpResponseRedirect(getHost(request) + "/books/")

    else:
        form = AuthenticationForm()
    return render_to_response("registration/login.html", {'form': form,})    

def addBook(request):
    if request.session.get('user', None) is None:
        return login(request)
    user = request.session['user']
    if request.method == 'POST' :
        form = BookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = Book(name=cd['name'], description=cd['description'], book_type=cd['book_type'])
            g.save()
            ub = User_Book()
            ub.user = user
            ub.book = g
            ub.is_owner = '1'
            ub.save()
            return HttpResponseRedirect(getHost(request) + "/books/")
    else:
        form = BookForm()
    return  render_to_response('books/book_form.html', {'form':form})

def listBook(request):
    if request.session.get('user', None) is None:
        return login(request)
    user = request.session['user']
    l = User_Book.objects.all().filter(user=user)
    li = []
    for ub in l:
        li.append(ub.book)
    return render_to_response('books/books.html', {'forms':li});

def deleteBooks(request):
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/books/")
