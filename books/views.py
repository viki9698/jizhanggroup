# Create your views here.
from books.forms import BookForm, BookTypeForm, ItemForm, ContactForm
from books.models import Book, Book_Type, Contact, Contact_Book,Bill,Bill_Item
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
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
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    l = Contact.objects.filter(create_by=request.user)
    return render_to_response('books/contacts.html', {'forms':l})

    
def bookDetail(request, bookId):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    book = Book.objects.get(id=bookId)
    amountIn = 0
    amountOut = 0
    bills = book.bill_set.all().order_by('-date', '-id')
    for bill in bills:
        if bill.amount > 0:
            amountIn += bill.amount
        else:
            amountOut -= bill.amount
    amount = amountIn - amountOut
    return render_to_response('books/book_detail.html', {'form':book, 'bills':bills, 'amountIn': amountIn, 'amountOut':amountOut, 'amount':amount})
    
def deleteBooks(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/books/")

def deleteContacts(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Contact.objects.get(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/contacts/")
    
def deleteItems(request,bookId):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Bill.objects.get(pk=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/books/" + bookId + "/")
    
def addItem(request, bookId):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    if request.method == 'POST' :
        #contactIds = request.REQUEST.getList("contact")
        form = ItemForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            num = float(cd['amount']) if cd['type'] == "1" else -float(cd['amount'])
            g = Bill(title=cd['title'], description=cd['description'], book=Book(pk=bookId), date=cd['date'], create_by=request.user, amount=num)
            g.save()
            for contactId in request.POST["contactIds"].strip(",").split(","):
                subAmount = request.POST['subCount_'+contactId]
                billItem = Bill_Item(contact=Contact(pk=contactId), amount=subAmount, bill=g)
                billItem.save()
            return HttpResponseRedirect(getHost(request) + "/books/" + bookId + "/")
    else:
        form = ItemForm(initial={'type':'1'})
    contacts = [contactBook.contact for contactBook in Contact_Book.objects.filter(book=Book(pk=bookId))]
    return  render_to_response('books/item_form.html', {'form':form, 'contacts':contacts},context_instance=RequestContext(request))
    
def addBookType(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    if request.method == 'POST' :
        form = BookTypeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            g = Book_Type(name=cd['name'], description=cd['description'])
            g.save()
            return HttpResponseRedirect(getHost(request) + "/bookTypes/")
    else:
        form = BookTypeForm()
    return  render_to_response('books/book_type_form.html', {'form':form}, context_instance=RequestContext(request))
    
def listBookTypes(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    l = Book_Type.objects.all()
    return render_to_response('books/book_types.html', {'forms':l})
    
def deleteBookTypes(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book_Type.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/bookTypes/")
