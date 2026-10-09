import os
import tkinter as tk
from tkinter import ttk
from conexion import obtener_ruta_icono
from PIL import Image, ImageTk


class vistaprincipal:
    """Vista principal: interfaz Tkinter y estilos uniformes."""

    def __init__(self, root):
        self.root = root
        self.root.title("ARMADO DE HORARIOS")
        self.root.geometry("1920x1080")
        self.root.iconbitmap(obtener_ruta_icono("icono.ico"))

        self.aplicar_estilo()
        self.crear_widgets()

    def aplicar_estilo(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        self.root.configure(bg="#f0f4f8")

        style.configure(
            "Custom.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(8, 10),
            foreground="#004080",
            background="#cce6ff",
            borderwidth=1,
            relief="raised",
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#99ccff")],
            foreground=[("active", "#00264d")],
        )
        style.configure(
            "TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#003366",
            background="#f0f4f8",
        )

    def crear_widgets(self):
        # Frame principal
        self.fondo_frame = tk.Frame(self.root)
        self.fondo_frame.pack(fill=tk.BOTH, expand=True)

        # Botonera superior
        self.button_frame = ttk.Frame(
            self.fondo_frame, padding=0, style="TFrame"
        )
        self.button_frame.pack(side=tk.TOP, fill=tk.X, pady=0)

        # --- IMAGEN DE FONDO (RUTA CORREGIDA PARA PYINSTALLER) ---
        import sys

        if getattr(sys, "frozen", False):
            # Si corre como ejecutable .exe (compilado)
            script_dir = os.path.dirname(sys.executable)
        else:
            # Si corre como script .py en desarrollo
            script_dir = os.path.dirname(os.path.abspath(__file__))

        fondo_path = os.path.join(script_dir, "fondo.jpg")

        self.original = Image.open(fondo_path)
        self.fondo_label = tk.Label(self.fondo_frame)
        self.fondo_label.pack(fill=tk.BOTH, expand=True)
        self.fondo_label.bind("<Configure>", self.redimensionar_imagen)

    def redimensionar_imagen(self, event):
        nueva = self.original.resize(
            (event.width, event.height), Image.LANCZOS
        )
        self.fondo_label.img = ImageTk.PhotoImage(nueva)
        self.fondo_label.config(image=self.fondo_label.img)

    def agregar_botonera(self, botones):
        """Recibe una lista de tuplas y arma la botonera superior con menús desplegables."""
        if isinstance(botones, dict):
            items_botones = list(botones.items())
        else:
            items_botones = list(botones)

        dict_botones = dict(items_botones)

        # Limpiar widgets previos
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        col_idx = 0

        # --- 1. MENÚ DESPLEGABLE: HORARIOS (Primero) ---
        cmd_chocolates = dict_botones.get(
            "HORARIOS CHOCOLATES", dict_botones.get("Chocolates", lambda: None)
        )
        cmd_golosinas = dict_botones.get(
            "HORARIOS GOLOSINAS", dict_botones.get("Golosinas", lambda: None)
        )

        menu_horarios = tk.Menu(
            self.root,
            tearoff=0,
            font=("Segoe UI", 11, "bold"),
            bg="#cce6ff",
            fg="#004080",
            activebackground="#99ccff",
            activeforeground="#00264d",
        )
        menu_horarios.add_command(label="Chocolates", command=cmd_chocolates)
        menu_horarios.add_command(label="Golosinas", command=cmd_golosinas)

        def desplegar_menu_horarios(btn_widget):
            x = btn_widget.winfo_rootx()
            y = btn_widget.winfo_rooty() + btn_widget.winfo_height()
            menu_horarios.post(x, y)

        btn_horarios = ttk.Button(
            self.button_frame, text="HORARIOS ▼", style="Custom.TButton"
        )
        btn_horarios.configure(
            command=lambda b=btn_horarios: desplegar_menu_horarios(b)
        )
        btn_horarios.grid(row=0, column=col_idx, padx=4, pady=8, sticky="nsew")
        self.button_frame.columnconfigure(col_idx, weight=1)
        col_idx += 1

        # --- 2. BOTONES FIJOS INTERMEDIOS ---
        claves_omitir = [
            "HORARIOS CHOCOLATES",
            "HORARIOS GOLOSINAS",
            "Chocolates",
            "Golosinas",
            "SECTORES",
            "TIPOS DE HORARIO",
            "SALIR",
        ]

        for texto, comando in items_botones:
            if texto in claves_omitir:
                continue

            btn = ttk.Button(
                self.button_frame, text=texto, command=comando, style="Custom.TButton"
            )
            btn.grid(row=0, column=col_idx, padx=4, pady=8, sticky="nsew")
            self.button_frame.columnconfigure(col_idx, weight=1)
            col_idx += 1

        # --- 3. MENÚ DESPLEGABLE: PARÁMETROS ---
        cmd_sectores = dict_botones.get("SECTORES", lambda: None)
        cmd_tipos_horario = dict_botones.get("TIPOS DE HORARIO", lambda: None)

        menu_parametros = tk.Menu(
            self.root,
            tearoff=0,
            font=("Segoe UI", 11, "bold"),
            bg="#cce6ff",
            fg="#004080",
            activebackground="#99ccff",
            activeforeground="#00264d",
        )
        menu_parametros.add_command(label="Sectores", command=cmd_sectores)
        menu_parametros.add_command(
            label="Tipos de Horario", command=cmd_tipos_horario
        )


        def desplegar_menu_parametros(btn_widget):
            x = btn_widget.winfo_rootx()
            y = btn_widget.winfo_rooty() + btn_widget.winfo_height()
            menu_parametros.post(x, y)

        btn_parametros = ttk.Button(
            self.button_frame, text="PARÁMETROS ▼", style="Custom.TButton"
        )
        btn_parametros.configure(
            command=lambda b=btn_parametros: desplegar_menu_parametros(b)
        )
        btn_parametros.grid(row=0, column=col_idx, padx=4, pady=8, sticky="nsew")
        self.button_frame.columnconfigure(col_idx, weight=1)
        col_idx += 1

        # --- 4. BOTÓN SALIR ---
        cmd_salir = dict_botones.get("SALIR", lambda: None)
        btn_salir = ttk.Button(
            self.button_frame, text="SALIR", command=cmd_salir, style="Custom.TButton"
        )
        btn_salir.grid(row=0, column=col_idx, padx=4, pady=8, sticky="nsew")
        self.button_frame.columnconfigure(col_idx, weight=1)