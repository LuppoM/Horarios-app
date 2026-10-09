import tkinter as tk
from tkinter import messagebox, ttk
from conexion import obtener_ruta_icono


class VistaHGolo(tk.Toplevel):

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Horarios golosinas")
        self.configure(bg="#ffffff")
        self.geometry("1920x1080")

        try:
            self.iconbitmap(obtener_ruta_icono("icono.ico"))
        except Exception:
            pass

        self.transient(parent)
        self.grab_set()

        # Variables de estado y UI
        self.semana_var = tk.StringVar()
        self.sector_frames = {}
        self.filas_widgets = {}
        self.botones_agregar = {}
        self.dotaciones_programadas = {}

        self.crear_top_bar()
        self.crear_scrollable_frame()

    def crear_top_bar(self):
        bg_color = "#ffffff"
        top_bar = tk.Frame(self, bg=bg_color)
        top_bar.pack(fill=tk.X, pady=8, padx=15)

        ttk.Button(
            top_bar, text="Exportar a PDF", command=self.controlador.exportar_a_pdf
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            top_bar, text="Guardar", command=self.controlador.guardar_datos
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            top_bar,
            text="Alistamiento / Fin de semana",
            command=self.controlador.abrir_fin_de_semana,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_bar, text="Cerrar", command=self.destroy).pack(
            side=tk.LEFT, padx=5
        )

        tk.Label(
            top_bar,
            text="Semana:",
            font=("Segoe UI", 12, "bold"),
            bg=bg_color,
            fg="#004080",
        ).pack(side=tk.LEFT, padx=(30, 5))

        semana_cb = ttk.Combobox(
            top_bar,
            width=5,
            textvariable=self.semana_var,
            font=("Segoe UI", 12, "bold"),
            state="readonly",
        )
        semana_cb.pack(side=tk.LEFT)
        semana_cb["values"] = [str(i) for i in range(1, 54)]
        semana_cb.bind("<MouseWheel>", lambda e: "break")

    def crear_scrollable_frame(self):
        bg_color = "#ffffff"
        contenedor = ttk.Frame(self)
        contenedor.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

        v_scrollbar = tk.Scrollbar(contenedor, orient="vertical")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        h_scrollbar = tk.Scrollbar(contenedor, orient="horizontal")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas = tk.Canvas(
            contenedor,
            bg=bg_color,
            highlightthickness=0,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)

        scrollable_frame = ttk.Frame(self.canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        canvas_window = self.canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(canvas_window, width=e.width),
        )

        self.canvas.bind(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"
            ),
        )

        self.scrollable_frame = scrollable_frame

    def actualizar_interfaz(
        self, sectores, dotacion_teorica, asignados_por_turno
    ):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.sector_frames = {}
        self.filas_widgets = {}
        self.botones_agregar = {}
        self.dotaciones_programadas = {}

        COLUMNAS = 3
        for col_idx in range(COLUMNAS):
            self.scrollable_frame.columnconfigure(
                col_idx, weight=1, uniform="sector_col"
            )

        row = 0
        col = 0

        for sector, tipo_horario, req_dotacion in sectores:
            sector_card = tk.LabelFrame(
                self.scrollable_frame,
                text=f"  {sector}  ",
                font=("Segoe UI", 11, "bold"),
                fg="#00264d",
                bg="#f0f4f8",
                bd=2,
                relief="groove",
            )
            sector_card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

            t_horario = str(tipo_horario).strip().upper() if tipo_horario else "ROTATIVO"
            es_especial = (t_horario == "CENTRAL")

            # Definimos es_libre directamente consultando el campo de la base de datos (0 = No requiere dotación / es libre)
            es_libre = (int(req_dotacion) == 0)

            turnos_a_renderizar = self.controlador.modelo.obtener_turnos_por_tipo(t_horario)

            if not turnos_a_renderizar:
                if es_especial:
                    turnos_a_renderizar = ["08:00 a 16:00"]
                else:
                    turnos_a_renderizar = ["06:00 a 14:00", "14:00 a 22:00", "22:00 a 06:00"]

            for turno in turnos_a_renderizar:
                raw_cant = dotacion_teorica.get(sector, {}).get(turno, 0)
                try:
                    cant_teorica = int(raw_cant) if raw_cant is not None else 0
                except (ValueError, TypeError):
                    cant_teorica = 0

                if es_especial or es_libre:
                    self.dotaciones_programadas[(sector, turno)] = 999999
                else:
                    self.dotaciones_programadas[(sector, turno)] = cant_teorica

                # Llamada pasando es_libre para controlar la etiqueta y los límites
                self.crear_turno_frame(sector_card, sector, turno, cant_teorica, es_especial, es_libre)

                if not es_especial and not es_libre and cant_teorica <= 0:
                    btn_agregar = self.botones_agregar.get((sector, turno))
                    if btn_agregar:
                        btn_agregar.config(state="disabled")

                operarios_guardados = asignados_por_turno.get(sector, {}).get(turno, [])
                if operarios_guardados:
                    for id_val, nombre_op in operarios_guardados:
                        self.agregar_fila(
                            sector, turno, id_val=id_val, operario=nombre_op
                        )

            col += 1
            if col >= COLUMNAS:
                col = 0
                row += 1

        row += 1
        tk.Frame(self.scrollable_frame, height=50, bg="#ffffff").grid(
            row=row, column=0, columnspan=COLUMNAS, sticky="ew"
        )

    def crear_turno_frame(self, parent_card, sector, turno, dotacion_programada, es_especial=False, es_libre=False):
        if es_especial:
            texto_etiqueta = f" Horario: {turno} "
        elif es_libre:
            texto_etiqueta = f" Turno: {turno} "
        else:
            texto_etiqueta = f" Turno: {turno}  |  Dotación programada: {dotacion_programada} "

        frame = tk.LabelFrame(
            parent_card,
            text=texto_etiqueta,
            font=("Segoe UI", 9, "bold"),
            fg="#004080",
            bg="#ffffff",
        )
        frame.pack(fill=tk.X, padx=6, pady=4, expand=False)

        self.sector_frames[(sector, turno)] = frame
        self.filas_widgets[(sector, turno)] = []

        btn_agregar = ttk.Button(
            frame,
            text="+ Agregar operario",
            command=lambda s=sector, t=turno: self.intentar_agregar_fila(s, t),
        )
        btn_agregar.pack(anchor="w", padx=5, pady=3)
        self.botones_agregar[(sector, turno)] = btn_agregar

    def intentar_agregar_fila(self, sector, turno):
        limite = self.dotaciones_programadas.get((sector, turno), 0)
        filas_actuales = len(self.filas_widgets.get((sector, turno), []))

        if limite < 999999 and limite > 0 and filas_actuales >= limite:
            messagebox.showwarning(
                "Límite alcanzado",
                f"No se pueden agregar más operarios. La dotación programada para este turno es de {limite}."
            )
            return

        self.agregar_fila(sector, turno)

    def agregar_fila(
        self,
        sector,
        turno,
        id_val="",
        operario="",
        nombres_operarios=None,
    ):
        semana = self.semana_var.get() or str(
            self.controlador.obtener_semana_actual()
        )
        self.semana_var.set(semana)

        frame = self.sector_frames.get((sector, turno))
        if frame is None:
            return

        fila_frame = tk.Frame(frame, bg="#ffffff")
        fila_frame.pack(anchor="w", pady=2, padx=5, fill=tk.X)

        # ID Entry
        tk.Label(
            fila_frame, text="ID:", font=("Segoe UI", 9, "bold"), bg="#ffffff"
        ).pack(side=tk.LEFT, padx=(0, 2))

        id_entry = ttk.Entry(fila_frame, width=5, font=("Segoe UI", 9))
        id_entry.pack(side=tk.LEFT, padx=(0, 5))
        if id_val:
            id_entry.insert(0, str(id_val))

        # Operario Combobox
        tk.Label(
            fila_frame,
            text="Operario:",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
        ).pack(side=tk.LEFT, padx=(0, 2))

        operario_cb = ttk.Combobox(
            fila_frame, font=("Segoe UI", 9), width=24, height=10
        )
        operario_cb.pack(side=tk.LEFT, padx=(0, 5))

        if operario:
            operario_cb.set(operario)

        # Cargar lista flotante al hacer clic o recibir foco
        def desplegar_lista(event=None):
            actual = operario_cb.get().strip()
            filtrados = [
                nombre
                for id_op, nombre in self.controlador.obtener_operarios_filtrados(
                    semana, operario_actual=actual
                )
            ]
            operario_cb["values"] = sorted(filtrados)

        # Filtrar operarios al presionar Enter y desplegar la lista emergente
        def filtrar_operarios_enter(event=None):
            texto_ingresado = operario_cb.get().strip().lower()
            actual = operario_cb.get().strip()

            try:
                todos_tuplas = self.controlador.obtener_operarios_filtrados(
                    semana, operario_actual=actual
                )
            except Exception as e:
                print(f"Error obteniendo operarios: {e}")
                todos_tuplas = []

            if not texto_ingresado:
                operario_cb["values"] = sorted([nombre for _, nombre in todos_tuplas])
            else:
                coincidencias_tuplas = [
                    (id_op, nombre) for id_op, nombre in todos_tuplas if texto_ingresado in nombre.lower()
                ]
                operario_cb["values"] = sorted([nombre for _, nombre in coincidencias_tuplas])

                if len(coincidencias_tuplas) == 1:
                    id_op, nombre = coincidencias_tuplas[0]
                    operario_cb.set(nombre)
                    id_entry.delete(0, "end")
                    id_entry.insert(0, str(id_op))
                    self.controlador.on_operario_selected(operario_cb, id_entry)

            operario_cb.focus_set()
            operario_cb.event_generate("<Down>")
            return "break"

        # Eventos
        operario_cb.bind("<Button-1>", desplegar_lista)
        operario_cb.bind("<FocusIn>", desplegar_lista)
        operario_cb.bind("<Return>", filtrar_operarios_enter)
        operario_cb.bind(
            "<<ComboboxSelected>>",
            lambda e: self.controlador.on_operario_selected(
                operario_cb, id_entry
            ),
        )

        # Bloquear el scroll de la rueda en el combobox pero mantener el scroll general
        operario_cb.bind(
            "<MouseWheel>",
            lambda e: (
                self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
                "break",
            )[1],
        )

        # Botón Eliminar Fila
        btn_eliminar = ttk.Button(
            fila_frame,
            text="Eliminar",
            width=7,
            command=lambda: self.controlador.eliminar_fila(
                sector, turno, id_entry, operario_cb, fila_frame
            ),
        )
        btn_eliminar.pack(side=tk.LEFT, padx=2)

        # Registrar fila
        self.filas_widgets[(sector, turno)].append((id_entry, operario_cb))