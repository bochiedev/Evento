from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from accounts.forms import UserCreationForm, LoginForm, OTPForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from evento.utils import send_email, generateOTP
from .models import OTP

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

            messages.success(request ,f'Welcome to Envento, Login to access account!')
            return redirect("auth:login")

        else:
            return render(request,'auth/register.html', {'form': form})

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
