from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
    
class Libro(models.Model):
    bookId = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    genero =  models.CharField(max_length=100)
    idioma = models.CharField(max_length=100, null=True)
    num_ratings_1 = models.IntegerField()
    num_ratings_2 = models.IntegerField()
    num_ratings_3 = models.IntegerField()
    num_ratings_4 = models.IntegerField()
    num_ratings_5 = models.IntegerField()
    
    def __str__(self):
        return self.titulo
    
class Puntuacion(models.Model):
    puntuacion = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    bookId = models.ForeignKey(Libro, on_delete=models.CASCADE)
    idUsuario = models.IntegerField()

    def __str__(self):
        return str(self.puntuacion)