from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from accounts.forms import UserCreationForm, LoginForm, OTPForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from evento.utils import send_email, generateOTP, Validate
from .models import OTP
from django.http import JsonResponse


# Create your views here.
class RegisterView(View):
    title = "Evento | Register"
    def get(self, request):
        if request.user.is_authenticated != True:
            form = UserCreationForm

            context = {
                'form': form,
                'title': self.title,
                }

            template = 'auth/register.html'
            return render(request=request,
                          template_name=template,
                          context=context)
        else:
         return redirect('home')


    def post(self, request):

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user_obj = form.save(commit=False)
            password = form.cleaned_data['password']

            user_obj.set_password(password)
            user_obj.is_superuser = False
            user_obj.is_staff = False
            user_obj.save()
            send_mail = send_email(subject = 'Welcome To Envento', mail_from='bochiegfx@gmail.com', to_emails=[form.cleaned_data['email']], template='includes/welcome.html', data={'username': form.cleaned_data['username']})

            data = {
                'success' :True,
                'message': 'Welcome to Envento, Login to access account!',
                }

            return JsonResponse(data)

        else:
            error_message = dict([(key, [error for error in value]) for key, value in form.errors.items()])

            data = {
                'success' :False,
                "message":error_message
            }
            return JsonResponse(data)


class LoginView(View):
    title = "Evento | Login"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = LoginForm
            context = {
                        'form': form,
                        'title':self.title,
                        }
            template = 'auth/login.html'
            return render(request=request,
                          template_name=template,
                          context=context)

    def post(self, request):
        if request.method == "POST":
            form = LoginForm(request.POST)

            username = form.data['username']
            password = form.data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                user = User.objects.get(username=username)
                otp = generateOTP()
                otp_obj, created = OTP.objects.get_or_create(
                        code=int(otp),
                        username=username,
                        secret=password,
                    )
                send_mail = send_email(subject = '2Factor-Auth OTP', mail_from='bochiegfx@gmail.com', to_emails=[user.email], template='includes/otp.html', data={'otp': otp})
                messages.success(request ,f'Please Enter The OTP sent to Your Email!')
                return redirect("auth:otp")

            else:
                messages.error(request, 'Wrong email or Password!')
                return redirect("auth:login")


class LogOutView(View):

    def get(self, request):
        try:
            logout(request)
            return redirect('home')

        except:
            return redirect('home')

class OTPView(View):

    def get(self, request):
        form = OTPForm
        context = {
                    'form': form
                    }
        template = 'auth/otp.html'
        return render(request=request,
                      template_name=template,
                      context=context)

    def post(self, request):
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                otp_obj = OTP.objects.get(code=otp)

                if otp_obj.is_expired:
                    otp_obj.delete()
                    messages.error(request, 'OTP has expired Please Login again!')
                    return redirect("auth:login")

                else:
                    user = authenticate(username=otp_obj.username, password=otp_obj.secret)
                    login(request, user)
                    otp_obj.delete()
                    return redirect("home")
            except:
                messages.error(request, 'OTP Does not exist!')
                return redirect("auth:otp")

def validate_password(request):
    password = request.GET.get('password', None)

    validate = Validate(password=password)
    validate_password = validate.validate_password()

    if validate_password == True:
        response = validate_password
        validate_password = "Password is strong!"
    else:
        response = False
        validate_password = validate_password

    data = {
        'password_response': response,
        'message': validate_password

    }
    return JsonResponse(data)

def validate_email(request):
    email = request.GET.get('email', None)
    is_taken = User.objects.filter(email__iexact=email).exists()

    data = {
        'email_is_taken': is_taken
    }
    return JsonResponse(data)

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'username_is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
