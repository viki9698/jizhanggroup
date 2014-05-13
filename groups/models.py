from django.db import models

# Create your models here.
class Group(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    create_date=models.DateField()
    group_type = models.CharField(max_length=10)

class User(models.Model):
    username=models.CharField(max_length=20)
    displayName=models.CharField(max_length=50)
    groups=models.ManyToManyField(Group)
    user_type = models.CharField(max_length=10)
class Bill(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    create_date = models.DateField()
    group = models.ForeignKey(Group)
    
class BillItem(models.Model):
    user = models.ForeignKey(User)
    itemType = models.CharField(max_length=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill = models.ForeignKey(Bill)
