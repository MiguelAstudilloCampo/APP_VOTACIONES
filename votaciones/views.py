from django.shortcuts import render, redirect
from .models import Grado, Votante, Candidato, Voto
from django.contrib import messages

def login(request): 
    if request.method == 'POST':
        grado_id = request.POST.get('grado')
        numero_lista = request.POST.get('numero_lista')
        
        try:
            grado = Grado.objects.get(id=grado_id)
            votante = Votante.objects.get(grado=grado, numero_lista=numero_lista)
            
            # Verificar si es Profesor
            if grado.nombre == "Profesor":
                # Redirigir a vista de conteo de votos
                request.session['votante_id'] = votante.id
                return redirect('vistaVotos')
            else:
                # Verificar si ya votó (solo para no profesores)
                if votante.ha_votado:
                    messages.error(request, 'Ya has votado.')
                    return redirect('login')
                # Redirigir a votación
                request.session['votante_id'] = votante.id
                return redirect('vistaVotacion')
                
        except (Grado.DoesNotExist, Votante.DoesNotExist):
            messages.error(request, 'Credenciales incorrectas.')
            return redirect('login')
    
    grados = Grado.objects.all()
    return render(request, 'Vistas_Aplicativo/login.html', {'grados': grados})

def vistaVotacion(request):  # Asegúrate de que el nombre coincida con la URL
    # Verificar sesión
    votante_id = request.session.get('votante_id')
    if not votante_id:
        return redirect('login')
    
    votante = Votante.objects.get(id=votante_id)
    
    # Si es profesor, redirigir
    if votante.grado.nombre == "Profesor":
        return redirect('vistaVotos')
    
    # Si ya votó, redirigir con mensaje
    if votante.ha_votado:
        messages.error(request, 'Ya has votado.')
        return redirect('login')
    
    # Procesar voto si es POST
    if request.method == 'POST':
        candidato_id = request.POST.get('candidato_id')
        
        # Manejar voto en blanco
        if candidato_id == 'blanco':
            # Crear voto en blanco (ajusta según tu modelo)
            Voto.objects.create(votante=votante, candidato=None)
        else:
            try:
                candidato = Candidato.objects.get(id=candidato_id)
                Voto.objects.create(votante=votante, candidato=candidato)
            except Candidato.DoesNotExist:
                messages.error(request, 'Candidato no válido.')
                return redirect('vistaVotacion')
        
        # Marcar votante como ha votado
        votante.ha_votado = True
        votante.save()
        
        # Cerrar sesión o redirigir
        del request.session['votante_id']
        messages.success(request, 'Voto registrado exitosamente.')
        return redirect('login')
    
    # GET: Mostrar candidatos
    candidatos = Candidato.objects.all()
    return render(request, 'Vistas_Aplicativo/vistas_votacion.html', {'candidatos': candidatos})

def conteoVotos(request):
    # Verificar sesión
    votante_id = request.session.get('votante_id')
    if not votante_id:
        return redirect('login')
    
    # Obtener votante y validar su grado
    votante = Votante.objects.get(id=votante_id)
    if votante.grado.nombre != "Profesor":
        messages.error(request, 'Acceso restringido.')
        return redirect('login')
    
    # Lógica del conteo de votos
    candidatos_con_votos = []
    for candidato in Candidato.objects.all():
        total = Voto.objects.filter(candidato=candidato).count()
        candidatos_con_votos.append({
            'nombre': candidato.nombre,
            'imagen': candidato.imagen,
            'votos': total
        })
    
    # Votos en blanco (asumiendo candidato=None)
    votos_blanco = Voto.objects.filter(candidato__isnull=True).count()
    
    return render(request, 'Vistas_Aplicativo/listas_votos.html', {
        'resultados': candidatos_con_votos,
        'votos_blanco': votos_blanco
    })