from tkinter import messagebox
import abmsectoresvista as vista
import abmsectoresmodelo as modelo

def iniciar_abm_sector(parent, conexion, modo, datos=None, on_guardar=None):
    titulo = "Agregar Sector" if modo == "agregar" else "Modificar Sector"
    ventana = vista.crear_ventana(parent)

    botones = vista.crear_toolstrip(ventana)
    
    tipos_disponibles = modelo.obtener_tipos_horario(conexion)
    campos = vista.crear_formulario(ventana, tipos_horario=tipos_disponibles)

    # Nota: Asegurate de que la consulta que trae 'datos' al abrir en modo modificar 
    # incluya también la columna requiere_dotacion (ej. sector_id, nombre, planta, tipo_horario, requiere_dotacion)
    if modo == "modificar" and datos:
        sector_id, nombre, planta, tipo_horario, requiere_dotacion = datos[:5]
        campos["nombre"].insert(0, nombre)
        campos["planta"].set(planta)
        if "tipo_horario" in campos and tipo_horario in tipos_disponibles:
            campos["tipo_horario"].set(tipo_horario)
        
        # Mapear 1/0 a Sí/No para el combobox
        val_dot = "Sí" if int(requiere_dotacion) == 1 else "No"
        campos["requiere_dotacion"].set(val_dot)

    def guardar():
        nombre = campos["nombre"].get().strip()
        planta = campos["planta"].get().strip()
        tipo_horario = campos["tipo_horario"].get().strip() if "tipo_horario" in campos else ""
        
        # Convertir "Sí"/"No" a 1 o 0 para la base de datos
        req_text = campos["requiere_dotacion"].get().strip()
        requiere_dotacion = 1 if req_text == "Sí" else 0

        if not nombre or not planta or not tipo_horario:
            messagebox.showwarning("Atención", "Complete todos los campos obligatorios", parent=ventana)
            return

        if modo == "agregar":
            modelo.insertar_sector(conexion, nombre, planta, tipo_horario, requiere_dotacion)
        else:
            modelo.modificar_sector(conexion, sector_id, nombre, planta, tipo_horario, requiere_dotacion)

        if on_guardar:
            on_guardar()

        ventana.destroy()

    botones["guardar"].config(command=guardar)
    botones["cancelar"].config(command=ventana.destroy)