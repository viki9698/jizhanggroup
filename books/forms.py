from django import forms

class BookForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    book_type = forms.CharField()
