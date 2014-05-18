from django import forms

class GroupForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    group_type = forms.CharField()
