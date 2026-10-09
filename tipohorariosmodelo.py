import sqlite3

def obtener_tipos_horarios(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, tipo, horarios_definidos
        FROM tipohorario
    """)
    return cursor.fetchall()

def obtener_tipo_horario_por_id(conexion, tipo_id):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, tipo, horarios_definidos
        FROM tipohorario
        WHERE id = ?
    """, (tipo_id,))
    return cursor.fetchone()

def eliminar_tipo_horario(conexion, tipo_id):
    cursor = conexion.cursor()
    cursor.execute("""
        DELETE FROM tipohorario
        WHERE id = ?
    """, (tipo_id,))
    conexion.commit()