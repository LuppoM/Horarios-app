from datetime import datetime
import json
from principalmodelo import modeloprincipal

class ModeloDTProgramada(modeloprincipal):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion



    def obtener_sectores_rotativos_por_planta(self, planta):
        """
        Realiza el SELECT sobre la tabla 'sectores' utilizando 'nombre_sector' 
        y filtrando por 'planta', 'tipo_horario' = 'ROTATIVO' y que requieran dotación (requiere_dotacion = 1).
        """
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""
                SELECT nombre_sector 
                FROM sectores 
                WHERE LOWER(planta) = LOWER(?) 
                  AND LOWER(tipo_horario) = 'rotativo'
                  AND requiere_dotacion = 1
                ORDER BY id ASC
            """, (planta,))
            
            filas = cursor.fetchall()
            return [f[0] for f in filas]

        except Exception as e:
            print(f"Error al realizar SELECT en la tabla sectores para {planta}: {e}")
            return []

    def obtener_turnos_por_tipo(self, tipo="ROTATIVO"):
        """
        Realiza un SELECT sobre la tabla 'tipohorario' para traer 'horarios_definidos'
        según el tipo (por defecto 'ROTATIVO').
        """
        cursor = self.conexion.cursor()
        horarios_predeterminados = ["06:00 a 14:00", "14:00 a 22:00", "22:00 a 06:00"]
        try:
            cursor.execute("""
                SELECT horarios_definidos 
                FROM tipohorario 
                WHERE LOWER(tipo) = LOWER(?)
            """, (tipo,))
            
            fila = cursor.fetchone()
            if fila and fila[0]:
                cadena_horarios = fila[0]
                if cadena_horarios.strip().startswith("["):
                    return json.loads(cadena_horarios)
                return [h.strip() for h in cadena_horarios.split(",") if h.strip()]
            
            return horarios_predeterminados

        except Exception as e:
            print(f"Error al realizar SELECT en la tabla tipohorario para tipo {tipo}: {e}")
            return horarios_predeterminados

    def guardar_dotaciones(self, semana, datos_completos):
        cursor = self.conexion.cursor()
        try:
            for planta, sectores in datos_completos.items():
                for sector, horarios in sectores.items():
                    for rango_horario, cantidad in horarios.items():
                        cursor.execute("""
                            INSERT OR REPLACE INTO dotacion_teorica_horarios 
                                (semana_inicio, planta, sector, rango_horario, cantidad_operarios)
                            VALUES (?, ?, ?, ?, ?)
                        """, (str(semana), planta, sector, rango_horario, cantidad))

            return True, "Guardado exitoso"
        except Exception as e:
            self.conexion.rollback()
            print(f"Error al guardar dotaciones: {e}")
            return False, str(e)

    def consultar_estado_semana(self, semana):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""
                SELECT estado, fecha_modificacion, modificado_por 
                FROM estados_programacion 
                WHERE semana = ?
            """, (str(semana),))
            fila = cursor.fetchone()
            if fila:
                return fila[0], fila[1], fila[2]
            return "PENDIENTE", None, None
        except Exception as e:
            print(f"Error al consultar estado de semana: {e}")
            return "PENDIENTE", None, None

    def obtener_dotaciones_semana(self, semana):
        cursor = self.conexion.cursor()
        resultado = {"Chocolate": {}, "Golosinas": {}}
        try:
            cursor.execute("""
                SELECT planta, sector, rango_horario, cantidad_operarios 
                FROM dotacion_teorica_horarios 
                WHERE semana_inicio = ?
            """, (str(semana),))
            filas = cursor.fetchall()
            for planta, sector, rango, cantidad in filas:
                if planta not in resultado:
                    resultado[planta] = {}
                if sector not in resultado[planta]:
                    resultado[planta][sector] = {}
                resultado[planta][sector][rango] = cantidad
            return resultado
        except Exception as e:
            print(f"Error al obtener dotaciones de la semana {semana}: {e}")
            return resultado