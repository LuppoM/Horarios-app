import os
import subprocess
import sys

# Ruta del servidor y ejecutable de la app
RUTA_RED = r"\\HUGO-PC5\Compartir\PRODUCTIVIDADnueva\Horariosapp"
EXE_APP = os.path.join(RUTA_RED, "principal.exe")  # Cambiá por el nombre real de tu .exe

if os.path.exists(EXE_APP):
  # cwd (Current Working Directory) hace que el .exe reconozca la base de datos que tiene al lado en la red
  subprocess.Popen([EXE_APP], cwd=RUTA_RED)
else:
  import tkinter as tk
  from tkinter import messagebox

  root = tk.Tk()
  root.withdraw()
  messagebox.showerror(
      "Error de Red",
      "No se pudo conectar con el servidor HUGO-PC5.\nVerifique la conexión de"
      " red o el cable e intente nuevamente.",
  )
  sys.exit()