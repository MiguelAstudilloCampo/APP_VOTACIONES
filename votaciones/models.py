from django.db import models

from django.db import models

class Candidato(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='candidatos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Grado(models.Model):
    nombre = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre

class Votante(models.Model):
    numero_lista = models.IntegerField()
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="estudiantes")
    ha_votado = models.BooleanField(default=False)

    class Meta:
        unique_together = ['grado', 'numero_lista']  

class Voto(models.Model):
    votante = models.OneToOneField(Votante, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Voto de {self.votante} para {self.candidato}"
