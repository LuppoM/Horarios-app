from datetime import date, timedelta
from tkinter import filedialog, messagebox

from Hgolofinde import mostrar_hgolo_finde
from hgolomodelo import ModeloHGolo
from Hgolovista import VistaHGolo
from operarios_cargados import operarios_cargados
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def manejar_errores(mensaje_error="Ocurrió un error"):
    def decorador(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                messagebox.showerror("Error", f"{mensaje_error}: {e}")
        return wrapper
    return decorador

class ControladorHGolo:
    def __init__(self, root, conexion, modelo_principal):
        self.root = root
        self.modelo_principal = modelo_principal
        self.modelo = ModeloHGolo(conexion)

        self.operarios_dict = self.modelo.obtener_operarios()
        self.nombres_a_id = {nombre: id_val for id_val, nombre in self.operarios_dict.items()}
        self.operarios_seleccionados = set()

        self.vista = VistaHGolo(root, self)
        self.cargar_semana()

    def obtener_semana_actual(self):
        fecha_proxima = date.today() + timedelta(days=7)
        if self.modelo_principal and hasattr(self.modelo_principal, 'obtener_numero_semana_personalizado'):
            return self.modelo_principal.obtener_numero_semana_personalizado(fecha_proxima)
        return self.modelo.obtener_numero_semana_personalizado(fecha_proxima)

    def obtener_operarios_filtrados(self, semana, operario_actual=""):
        disponibles = self.modelo.obtener_operarios_disponibles(semana)
        ocupados = self.modelo.obtener_operarios_asignados_en_otro_sector(semana)
        filtrados = []

        for id_val, nombre in disponibles:
            if (id_val not in ocupados and nombre not in operarios_cargados) or nombre == operario_actual:
                filtrados.append((id_val, nombre))

        return filtrados
    def abrir_fin_de_semana(self):
        mostrar_hgolo_finde(self.root, self.modelo.conexion)
    @manejar_errores("Error al cargar la semana")
    def cargar_semana(self):
        semana = self.vista.semana_var.get() or str(self.obtener_semana_actual())
        self.vista.semana_var.set(semana)

        self.operarios_seleccionados = set()
        global operarios_cargados
        operarios_cargados = set()

        sectores = self.modelo.obtener_sectores_golosinas()
        dotacion_teorica = self.modelo.obtener_dotacion_teorica(semana)
        datos_guardados = self.modelo.obtener_datos_semana(semana)

        asignados_por_turno = {}
        for id_val, operario, horario, sector in datos_guardados:
            if sector not in asignados_por_turno:
                asignados_por_turno[sector] = {}
            if horario not in asignados_por_turno[sector]:
                asignados_por_turno[sector][horario] = []
            if operario:
                asignados_por_turno[sector][horario].append((id_val, operario))
                self.operarios_seleccionados.add(operario)
                operarios_cargados.add(operario)

        self.vista.actualizar_interfaz(sectores, dotacion_teorica, asignados_por_turno)
        self.actualizar_comboboxes()

    @manejar_errores("Error al actualizar listas")
    def actualizar_comboboxes(self):
        semana = self.vista.semana_var.get()

        for filas in self.vista.filas_widgets.values():
            for id_entry, cb in filas:
                actual = cb.get().strip()

                nombres_disponibles = [
                    nombre
                    for id_op, nombre in self.obtener_operarios_filtrados(
                        semana, operario_actual=actual
                    )
                ]

                cb["values"] = sorted(nombres_disponibles)

                if actual:
                    cb.set(actual)

    def on_operario_selected(self, operario_cb, id_entry):
        nombre = operario_cb.get().strip()
        id_valor = self.nombres_a_id.get(nombre, "")

        id_entry.delete(0, "end")
        id_entry.insert(0, str(id_valor))

        self.operarios_seleccionados.add(nombre)
        operarios_cargados.add(nombre)
        # IMPORTANTE: Se quita self.actualizar_comboboxes() para evitar el reescrito masivo de listas.

    @manejar_errores("Error al eliminar la fila")
    def eliminar_fila(self, sector, turno, id_entry, operario_cb, fila_frame):
        nombre = operario_cb.get().strip()
        id_valor = id_entry.get().strip()

        if nombre:
            self.operarios_seleccionados.discard(nombre)
            operarios_cargados.discard(nombre)

        if id_valor:
            self.modelo.limpiar_operario(int(id_valor))

        fila_frame.destroy()

        filas = self.vista.filas_widgets.get((sector, turno), [])
        self.vista.filas_widgets[(sector, turno)] = [
            f for f in filas if f[0] != id_entry and f[1] != operario_cb
        ]

        self.actualizar_comboboxes()

    @manejar_errores("Error al guardar datos")
    def guardar_datos(self):
        semana = self.vista.semana_var.get().strip()

        if not semana:
            messagebox.showwarning("Aviso", "Debes seleccionar la semana.")
            return

        registros_pantalla = []

        # Recorremos todas las filas/combos dibujados en la pantalla
        for (sector, turno), filas in self.vista.filas_widgets.items():
            for id_entry, cb in filas:
                operario_nombre = cb.get().strip()

                if operario_nombre:
                    # 1. Buscamos la ID real asociada al nombre elegido en el Combobox
                    id_real = self.nombres_a_id.get(operario_nombre)

                    # Si por alguna razón no está en el diccionario, intentamos leer la casilla
                    if not id_real:
                        id_real = id_entry.get().strip()

                    if id_real:
                        # 2. Actualizamos visualmente la casilla ID para que coincida con el nuevo operario
                        id_entry.config(state="normal")
                        id_entry.delete(0, "end")
                        id_entry.insert(0, str(id_real))

                        # 3. Agregamos a la lista de personas que se van a conservar/asignar
                        registros_pantalla.append((id_real, operario_nombre, turno, sector))

        # 4. Llamamos a guardar_datos_semana del modelo (que usará limpiar_operario y guardar_operario)
        self.modelo.guardar_datos_semana(semana, registros_pantalla)

        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        
        # Recargamos la semana para verificar que no queden duplicados ni desfasajes
        self.cargar_semana()
    @manejar_errores("Error al exportar el PDF")
    def exportar_a_pdf(self):
        semana_texto = self.vista.semana_var.get().strip()

        if not semana_texto:
            messagebox.showwarning("Aviso", "Debes seleccionar la semana.")
            return

        archivo_pdf = filedialog.asksaveasfilename(
            title="Guardar PDF",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            initialfile=f"Horarios golosinas semana {semana_texto}.pdf",
        )

        if not archivo_pdf:
            return

        doc = SimpleDocTemplate(archivo_pdf, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(
            Paragraph(
                f"<b>Semana {semana_texto} - PLANTA DE GOLOSINAS</b>",
                styles["Title"],
            )
        )
        elements.append(Spacer(1, 12))

        sectores_operarios = {}

        for (sector, turno), filas in self.vista.filas_widgets.items():
            if sector not in sectores_operarios:
                sectores_operarios[sector] = {}
            if turno not in sectores_operarios[sector]:
                sectores_operarios[sector][turno] = []

            for id_entry, cb in filas:
                operario = cb.get().strip()
                if operario:
                    sectores_operarios[sector][turno].append(operario)

        for sector, turnos in sectores_operarios.items():
            if all(len(lst) == 0 for lst in turnos.values()):
                continue

            elements.append(Paragraph(f"<b>{sector}</b>", styles["Heading2"]))
            elements.append(Spacer(1, 6))

            columnas = list(turnos.keys())
            data = [columnas]

            max_filas = max(len(turnos[t]) for t in columnas) if columnas else 0

            for i in range(max_filas):
                fila = [turnos[t][i] if i < len(turnos[t]) else "" for t in columnas]
                data.append(fila)

            table = Table(data, colWidths=[180] * len(columnas))
            table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ])
            )

            elements.append(table)
            elements.append(Spacer(1, 12))

        doc.build(elements)
        messagebox.showinfo("Éxito", f"PDF guardado correctamente:\n{archivo_pdf}")