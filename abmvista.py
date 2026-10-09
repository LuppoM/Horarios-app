# abmmoi_vista.py
import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono


class abmmodmoivista(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Orden de Trabajo")
        self.geometry("600x400")
        self.iconbitmap(obtener_ruta_icono("icono.ico"))
        self.configure(bg="#f0f4f8")
        self.transient(parent)
        self.grab_set()

        self.campos = {}

        # Opciones para los Combobox
        self.opciones_tipo_mo = ["MOD", "MOI"]
        self.opciones_horario = [
            "06:00 a 14:00",
            "14:00 a 22:00",
            "22:00 a 06:00",
        ]

        self._crear_toolstrip()
        self._crear_formulario()

    def _crear_toolstrip(self):
        self.toolstrip = tk.Frame(self, bg="#dde6ed", height=50)
        self.toolstrip.pack(fill=tk.X)
        self.toolstrip.pack_propagate(False)

        self.lblorden = tk.Label(
            self.toolstrip,
            text="Agregar",
            bg="#dde6ed",
            fg="#333",
            font=("Segoe UI", 10, "bold"),
        )
        self.lblorden.pack(side=tk.LEFT, padx=10)

        self.btn_accion = tk.Button(
            self.toolstrip,
            text="Agregar",
            font=("Segoe UI", 10, "bold"),
            bg="#c6efce",
            fg="#006100",
        )
        self.btn_accion.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_cancelar = tk.Button(
            self.toolstrip,
            text="❌ Cancelar",
            font=("Segoe UI", 10, "bold"),
            bg="#ffc7ce",
            fg="#9c0006",
            command=self.destroy,
        )
        self.btn_cancelar.pack(side=tk.LEFT, padx=10, pady=5)

    def _crear_formulario(self):
        form = tk.Frame(self, bg="#f0f4f8")
        form.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        campos = [
            (
                "calificacion_mano_obra",
                "Calificación Mano de Obra",
                "combo_tipo",
            ),
            ("operario", "Operario", "entry"),
            ("horario", "Horario", "combo_horario"),
        ]

        for i, (campo, etiqueta, tipo) in enumerate(campos):
            lbl = tk.Label(
                form, text=f"{etiqueta}:", bg="#f0f4f8", font=("Segoe UI", 10)
            )
            lbl.grid(row=i, column=0, sticky="e", padx=10, pady=8)

            if tipo == "combo_tipo":
                entrada = ttk.Combobox(
                    form,
                    values=self.opciones_tipo_mo,
                    state="readonly",
                    font=("Segoe UI", 10),
                    width=23,
                )
            elif tipo == "combo_horario":
                entrada = ttk.Combobox(
                    form,
                    values=self.opciones_horario,
                    state="readonly",
                    font=("Segoe UI", 10),
                    width=23,
                )
            else:
                entrada = ttk.Entry(form, font=("Segoe UI", 10), width=25)

            entrada.grid(row=i, column=1, sticky="w", pady=8)
            self.campos[campo] = entrada