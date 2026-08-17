from django import forms
from .models import Group


class GroupCreateForm(forms.Form):
    name = forms.CharField(max_length=100, label='اسم گروه')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز گروه')


class GroupJoinForm(forms.Form):
    name = forms.CharField(max_length=100, label='اسم گروه')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز گروه')