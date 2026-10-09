import tkinter as tk
from Hchococontrolador import ControladorHChoco

def mostrar_hchoco(root, conexion):
  # se llama al controlador que trae vista y modeloi
    controlador = ControladorHChoco(root, conexion)
