from principalmodelo import modeloprincipal
from principalvista import vistaprincipal
import HCHOCO, HGOLO, MODMOI, dtprogramada
import sectores  
import tipohorarios

class AppController:

    def __init__(self, root):
        self.root = root
        self.model = modeloprincipal()

        # 1. LIMPIEZA INMEDIATA
        try:
            self.model.eliminar_datos_semanas_anteriores()
        except Exception as e:
            print(f"Error crítico al limpiar base de datos: {e}")

        self.view = vistaprincipal(root)

        # 2. CONFIGURACIÓN DE BOTONERAS Y MENÚS
        botones = [
            ("HORARIOS CHOCOLATES", self.abrir_horarios_chocolates),
            ("HORARIOS GOLOSINAS", self.abrir_horarios_golosinas),
            ("CONSOLIDADO AMBAS PLANTAS", self.abrir_ordenes_trabajo),
            ("DOTACION PROGRAMADA", self.abrir_dotacion),
            # Opciones dentro del menú desplegable PARÁMETROS
            ("SECTORES", self.abrir_sectores),
            ("TIPOS DE HORARIO", self.abrir_tipos_horario),
            ("SALIR", self.salir),
        ]
        self.view.agregar_botonera(botones)

        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    def abrir_horarios_chocolates(self):
        HCHOCO.mostrar_hchoco(self.root, self.model.conexion_db)

    def abrir_horarios_golosinas(self):
        HGOLO.mostrar_hgolo(self.root, self.model.conexion_db, self.model)

    def abrir_ordenes_trabajo(self):
        MODMOI.mostrar_modmoi(self.root, self.model.conexion_db)

    def abrir_sectores(self):
        sectores.abrir_sectores(self.root, self.model.conexion_db)

    def abrir_tipos_horario(self):
        tipohorarios.abrir_tipohorarios(self.root, self.model.conexion_db)

    def abrir_dotacion(self):
        dtprogramada.mostrar_dtprogramada(self.root, self.model.conexion_db)

    def salir(self):
        self.model.cerrar_conexion()
        self.root.destroy()