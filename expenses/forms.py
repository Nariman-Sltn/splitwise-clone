from django import forms
from django.contrib.auth.models import User
from .models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

class SettlementForm(forms.Form):
    paid_to = forms.ModelChoiceField(queryset=None, label='به چه کسی پرداخت کردی؟')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='مبلغ')

    def __init__(self, *args, group=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        member_users = User.objects.filter(group_memberships__group=group).exclude(id=user.id)
        self.fields['paid_to'].queryset = member_users


class FarsiUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'نام کاربری الزامیه.',
            'unique': 'این نام کاربری قبلاً استفاده شده.',
        }
        self.fields['password1'].error_messages = {
            'required': 'رمز عبور الزامیه.',
        }
        self.fields['password2'].error_messages = {
            'required': 'تکرار رمز عبور الزامیه.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('رمزهای عبور با هم مطابقت ندارن.')
        return password2

    def _post_clean(self):
        super()._post_clean()
        # خطاهای مربوط به قدرت پسورد رو فارسی می‌کنیم
        if self.errors.get('password2'):
            return
        password = self.cleaned_data.get('password1')
        if password:
            errors = []
            if len(password) < 8:
                errors.append('رمز عبور باید حداقل ۸ کاراکتر باشه.')
            if password.isdigit():
                errors.append('رمز عبور نمی‌تونه فقط عدد باشه.')
            if errors:
                self.add_error('password1', errors)