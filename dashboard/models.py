from django.db import models
from examenes.models import Examen, Respuesta
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Invitation(models.Model):
    status = models.BooleanField(default=False)
    code = models.CharField(max_length=10)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Quien hizo el examen
    date_create = models.DateTimeField(auto_now_add=True)
    date_use = models.DateTimeField(blank=True, null=True)
    link = models.CharField(max_length=1000,blank=True, null=True)

    class Meta:
        ordering = ["date_create"]
        verbose_name_plural = 'Invitaciones'  
 
    #metodos para calcular la complejidad
    def __str__(self):
        return self.code      
    
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

    #percent
    answers_response = models.FloatField(default=0, null=True, blank=True)
    percent_time_ussles = models.FloatField(default=0, null=True, blank=True)  
    
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
    test_aproval = models.IntegerField(default=0)
    test_failures = models.IntegerField(default=0)
    test_incomplete = models.IntegerField(default=0)
    invitation_code = models.ForeignKey(Invitation,on_delete=models.CASCADE ,  null=True, blank=True)
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

    def actualizar_promedio_general(self):
        # Obtén todos los exámenes asociados al usuario
        examenes = MiExamen.objects.filter(user=self.user)

        # Calcula el nuevo promedio general
        total_examenes = examenes.count()
        sumatoria_promedios = sum(examen.score for examen in examenes)
        
        if total_examenes > 0:
            self.average = sumatoria_promedios / total_examenes
        else:
            self.average = 0.0
        self.average = float("{0:.2f}".format(self.average))
        # Guarda la instancia actualizada
        self.save()

    def actualizar_total_examenes(self):
        # Obtén la cantidad total de exámenes realizados
        total_examenes = MiExamen.objects.filter(user=self.user).count()

        # Actualiza el campo total_test
        self.total_test = total_examenes

        # Guarda la instancia actualizada
        self.save()        

    def actualizar_estadisticas_examenes(self, examen):
        # Actualiza las estadísticas en función de si el examen fue aprobado o reprobado
        if examen.status == "Aprobado":
            self.test_aproval += 1
        elif examen.status == "Incompleto":
            self.test_incomplete +=1
        elif examen.status == "Reprobado":
            self.test_failures += 1

        # Guarda la instancia actualizada
        self.save()        

    @property
    def categorias_diferentes(self):
        return self.contar_categorias_diferentes()
    

    def contar_categorias_diferentes(self):
        # Obtén todas las categorías de exámenes realizados por el usuario
        categorias_diferentes = MiExamen.objects.filter(user=self.user).values_list('test__category__name', flat=True).distinct()

        # Devuelve la cantidad de categorías diferentes
        return len(categorias_diferentes)        
    
    @property
    def porcentaje_aprobados(self):
        return "{0:.1f}".format(MiExamen.objects.filter(status='Aprobado').count() / self.total_test * 100 if self.total_test > 0 else 0) 

    @property
    def porcentaje_tiempo_acabado(self):
        return "{0:.1f}".format(MiExamen.objects.filter(status='Incompleto').count() / self.total_test * 100 if self.total_test > 0 else 0)

    @property
    def porcentaje_reprobados(self):
        return "{0:.1f}".format(MiExamen.objects.filter(status='Reprobado').count() / self.total_test * 100 if self.total_test > 0 else 0)