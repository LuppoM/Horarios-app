import tkinter as tk
from Hgolocontrolador import ControladorHGolo

def mostrar_hgolo(root, conexion, modelo_principal):
    controlador = ControladorHGolo(root, conexion, modelo_principal)