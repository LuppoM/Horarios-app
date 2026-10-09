import sqlite3

def obtener_sectores(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, nombre_sector, planta, tipo_horario, requiere_dotacion
        FROM sectores
    """)
    return cursor.fetchall()

def obtener_sector_por_id(conexion, sector_id):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, nombre_sector, planta, tipo_horario, requiere_dotacion
        FROM sectores
        WHERE id = ?
    """, (sector_id,))
    return cursor.fetchone()

def eliminar_sector(conexion, sector_id):
    cursor = conexion.cursor()
    cursor.execute("""
        DELETE FROM sectores
        WHERE id = ?
    """, (sector_id,))
    conexion.commit()