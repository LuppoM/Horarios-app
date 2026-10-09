import os
import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono

def crear_ventana(parent, titulo="Supervisor"):
    ventana = tk.Toplevel(parent)
    ventana.title(titulo)
    ventana.geometry("500x230")
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
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

    # Campo Nombre y Apellido
    tk.Label(
        frame, text="Nombre:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=0, column=0, sticky="w", pady=8)
    entry_nombre = ttk.Entry(frame, width=38, font=("Segoe UI", 10))
    entry_nombre.grid(row=0, column=1, pady=8, padx=10)

    # Campo Email
    tk.Label(
        frame, text="Email:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=1, column=0, sticky="w", pady=8)
    entry_email = ttk.Entry(frame, width=38, font=("Segoe UI", 10))
    entry_email.grid(row=1, column=1, pady=8, padx=10)

    # Campo Planta
    tk.Label(
        frame, text="Planta:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=2, column=0, sticky="w", pady=8)
    combo_planta = ttk.Combobox(
        frame, values=["Chocolate", "Golosinas"], state="readonly", width=36, font=("Segoe UI", 10)
    )
    combo_planta.grid(row=2, column=1, pady=8, padx=10)
    combo_planta.current(0)

    return {
        "nombre": entry_nombre,
        "email": entry_email,
        "planta": combo_planta
    }