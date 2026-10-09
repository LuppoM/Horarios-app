# principal.py
import tkinter as tk
from principalcontrolador import AppController

def principal():
    try:
        root = tk.Tk()
        app = AppController(root)
        root.mainloop()

    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    principal()
