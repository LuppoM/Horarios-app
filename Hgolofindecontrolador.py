from datetime import date, timedelta
import tkinter as tk
from tkinter import messagebox

from hgolofindemodelo import ModeloHGoloFinde
from Hgolofindevista import VistaHGoloFinde


def manejar_errores(mensaje_error="Ocurrió un error"):
    def decorador(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                messagebox.showerror("Error", f"{mensaje_error}: {e}")
        return wrapper
    return decorador


class ControladorHGoloFinde:

    def __init__(self, root, conexion):
        self.root = root
        self.modelo = ModeloHGoloFinde(conexion)

        self.operarios_dict = {}
        self.nombres_a_id = {}

        self.semana_actual = str(self.obtener_numero_semana_personalizado())
        self.vista = VistaHGoloFinde(root, self)
        self.cargar_semana()

    def obtener_numero_semana_personalizado(self, fecha=None):
        if fecha is None:
            fecha = date.today() + timedelta(days=7)

        anio_actual = fecha.year
        primer_dia_anio = date(anio_actual, 1, 1)

        if primer_dia_anio.weekday() == 0:
            inicio_semana_1 = primer_dia_anio
        else:
            dias_hasta_lunes = (7 - primer_dia_anio.weekday()) % 7
            if dias_hasta_lunes == 0:
                dias_hasta_lunes = 7
            inicio_semana_1 = primer_dia_anio + timedelta(days=dias_hasta_lunes)

        if fecha < inicio_semana_1:
            anio_anterior = anio_actual - 1
            primer_dia_anterior = date(anio_anterior, 1, 1)

            if primer_dia_anterior.weekday() == 0:
                inicio_anterior = primer_dia_anterior
            else:
                inicio_anterior = primer_dia_anterior + timedelta(
                    days=(7 - primer_dia_anterior.weekday()) % 7
                )

            diferencia_dias = (fecha - inicio_anterior).days
            semana = (diferencia_dias // 7) + 1
        else:
            diferencia_dias = (fecha - inicio_semana_1).days
            semana = (diferencia_dias // 7) + 1

        return semana

    def obtener_operarios_filtrados(self, semana, nombre_dia_key="Sábado", operario_actual=""):
        disponibles = self.modelo.obtener_operarios_disponibles(semana, nombre_dia_key)
        return disponibles

    @manejar_errores("Error al cargar la semana")
    def cargar_semana(self):
        semana_ingresada = (
            self.vista.semana_entry.get().strip()
            if hasattr(self.vista, "semana_entry")
            else ""
        )
        semana = semana_ingresada or self.semana_actual

        self.vista.semana_entry.delete(0, tk.END)
        self.vista.semana_entry.insert(0, semana)

        self.operarios_dict = self.modelo.obtener_operarios(semana)
        self.nombres_a_id = {
            nombre: id_val for id_val, nombre in self.operarios_dict.items()
        }

        for container in list(self.vista.dias_frames.values()):
            container.master.destroy()

        self.vista.dias_frames.clear()
        self.vista.filas_widgets.clear()
        if hasattr(self.vista, "dias_vars"):
            self.vista.dias_vars.clear()

        datos = self.modelo.obtener_datos_semana_finde(semana)

        if datos:
            registros_por_dia = {}
            for id_op, operario, dia, horario, sector in datos:
                dia_nombre = dia if dia else "Sábado"
                if dia_nombre not in registros_por_dia:
                    registros_por_dia[dia_nombre] = []
                registros_por_dia[dia_nombre].append(
                    (id_op, operario, horario, sector)
                )

            for dia_nombre, filas in registros_por_dia.items():
                self.vista.agregar_contenedor_dia(dia_nombre)
                for id_op, operario, horario, sector in filas:
                    self.vista.agregar_fila(
                        nombre_dia=dia_nombre,
                        id_val=id_op or "",
                        operario=operario or "",
                        horario=horario or "",
                        sector=sector or "",
                    )
        else:
            for dia in ["Sábado", "Domingo"]:
                self.vista.agregar_contenedor_dia(dia)
                self.vista.agregar_fila(dia)

        self.actualizar_comboboxes()

    def eliminar_bloque_dia(self, nombre_dia):
        if nombre_dia in self.vista.dias_frames:
            container = self.vista.dias_frames[nombre_dia]
            container.master.destroy()

            del self.vista.dias_frames[nombre_dia]
            if nombre_dia in self.vista.filas_widgets:
                del self.vista.filas_widgets[nombre_dia]
            if hasattr(self.vista, "dias_vars") and nombre_dia in self.vista.dias_vars:
                del self.vista.dias_vars[nombre_dia]

            self.vista.reordenar_grid_bloques()
            self.actualizar_comboboxes()

    def agregar_dia_dialogo(self):
        dias_existentes = list(self.vista.dias_frames.keys())
        secuencia_dias = [
            "Sábado",
            "Domingo",
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
        ]

        nuevo_dia = None
        for dia in secuencia_dias:
            if dia not in dias_existentes:
                nuevo_dia = dia
                break

        if not nuevo_dia:
            ultimo_dia = dias_existentes[-1] if dias_existentes else "Viernes"
            idx_ultimo = (
                secuencia_dias.index(ultimo_dia.split(" ")[0])
                if ultimo_dia.split(" ")[0] in secuencia_dias
                else 6
            )
            siguiente_dia_base = secuencia_dias[(idx_ultimo + 1) % 7]
            num_repeticiones = (
                sum(1 for d in dias_existentes if siguiente_dia_base in d) + 1
            )
            nuevo_dia = f"{siguiente_dia_base} ({num_repeticiones})"

        self.vista.agregar_contenedor_dia(nuevo_dia)
        self.vista.agregar_fila(nuevo_dia)
        self.actualizar_comboboxes()

    @manejar_errores("Error al actualizar operarios")
    def actualizar_comboboxes(self):
        semana = self.vista.semana_entry.get().strip() or self.semana_actual

        for nombre_dia_key, filas in self.vista.filas_widgets.items():
            for id_entry, op_cb, hor_cb, sec_cb in filas:
                actual = op_cb.get().strip()
                nombres = [
                    nombre
                    for id_op, nombre in self.obtener_operarios_filtrados(
                        semana=semana,
                        nombre_dia_key=nombre_dia_key,
                        operario_actual=actual,
                    )
                ]
                op_cb["values"] = sorted(nombres)
                if actual:
                    op_cb.set(actual)

    def on_operario_selected(self, operario_cb, id_entry):
        nombre = operario_cb.get().strip()
        id_valor = self.nombres_a_id.get(nombre, "")

        id_entry.delete(0, tk.END)
        id_entry.insert(0, str(id_valor))

        self.actualizar_comboboxes()

    def eliminar_fila(self, nombre_dia, id_entry, operario_cb, fila_frame):
        fila_frame.destroy()

        filas = self.vista.filas_widgets.get(nombre_dia, [])
        self.vista.filas_widgets[nombre_dia] = [
            f for f in filas if f[0] != id_entry and f[1] != operario_cb
        ]

        self.actualizar_comboboxes()

    @manejar_errores("Error al guardar fin de semana")
    def guardar_datos(self):
        semana = self.vista.semana_entry.get().strip() or self.semana_actual

        registros = []
        for nombre_dia_key, filas in self.vista.filas_widgets.items():
            dia_real = (
                self.vista.dias_vars[nombre_dia_key].get().strip()
                if hasattr(self.vista, "dias_vars") and nombre_dia_key in self.vista.dias_vars
                else nombre_dia_key
            )

            for id_entry, op_cb, hor_cb, sec_cb in filas:
                id_val = id_entry.get().strip()
                horario = hor_cb.get().strip()
                sector = sec_cb.get().strip()

                if id_val and (horario or sector):
                    registros.append((id_val, dia_real, horario, sector))

        self.modelo.guardar_datos_finde(semana, registros)
        messagebox.showinfo(
            "Éxito", "Datos de Fin de Semana (Golosinas) guardados correctamente."
        )
        self.cargar_semana()