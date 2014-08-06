# encoding: utf-8
from django import forms
from books.models import Book

class BookForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    
    class Meta :
        model = Book
        fields = ('name', 'description', 'book_type')
class ItemForm(forms.Form):
    title = forms.CharField(label='名称')
    description = forms.CharField(label='描述', required=False)
    mount = forms.DecimalField(label='金额')
    type = forms.CharField(label='类型', widget=forms.Select(choices=[('0', '支出'),('1', '存入')]))
    relatedUsers = forms.CharField()
    
class BookTypeForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()

