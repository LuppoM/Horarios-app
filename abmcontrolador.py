# abmmodmoi_controlador.py
import tkinter as tk
from tkinter import messagebox
from abmmodelo import abmmodmoimodelo
from abmvista import abmmodmoivista


class AbmModMoiControlador:

    def __init__(
        self, parent, conexion, callback_recarga=None, datos_existentes=None
    ):
        self.vista = abmmodmoivista(parent)
        self.modelo = abmmodmoimodelo(conexion)
        self.callback_recarga = callback_recarga
        self.datos_existentes = datos_existentes

        # Cambiar labels y botones según si es modificar o agregar
        if self.datos_existentes:
            self.vista.lblorden.config(text="Modificar")
            self.vista.btn_accion.config(
                text="Guardar cambios", command=self.modificar
            )
            self.cargar_datos_en_vista()
        else:
            self.vista.btn_accion.config(command=self.insertar)

    def insertar(self):
        self._guardar_en_bd(modo="insertar")

    def modificar(self):
        self._guardar_en_bd(modo="modificar")

    def _guardar_en_bd(self, modo):
        try:
            datos = {}

            # 1. Recorrer y obtener todos los campos dinámicos
            for campo, widget in self.vista.campos.items():
                if isinstance(widget, tk.Text):
                    valor = widget.get("1.0", "end").strip()
                else:
                    valor = widget.get().strip()

                if not valor:
                    messagebox.showwarning(
                        "Campo vacío",
                        f"El campo '{campo}' no puede estar vacío.",
                    )
                    return

                datos[campo] = valor

            # 2. Validación explícita de seguridad para el campo Horario
            horario_widget = getattr(self.vista, "horario_cb", None) or getattr(
                self.vista, "horario_entry", None
            )

            if horario_widget:
                horario_val = horario_widget.get().strip()
                if not horario_val:
                    messagebox.showwarning(
                        "Horario requerido",
                        "Debe seleccionar o ingresar un horario.",
                    )
                    return
                datos["horario"] = horario_val
            elif "horario" in datos and not datos["horario"]:
                messagebox.showwarning(
                    "Horario requerido",
                    "El campo horario no puede estar vacío.",
                )
                return

            # 3. Guardado según el modo
            if modo == "insertar":
                self.modelo.insertar(datos)
            else:
                self.modelo.modificar(self.datos_existentes["id"], datos)

            messagebox.showinfo("Éxito", "Datos guardados correctamente.")

            if self.callback_recarga:
                self.callback_recarga()

            self.vista.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo guardar la orden de trabajo:\n{e}"
            )

    def cargar_datos_en_vista(self):
        try:
            for campo, widget in self.vista.campos.items():
                valor = self.datos_existentes.get(campo, "")
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", str(valor))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, str(valor))
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo cargar la información:\n{e}"
            )