# notificaciones.py

def notificar_dotacion_cargada(modelo, semana):
    """Recibe la instancia del modelo y el número de semana para delegar la inserción"""
    mensaje = f"La dotación teórica programada para la Semana {semana} ya se encuentra cargada en el sistema."
    
    # Se llama directamente al método que está adentro del Modelo
    exito = modelo.registrar_notificacion_global(semana, mensaje)
    
    if exito:
        print("Notificación registrada en la base de datos.")
    else:
        print("Error al registrar la notificación global.")