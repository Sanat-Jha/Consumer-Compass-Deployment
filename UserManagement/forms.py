from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Consumer

class ConsumerRegistrationForm(UserCreationForm):
    class Meta:
        model = Consumer
        fields = ['email', 'username', 'password1', 'password2']

class ConsumerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError('Invalid login credentials')
        return self.cleaned_data
