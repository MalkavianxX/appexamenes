from django.db import models
from examenes.models import Examen, Respuesta
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Universidad(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to='unis_images')
    gn_average_min = models.FloatField(default=0.0) #promedio minimo
    gn_average_max = models.FloatField(default=0.0) #promedio maxmimo
    gn_students = models.IntegerField(default=0.0) #numero total de aspirantes
    gn_success_st = models.FloatField(default=0.0) #numero de admitidos

    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'Universidades'  

    #metodos para calcular la complejidad
    def __str__(self):
        return self.name      

class MiExamen(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Quien hizo el examen
    test = models.ForeignKey(Examen, on_delete=models.CASCADE)  #Que examen hizo
    score = models.FloatField(default=0.0) #calificacion que obtuvo
    time = models.CharField(max_length=1000000) #tiempo que le llevo hacerlo
    status = models.CharField(max_length=50, blank=True, null=True ) #estado del examen (aprobado, reprobado, incompleto)
    date = models.DateTimeField(auto_now_add=True) #fecha que hizo el examen
    asnwers = models.ManyToManyField(Respuesta,blank=True, null=True) #respuestas que seleccionó
    time_ans = models.CharField(max_length=10000, blank=True, null=True) #lista del intervalo de tiempo entre preguntas (osea el tiempo que tardo en responder cada pregunta)

    class Meta:
        ordering = ["score"]
        verbose_name_plural = 'MisExamenes'  

    def __str__(self):
        return str(self.test)          

class MiPerfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    average = models.FloatField(default=0.0)
    objectives = models.ManyToManyField(Universidad)
    total_test = models.IntegerField(default=0)

    def __str__(self):
        return str(self.average)

    # Señal para crear automáticamente un perfil cuando se crea un nuevo usuario
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_mi_perfil(sender, instance, created, **kwargs):
        if created:
            MiPerfil.objects.create(user=instance)

    # Señal para guardar automáticamente el perfil cuando se guarda el usuario
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_mi_perfil(sender, instance, **kwargs):
        instance.miperfil.save()
