import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono


class VistaHChocoFinde(tk.Toplevel):

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Alistamiento / Fin de semana - Chocolates")
        self.configure(bg="#ffffff")

        self.state("zoomed")
        try:
            self.iconbitmap(obtener_ruta_icono("icono.ico"))
        except Exception:
            pass

        self.transient(parent)
        self.grab_set()

        self.dias_frames = {}
        self.filas_widgets = {}
        self.dias_vars = {}

        self.dias_semana = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
        ]

        self.sectores = [
            "PLANTA DE PASTA",
            "TROQUELADO",
            "LUSTRADO",
            "BOILER",
            "GRAGEADO",
            "ELABORACION DE RAMA",
            "GRANEL",
            "CREMINI",
            "MOLDEO DE TABLETAS",
            "ENVASADO DE CARRUCEL",
            "FLOW PACK",
            "GBA",
            "ESTUCHADO MANUAL",
            "MOLDEO DE PASCUAS",
            "PELADO DE CONFITES /HUEVOS",
            "REPUJADO Y ESTUCHADO",
            "RELLENOS",
            "DECORADO",
            "VERTICAL VOLUMETRICA Y BALANZA",
            "AWEMA",
            "RELEVOS",
            "PERSONAL CON CARPETAS MEDICAS",
            "PERSONAL DE VACACIONES",
            "SUPERVISORES",
        ]

        self.turnos = [
            "06:00 a 14:00",
            "14:00 a 22:00",
            "22:00 a 06:00",
            "00:00 a 06:00",
        ]

        self.crear_top_bar()
        self.crear_scrollable_frame()

    def crear_top_bar(self):
        bg_color = "#ffffff"
        top_bar = tk.Frame(self, bg=bg_color)
        top_bar.pack(fill=tk.X, pady=8, padx=15)

        ttk.Button(
            top_bar, text="Guardar", command=self.controlador.guardar_datos
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            top_bar,
            text="+ Agregar Día",
            command=self.controlador.agregar_dia_dialogo,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_bar, text="Cerrar", command=self.destroy).pack(
            side=tk.LEFT, padx=5
        )

        tk.Label(
            top_bar,
            text="Semana:",
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg="#004080",
        ).pack(side=tk.LEFT, padx=(20, 5))

        self.semana_entry = ttk.Entry(
            top_bar, width=5, font=("Segoe UI", 10, "bold")
        )
        self.semana_entry.pack(side=tk.LEFT, padx=2)

    def crear_scrollable_frame(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(contenedor, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            contenedor, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas)

        def actualizar_scrollregion(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scrollable_frame.bind("<Configure>", actualizar_scrollregion)

        canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        def recalcular_ancho(event):
            self.canvas.itemconfig(canvas_window, width=event.width)

        self.canvas.bind("<Configure>", recalcular_ancho)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.columnconfigure(0, weight=1, uniform="col")
        self.scrollable_frame.columnconfigure(1, weight=1, uniform="col")

        self.canvas.yview_moveto(0)

    def _bind_mousewheel(self, event):
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        bbox = self.canvas.bbox("all")
        if not bbox:
            return

        altura_contenido = bbox[3] - bbox[1]
        altura_visible = self.canvas.winfo_height()

        if altura_contenido > altura_visible:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _propagar_mousewheel_canvas(self, event):
        bbox = self.canvas.bbox("all")
        if not bbox:
            return "break"

        altura_contenido = bbox[3] - bbox[1]
        altura_visible = self.canvas.winfo_height()

        if altura_contenido > altura_visible:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        return "break"

    def agregar_contenedor_dia(self, nombre_dia):
        if nombre_dia in self.dias_frames:
            return

        num_dias = len(self.dias_frames)
        row = num_dias // 2
        col = num_dias % 2

        dia_card = tk.LabelFrame(
            self.scrollable_frame,
            font=("Segoe UI", 11, "bold"),
            fg="#00264d",
            bg="#f0f4f8",
            bd=2,
            relief="groove",
        )
        dia_card.grid(row=row, column=col, sticky="new", padx=10, pady=10)

        header_dia = tk.Frame(dia_card, bg="#f0f4f8")
        header_dia.pack(fill=tk.X, padx=5, pady=5)

        dia_var = tk.StringVar(value=nombre_dia)
        dia_cb = ttk.Combobox(
            header_dia,
            textvariable=dia_var,
            values=self.dias_semana,
            font=("Segoe UI", 10, "bold"),
            width=12,
        )
        dia_cb.pack(side=tk.LEFT, padx=2)
        dia_cb.bind("<MouseWheel>", self._propagar_mousewheel_canvas)
        self.dias_vars[nombre_dia] = dia_var

        btn_eliminar_dia = tk.Label(
            header_dia,
            text=" ✕ ",
            font=("Segoe UI", 10, "bold"),
            fg="#cc0000",
            bg="#f0f4f8",
            cursor="hand2",
        )
        btn_eliminar_dia.pack(side=tk.RIGHT, padx=5)

        btn_eliminar_dia.bind(
            "<Enter>", lambda e: e.widget.config(fg="#ffffff", bg="#cc0000")
        )
        btn_eliminar_dia.bind(
            "<Leave>", lambda e: e.widget.config(fg="#cc0000", bg="#f0f4f8")
        )
        btn_eliminar_dia.bind(
            "<Button-1>",
            lambda e, d=nombre_dia: self.controlador.eliminar_bloque_dia(d),
        )

        header_frame = tk.Frame(dia_card, bg="#d9e2ec")
        header_frame.pack(fill=tk.X, padx=5, pady=(5, 2))

        for text, width, anchor in [
            ("ID", 4, "center"),
            ("OPERARIO", 25, "w"),
            ("HORARIO", 15, "center"),
            ("SECTOR", 22, "w"),
            ("ACCIÓN", 8, "center"),
        ]:
            tk.Label(
                header_frame,
                text=text,
                font=("Segoe UI", 9, "bold"),
                width=width,
                bg="#d9e2ec",
                anchor=anchor,
            ).pack(side=tk.LEFT, padx=2)

        filas_container = tk.Frame(dia_card, bg="#f0f4f8")
        filas_container.pack(fill=tk.X, expand=True, padx=5)

        ttk.Button(
            dia_card,
            text="+ Agregar Registro",
            command=lambda d=nombre_dia: self.agregar_fila(d),
        ).pack(anchor="w", padx=5, pady=5)

        self.dias_frames[nombre_dia] = filas_container
        self.filas_widgets[nombre_dia] = []

    def reordenar_grid_bloques(self):
        for idx, container in enumerate(self.dias_frames.values()):
            dia_card = container.master
            row = idx // 2
            col = idx % 2
            dia_card.grid_configure(row=row, column=col)

    def obtener_operarios_seleccionados_dia(self, nombre_dia, excep_combobox=None):
        seleccionados = set()
        for _, op_cb, _, _ in self.filas_widgets.get(nombre_dia, []):
            if op_cb != excep_combobox and op_cb.get().strip():
                seleccionados.add(op_cb.get().strip())
        return seleccionados

    def obtener_lista_base_dia(self, nombre_dia, op_cb):
        semana = (
            self.semana_entry.get().strip()
            if hasattr(self, "semana_entry") and self.semana_entry.get().strip()
            else getattr(self.controlador, "semana_actual", "")
        )

        operario_actual = op_cb.get().strip()
        usados_en_dia = self.obtener_operarios_seleccionados_dia(
            nombre_dia, excep_combobox=op_cb
        )

        if hasattr(self.controlador, "obtener_operarios_filtrados"):
            todos_disponibles = [
                nombre
                for _, nombre in self.controlador.obtener_operarios_filtrados(
                    semana, operario_actual=operario_actual
                )
            ]
        else:
            todos_disponibles = getattr(self.controlador, "nombres_operarios", [])

        return [
            op
            for op in todos_disponibles
            if op not in usados_en_dia or op == operario_actual
        ]

    def actualizar_opciones_comboboxes_dia(self, nombre_dia):
        for _, op_cb, _, _ in self.filas_widgets.get(nombre_dia, []):
            op_cb["values"] = self.obtener_lista_base_dia(nombre_dia, op_cb)

    def agregar_fila(
        self,
        nombre_dia,
        id_val="",
        operario="",
        horario="",
        sector="",
        nombres_operarios=None,
    ):
        if nombre_dia not in self.dias_frames:
            return

        container = self.dias_frames[nombre_dia]
        fila_frame = tk.Frame(container, bg="#ffffff", bd=1, relief="solid")
        fila_frame.pack(fill=tk.X, pady=2)

        id_entry = ttk.Entry(fila_frame, width=5, font=("Segoe UI", 9))
        id_entry.pack(side=tk.LEFT, padx=2, pady=2)
        if id_val:
            id_entry.insert(0, str(id_val))

        operario_cb = ttk.Combobox(fila_frame, font=("Segoe UI", 9), width=25)
        operario_cb.pack(side=tk.LEFT, padx=2, pady=2)

        if operario:
            operario_cb.set(operario)

        def desplegar_lista(event=None):
            operario_cb["values"] = sorted(
                self.obtener_lista_base_dia(nombre_dia, operario_cb)
            )

        def on_select_operario(event=None):
            self.controlador.on_operario_selected(operario_cb, id_entry)
            self.actualizar_opciones_comboboxes_dia(nombre_dia)

        def filtrar_operarios_enter(event=None):
            texto_ingresado = operario_cb.get().strip().lower()
            semana = (
                self.semana_entry.get().strip()
                if hasattr(self, "semana_entry") and self.semana_entry.get().strip()
                else getattr(self.controlador, "semana_actual", "")
            )

            try:
                todos_tuplas = self.controlador.obtener_operarios_filtrados(
                    semana, operario_actual=operario_cb.get().strip()
                )
            except Exception:
                todos_tuplas = []

            if not texto_ingresado:
                operario_cb["values"] = sorted([nombre for _, nombre in todos_tuplas])
            else:
                coincidencias = [
                    (id_op, nombre)
                    for id_op, nombre in todos_tuplas
                    if texto_ingresado in nombre.lower()
                ]
                operario_cb["values"] = sorted([nombre for _, nombre in coincidencias])

                if len(coincidencias) == 1:
                    id_op, nombre = coincidencias[0]
                    operario_cb.set(nombre)
                    id_entry.delete(0, "end")
                    id_entry.insert(0, str(id_op))
                    self.controlador.on_operario_selected(operario_cb, id_entry)

            operario_cb.focus_set()
            operario_cb.event_generate("<Down>")
            return "break"

        operario_cb.bind("<Button-1>", desplegar_lista)
        operario_cb.bind("<FocusIn>", desplegar_lista)
        operario_cb.bind("<<ComboboxSelected>>", on_select_operario)
        operario_cb.bind("<Return>", filtrar_operarios_enter)
        operario_cb.bind(
            "<MouseWheel>",
            lambda e: (self._propagar_mousewheel_canvas(e), "break")[1],
        )

        horario_cb = ttk.Combobox(
            fila_frame,
            font=("Segoe UI", 9),
            width=15,
            values=self.turnos,
        )
        horario_cb.pack(side=tk.LEFT, padx=2, pady=2)
        horario_cb.bind("<MouseWheel>", self._propagar_mousewheel_canvas)
        if horario:
            horario_cb.set(horario)

        sector_cb = ttk.Combobox(
            fila_frame,
            font=("Segoe UI", 9),
            width=22,
            values=self.sectores,
            state="readonly",
        )
        sector_cb.pack(side=tk.LEFT, padx=2, pady=2)
        sector_cb.bind("<MouseWheel>", self._propagar_mousewheel_canvas)
        if sector:
            sector_cb.set(sector)

        widgets_tuple = (id_entry, operario_cb, horario_cb, sector_cb)
        self.filas_widgets[nombre_dia].append(widgets_tuple)

        ttk.Button(
            fila_frame,
            text="Eliminar",
            width=8,
            command=lambda: self.eliminar_fila_local(
                nombre_dia, widgets_tuple, fila_frame
            ),
        ).pack(side=tk.LEFT, padx=2)

        self.actualizar_opciones_comboboxes_dia(nombre_dia)

    def eliminar_fila_local(self, nombre_dia, widgets_tuple, fila_frame):
        if (
            nombre_dia in self.filas_widgets
            and widgets_tuple in self.filas_widgets[nombre_dia]
        ):
            self.filas_widgets[nombre_dia].remove(widgets_tuple)
        fila_frame.destroy()
        self.actualizar_opciones_comboboxes_dia(nombre_dia)

    def obtener_estructura_datos(self):
        datos = {}
        for nombre_dia, filas in self.filas_widgets.items():
            dia_real = (
                self.dias_vars[nombre_dia].get()
                if nombre_dia in self.dias_vars
                else nombre_dia
            )
            datos[dia_real] = [
                {
                    "id_operario": id_entry.get().strip(),
                    "operario": operario_cb.get().strip(),
                    "horario": horario_cb.get().strip(),
                    "sector": sector_cb.get().strip(),
                }
                for id_entry, operario_cb, horario_cb, sector_cb in filas
            ]
        return datos