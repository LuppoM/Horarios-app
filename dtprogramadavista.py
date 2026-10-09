import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono

class VistaDTProgramada(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Dotación Teórica por Horarios / Sector")
        
        self.state("zoomed")
        self.configure(bg="#f4f6f9")
        try:
            self.iconbitmap(obtener_ruta_icono("icono.ico"))
        except Exception:
            pass
        self.transient(parent)
        self.grab_set()

        self.entries_choco = {}
        self.entries_choco_dias = {}
        self.entries_golo = {}
        self.entries_golo_dias = {}

        self.crear_top_bar()
        self.crear_notebook_matrices()

    def crear_top_bar(self):
        top_frame = tk.Frame(self, bg="#004080")
        top_frame.pack(fill=tk.X, ipady=10)

        tk.Label(
            top_frame, 
            text="DOTACIÓN TEÓRICA - HORARIOS POR SECTOR", 
            font=("Segoe UI", 13, "bold"), 
            fg="white", 
            bg="#004080"
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            top_frame, 
            text="Semana:", 
            font=("Segoe UI", 11, "bold"), 
            fg="white", 
            bg="#004080"
        ).pack(side=tk.LEFT, padx=(20, 5))

        self.semana_var = tk.StringVar(value=str(self.controlador.obtener_semana_actual()))
        semana_entry = tk.Entry(top_frame, textvariable=self.semana_var, width=5, font=("Segoe UI", 11, "bold"), justify="center")
        semana_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_frame, text="Buscar / Cargar", command=self.controlador.cargar_tabla).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Guardar Cambios", command=self.controlador.guardar_datos).pack(side=tk.LEFT, padx=5)

       

        ttk.Button(top_frame, text="Cerrar", command=self.destroy).pack(side=tk.RIGHT, padx=10)

    def crear_notebook_matrices(self):
        contenedor_principal = tk.Frame(self, bg="#ffffff")
        contenedor_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(contenedor_principal)
        notebook.pack(fill=tk.BOTH, expand=True)

        tab_choco = ttk.Frame(notebook)
        tab_golo = ttk.Frame(notebook)

        notebook.add(tab_choco, text="  Chocolates  ")
        notebook.add(tab_golo, text="  Golosinas  ")

        horarios_dinamicos = getattr(self.controlador.modelo, "obtener_turnos_por_tipo", lambda t: self.controlador.horarios_keys)("ROTATIVO")
        self.controlador.horarios_keys = horarios_dinamicos

        headers_completo = ["LÍNEA / SECTOR"] + horarios_dinamicos + ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]
        dias_keys = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        cant_turnos = len(horarios_dinamicos)

        # --- PESTAÑA 1: CHOCOLATES ---
        canvas_choco = tk.Canvas(tab_choco, bg="#ffffff", highlightthickness=0)
        v_scroll_choco = ttk.Scrollbar(tab_choco, orient="vertical", command=canvas_choco.yview)
        h_scroll_choco = ttk.Scrollbar(tab_choco, orient="horizontal", command=canvas_choco.xview)
        
        scroll_frame_choco = tk.Frame(canvas_choco, bg="#ffffff")
        scroll_frame_choco.bind("<Configure>", lambda e: canvas_choco.configure(scrollregion=canvas_choco.bbox("all")))
        canvas_choco.create_window((0, 0), window=scroll_frame_choco, anchor="nw")
        
        canvas_choco.configure(yscrollcommand=v_scroll_choco.set, xscrollcommand=h_scroll_choco.set)

        h_scroll_choco.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll_choco.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_choco.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        table_choco = tk.Frame(scroll_frame_choco, bg="#ffffff")
        table_choco.pack(fill=tk.BOTH, padx=5, pady=5)

        tk.Label(table_choco, text="", bg="#003366", width=26).grid(row=0, column=0, sticky="nsew")
        tk.Label(
            table_choco, text="DOTACIÓN POR TURNO", font=("Segoe UI", 9, "bold"),
            bg="#28a745", fg="white", relief="solid", bd=1
        ).grid(row=0, column=1, columnspan=cant_turnos, sticky="nsew", ipady=2)
        tk.Label(
            table_choco, text="TURNOS X DÍA", font=("Segoe UI", 9, "bold"),
            bg="#17a2b8", fg="white", relief="solid", bd=1
        ).grid(row=0, column=cant_turnos + 1, columnspan=5, sticky="nsew", ipady=2)

        for col_idx, text in enumerate(headers_completo):
            bg = "#003366" if col_idx == 0 else ("#28a745" if col_idx <= cant_turnos else "#17a2b8")
            tk.Label(
                table_choco, text=text, font=("Segoe UI", 9, "bold"),
                bg=bg, fg="white", width=26 if col_idx == 0 else 14, relief="solid", bd=1
            ).grid(row=1, column=col_idx, sticky="nsew", ipady=4)

        for idx, sector in enumerate(self.controlador.sectores_chocolate, start=2):
            tk.Label(
                table_choco, text=sector, font=("Segoe UI", 9, "bold"),
                bg="#f0f4f8", anchor="w", relief="solid", bd=1, padx=5
            ).grid(row=idx, column=0, sticky="nsew")

            self.entries_choco[sector] = {}
            for c_idx, key in enumerate(self.controlador.horarios_keys, start=1):
                entry = tk.Entry(table_choco, font=("Segoe UI", 9), justify="center", bg="#ffffff", relief="solid", bd=1)
                entry.insert(0, "0")
                entry.grid(row=idx, column=c_idx, sticky="nsew", ipady=2)
                self.entries_choco[sector][key] = entry

            self.entries_choco_dias[sector] = {}
            for c_idx, dia_key in enumerate(dias_keys, start=cant_turnos + 1):
                entry = tk.Entry(table_choco, font=("Segoe UI", 9), justify="center", bg="#e9ecef", relief="solid", bd=1)
                entry.insert(0, "0")
                entry.config(takefocus=0)
                entry.bind("<Key>", lambda e: "break")
                entry.grid(row=idx, column=c_idx, sticky="nsew", ipady=2)
                self.entries_choco_dias[sector][dia_key] = entry

        # --- PESTAÑA 2: GOLOSINAS ---
        canvas_golo = tk.Canvas(tab_golo, bg="#ffffff", highlightthickness=0)
        v_scroll_golo = ttk.Scrollbar(tab_golo, orient="vertical", command=canvas_golo.yview)
        h_scroll_golo = ttk.Scrollbar(tab_golo, orient="horizontal", command=canvas_golo.xview)
        
        scroll_frame_golo = tk.Frame(canvas_golo, bg="#ffffff")
        scroll_frame_golo.bind("<Configure>", lambda e: canvas_golo.configure(scrollregion=canvas_golo.bbox("all")))
        canvas_golo.create_window((0, 0), window=scroll_frame_golo, anchor="nw")
        
        canvas_golo.configure(yscrollcommand=v_scroll_golo.set, xscrollcommand=h_scroll_golo.set)

        h_scroll_golo.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll_golo.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_golo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        table_golo = tk.Frame(scroll_frame_golo, bg="#ffffff")
        table_golo.pack(fill=tk.BOTH, padx=5, pady=5)

        tk.Label(table_golo, text="", bg="#003366", width=26).grid(row=0, column=0, sticky="nsew")
        tk.Label(
            table_golo, text="DOTACIÓN POR TURNO", font=("Segoe UI", 9, "bold"),
            bg="#28a745", fg="white", relief="solid", bd=1
        ).grid(row=0, column=1, columnspan=cant_turnos, sticky="nsew", ipady=2)
        tk.Label(
            table_golo, text="TURNOS X DÍA", font=("Segoe UI", 9, "bold"),
            bg="#17a2b8", fg="white", relief="solid", bd=1
        ).grid(row=0, column=cant_turnos + 1, columnspan=5, sticky="nsew", ipady=2)

        for col_idx, text in enumerate(headers_completo):
            bg = "#003366" if col_idx == 0 else ("#28a745" if col_idx <= cant_turnos else "#17a2b8")
            tk.Label(
                table_golo, text=text, font=("Segoe UI", 9, "bold"),
                bg=bg, fg="white", width=26 if col_idx == 0 else 14, relief="solid", bd=1
            ).grid(row=1, column=col_idx, sticky="nsew", ipady=4)

        for idx, sector in enumerate(self.controlador.sectores_golosinas, start=2):
            tk.Label(
                table_golo, text=sector, font=("Segoe UI", 9, "bold"),
                bg="#f0f4f8", anchor="w", relief="solid", bd=1, padx=5
            ).grid(row=idx, column=0, sticky="nsew")

            self.entries_golo[sector] = {}
            for c_idx, key in enumerate(self.controlador.horarios_keys, start=1):
                entry = tk.Entry(table_golo, font=("Segoe UI", 9), justify="center", bg="#ffffff", relief="solid", bd=1)
                entry.insert(0, "0")
                entry.grid(row=idx, column=c_idx, sticky="nsew", ipady=2)
                self.entries_golo[sector][key] = entry

            self.entries_golo_dias[sector] = {}
            for c_idx, dia_key in enumerate(dias_keys, start=cant_turnos + 1):
                entry = tk.Entry(table_golo, font=("Segoe UI", 9), justify="center", bg="#e9ecef", relief="solid", bd=1)
                entry.insert(0, "0")
                entry.config(takefocus=0)
                entry.bind("<Key>", lambda e: "break")
                entry.grid(row=idx, column=c_idx, sticky="nsew", ipady=2)
                self.entries_golo_dias[sector][dia_key] = entry

        def _on_mousewheel(event):
            try:
                current_tab = notebook.select()
                if current_tab == str(tab_choco):
                    canvas_choco.yview_scroll(int(-1 * (event.delta / 120)), "units")
                elif current_tab == str(tab_golo):
                    canvas_golo.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except Exception:
                pass
        
        canvas_choco.bind_all("<MouseWheel>", _on_mousewheel)