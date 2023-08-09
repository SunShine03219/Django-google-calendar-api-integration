from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import Company
from django.contrib import messages




class UpdateUsernameEmail(forms.Form):
    username    = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email       = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control','type': 'email'}))
    class Meta:
        model = User
        fields = ('username', 'email')
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Please Enter your old Password'}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Please Enter your new Password'}),
        strip=False,
        help_text="Your new password can't be too similar to your other personal information. "
                  "Your password must contain at least 8 characters. "
                  "Your password can't be a commonly used password. "
                  "Your password can't be entirely numeric."
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Please Re-Enter your new Password'}),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return old_password

class CompanyEdit(forms.ModelForm):
    COUNTRY_CHOICES = (
        ('L', 'Luxembourg'),
        ('F', 'France'),
        ('BE', 'Belgique'),
        ('DE', 'Allemagne'),
    )

    logo            =   forms.ImageField    (required=False, widget=forms.FileInput(attrs={'class': 'form-control btn btn-primary','accept': 'image/*',}),label='Logo')
    company         =   forms.CharField     (max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Companie Name'}),label='Company Name')
    tva             =   forms.CharField     (max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter TVA number'}),label='TVA number')
    emailToContact  =   forms.EmailField    (required=True,widget=forms.EmailInput(attrs={'class': 'form-control','type': 'email','placeholder': 'Email Adresse for Customers'}),label='Email')
    telephone       =   forms.CharField     (max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter phone number'}),label='Phone number')
    address         =   forms.CharField     (max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter address'}),label='Address')
    postcode        =   forms.CharField     (max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter postal code'}),label='Postal code')
    city            =   forms.CharField     (max_length=20,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter city'}),label='City')
    state           =   forms.ChoiceField   (choices=COUNTRY_CHOICES,widget=forms.Select(attrs={'class': 'form-select'}),label='State or Province')
    description     =   forms.CharField     (max_length=10000, widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'Description', 'rows': 4}),label='Description')

    class Meta:
        model = Company
        fields = ('logo', 'company', 'tva', 'emailToContact', 'telephone', 'address', 'postcode', 'city', 'state', 'description')
