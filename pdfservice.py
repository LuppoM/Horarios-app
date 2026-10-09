import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors

class PDFService:

    def __init__(self):
        if getattr(sys, 'frozen', False):
            carpeta_base = os.path.dirname(sys.executable)
        else:
            carpeta_base = os.path.dirname(os.path.abspath(__file__))

        self.carpeta_pdf = os.path.join(carpeta_base, "matriz")
        os.makedirs(self.carpeta_pdf, exist_ok=True)

    # ---------------------------------------------------------------------
    def generar_matriz_pdf(self, operarios, lineas, matriz_datos, fila_s, fila_t):
        ruta_pdf = os.path.join(self.carpeta_pdf, "Matriz_Polivalencia.pdf")

        # Hoja horizontal A4 (842 x 595 puntos)
        c = canvas.Canvas(ruta_pdf, pagesize=landscape(A4))

        # --- AJUSTES GEOMÉTRICOS INTEGRALES ---
        x_inicio = 25
        y_maxima_hoja = 540   # Techo de la grilla
        ancho_nombre = 240    # Espacio para los nombres de operarios
        ancho_linea = 17      # Ancho fijo de cada columna
        alto_fila = 14        # Altura de las filas del cuerpo
        
        # ¡REFORZADO! Pasamos de 70 a 105 para dar espacio suficiente a las descripciones extensas
        alto_cabecera = 105   

        # Reducimos levemente el límite por hoja debido al incremento de la cabecera
        max_filas_por_pagina = 26 

        ancho_total_grilla = ancho_nombre + (len(lineas) * ancho_linea)
        contador_operarios_pagina = 0

        def dibujar_encabezado_pagina():
            # TÍTULO PRINCIPAL
            c.setFillColor(colors.HexColor("#000000"))
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x_inicio, y_maxima_hoja + 25, "MATRIZ DE POLIVALENCIA")

            # RECTÁNGULO AZUL DE FONDO
            c.setFillColor(colors.HexColor("#004080"))
            c.setStrokeColor(colors.HexColor("#004080"))
            c.rect(x_inicio, y_maxima_hoja - alto_cabecera, ancho_total_grilla, alto_cabecera, fill=1, stroke=1)

            # Texto estático: Apellido y Nombre
            c.setFillColor(colors.HexColor("#FFFFFF"))
            c.setFont("Helvetica-Bold", 9)
            # Centrado vertical dentro del nuevo alto de cabecera
            c.drawString(x_inicio + 10, y_maxima_hoja - (alto_cabecera / 2) - 4, "Apellido y Nombre")

            # SECTORES VERTICALES A 90 GRADOS
            # Reducido a 5.5 para optimizar legibilidad en celdas de 17pt de ancho
            c.setFont("Helvetica-Bold", 5.5) 
            
            for i, linea in enumerate(lineas):
                x_celda_cabecera = x_inicio + ancho_nombre + (i * ancho_linea)
                
                # Separadores blancos verticales
                c.setStrokeColor(colors.HexColor("#FFFFFF"))
                c.setLineWidth(0.5)
                c.line(x_celda_cabecera, y_maxima_hoja - alto_cabecera, x_celda_cabecera, y_maxima_hoja)

                c.saveState()
                # Trasladamos al eje inferior dinámico de la celda.
                # Dejamos 5 puntos de margen desde el piso del bloque azul.
                c.translate(x_celda_cabecera + (ancho_linea / 2) + 2, y_maxima_hoja - alto_cabecera + 5)
                c.rotate(90)
                
                # Al dibujar en (0,0), el texto se extenderá hacia arriba hasta un máximo de ~95 puntos,
                # calzando perfecto dentro de los 105 del alto total de la cabecera.
                c.drawString(0, 0, linea)
                c.restoreState()

        # Dibujamos la primera página
        dibujar_encabezado_pagina()
        y_actual = y_maxima_hoja - alto_cabecera

        # -----------------------------------------------------------------
        # CUERPO DE LA TABLA (OPERARIOS)
        # -----------------------------------------------------------------
        for idx, (op_id, text_op) in enumerate(operarios):
            
            if contador_operarios_pagina >= max_filas_por_pagina:
                c.showPage()
                dibujar_encabezado_pagina()
                y_actual = y_maxima_hoja - alto_cabecera
                contador_operarios_pagina = 0

            y_fila = y_actual - alto_fila

            if contador_operarios_pagina % 2 == 0:
                c.setFillColor(colors.HexColor("#FFFFFF"))
            else:
                c.setFillColor(colors.HexColor("#F2F5F9"))
            
            c.setStrokeColor(colors.HexColor("#C0C0C0"))
            c.setLineWidth(0.5)
            c.rect(x_inicio, y_fila, ancho_total_grilla, alto_fila, fill=1, stroke=1)

            c.setFillColor(colors.HexColor("#000000"))
            c.setFont("Helvetica", 7)
            c.drawString(x_inicio + 6, y_fila + 3.5, text_op)

            for j, linea in enumerate(lineas):
                x_celda = x_inicio + ancho_nombre + (j * ancho_linea)
                c.line(x_celda, y_fila, x_celda, y_fila + alto_fila)

                rol_actual = matriz_datos.get((int(op_id), linea), "")
                texto_celda = "T" if rol_actual == "TITULAR" else "S" if rol_actual == "SUPLENTE" else ""

                if texto_celda:
                    c.setFont("Helvetica-Bold", 7.5)
                    c.drawCentredString(x_celda + (ancho_linea / 2), y_fila + 3.5, texto_celda)

            y_actual = y_fila
            contador_operarios_pagina += 1

        # -----------------------------------------------------------------
        # SECCIÓN DE TOTALES (VERDE EXCEL)
        # -----------------------------------------------------------------
        if y_actual - (alto_fila * 2) < 40:
            c.showPage()
            dibujar_encabezado_pagina()
            y_actual = y_maxima_hoja - alto_cabecera

        y_fila_s = y_actual - alto_fila
        y_fila_t = y_actual - (alto_fila * 2)

        c.setFillColor(colors.HexColor("#E2EFDA"))
        c.setStrokeColor(colors.HexColor("#375623"))
        c.rect(x_inicio, y_fila_t, ancho_total_grilla, alto_fila * 2, fill=1, stroke=1)

        c.setFillColor(colors.HexColor("#375623"))
        c.setFont("Helvetica-Bold", 7.5)

        c.drawRightString(x_inicio + ancho_nombre - 10, y_fila_s + 4, str(fila_s[0]))
        c.drawRightString(x_inicio + ancho_nombre - 10, y_fila_t + 4, str(fila_t[0]))

        for k in range(1, len(fila_s)):
            x_celda_total = x_inicio + ancho_nombre + ((k - 1) * ancho_linea)
            c.line(x_celda_total, y_fila_t, x_celda_total, y_actual)

            c.drawCentredString(x_celda_total + (ancho_linea / 2), y_fila_s + 4, str(fila_s[k]))
            c.drawCentredString(x_celda_total + (ancho_linea / 2), y_fila_t + 4, str(fila_t[k]))

        c.setLineWidth(1.2)
        c.line(x_inicio, y_actual, x_inicio + ancho_total_grilla, y_actual)

        c.showPage()
        c.save()

        return ruta_pdf