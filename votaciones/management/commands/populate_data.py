from django.core.management.base import BaseCommand
from votaciones.models import Grado, Votante

class Command(BaseCommand):
    help = "Crea grados y asigna estudiantes automáticamente"

    def handle(self, *args, **kwargs):
        # Crear los grados si no existen
        grados_nombres = ["1°", "2°", "3°", "4°", "5°"]
        for nombre in grados_nombres:
            grado, created = Grado.objects.get_or_create(nombre=nombre)
            if created:
                # Agregar 30 estudiantes al grado
                for i in range(1, 31):
                    Votante.objects.create(numero_lista=i, grado=grado)

        self.stdout.write(self.style.SUCCESS("Grados y estudiantes creados correctamente"))
