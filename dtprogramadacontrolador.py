from datetime import date, timedelta
from tkinter import messagebox
from dtprogramadamodelo import ModeloDTProgramada
from dtprogramadavista import VistaDTProgramada

class ControladorDTProgramada:
    def __init__(self, root, conexion):
        self.root = root
        self.modelo = ModeloDTProgramada(conexion)
        
        # Traer sectores de la BD mediante SELECT según planta
        self.sectores_chocolate = self.modelo.obtener_sectores_rotativos_por_planta("Chocolate")
        self.sectores_golosinas = self.modelo.obtener_sectores_rotativos_por_planta("Golosinas")
        
        self.horarios_keys = ["06:00 a 14:00", "14:00 a 22:00", "22:00 a 06:00"]
        self.dias_keys = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]

        self.vista = VistaDTProgramada(root, self)
        self.cargar_tabla()

    def obtener_semana_actual(self):
        fecha_proxima = date.today() + timedelta(days=7)
        return self.modelo.obtener_numero_semana_personalizado(fecha_proxima)

    def cargar_tabla(self):
        semana = self.vista.semana_var.get()
        datos = self.modelo.obtener_dotaciones_semana(semana)

        # Cargar Chocolates
        datos_choco = datos.get("Chocolate", {})
        for sector in self.sectores_chocolate:
            horarios_sector = datos_choco.get(sector, {})
            if sector in self.vista.entries_choco:
                for key in self.horarios_keys:
                    val = horarios_sector.get(key, 0)
                    entry = self.vista.entries_choco[sector][key]
                    entry.delete(0, "end")
                    entry.insert(0, str(val))
            
            activos = sum(1 for key in self.horarios_keys if horarios_sector.get(key, 0) > 0)
            if sector in self.vista.entries_choco_dias:
                for dia_key in self.dias_keys:
                    entry_dia = self.vista.entries_choco_dias[sector][dia_key]
                    entry_dia.delete(0, "end")
                    entry_dia.insert(0, str(activos))

        # Cargar Golosinas
        datos_golo = datos.get("Golosinas", {})
        for sector in self.sectores_golosinas:
            horarios_sector = datos_golo.get(sector, {})
            if sector in self.vista.entries_golo:
                for key in self.horarios_keys:
                    val = horarios_sector.get(key, 0)
                    entry = self.vista.entries_golo[sector][key]
                    entry.delete(0, "end")
                    entry.insert(0, str(val))
            
            activos = sum(1 for key in self.horarios_keys if horarios_sector.get(key, 0) > 0)
            if sector in self.vista.entries_golo_dias:
                for dia_key in self.dias_keys:
                    entry_dia = self.vista.entries_golo_dias[sector][dia_key]
                    entry_dia.delete(0, "end")
                    entry_dia.insert(0, str(activos))

    def contar_turnos_activos(self, horarios_dict):
        return sum(1 for key in self.horarios_keys if horarios_dict.get(key, 0) > 0)

    def guardar_datos(self):
        semana = self.vista.semana_var.get()
        if not semana:
            messagebox.showwarning("Aviso", "Seleccione una semana.")
            return

        datos_completos = {"Chocolate": {}, "Golosinas": {}}

        # Recopilar datos Chocolates
        for sector in self.sectores_chocolate:
            if sector not in self.vista.entries_choco:
                continue
            horarios_dict = {}
            for key in self.horarios_keys:
                val = self.vista.entries_choco[sector][key].get().strip()
                horarios_dict[key] = int(val) if val.isdigit() else 0
            
            turnos_activos = self.contar_turnos_activos(horarios_dict)
            if sector in self.vista.entries_choco_dias:
                for dia_key in self.dias_keys:
                    entry_dia = self.vista.entries_choco_dias[sector][dia_key]
                    entry_dia.delete(0, "end")
                    entry_dia.insert(0, str(turnos_activos))

            datos_completos["Chocolate"][sector] = horarios_dict

        # Recopilar datos Golosinas
        for sector in self.sectores_golosinas:
            if sector not in self.vista.entries_golo:
                continue
            horarios_dict = {}
            for key in self.horarios_keys:
                val = self.vista.entries_golo[sector][key].get().strip()
                horarios_dict[key] = int(val) if val.isdigit() else 0
            
            turnos_activos = self.contar_turnos_activos(horarios_dict)
            if sector in self.vista.entries_golo_dias:
                for dia_key in self.dias_keys:
                    entry_dia = self.vista.entries_golo_dias[sector][dia_key]
                    entry_dia.delete(0, "end")
                    entry_dia.insert(0, str(turnos_activos))

            datos_completos["Golosinas"][sector] = horarios_dict

        # Guardar en BD
        exito, msg = self.modelo.guardar_dotaciones(semana, datos_completos)

        if exito:
            messagebox.showinfo(
                "Éxito", 
                f"Dotación teórica guardada correctamente para la Semana {semana}."
            )
        else:
            messagebox.showerror("Error", f"Ocurrió un error al guardar en la base de datos:\n{msg}")