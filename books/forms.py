# encoding: utf-8
from django import forms
from books.models import Book, Contact
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)
    class Meta :
        model = Book
        fields = ('name', 'description', 'book_type')
        
class ContactForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    
    class Meta :
        model = Contact
        fields = ('name', 'description', 'user')
        
class ItemForm(forms.Form):
    title = forms.CharField(label='名称')
    description = forms.CharField(label='描述', required=False)
    amount = forms.DecimalField(label='金额')
    date = forms.DateField(label='日期')
    type = forms.CharField(label='类型', widget=forms.RadioSelect(choices=[('0', '支出'),('1', '存入')]))
    
class BookTypeForm(forms.Form):
    code = forms.CharField()
    name = forms.CharField()
    description = forms.CharField()

