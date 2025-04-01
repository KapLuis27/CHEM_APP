from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class SignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    license_expiration = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Member
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'marital_status', 'license_expiration', 'password1', 'password2']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'marital_status', 'license_expiration']
        