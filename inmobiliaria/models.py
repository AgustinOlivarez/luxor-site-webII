from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Consulta(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    fecha = models.DateField()
    categoria = models.CharField(max_length=50, default="General")
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"
class UsuarioPermitido(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    codigo_validacion = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} - {self.email}"