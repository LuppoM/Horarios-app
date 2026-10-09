# abmmodmoi.py
from abmcontrolador import AbmModMoiControlador

def mostrar_abmmodmoi(parent, conexion, callback_recarga=None, datos_existentes=None):
    """
    Abre la ventana ABM MOD/MOI.
    """
    AbmModMoiControlador(parent, conexion, callback_recarga, datos_existentes)
