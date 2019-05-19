from django.db import models
from django.contrib.auth import get_user_model
from evento.utils import now_plus_5_minutes
from datetime import datetime
from django.utils import timezone


# Create your models here.

class OTP(models.Model):
    code = models.IntegerField()
    username = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(default=now_plus_5_minutes)

    @property
    def is_expired(self):
        if timezone.now() > self.expiry:
            return True
        return False
