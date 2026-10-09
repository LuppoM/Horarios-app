from tkinter import messagebox
import tipohorariosmodelo as modelo
import tipohorariosvista as vista
import abmtipohorarioscontrolador as abm_controlador

def iniciar_tipohorarios(parent, conexion):
    ventana = vista.crear_ventana(parent)
    botones = vista.crear_toolstrip(ventana)
    tree = vista.crear_tabla(ventana)

    def cargar_datos():
        tree.delete(*tree.get_children())
        for fila in modelo.obtener_tipos_horarios(conexion):
            tree.insert("", "end", values=fila)

    def agregar():
        abm_controlador.iniciar_abm_tipohorario(
            parent=ventana,
            conexion=conexion,
            modo="agregar",
            on_guardar=cargar_datos
        )

    def modificar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un tipo de horario", parent=ventana)
            return

        datos = tree.item(seleccionado)["values"]
        abm_controlador.iniciar_abm_tipohorario(
            parent=ventana,
            conexion=conexion,
            modo="modificar",
            datos=datos,
            on_guardar=cargar_datos
        )

    def eliminar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un tipo de horario", parent=ventana)
            return

        tipo_id = tree.item(seleccionado)["values"][0]
        if messagebox.askyesno("Confirmar", "¿Desea eliminar el tipo de horario seleccionado?", parent=ventana):
            modelo.eliminar_tipo_horario(conexion, tipo_id)
            cargar_datos()

    botones["agregar"].config(command=agregar)
    botones["modificar"].config(command=modificar)
    botones["eliminar"].config(command=eliminar)
    botones["atras"].config(command=ventana.destroy)

    cargar_datos()