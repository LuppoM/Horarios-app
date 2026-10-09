import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono

class VistaPolivalencia(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("MATRIZ DE POLIVALENCIA")
        
        self.geometry("1366x768")
        self.state('zoomed') 
        self.iconbitmap(obtener_ruta_icono("icono.ico"))
        
        self.transient(parent)
        self.grab_set()

        # --- LISTAS DE LÍNEAS / SECTORES REALES ---
        self.sectores = [
            "Linea turron oblea", "Linea turron de fiesta", "linea caramelo", "linea confitado",
            "linea gomita", "Linea de turron duro", "Linea de garrapiñada", "Tostado de mani",
            "Lustrado", "Bases de mani", "Azucar impalpable", "Balanza Vertical 1-2 Sower",
            "Balanza volumetrica", "Envasado de fiesta", "Envasado de obleas", "Graneles",
            "Elaboracion de obleas", "Estuchado", "Linea awema", "Linea tabletas",
            "Linea rama", "Volumetrica", "Vertical", "Vertical 5 costuras","Lider",
            "Linea Bonbones Gba", "Planta de pasta", "Confitado de boiler", "Grageado",
            "Carrucel", "Decorado de huevos", "Envasado de nagema", "Linea cremini", "Troquelado"
        ]
        self.sectores_especiales = []

        # Variables de control de estado
        self.editando = False
        self.valores_celdas = {}   
        self.operarios_ids = []    
        
        self.aplicar_estilo()
        self.crear_widgets()

    def aplicar_estilo(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        self.configure(bg="#f0f4f8")

        # Botones superiores
        style.configure('Polivalencia.TButton',
                        font=('Segoe UI', 11, 'bold'),
                        padding=8,
                        foreground='#004080',
                        background='#cce6ff',
                        borderwidth=1,
                        relief="raised")
        style.map('Polivalencia.TButton', background=[('active', '#99ccff')])

        # Configuración estilo Excel para datos
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=32,
                        background="#ffffff",
                        foreground="#00264d",
                        fieldbackground="#ffffff",
                        gridcolor="#dcdcdc")
                        
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 9, "bold"),
                        background="#004080",
                        foreground="#ffffff",
                        relief="flat",
                        borderwidth=1)

        # Estilo especial para la mini-tabla de totales (Verde Excel)
        style.configure("Totales.Treeview",
                        font=("Segoe UI", 10, "bold"),
                        rowheight=28,
                        background="#e2efda",
                        foreground="#375623",
                        fieldbackground="#e2efda",
                        gridcolor="#dcdcdc")

    def crear_widgets(self):
        # 1. Panel superior de herramientas
        self.top_bar = tk.Frame(self, bg="#f0f4f8")
        self.top_bar.pack(fill=tk.X, side=tk.TOP, padx=20, pady=10)

        self.btn_accion = ttk.Button(self.top_bar, text="Editar Matriz", 
                                     command=self.controlador.alternar_edicion, style='Polivalencia.TButton')
        self.btn_accion.pack(side=tk.LEFT, padx=5)

        self.btn_cancelar = ttk.Button(self.top_bar, text="Cancelar", 
                                       command=self.cancelar_edicion, style='Polivalencia.TButton')

        self.btn_imprimir = ttk.Button(self.top_bar, text="Imprimir Matriz", 
                                       command=lambda: print("Imprimir presionado"), style='Polivalencia.TButton')
        self.btn_imprimir.pack(side=tk.LEFT, padx=5)

        # --- FILTRO NUEVO DE LÍNEA ---
        frame_filtro = ttk.LabelFrame(self.top_bar, text=" Filtrar por Línea / Sector ")
        frame_filtro.pack(side=tk.LEFT, padx=25)
        
        ttk.Label(frame_filtro, text="Ver Columna: ", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5, pady=5)
        self.combo_filtro = ttk.Combobox(frame_filtro, state="readonly", width=30, font=("Segoe UI", 10))
        self.combo_filtro.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(self.top_bar, text="Cerrar Matriz", 
                   command=self.destroy, style='Polivalencia.TButton').pack(side=tk.RIGHT, padx=5)

        # 2. Contenedor de la grilla principal
        self.contenedor_grilla = tk.Frame(self, bg="#ffffff", highlightbackground="#cce6ff", highlightthickness=1)
        self.contenedor_grilla.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 15))

        # Grid interno para acoplar Tablas, Scrollbars y Totales
        self.contenedor_grilla.grid_rowconfigure(0, weight=1)  
        self.contenedor_grilla.grid_rowconfigure(1, weight=0)  
        self.contenedor_grilla.grid_rowconfigure(2, weight=0)  
        self.contenedor_grilla.grid_columnconfigure(0, weight=1)
        self.contenedor_grilla.grid_columnconfigure(1, weight=0)

        # --- TREEVIEW PRINCIPAL (OPERARIOS) ---
        self.tree = ttk.Treeview(self.contenedor_grilla, show="headings", selectmode="browse", height=13)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # --- TREEVIEW SECUNDARIO (TOTALES ALINEADOS) ---
        self.tree_totales = ttk.Treeview(self.contenedor_grilla, show="", style="Totales.Treeview", height=2)
        self.tree_totales.grid(row=1, column=0, sticky="ew")

        # Barras de desplazamiento
        vbar = ttk.Scrollbar(self.contenedor_grilla, orient=tk.VERTICAL, command=self.tree.yview)
        vbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vbar.set)

        hbar = ttk.Scrollbar(self.contenedor_grilla, orient=tk.HORIZONTAL, command=self.sincronizar_scroll_x)
        hbar.grid(row=2, column=0, sticky="ew")
        
        self.tree.configure(xscrollcommand=hbar.set)
        self.tree_totales.configure(xscrollcommand=hbar.set)

        self.tree.bind("<Double-1>", self.on_doble_clic)

    def sincronizar_scroll_x(self, *args):
        self.tree.xview(*args)
        self.tree_totales.xview(*args)

    def construir_matriz(self, operarios, lineas, matriz_datos, fila_s, fila_t):
        columnas = ["operario"] + lineas
        
        self.tree["columns"] = columnas
        self.tree_totales["columns"] = columnas
        
        self.tree.heading("operario", text="APELLIDO Y NOMBRE", anchor="w")
        self.tree.column("operario", width=320, minwidth=250, anchor="w")
        self.tree_totales.column("operario", width=320, minwidth=250, anchor="e") 

        for linea in lineas:
            self.tree.heading(linea, text=linea.upper(), anchor="center")
            self.tree.column(linea, width=190, minwidth=160, anchor="center")
            self.tree_totales.column(linea, width=190, minwidth=160, anchor="center")

        self.tree.delete(*self.tree.get_children())
        self.valores_celdas.clear()
        self.operarios_ids.clear()

        for op_id, text_op in operarios:
            fila_valores = [text_op]
            self.operarios_ids.append(op_id)

            for linea in lineas:
                rol_actual = matriz_datos.get((int(op_id), linea), "")
                texto_celda = "T" if rol_actual == "TITULAR" else "S" if rol_actual == "SUPLENTE" else ""
                fila_valores.append(texto_celda)
                self.valores_celdas[(str(op_id), linea)] = rol_actual

            self.tree.insert("", "end", iid=str(op_id), values=fila_valores)

        for idx, item in enumerate(self.tree.get_children()):
            tag = "par" if idx % 2 == 0 else "impar"
            self.tree.item(item, tags=(tag,))
        self.tree.tag_configure("par", background="#ffffff")
        self.tree.tag_configure("impar", background="#f4f8fb")

        self.tree_totales.delete(*self.tree_totales.get_children())
        self.tree_totales.insert("", "end", iid="tot_suplente", values=fila_s)
        self.tree_totales.insert("", "end", iid="tot_titular", values=fila_t)

    def cambiar_a_modo_edicion(self):
        self.editando = True 
        self.btn_accion.config(text="Guardar Cambios")
        self.btn_cancelar.pack(side=tk.LEFT, padx=5, after=self.btn_accion)
        self.tree.configure(selectmode="none")

    def regresar_a_modo_lectura(self):
        self.editando = False
        self.btn_accion.config(text="Editar Matriz")
        self.btn_cancelar.pack_forget()
        self.tree.configure(selectmode="browse")

    def cancelar_edicion(self):
        self.controlador.restaurar_valores_originales()
        self.regresar_a_modo_lectura()

    def on_doble_clic(self, event):
        if not self.editando:
            return

        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        col_idx = int(column.replace("#", "")) - 1
        if col_idx == 0:
            return 

        op_id = str(row_id)
        linea_nombre = self.controlador.lineas[col_idx - 1]

        valores_bbox = self.tree.bbox(row_id, column)
        if not valores_bbox:
            return
            
        x, y, width, height = valores_bbox

        self.combobox_flotante = ttk.Combobox(self.tree, values=["", "TITULAR", "SUPLENTE"], state="readonly", font=("Segoe UI", 9))
        self.combobox_flotante.set(self.valores_celdas.get((op_id, linea_nombre), ""))
        self.combobox_flotante.place(x=x, y=y, width=width, height=height)
        self.combobox_flotante.focus()

        self.combobox_flotante.bind("<FocusOut>", lambda e: self.cerrar_combobox_flotante(op_id, linea_nombre, col_idx))
        self.combobox_flotante.bind("<<ComboboxSelected>>", lambda e: self.cerrar_combobox_flotante(op_id, linea_nombre, col_idx))

    def cerrar_combobox_flotante(self, op_id, linea_nombre, col_idx):
        if hasattr(self, 'combobox_flotante') and self.combobox_flotante.winfo_exists():
            nuevo_valor = self.combobox_flotante.get()
            
            # Actualización local en diccionario interno
            self.valores_celdas[(str(op_id), linea_nombre)] = nuevo_valor
            
            # Render en grilla del Treeview
            texto_celda = "T" if nuevo_valor == "TITULAR" else "S" if nuevo_valor == "SUPLENTE" else ""
            valores_fila = list(self.tree.item(str(op_id), "values"))
            valores_fila[col_idx] = texto_celda
            self.tree.item(str(op_id), values=valores_fila)
            self.combobox_flotante.destroy()
            
            # Guardado inmediato e indoloro en base de datos
            self.controlador.guardar_celda_dinamico(int(op_id), linea_nombre, nuevo_valor)
            
            # Recálculo de totales basándose en el filtro de columnas activo
            f_s, f_t = self.controlador.obtener_y_calcular_totales(self.controlador.operarios, self.controlador.lineas, self.valores_celdas)
            self.tree_totales.delete(*self.tree_totales.get_children())
            self.tree_totales.insert("", "end", iid="tot_suplente", values=f_s)
            self.tree_totales.insert("", "end", iid="tot_titular", values=f_t)