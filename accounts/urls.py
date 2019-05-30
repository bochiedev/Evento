from django.urls import path
from .views import RegisterView, LoginView, LogOutView, OTPView, validate_password, validate_username, validate_email

app_name = 'auth'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('otp-confirm/', OTPView.as_view(), name='otp'),
    path('validate-password/', validate_password , name='validate_password'),
    path('validate-username/', validate_username, name='validate_username'),
    path('validate-email/', validate_email, name='validate_email'),


]
