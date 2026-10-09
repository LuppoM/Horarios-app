import os
import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono


def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Agregar sector")
    ventana.geometry("600x260")  # Ampliado para dar espacio al nuevo campo
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()

    # Se invoca obtener_ruta_icono igual que en VistaHChoco
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


def crear_formulario(ventana, tipos_horario=None):
    frame = tk.Frame(ventana, bg="#f0f4f8")
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    # Campo Sector
    tk.Label(
        frame, text="Sector:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=0, column=0, sticky="w", pady=6)
    entry_nombre = ttk.Entry(frame, width=40, font=("Segoe UI", 10))
    entry_nombre.grid(row=0, column=1, pady=6, padx=10)

    # Campo Planta
    tk.Label(
        frame, text="Planta:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=1, column=0, sticky="w", pady=6)
    combo_planta = ttk.Combobox(
        frame, values=["Chocolate", "Golosinas"], state="readonly", width=38, font=("Segoe UI", 10)
    )
    combo_planta.grid(row=1, column=1, pady=6, padx=10)
    combo_planta.current(0)

    # Campo Tipo Horario
    tk.Label(
        frame, text="Tipo Horario:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=2, column=0, sticky="w", pady=6)
    
    opciones_tipos = tipos_horario if tipos_horario else ["ROTATIVO", "CENTRAL"]
    combo_tipohorario = ttk.Combobox(
        frame, values=opciones_tipos, state="readonly", width=38, font=("Segoe UI", 10)
    )
    combo_tipohorario.grid(row=2, column=1, pady=6, padx=10)
    if opciones_tipos:
        combo_tipohorario.current(0)

    # --- NUEVO CAMPO: Requiere Dotación ---
    tk.Label(
        frame, text="Requiere Dotación:", bg="#f0f4f8", font=("Segoe UI", 11, "bold")
    ).grid(row=3, column=0, sticky="w", pady=6)
    
    combo_dotacion = ttk.Combobox(
        frame, values=["Sí", "No"], state="readonly", width=38, font=("Segoe UI", 10)
    )
    combo_dotacion.grid(row=3, column=1, pady=6, padx=10)
    combo_dotacion.set("Sí")  # Por defecto en Sí

    return {
        "nombre": entry_nombre, 
        "planta": combo_planta, 
        "tipo_horario": combo_tipohorario,
        "requiere_dotacion": combo_dotacion
    }