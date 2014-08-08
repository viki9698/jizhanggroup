from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Book_Type(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    create_date=models.DateField('date published', blank=True, 
        default=datetime.datetime.now().date())
    def __unicode__(__self):
        return __self.name

class Book(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    create_date=models.DateField('date published', blank=True, 
        default=datetime.datetime.now().date())
    create_by = models.ForeignKey(User, null=True)
    book_type = models.ForeignKey(Book_Type)
    def __unicode__(__self):
        return __self.name

class Contact(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    create_date=models.DateField('date published', blank=True, 
        default=datetime.datetime.now().date())
    create_by = models.ForeignKey(User, related_name='creator')
    user =  models.ForeignKey(User, blank=True, null=True, related_name='user')
    def __unicode__(__self):
        return __self.name
        
class Contact_Book(models.Model):
    contact = models.ForeignKey(Contact)
    book = models.ForeignKey(Book)
    is_owner = models.CharField(max_length=1, default='0')

class Bill(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    create_date=models.DateField('date published', blank=True, 
        default=datetime.datetime.now().date())
    book = models.ForeignKey(Book)
    
class BillItem(models.Model):
    user = models.ForeignKey(User)
    itemType = models.CharField(max_length=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill = models.ForeignKey(Bill)
