from django.db import models
import datetime
# Create your models here.
class Group(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    create_date=models.DateField('date published', blank=True, 
        default=datetime.datetime.now().date())
    group_type = models.CharField(max_length=10)
    def __unicode__(__self):
        return __self.name

class User(models.Model):
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    displayName=models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10)
    create_date=models.DateField('date published', blank=True, 
        default=datetime.datetime.now().date())
    def __unicode__(__self):
        return __self.displayName

class User_Group(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_owner = models.CharField(max_length=1)

class Bill(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    create_date=models.DateField('date published', blank=True, 
        default=datetime.datetime.now().date())
    group = models.ForeignKey(Group)
    
class BillItem(models.Model):
    user = models.ForeignKey(User)
    itemType = models.CharField(max_length=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill = models.ForeignKey(Bill)
