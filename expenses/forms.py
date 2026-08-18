from django import forms
from django.contrib.auth.models import User
from .models import Group


class GroupCreateForm(forms.Form):
    name = forms.CharField(max_length=100, label='اسم گروه')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز گروه')


class GroupJoinForm(forms.Form):
    name = forms.CharField(max_length=100, label='اسم گروه')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز گروه')


class ExpenseCreateForm(forms.Form):
    title = forms.CharField(max_length=200, label='بابت چی؟')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='مبلغ کل')
    paid_by = forms.ModelChoiceField(queryset=None, label='چه کسی پرداخت کرد؟')
    participants = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label='چه کسانی تو این هزینه سهیم‌ان؟'
    )

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        member_users = User.objects.filter(group_memberships__group=group)
        self.fields['paid_by'].queryset = member_users
        self.fields['participants'].queryset = member_users