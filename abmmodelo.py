# abmmodelo.py

from typing import Dict, Any
import traceback

class abmmodmoimodelo:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar(self, datos: Dict[str, Any]) -> None:
        try:
            if not datos:
                raise ValueError("No se proporcionaron datos para insertar.")

            campos = ', '.join(f"[{k}]" for k in datos.keys())
            placeholders = ', '.join(['?'] * len(datos))
            valores = list(datos.values())

            query = f"INSERT INTO modymoi ({campos}) VALUES ({placeholders})"
            cursor = self.conexion.cursor()
            cursor.execute(query, valores)
            self.conexion.commit()
            cursor.close()
        except Exception as e:
            raise Exception(f"Error al insertar: {e}\n{traceback.format_exc()}")

    def modificar(self, id: int, datos: Dict[str, Any]) -> None:
        try:
            if not datos:
                raise ValueError("No se proporcionaron datos para modificar.")

            set_clause = ', '.join(f"[{k}] = ?" for k in datos.keys())
            valores = list(datos.values())
            valores.append(id)

            query = f"UPDATE modymoi SET {set_clause} WHERE id = ?"
            cursor = self.conexion.cursor()
            cursor.execute(query, valores)
            self.conexion.commit()
            cursor.close()
        except Exception as e:
            raise Exception(f"Error al modificar: {e}\n{traceback.format_exc()}")
