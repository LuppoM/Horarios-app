# notificaciones.py
import os
from plyer import notification
from conexion import obtener_ruta_icono

def enviar_notificacion_windows(titulo, mensaje, tiempo_segundos=5):
    """
    Lanza una notificación nativa en el escritorio de Windows.
    """
    ruta_icono = None
    try:
        ruta_icono = obtener_ruta_icono("icono.ico")
        if not os.path.exists(ruta_icono):
            ruta_icono = None
    except Exception:
        ruta_icono = None

    try:
        notification.notify(
            title=titulo,
            message=mensaje,
            app_name="Sistema de Dotaciones",
            app_icon=ruta_icono,
            timeout=tiempo_segundos
        )
    except Exception as e:
        print(f"Error al enviar notificación de Windows: {e}")

def notificar_dotacion_cargada(semana):
    """
    Función específica para el flujo de Dotación Teórica Programada.
    """
    titulo = "Dotación Teórica Cargada"
    mensaje = f"La dotación para la Semana {semana} fue guardada exitosamente y queda lista para supervisión."
    enviar_notificacion_windows(titulo, mensaje)