from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class OTP(models.Model):
    code = models.CharField(max_length=20)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
