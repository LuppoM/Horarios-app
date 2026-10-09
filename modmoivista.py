import tkinter as tk
from tkinter import ttk

from conexion import obtener_ruta_icono


class ModMoiView(tk.Toplevel):

  def __init__(self, parent, controlador):
    super().__init__(parent)
    self.controlador = controlador
    self.title("Mano de obra directa")
    self.geometry("1920x1080")
    self.configure(bg="#f0f4f8")
    self.transient(parent)
    self.grab_set()
    self.iconbitmap(obtener_ruta_icono("icono.ico"))
    self.acceso_autorizado = False

    self.columnas = []
    self.datos_originales = []

    self._crear_toolstrip()
    self._crear_tabla()
    self._crear_filtro()
    self._crear_titulo()

  # ------------------ TOOLSTRIP ------------------
  def _crear_toolstrip(self):
    self.toolstrip = tk.Frame(self, bg="#dde6ed", height=70)
    self.toolstrip.pack(fill=tk.X, side=tk.TOP)
    self.toolstrip.pack_propagate(False)

    self.fuente_boton = ("Segoe UI", 12, "bold")
    self.color_texto = "#003366"
    self.fondo_boton = "#cfe2f3"
    self.fondo_hover = "#a4c2f4"

  def crear_boton(self, texto, comando, x):
    boton = tk.Button(
        self.toolstrip,
        text=texto,
        font=self.fuente_boton,
        fg=self.color_texto,
        bg=self.fondo_boton,
        activebackground=self.fondo_hover,
        activeforeground=self.color_texto,
        bd=0,
        relief="flat",
        command=comando,
    )
    boton.place(x=x, y=15, width=120, height=40)
    return boton

  # ------------------ TABLA ------------------
  def _crear_tabla(self):
    self.tabla_frame = tk.Frame(self, bg="#f0f4f8")
    self.tabla_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

    self.tree_scroll_y = tk.Scrollbar(self.tabla_frame, orient="vertical")
    self.tree_scroll_y.grid(row=0, column=1, sticky="ns")

    self.tree_scroll_x = tk.Scrollbar(self.tabla_frame, orient="horizontal")
    self.tree_scroll_x.grid(row=1, column=0, sticky="ew")

    self.tree = ttk.Treeview(
        self.tabla_frame,
        show="headings",
        yscrollcommand=self.tree_scroll_y.set,
        xscrollcommand=self.tree_scroll_x.set,
        height=18,
    )
    self.tree.grid(row=0, column=0, sticky="nsew")
    self.tabla_frame.grid_rowconfigure(0, weight=1)
    self.tabla_frame.grid_columnconfigure(0, weight=1)

    self.tree_scroll_y.config(command=self.tree.yview)
    self.tree_scroll_x.config(command=self.tree.xview)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),
        background="#d9e1f2",
        foreground="#003366",
    )
    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28,
        background="white",
        fieldbackground="white",
    )

  def actualizar_tabla(self):
    self.tree.delete(*self.tree.get_children())
    self.tree["columns"] = self.columnas
    for col in self.columnas:
      self.tree.heading(col, text=col)
      self.tree.column(col, anchor="center", width=150)

    for fila in self.datos_originales:
      self.tree.insert("", "end", values=fila)

  # ------------------ FILTRO Y COMBOBOX DE VISTA ------------------
  def _crear_filtro(self):
    self.filtro_frame = tk.Frame(self, bg="#f0f4f8")
    self.filtro_frame.pack(pady=(0, 10))

    # Selector de tipo de tabla (Semana / Fin de semana)
    tk.Label(
        self.filtro_frame,
        text="Ver horarios:",
        bg="#f0f4f8",
        font=("Segoe UI", 11, "bold"),
        fg="#003366",
    ).pack(side=tk.LEFT, padx=(5, 2))
    self.combo_vista = ttk.Combobox(
        self.filtro_frame,
        state="readonly",
        width=15,
        values=["Semana", "Fin de Semana"],
    )
    self.combo_vista.set("Semana")
    self.combo_vista.pack(side=tk.LEFT, padx=(0, 15))

    tk.Label(
        self.filtro_frame, text="Columna:", bg="#f0f4f8", font=("Segoe UI", 11)
    ).pack(side=tk.LEFT, padx=5)
    self.combo_columnas = ttk.Combobox(
        self.filtro_frame, state="readonly", width=25
    )
    self.combo_columnas.pack(side=tk.LEFT, padx=5)

    tk.Label(
        self.filtro_frame, text="Filtro:", bg="#f0f4f8", font=("Segoe UI", 11)
    ).pack(side=tk.LEFT, padx=5)
    self.entrada_filtro = ttk.Entry(self.filtro_frame, width=25)
    self.entrada_filtro.pack(side=tk.LEFT, padx=5)

    self.contador_label = tk.Label(
        self,
        text="MOD (Directa): 0   |   MOI (Indirecta): 0",
        bg="#f0f4f8",
        font=("Segoe UI", 11, "bold"),
        fg="#003366",
    )
    self.contador_label.pack(pady=(0, 10))

  # ------------------ TITULO ------------------
  def _crear_titulo(self):
    self.titulo = tk.Label(
        self,
        text="GESTION DE MANO DE OBRA DIRECTA",
        font=("Segoe UI", 20, "bold"),
        bg="#f0f4f8",
        fg="#003366",
    )
    self.titulo.pack(pady=(20, 5))