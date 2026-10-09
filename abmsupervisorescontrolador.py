from tkinter import messagebox
import abmsupervisoresvista as vista
import abmsupervisoresmodelo as modelo

def iniciar_abm_supervisor(parent, conexion, modo, datos=None, on_guardar=None):
    titulo = "Agregar Supervisor" if modo == "agregar" else "Modificar Supervisor"
    ventana = vista.crear_ventana(parent, titulo=titulo)

    botones = vista.crear_toolstrip(ventana)
    campos = vista.crear_formulario(ventana)

    if modo == "modificar" and datos:
        supervisor_id, nombre, email, planta = datos
        campos["nombre"].insert(0, nombre)
        campos["email"].insert(0, email)
        campos["planta"].set(planta)

    def guardar():
        nombre = campos["nombre"].get().strip()
        email = campos["email"].get().strip()
        planta = campos["planta"].get().strip()

        if not nombre or not email or not planta:
            messagebox.showwarning("Atención", "Complete todos los campos", parent=ventana)
            return

        if modo == "agregar":
            modelo.insertar_supervisor(conexion, nombre, email, planta)
        else:
            modelo.modificar_supervisor(conexion, datos[0], nombre, email, planta)

        if on_guardar:
            on_guardar()

        ventana.destroy()

    botones["guardar"].config(command=guardar)
    botones["cancelar"].config(command=ventana.destroy)