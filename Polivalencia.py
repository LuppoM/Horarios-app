import tkinter as tk
from polivalenciacontrolador import ControladorPolivalencia

def mostrar_matriz_polivalencia(root, conexion):
    """
    Función puente homóloga a tu 'mostrar_hchoco'.
    Lanza la grilla interactiva vinculada a los operarios ya existentes.
    """
    controlador = ControladorPolivalencia(root, conexion)