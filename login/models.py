from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError

def validate_file_type(value):
    ext = value.name.split('.')[-1]  # Obtiene la extensión del archivo
    valid_extensions = ['jpg', 'jpeg', 'png','gif']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Tipo de archivo no válido. Los tipos de archivo admitidos son jpg, jpeg, png.')
    
class User(AbstractUser):
    last_session_key = models.CharField(blank=True, null=True, max_length=40)
    description = models.TextField(default="Hola, esta es mi descripcion")
    color = models.CharField(max_length=1000,default="#5c70be")
    icon = models.ImageField(upload_to='profile_icons', blank=True, null=True,default='profile_icons/avatar_def.png', validators=[validate_file_type,])
    def set_session_key(self, key):
        if self.last_session_key and not self.last_session_key == key:
            try:
                Session.objects.get(session_key=self.last_session_key).delete()
            except Session.DoesNotExist:
                pass
        self.last_session_key = key
        self.save()
