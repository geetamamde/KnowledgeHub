
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate ,login


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=20 , required = True)
    last_name = forms.CharField(max_length=20 , required = True)
    email = forms.EmailField(max_length=25 , required = True)
    class Meta:
        model = User
        fields = ['first_name'
         , 'last_name' , 'username'
          , "email" , 'password1'  ]
        
    def clean_email(self):
        email = self.cleaned_data['email']
        user = None
        try:
            user = User.objects.get(email = email)
         #user = User.objects.get(emial = email)
        except:
          return email
        if(user is not None):
           raise ValidationError ('User Already Exists')
    

class LoginForm(AuthenticationForm):

    username = forms.EmailField(max_length=25 , required = True , label='Email Address')

    def clean(self):
        email = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = None
        try:
            user = User.objects.get(email = email)
            result = authenticate(username = user.username , password = password)

            if(result is not None):
                return result
            else:
                raise ValidationError("Email or Password invalid")
        except:
            raise ValidationError("Email or Password invalid")