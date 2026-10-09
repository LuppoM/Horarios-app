class ModeloHGoloFinde:

    def __init__(self, conexion):
        self.conexion = conexion
        self.planta = "Golosinas"

    def obtener_operarios(self, semana):
        """Obtiene los operarios validados de la semana (de cualquier planta) para listar en Golosinas."""
        cursor = self.conexion.cursor()
        sem_val = int(semana) if str(semana).isdigit() else semana
        cursor.execute(
            """
            SELECT DISTINCT id, operario 
            FROM modymoi 
            WHERE (semana = ? OR semana = ?)
              AND horario IS NOT NULL AND TRIM(horario) != ''
              AND sector IS NOT NULL AND TRIM(sector) != ''
            ORDER BY operario ASC
            """,
            (str(semana), sem_val),
        )
        return {row[0]: row[1] for row in cursor.fetchall()}

    def obtener_operarios_disponibles(self, semana, dia="Sábado"):
        """Retorna todos los operarios validados en la semana (sin restringir planta de origen)."""
        cursor = self.conexion.cursor()
        sem_val = int(semana) if str(semana).isdigit() else semana
        cursor.execute(
            """
            SELECT DISTINCT m.id, m.operario
            FROM modymoi m
            WHERE (m.semana = ? OR m.semana = ?)
              AND m.horario IS NOT NULL AND TRIM(m.horario) != ''
              AND m.sector IS NOT NULL AND TRIM(m.sector) != ''
            ORDER BY m.operario ASC
            """,
            (str(semana), sem_val),
        )
        return cursor.fetchall()

    def obtener_datos_semana_finde(self, semana):
        cursor = self.conexion.cursor()
        sem_val = int(semana) if str(semana).isdigit() else semana
        cursor.execute(
            """
            SELECT f.id_operario, m.operario, f.dia, f.horario, f.sector
            FROM modymoi_finde f
            INNER JOIN modymoi m ON f.id_operario = m.id
            WHERE (f.semana = ? OR f.semana = ?)
              AND LOWER(TRIM(f.planta)) = 'golosinas'
            ORDER BY f.id ASC
            """,
            (str(semana), sem_val),
        )
        return cursor.fetchall()

    def guardar_datos_finde(self, semana, registros):
        cursor = self.conexion.cursor()
        sem_val = int(semana) if str(semana).isdigit() else semana

        cursor.execute(
            """
            DELETE FROM modymoi_finde
            WHERE (semana = ? OR semana = ?)
              AND LOWER(TRIM(planta)) = 'golosinas'
            """,
            (str(semana), sem_val),
        )

        for id_op, dia, horario, sector in registros:
            cursor.execute(
                """
                INSERT INTO modymoi_finde (id_operario, semana, dia, horario, sector, planta)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (id_op, sem_val, dia, horario, sector, self.planta),
            )

        self.conexion.commit()

    def eliminar_registro_operario(self, id_op, semana):
        cursor = self.conexion.cursor()
        sem_val = int(semana) if str(semana).isdigit() else semana
        cursor.execute(
            """
            DELETE FROM modymoi_finde
            WHERE id_operario = ? 
              AND (semana = ? OR semana = ?) 
              AND LOWER(TRIM(planta)) = 'golosinas'
            """,
            (id_op, str(semana), sem_val),
        )
        self.conexion.commit()