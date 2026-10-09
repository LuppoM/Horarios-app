import os
from tkinter import messagebox
from Polivalenciamodelo import ModeloPolivalencia
from Polivalenciavista import VistaPolivalencia
from pdfservice import PDFService 

class ControladorPolivalencia:
    def __init__(self, root, conexion):
        self.root = root
        self.modelo = ModeloPolivalencia(conexion)
        
        self.operarios = self.modelo.obtener_todos_los_operarios()
        self.matriz_datos = self.modelo.obtener_matriz_roles()

        self.vista = VistaPolivalencia(root, self)
        
        # Guardamos la lista maestra original
        self.todas_las_lineas = self.vista.sectores + self.vista.sectores_especiales
        self.lineas = list(self.todas_las_lineas)

        # Asignamos comando de impresión
        self.vista.btn_imprimir.config(command=self.imprimir_y_abrir_matriz)

        # Configuramos los datos del combo de filtros
        self.vista.combo_filtro.config(values=["-- MOSTRAR TODAS LAS LÍNEAS --"] + sorted(self.todas_las_lineas))
        self.vista.combo_filtro.set("-- MOSTRAR TODAS LAS LÍNEAS --")
        self.vista.combo_filtro.bind("<<ComboboxSelected>>", self.filtrar_matriz_por_linea)

        self.refrescar_interfaz()

    def refrescar_interfaz(self):
        fila_s, fila_t = self.obtener_y_calcular_totales(self.operarios, self.lineas, self.matriz_datos)
        self.vista.construir_matriz(self.operarios, self.lineas, self.matriz_datos, fila_s, fila_t)

    def filtrar_matriz_por_linea(self, event):
        seleccion = self.vista.combo_filtro.get()
        if seleccion == "-- MOSTRAR TODAS LAS LÍNEAS --":
            self.lineas = list(self.todas_las_lineas)
        else:
            self.lineas = [seleccion]
        self.refrescar_interfaz()

    def sincronizar_scroll_x(self, *args):
        self.vista.tree.xview(*args)
        self.vista.tree_totales.xview(*args)

    def obtener_y_calcular_totales(self, operarios, lineas, datos_fuente):
        fila_s = ["SUPLENTE"]
        fila_t = ["TITULAR"]
        for linea in lineas:
            contador_t = 0
            contador_s = 0
            for op_id, _ in operarios:
                rol = datos_fuente.get((int(op_id), linea), "")
                if rol == "TITULAR":
                    contador_t += 1
                elif rol == "SUPLENTE":
                    contador_s += 1
            fila_t.append(str(contador_t) if contador_t > 0 else "0")
            fila_s.append(str(contador_s) if contador_s > 0 else "0")
        return fila_s, fila_t

    def imprimir_y_abrir_matriz(self):
        try:
            servicio_pdf = PDFService()
            fila_s, fila_t = self.obtener_y_calcular_totales(self.operarios, self.lineas, self.matriz_datos)
            ruta_final_pdf = servicio_pdf.generar_matriz_pdf(
                self.operarios, self.lineas, self.matriz_datos, fila_s, fila_t
            )
            os.startfile(ruta_final_pdf)
        except Exception as e:
            messagebox.showerror("Error de Impresión", f"No se pudo generar o abrir el archivo de impresión:\n{e}")

    def alternar_edicion(self):
        if not self.vista.editando:
            self.vista.cambiar_a_modo_edicion()
        else:
            self.guardar_todo()

    def restaurar_valores_originales(self):
        self.matriz_datos = self.modelo.obtener_matriz_roles()
        self.refrescar_interfaz()

    def guardar_celda_dinamico(self, op_id_int, linea_nombre, nuevo_valor):
        """Guarda los datos inmediatamente de forma silenciosa al cambiar la celda."""
        try:
            valor_original_db = self.matriz_datos.get((op_id_int, linea_nombre), "")
            if nuevo_valor != valor_original_db:
                self.modelo.guardar_celda_matriz(op_id_int, linea_nombre, nuevo_valor)
                self.matriz_datos[(op_id_int, linea_nombre)] = nuevo_valor
        except Exception as e:
            print(f"[Error Autoguardado] No se pudo persistir op_id {op_id_int} en {linea_nombre}: {e}")

    def guardar_todo(self):
        """Finaliza el modo edición de forma limpia sin alertas intermedias."""
        try:
            self.vista.regresar_a_modo_lectura()
            self.refrescar_interfaz()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al regresar al modo lectura: {e}")