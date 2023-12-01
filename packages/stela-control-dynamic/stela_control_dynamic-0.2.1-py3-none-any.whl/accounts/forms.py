from cProfile import label
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm, PasswordResetForm
from django import forms
from .models import UserBase
from geolocation.models import City, Country
from django.utils.translation import gettext_lazy as _
import re



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3', 'placeholder': 'example@email.com', 'id': 'login-username'}
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**********',
                'id': 'login-pwd',
            }
        )
    )

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'example@email.com', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '********',
            'id': 'login-pwd',
        }
    ))

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('username', 'email', 'full_name', 'address', 'phone_number', 'country_profile', 'city_profile', 'newsletter', )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        reg = UserBase.objects.filter(username=username)
        if reg.count():
            raise forms.ValidationError(_("This username already exists"))
        elif not re.match(r'^[a-z0-9_]+$', username):
            raise forms.ValidationError(_("invalid username only lower case, numbers and (_) accepted"))
        return username
    
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[a-zA-Z ]+$', full_name):
            raise forms.ValidationError(_("special characters not accepted"))
        return full_name
    
    def clean_phone_number(self): 
        phone_number = self.cleaned_data['phone_number'] 
        reg = UserBase.objects.filter(phone_number=phone_number) 
        if reg.count(): raise forms.ValidationError(_("This phone number already exists")) 
        elif not re.match(r'^\+?1?\d{9,15}$', phone_number): 
            raise forms.ValidationError(_("The phone number must be in format eg: +1654123456.")) 
        return phone_number
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if not re.match(r'^[a-zA-Z0-9, ]+$', address):
            raise forms.ValidationError(_("special characters not accepted"))
        return address
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError(_("Password must be at least 8 characters long"))
        if not re.match(r'^[a-zA-Z0-9*.$_]+$', password):
            raise forms.ValidationError(_("Password must contain only alphanumeric characters and some special characters"))
        if password.isdigit():
            raise forms.ValidationError(_("Password must contain at least one letter"))
        if password.isalpha():
            raise forms.ValidationError(_("Password must contain at least one number"))
        return password
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Password_mismatch.'))
        return cd['password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'example21'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'example@email.com', 'name': 'email', 'id': 'email' })
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': '********'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': '********'})
        self.fields['full_name'].label = False
        self.fields['username'].label = False
        self.fields['phone_number'].label = False 
        self.fields['password'].label = False 
        self.fields['password2'].label = False    
        self.fields['country_profile'].label = False
        self.fields['address'].label = False
        self.fields['city_profile'].queryset = City.objects.none()
        self.fields['city_profile'].label = False

        if 'country_profile' in self.data:
            try:
                country_id = int(self.data.get('country_profile'))
                self.fields['city_profile'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset



class UserEditForm(forms.ModelForm):

  email = forms.EmailField(
      label='Email (cannot be modified)', max_length=200, widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

  username = forms.CharField(
        label='Username (cannot be modified)', min_length=4, max_length=50, widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 'placeholder': 'place user', 'id': 'form-username', 'readonly': 'readonly'}))
    
  full_name = forms.CharField(
        label='Full Name', min_length=10, max_length=150, widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 'placeholder': 'Tell us your name', 'id': 'form-firstname'}))

  phone_number = forms.CharField(
        label='Phone', min_length=13, max_length=13, widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 'placeholder': '+582421234567', 'id': 'form-phone'}))

  address = forms.CharField(
        label='Address', min_length=15, max_length=300, widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 'placeholder': 'Street Avenue Building House', 'id': 'form-address'}))   

  class Meta:
        model = UserBase
        fields = ('email', 'username', 'full_name', 'image', 'country_profile', 'city_profile', 'phone_number', 'address')
        
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['city_profile'].queryset = City.objects.none()

        if 'country_profile' in self.data:
            try:
                country_id = int(self.data.get('country_profile'))
                self.fields['city_profile'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            try:
                self.fields['city_profile'].queryset = self.instance.country_profile.city_set.all()
            except:
                self.fields['city_profile'].queryset = City.objects.none()

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'E-mail','id': 'form-email'}), label=''
    )
    
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
         label=_('New Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Contraseña', 'id': 'form-newpasswd'}))
     
    new_password2 = forms.CharField(
         label=_('Confirm Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Contraseña', 'id': 'form-confirmpasswd'}))   
     
    def clean_new_password1(self):
        password = self.cleaned_data['new_password1']
        if len(password) < 8:
            raise forms.ValidationError(_("Password must be at least 8 characters long"))
        if not re.match(r'^[a-zA-Z0-9*.$_]+$', password):
            raise forms.ValidationError(_("Password must contain only alphanumeric characters and some special characters"))
        if password.isdigit():
            raise forms.ValidationError(_("Password must contain at least one letter"))
        if password.isalpha():
            raise forms.ValidationError(_("Password must contain at least one number"))
        return password

class CleanForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ['country_profile','city_profile','phone_number','address']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_profile'].queryset = City.objects.none()

        if 'country_profile' in self.data:
            try:
                country_id = int(self.data.get('country_profile'))
                self.fields['city_profile'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            try:
                self.fields['city_profile'].queryset = self.instance.country_profile.city_set.all()
            except:
                self.fields['city_profile'].queryset = City.objects.none()