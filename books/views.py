# coding=utf-8
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
from django.contrib.auth.views import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render_to_response("registration/register_success.html", context_instance=RequestContext(request))
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form,}, context_instance=RequestContext(request))
    
def qqLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        if not User.objects.filter(username=username) :        
            user = User()
            user.username = username
            user.first_name = request.POST.get('firstName', '')
            user.set_password('123456')           
            user.save();
        return login(request)
        
        
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
    return render_to_response('books/books.html', {'forms':l},context_instance=RequestContext(request))
    
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
    return render_to_response('books/contacts.html', {'forms':l},context_instance=RequestContext(request))
    
def bookDetail(request, bookId):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    book = Book.objects.get(id=bookId)
    bookType = book.book_type.name
    if bookType.find("AA") >= 0:
        bills = book.bill_set.all().order_by('-date', '-id')
        iMap = {}
        for bill in bills:
            for item in bill.bill_item_set.all():
                if iMap.has_key(item.contact.name):
                    iMap[item.contact.name] += item.amount
                else:
                    iMap[item.contact.name] = item.amount
            
        return render_to_response('books/book_detail_aa.html', {'form':book, 'bills':bills, 'iMap':iMap},context_instance=RequestContext(request))    
    else:
        amountIn = 0
        amountOut = 0
        bills = book.bill_set.all().order_by('-date', '-id')
        for bill in bills:
            if bill.amount > 0:
                amountIn += bill.amount
            else:
                amountOut -= bill.amount
        amount = amountIn - amountOut
        return render_to_response('books/book_detail.html', {'form':book, 'bills':bills, 'amountIn': amountIn, 'amountOut':amountOut, 'amount':amount},context_instance=RequestContext(request))
        
def balance(request, bookId):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    book = Book.objects.get(id=bookId)
    bills = book.bill_set.all()
    dic = {}
    for bill in bills:
        for item in bill.bill_item_set.all():
            if dic.has_key(item.contact.id):
                dic[item.contact.id] += item.amount
            else:
                dic[item.contact.id] = item.amount
    num = 0
    g = Bill(title='结账', book=book, create_by=request.user)
    billItems = []
    for k, v in dic.items():
        if v > 0:
            num +=v
        billItems.append(Bill_Item(contact=Contact(pk=k), amount=-v))
    g.amount = num
    g.save()    
    for billItem in billItems:
        billItem.bill = g
        billItem.save()
    
    return bookDetail(request, bookId)    
    
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
    
def addItem_aa(request, bookId):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    if request.method == 'POST' :
        #contactIds = request.REQUEST.getList("contact")
        form = ItemForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            billItems = []
            g = Bill(title=cd['title'], description=cd['description'], book=Book(pk=bookId), date=cd['date'], create_by=request.user, amount=cd['amount'])
            g.save()
            for contactId in request.POST["contactId0s"].strip(",").split(","):
                subAmount = request.POST['subCount0_'+contactId]
                billItems.append(Bill_Item(contact=Contact(pk=contactId), amount=subAmount, bill=g))

            for contactId in request.POST["contactIds"].strip(",").split(","):
                subAmount = -float(request.POST['subCount_'+contactId])
                billItems.append(Bill_Item(contact=Contact(pk=contactId), amount=subAmount, bill=g))
            for billItem in billItems:
                billItem.save()
            return HttpResponseRedirect(getHost(request) + "/books/" + bookId + "/")
    else:
        form = ItemForm(initial={'type':'1'})
    contacts = [contactBook.contact for contactBook in Contact_Book.objects.filter(book=Book(pk=bookId))]
    return  render_to_response('books/item_form_aa.html', {'form':form, 'contacts':contacts},context_instance=RequestContext(request))
    
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
    return render_to_response('books/book_types.html', {'forms':l},context_instance=RequestContext(request))
    
def deleteBookTypes(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(getHost(request) + '/login/?next=%s' % request.path)  
    ids = request.GET["ids"].split(",")
    for idItem in ids:
        if idItem:
            Book_Type.objects.all().filter(id=idItem).delete()
    return HttpResponseRedirect(getHost(request) + "/bookTypes/")
