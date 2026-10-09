class ModeloPolivalencia:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_todos_los_operarios(self):
        """
        Trae el listado de operarios únicos cruzando por nombre 
        para evitar duplicados en las filas de la matriz.
        """
        cursor = self.conexion.cursor()
        cursor.execute("""
    SELECT MIN(id), operario 
        FROM modymoi 
        WHERE operario IS NOT NULL 
        AND operario != '' 
        AND calificacion_mano_obra = 'MOD' 
        GROUP BY operario 
        ORDER BY operario ASC
            """)
        return cursor.fetchall()

    def obtener_matriz_roles(self):
        """Trae las asignaciones de polivalencia existentes desde la BD"""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT operario_id, linea_nombre, rol FROM polivalencias")
        # Retorna un diccionario indexado como {(id_operario, 'Nombre Linea'): 'TITULAR' o 'SUPLENTE'}
        return {(row[0], row[1]): row[2] for row in cursor.fetchall()}

    def guardar_celda_matriz(self, operario_id, linea_nombre, rol):
        """Guarda, actualiza o elimina la celda de la matriz de forma directa y universal"""
        cursor = self.conexion.cursor()
        
        if not rol or rol.strip() == "":
            # Si el usuario dejó la celda en blanco, borramos el registro
            cursor.execute("""
                DELETE FROM polivalencias 
                WHERE operario_id = ? AND linea_nombre = ?
            """, (operario_id, linea_nombre))
        else:
            # LÓGICA COMPATIBLE: Primero intentamos actualizar por las dudas de que ya exista
            cursor.execute("""
                UPDATE polivalencias 
                SET rol = ? 
                WHERE operario_id = ? AND linea_nombre = ?
            """, (rol, operario_id, linea_nombre))
            
            # Si no se actualizó ninguna fila, significa que es un registro nuevo; hacemos el INSERT
            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO polivalencias (operario_id, linea_nombre, rol) 
                    VALUES (?, ?, ?)
                """, (operario_id, linea_nombre, rol))
                
        self.conexion.commit()