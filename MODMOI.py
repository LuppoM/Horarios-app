# modmoi.py
from modmoicontrolador import ModMoiController

def mostrar_modmoi(parent, conexion):
    """
    Punto de entrada para abrir la ventana MOD/MOI desde la aplicación principal.
    """
    # El controlador se encarga de crear la vista y comunicarse con el modelo
    ModMoiController(parent, conexion)
