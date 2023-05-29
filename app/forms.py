from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    """
    A registration form for customers.

    Inherits from the UserCreationForm provided by Django and adds custom styling to form fields.

    """
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class loginForm(AuthenticationForm):
    """
    A login form for customers.

    Inherits from the AuthenticationForm provided by Django and adds custom styling to form fields.

    """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    """
    A form for updating customer profile information.

    Inherits from the ModelForm provided by Django and specifies the fields and widgets for the form.

    """
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode']
        widgets = {
            'name' :forms.TextInput(attrs={'class' : 'form-control'}),
            'locality' :forms.TextInput(attrs={'class' : 'form-control'}),
            'city' :forms.TextInput(attrs={'class' : 'form-control'}),
            'mobile' :forms.NumberInput(attrs={'class' : 'form-control'}),
            'state' :forms.Select(attrs={'class' : 'form-control'}),
            'zipcode' :forms.NumberInput(attrs={'class' : 'form-control'}),
        }

class MyPasswordChangeForm(PasswordChangeForm):
    """
    A form for changing password information.

    Inherits from the PasswordChangeForm provided by Django and specifies the fields and widgets for the form.

    """
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password', 'class':'form-control' }))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password', 'class':'form-control' }))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password', 'class':'form-control' }))

class MySetPasswordForm(SetPasswordForm):
    """
    A form for setting the password information.

    Inherits from the SetPasswordForm provided by Django and specifies the fields and widgets for the form.

    """
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control' }))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control' }))