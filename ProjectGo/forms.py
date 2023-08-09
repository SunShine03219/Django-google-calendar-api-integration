from django                     import forms
from Communication.models       import MessagesHome
from django.contrib.auth.forms  import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth        import authenticate
from django.contrib.auth.models import User

class SignIn(AuthenticationForm):
        
    username    = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your username'}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your password'}))
    
    def is_credentials_valid(self):
        print(self.is_valid())
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
        
            # Check if the username and password are correct
            user = authenticate(username=username, password=password)
            if user is None:
                print('Error...')
                return True
        else:
            print(self.errors)  # Print the form errors
        
        return False  
    

class SignupForm(UserCreationForm):
    username    = forms.CharField   (widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username' }))
    email       = forms.EmailField  (widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your email' }))
    password1   = forms.CharField   (widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your password'}),label='Password')
    password2   = forms.CharField   (widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm your password'}), label='Confirm Password')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class MessagesHomeForm(forms.ModelForm):
    class Meta:
        model = MessagesHome
        fields = ['name', 'phone', 'email', 'message']

        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter your Name'}),
            'phone':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': '... and your Phone'}),
            'email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '... and your Email'}),
            'message':  forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Thank you for your Message'}),
        }
        
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user with this email.")
        return email