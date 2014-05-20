# Create your views here.
from books.forms import BookForm
from books.models import Book
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from common import getHost
from django import forms
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(getHost(request) + "/books/")
    else:
        form = UserCreationForm()
    return render_to_response("books/register.html", {'form': form,})

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
