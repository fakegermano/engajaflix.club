from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class UuidSession(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.uuid)
    
    @property
    def has_email_reserve(self) -> bool:
        has_reserve = False
        try:
            has_reserve = (self.email_reserve is not None)
        except EmailReserve.DoesNotExist:
            pass
        return has_reserve

class EmailReserve(models.Model):
    email = models.EmailField(unique=True)
    social = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.OneToOneField(UuidSession, on_delete=models.CASCADE, related_name="email_reserve")
    reserved = models.BooleanField(default=True)

    def __str__(self):
        return self.email