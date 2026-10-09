
import os
import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono

def crear_ventana(parent, titulo):
    ventana = tk.Toplevel(parent)
    ventana.title(titulo)
    ventana.geometry("650x320")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()

    try:
        ventana.iconbitmap(obtener_ruta_icono("icono.ico"))
    except Exception:
        pass

    return ventana

def crear_toolstrip(ventana):
    barra = tk.Frame(ventana, bg="#dde6ed", height=60)
    barra.pack(fill=tk.X)
    barra.pack_propagate(False)

    fuente = ("Segoe UI", 11, "bold")
    fg = "#003366"
    bg = "#cfe2f3"
    hover = "#a4c2f4"

    def boton(texto, x):
        b = tk.Button(
            barra,
            text=texto,
            font=fuente,
            fg=fg,
            bg=bg,
            activebackground=hover,
            activeforeground=fg,
            bd=0,
            relief="flat",
        )
        b.place(x=x, y=10, width=120, height=40)
        return b

    return {"guardar": boton("Guardar", 10), "cancelar": boton("Cancelar", 150)}

def crear_formulario(ventana):
    frame = tk.Frame(ventana, bg="#f0f4f8")
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    tk.Label(
        frame, text="Tipo:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=0, column=0, sticky="w", pady=10)
    
    # --- CORRECCIÓN: Se reemplaza ttk.Combobox por ttk.Entry ---
    txt_tipo = ttk.Entry(
        frame, 
        width=45,
        font=("Segoe UI", 10)
    )
    txt_tipo.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky="w")
    txt_tipo.focus() # Opcional: enfoca directamente el campo al abrir

    tk.Label(
        frame, text="Horarios / Turnos:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=1, column=0, sticky="nw", pady=5)

    # Contenedor para los selectores dinámicos de horarios y el botón "+"
    frame_contenidos = tk.Frame(frame, bg="#f0f4f8")
    frame_contenidos.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    return {
        "tipo": txt_tipo, 
        "frame_contenidos": frame_contenidos
    }