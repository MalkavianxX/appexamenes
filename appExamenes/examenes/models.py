from django.db import models

# Create your models here.
class Categoria(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.name
    
class Pregunta(models.Model):
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    text = models.CharField(max_length=100000)
    imgage = models.ImageField(upload_to='pregunta_images/',blank=True, null=True)
    weight = models.IntegerField(default=1)
    answer = models.TextField(max_length=100000 , blank=True, null=True)
    date = models.DateField(auto_now_add=True)


    class Meta:
        ordering = ["text"]
        verbose_name_plural = 'preguntas'  

    def __str__(self):
        return self.text          


class Respuesta(models.Model):
    text = models.CharField(max_length=10000)
    correct = models.BooleanField(default=False)
    ask = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["text"]
        verbose_name_plural = 'respuestas'     

    def __str__(self):
        return self.text        
    

class Examen(models.Model):
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    time = models.FloatField(default=15.0)
    asks = models.ManyToManyField(Pregunta)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = 'examenes'    


    def __str__(self):
        return self.title   
