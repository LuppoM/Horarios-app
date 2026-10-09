from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import abmtipohorariosvista as vista
import abmtipohorariosmodelo as modelo

def iniciar_abm_tipohorario(parent, conexion, modo, datos=None, on_guardar=None):
    titulo = "Agregar Tipo de Horario" if modo == "agregar" else "Modificar Tipo de Horario"
    ventana = vista.crear_ventana(parent, titulo)

    botones = vista.crear_toolstrip(ventana)
    elementos = vista.crear_formulario(ventana)
    
    # 1. Referencia al Entry (textbox)
    txt_tipo = elementos["tipo"]
    frame_contenidos = elementos["frame_contenidos"]
    
    filas_horarios = []
    
    # Generar lista de horas estándar (formato HH:00 o HH:MM)
    horas_disponibles = [f"{h:02d}:00" for h in range(24)]

    def agregar_fila_horario(val_inicio="", val_fin=""):
        row_frame = tk.Frame(frame_contenidos, bg="#f0f4f8")
        row_frame.pack(fill=tk.X, pady=3)

        cb_inicio = ttk.Combobox(row_frame, values=horas_disponibles, width=8, state="readonly", font=("Segoe UI", 10))
        cb_inicio.pack(side=tk.LEFT, padx=2)
        if val_inicio in horas_disponibles:
            cb_inicio.set(val_inicio)
        else:
            cb_inicio.current(6) # Default 06:00

        tk.Label(row_frame, text="a", bg="#f0f4f8", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)

        cb_fin = ttk.Combobox(row_frame, values=horas_disponibles, width=8, state="readonly", font=("Segoe UI", 10))
        cb_fin.pack(side=tk.LEFT, padx=2)
        if val_fin in horas_disponibles:
            cb_fin.set(val_fin)
        else:
            cb_fin.current(14) # Default 14:00

        # Botón para eliminar fila si hay más de una
        def eliminar_esta_fila():
            if len(filas_horarios) > 1:
                row_frame.destroy()
                filas_horarios.remove((cb_inicio, cb_fin))

        btn_eliminar = tk.Button(row_frame, text="✕", bg="#ffcccc", fg="#990000", bd=0, font=("Segoe UI", 9, "bold"), command=eliminar_esta_fila)
        btn_eliminar.pack(side=tk.LEFT, padx=8)

        filas_horarios.append((cb_inicio, cb_fin))

    # Botón "+" para agregar un nuevo selector de horario debajo
    btn_mas = tk.Button(
        frame_contenidos, 
        text="+ Agregar turno", 
        bg="#cfe2f3", 
        fg="#003366", 
        font=("Segoe UI", 9, "bold"),
        bd=0,
        relief="flat",
        command=lambda: agregar_fila_horario()
    )
    btn_mas.pack(anchor="w", pady=5)

    # Carga de datos si es modo modificar
    if modo == "modificar" and datos:
        tipo_id, tipo, horarios_str = datos
        # 2. Cargar texto en el Entry
        txt_tipo.delete(0, tk.END)
        txt_tipo.insert(0, tipo)
        
        # Desglosar los turnos guardados (ej: "06:00 a 14:00, 14:00 a 22:00")
        turnos = horarios_str.split(",")
        for t in turnos:
            partes = t.strip().split(" a ")
            if len(partes) == 2:
                agregar_fila_horario(partes[0].strip(), partes[1].strip())
            else:
                agregar_fila_horario()
    else:
        agregar_fila_horario("08:00", "16:00") # Fila inicial por defecto

    def guardar():
        # 3. Leer y normalizar texto del Entry
        tipo = txt_tipo.get().strip().upper()
        
        # Recolectar todos los horarios formados por los pares de comboboxes
        lista_final = []
        for cb_ini, cb_fin in filas_horarios:
            h_ini = cb_ini.get().strip()
            h_fin = cb_fin.get().strip()
            lista_final.append(f"{h_ini} a {h_fin}")

        if not tipo or not lista_final:
            messagebox.showwarning("Atención", "Ingrese el nombre del tipo y al menos un horario", parent=ventana)
            return

        # Unificar con comas para la base de datos
        horarios_final = ", ".join(lista_final)

        if modo == "agregar":
            modelo.insertar_tipo_horario(conexion, tipo, horarios_final)
        else:
            modelo.modificar_tipo_horario(conexion, tipo_id, tipo, horarios_final)

        if on_guardar:
            on_guardar()

        ventana.destroy()

    botones["guardar"].config(command=guardar)
    botones["cancelar"].config(command=ventana.destroy)