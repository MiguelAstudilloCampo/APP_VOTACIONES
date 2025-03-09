from django.contrib import admin
from votaciones.models import Grado, Votante, Candidato, Voto

# Register your models here.

admin.site.register(Grado)
admin.site.register(Votante)
admin.site.register(Candidato)
