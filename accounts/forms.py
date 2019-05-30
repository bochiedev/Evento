from django import forms
from django.contrib.auth.models import User
from evento.utils import Validate


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label="Password")

    class Meta:
        model = User
        fields = ('username','email','password')
        widgets = {
            'username': forms.TextInput(attrs={"placeholder":"Enter Username"}),
            'email': forms.EmailInput(attrs={"placeholder":"Enter Email Address"}),
            'password': forms.PasswordInput(attrs={"placeholder":"Enter Password"}),

        }

    def __init__(self,  *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = "Password must contain a minimum of 6 characters, atleast one uppercase,one lowercase, one digit and a character "
        self.fields['email'].help_text = "Enter a valid email"
        self.fields['username'].help_text = "Letters digits and characters only"



    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username {} is already in use.'.format(username))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Email {} is already in use.'.format(email))
        else:
            validate = Validate(email=email)
            validate_email = validate.validate_email()

            if validate_email == True:
                password = validate_email
            else:
                raise forms.ValidationError(validate_email)

        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        validate = Validate(password=password)
        validate_password = validate.validate_password()

        if validate_password == True:
            password = self.cleaned_data['password']
        else:
            raise forms.ValidationError(validate_password)

        return password


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username']

class OTPForm(forms.Form):
    otp = forms.IntegerField()
