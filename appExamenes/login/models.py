from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session

class User(AbstractUser):
    last_session_key = models.CharField(blank=True, null=True, max_length=40)

    def set_session_key(self, key):
        if self.last_session_key and not self.last_session_key == key:
            Session.objects.get(session_key=self.last_session_key).delete()
        self.last_session_key = key
        self.save()
