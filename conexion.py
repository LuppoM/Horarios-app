import os
import sqlite3
import sys

def obtener_conexion():
    if getattr(sys, 'frozen', False):
        # Si está congelado por PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # En desarrollo (sin compilar)
        base_path = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(base_path, "HORARIOS.db")
    return sqlite3.connect(db_path)

def obtener_ruta_icono(nombre_icono="icono.ico"):
    if getattr(sys, 'frozen', False):
        # Si está congelado por PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # En desarrollo
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, nombre_icono)