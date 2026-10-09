# Hchocomodelo.py
from datetime import date
from principalmodelo import modeloprincipal


class Modelohchoco(modeloprincipal):

    def __init__(self, conexion):
        self.conexion = conexion
        self.conexion_db = conexion

        self.operarios_dict = {}
        self.operarios_asignados = {}

        self.cargar_operarios()

    def cargar_operarios(self):
        """Carga todos los operarios desde la base de datos"""
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, operario FROM modymoi ORDER BY operario ASC")
        rows = cursor.fetchall()
        self.operarios_dict = {row[0]: row[1] for row in rows}

    def obtener_operarios(self):
        """Devuelve todos los operarios cargados"""
        return self.operarios_dict

    def obtener_sectores_chocolates(self):
        """Obtiene los sectores, su tipo de horario y si requieren dotación de Chocolates desde la base de datos"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute(
                "SELECT nombre_sector, tipo_horario, requiere_dotacion FROM sectores WHERE planta='Chocolate'"
            )
            rows = cursor.fetchall()
            return rows if rows else []
        except Exception as e:
            print(f"Error al obtener sectores de chocolates: {e}")
            return []

    def obtener_turnos_por_tipo(self, tipo_horario):
        """Busca en la base de datos los turnos asociados al tipo de horario usando la tabla tipohorario y la columna horarios_definidos"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute(
                "SELECT horarios_definidos FROM tipohorario WHERE UPPER(TRIM(tipo)) = ?",
                (tipo_horario.upper(),)
            )
            row = cursor.fetchone()
            if row and row[0]:
                # Divide los horarios separados por comas guardados en la tabla
                return [t.strip() for t in row[0].split(",")]
        except Exception as e:
            print(f"Error al obtener turnos por tipo: {e}")
        return []

    def obtener_dotacion_teorica(self, semana):
        """Obtiene la dotación teórica por sector y horario para Chocolates"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute(
                """
                    SELECT sector, rango_horario, cantidad_operarios
                    FROM dotacion_teorica_horarios
                    WHERE semana_inicio=? AND planta='Chocolate'
                """,
                (str(semana),),
            )
            resultados = {}
            for sector, rango, cantidad in cursor.fetchall():
                if sector not in resultados:
                    resultados[sector] = {}
                resultados[sector][rango] = cantidad
            return resultados
        except Exception as e:
            print(f"Error al obtener dotación teórica: {e}")
            return {}

    def obtener_operarios_asignados_en_otro_sector(self, semana):
        """Devuelve IDs de operarios que ya tienen sector asignado en una semana"""
        if semana in self.operarios_asignados:
            return self.operarios_asignados[semana]

        cursor = self.conexion.cursor()
        cursor.execute(
            """
                SELECT id
                FROM modymoi
                WHERE semana=? AND operario != '' AND sector != ''
            """,
            (semana,),
        )
        asignados = set(row[0] for row in cursor.fetchall())
        self.operarios_asignados[semana] = asignados
        return asignados

    def obtener_operarios_disponibles(self, semana):
        """Devuelve los operarios que no tienen sector asignado"""
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT id, operario
            FROM modymoi
            WHERE (sector IS NULL OR sector='') ORDER BY operario ASC
        """)
        return cursor.fetchall()

    def obtener_datos_semana(self, semana):
        """Devuelve los datos semanales de los operarios para 'Chocolates'"""
        cursor = self.conexion.cursor()
        cursor.execute(
            """
                SELECT id, operario, horario, sector
                FROM modymoi
                WHERE semana=? AND (planta='Chocolates' OR planta='Chocolate')
            """,
            (semana,),
        )
        return cursor.fetchall()

    def obtener_datos_semana_finde(self, semana):
        """Devuelve los registros que tengan datos cargados en sectorfinde para la semana elegida"""
        cursor = self.conexion.cursor()

        semana_str = str(semana).strip()

        cursor.execute(
            """
                SELECT id, operario, horariofinde, sectorfinde 
                FROM modymoi 
                WHERE (semana = ? OR semana = ?)
                  AND sectorfinde IS NOT NULL 
                  AND TRIM(sectorfinde) != ''
                  AND operario IS NOT NULL 
                  AND TRIM(operario) != ''
            """,
            (semana_str, int(semana_str) if semana_str.isdigit() else semana_str),
        )

        return cursor.fetchall()

    def guardar_operario(self, id_val, operario, horario, sector, semana):
        """Guarda o actualiza un operario en la base de datos"""
        cursor = self.conexion.cursor()
        cursor.execute(
            """
                UPDATE modymoi
                SET operario=?, horario=?, sector=?, planta='Chocolates', semana=?
                WHERE id=?
            """,
            (operario, horario, sector, str(semana), id_val),
        )
        self.conexion.commit()

        self.operarios_dict[id_val] = operario
        if semana in self.operarios_asignados:
            self.operarios_asignados[semana].add(id_val)

    def limpiar_operario(self, id_val):
        """Elimina la asignación de un operario"""
        cursor = self.conexion.cursor()
        cursor.execute(
            """
                UPDATE modymoi
                SET horario='', sector='', planta=''
                WHERE id=?
            """,
            (id_val,),
        )
        self.conexion.commit()

        for semana, asignados in self.operarios_asignados.items():
            asignados.discard(id_val)

    def guardar_datos_semana(self, semana, registros_pantalla):
        """
        Guarda la grilla semanal reutilizando limpiar_operario y guardar_operario.
        `registros_pantalla` es una lista de tuplas: (id_operario, operario_nombre, horario, sector)
        """
        cursor = self.conexion.cursor()
        sem_val = str(semana).strip()

        # 1. Obtenemos los IDs de los operarios que estaban en Chocolates para esta semana en la BD
        cursor.execute(
            """
            SELECT id 
            FROM modymoi 
            WHERE semana = ? AND LOWER(TRIM(planta)) IN ('chocolates', 'chocolate')
            """,
            (sem_val,),
        )
        ids_previos_en_bd = set(row[0] for row in cursor.fetchall())

        # 2. Obtenemos los IDs presentes actualmente en la pantalla
        ids_actuales_en_pantalla = set(r[0] for r in registros_pantalla)

        # 3. Calculamos quiénes fueron reemplazados o quitados
        ids_a_limpiar = ids_previos_en_bd - ids_actuales_en_pantalla

        # 4. Reutilizamos limpiar_operario para los que ya no están
        for id_old in ids_a_limpiar:
            self.limpiar_operario(id_old)

        # 5. Reutilizamos guardar_operario para asignar los seleccionados
        for id_op, operario_nombre, turno, sector in registros_pantalla:
            self.guardar_operario(id_op, operario_nombre, turno, sector, sem_val)