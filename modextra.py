import tkinter as tk
from tkinter import ttk, messagebox , filedialog
from conexion import obtener_ruta_icono
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import os

def obtener_operarios(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, operario
        FROM modymoi
        ORDER BY operario ASC
    """)
    datos = cursor.fetchall()
    return datos
def obtener_operarios_asignados_en_otro_sector(conexion, semana_actual):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT operario
        FROM modymoi
        WHERE semana = ? AND operario != '' AND sector != ''
    """, (semana_actual,))
    return set(row[0] for row in cursor.fetchall())



def mostrar_horarios_extras(parent, conexion):
   
    ventana = tk.Toplevel(parent)
    ventana.title("Horas extras")
    bg_color = "#ffffff"
    ventana.configure(bg=bg_color)
    ventana.geometry("1920x1080")  # Ancho 1280 px, alto 720 px
    


    ventana.transient(parent)
    ventana.grab_set()
    ventana.iconbitmap(obtener_ruta_icono("icono.ico"))
    style = ttk.Style(ventana)
    style.theme_use('clam')
    style.configure('TButton',
                    font=('Segoe UI', 12, 'bold'),
                    padding=10,
                    foreground='#004080',
                    background='#cce6ff')
    style.map('TButton',
              foreground=[('active', '#00264d')],
              background=[('active', '#99ccff')])

    top_bar = tk.Frame(ventana, bg=bg_color)
    top_bar.pack(fill=tk.X, pady=5, padx=10)

    semana_var = tk.StringVar()

    def exportar_a_pdf():
        try:
            semana_texto = semana_var.get().strip()
            if not semana_texto:
                messagebox.showwarning("Aviso", "Debes seleccionar el número de semana.")
                return

            # Ruta fija donde se guardará el PDF
            carpeta_destino = r"\\HUGO-PC5\Compartir\PRODUCTIVIDADnueva\Horarios"
            nombre_archivo = f"Horarios chocolate semana {semana_texto}.pdf"
            archivo_pdf = os.path.join(carpeta_destino, nombre_archivo)

            # Crear el documento PDF
            doc = SimpleDocTemplate(archivo_pdf, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()

            titulo = Paragraph(f"<b>Semana {semana_texto} - PLANTA DE CHOCOLATES</b>", styles['Title'])
            elements.append(titulo)
            elements.append(Spacer(1, 12))

            sectores_operarios = {}

            for (sector_nombre, turno), frame in sector_frames.items():
                if sector_nombre not in sectores_operarios:
                    sectores_operarios[sector_nombre] = {"MAÑANA": [], "TARDE": [], "NOCHE": []}

                for fila_frame in frame.winfo_children():
                    widgets = fila_frame.winfo_children()
                    if len(widgets) < 4:
                        continue
                    operario_cb = widgets[3]
                    operario = operario_cb.get().strip()
                    if operario:
                        if "MAÑANA" in turno.upper():
                            sectores_operarios[sector_nombre]["MAÑANA"].append(operario)
                        elif "TARDE" in turno.upper():
                            sectores_operarios[sector_nombre]["TARDE"].append(operario)
                        elif "NOCHE" in turno.upper():
                            sectores_operarios[sector_nombre]["NOCHE"].append(operario)

            for sector_nombre, turnos in sectores_operarios.items():
                mañana = turnos["MAÑANA"]
                tarde = turnos["TARDE"]
                noche = turnos["NOCHE"]

                if not (mañana or tarde or noche):
                    continue

                sector_titulo = Paragraph(f"<b>{sector_nombre}</b>", styles['Heading2'])
                elements.append(sector_titulo)
                elements.append(Spacer(1, 6))

                data = [["06 A 14 - MAÑANA", "14 A 22 - TARDE", "22 A 06 - NOCHE"]]
                max_filas = max(len(mañana), len(tarde), len(noche))

                for i in range(max_filas):
                    op_m = mañana[i] if i < len(mañana) else ""
                    op_t = tarde[i] if i < len(tarde) else ""
                    op_n = noche[i] if i < len(noche) else ""
                    data.append([op_m, op_t, op_n])

                table = Table(data, colWidths=[195, 195, 195])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))

            doc.build(elements)
            messagebox.showinfo("Éxito", f"PDF guardado como:\n{archivo_pdf}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al exportar: {e}")

    exportar_btn = ttk.Button(top_bar, text="Exportar a PDF", command=exportar_a_pdf)
    exportar_btn.pack(side=tk.LEFT, padx=10)

    guardar_btn = ttk.Button(top_bar, text="Guardar")
    guardar_btn.pack(side=tk.LEFT, padx=10)

    cerrar_btn = ttk.Button(top_bar, text="Cerrar", command=ventana.destroy)
    cerrar_btn.pack(side=tk.LEFT, padx=10)

    tk.Label(top_bar, text="Semana:", font=("Segoe UI", 12, "bold"),
             bg=bg_color, fg="#004080").pack(side=tk.LEFT, padx=(30, 5))

    semana_combobox = ttk.Combobox(top_bar, width=5, textvariable=semana_var,
                                   font=("Segoe UI", 12, "bold"), state="readonly")
    semana_combobox.pack(side=tk.LEFT)

    cargar_btn = ttk.Button(top_bar, text="Cargar semana")
    cargar_btn.pack(side=tk.LEFT, padx=10)

    semanas = [str(i) for i in range(1, 54)]
    semana_combobox['values'] = semanas

    semana_actual = str(datetime.now().isocalendar()[1] + 1)

    semana_combobox.set(semana_actual)

    lista_operarios = obtener_operarios(conexion)
    nombres_operarios = [op[1] for op in lista_operarios]

    sector_frames = {}
    filas_widgets = []

    sectores = ["ALISTAMIENTO"]
    turnos = ["22:00 a 06:00", "00:00 a 06:00"]
   
    def obtener_operarios_asignados():
        asignados_local = set(cb.get() for _, cb in filas_widgets if cb.get())
        asignados_bd = obtener_operarios_asignados_en_otro_sector(conexion, semana_var.get())
        return asignados_local.union(asignados_bd)


    def actualizar_comboboxes():
        asignados = obtener_operarios_asignados()
        for id_entry, cb in filas_widgets:
            actual = cb.get()
            disponibles = [op for op in nombres_operarios if op not in asignados or op == actual]
            cb['values'] = sorted(disponibles)

    def on_combobox_entry(event, combobox):
        texto = combobox.get().lower()
        asignados = obtener_operarios_asignados() - {combobox.get()}
        filtrados = [op for op in nombres_operarios if texto in op.lower() and op not in asignados]
        combobox['values'] = sorted(filtrados)

    def agregar_fila(sector, turno, id_inicial="", operario_inicial=""):
        fila_frame = tk.Frame(sector_frames[(sector, turno)], bg=bg_color)
        fila_frame.pack(anchor='w', pady=3, padx=5, fill=tk.X)

        tk.Label(fila_frame, text="ID:", font=("Segoe UI", 12), bg=bg_color).pack(side=tk.LEFT, padx=(0, 5))
        id_entry = ttk.Entry(fila_frame, width=5, font=("Segoe UI", 12))
        id_entry.pack(side=tk.LEFT, padx=(0, 10))
        id_entry.insert(0, str(id_inicial))

        tk.Label(fila_frame, text="Operario:", font=("Segoe UI", 12), bg=bg_color).pack(side=tk.LEFT, padx=(0, 5))
        operario_cb = ttk.Combobox(fila_frame, font=("Segoe UI", 12), width=30)
        operario_cb.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        filas_widgets.append((id_entry, operario_cb))
        operario_cb['values'] = sorted(nombres_operarios)

        if operario_inicial:
            operario_cb.set(operario_inicial)
        actualizar_comboboxes()

        def actualizar_id(event=None):
            nombre = operario_cb.get()
            for _id, operario in lista_operarios:
                if operario == nombre:
                    id_entry.delete(0, tk.END)
                    id_entry.insert(0, str(_id))
                    break
            actualizar_comboboxes()

        operario_cb.bind("<KeyRelease>", lambda e: on_combobox_entry(e, operario_cb))
        operario_cb.bind("<<ComboboxSelected>>", actualizar_id)

        eliminar_btn = ttk.Button(fila_frame, text="Eliminar",
                                  command=lambda: eliminar(fila_frame, id_entry, operario_cb))
        eliminar_btn.pack(side=tk.LEFT, padx=(10, 0))

    def eliminar(fila_frame, id_entry, operario_cb):
        # 1. Eliminar de la lista de widgets
        filas_widgets.remove((id_entry, operario_cb))

        # 2. Limpiar horario, sector y planta del operario con ese ID
        try:
            id_valor = id_entry.get()
            if id_valor:
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE modymoi
                    SET semana='', horario = '', sector = '', planta = ''
                    WHERE id = ?
                """, (id_valor,))
                conexion.commit()
        except Exception as e:
            print(f"Error al limpiar datos del operario: {e}")

        # 3. Quitar de la interfaz
        fila_frame.destroy()

        # 4. Actualizar comboboxes
        actualizar_comboboxes()


    def cargar_datos_semana(semana):
        for (sector, turno), frame in sector_frames.items():
            for widget in frame.winfo_children():
                widget.destroy()
        filas_widgets.clear()

        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, operario, Horario, Sector
            FROM modymoi
            WHERE semana=? AND Planta='Chocolates'
        """, (semana,))
        datos = cursor.fetchall()

        datos_por_sector_turno = {}
        for id_val, operario, horario, sector in datos:
            key = (sector, horario)
            if key not in datos_por_sector_turno:
                datos_por_sector_turno[key] = []
            datos_por_sector_turno[key].append((id_val, operario))

        for sector in sectores:
            for turno in turnos:
                key = (sector, turno)
                frame_turno = sector_frames.get(key)
                if not frame_turno:
                    continue

                btn_agregar = ttk.Button(frame_turno, text="Agregar fila",
                                         command=lambda s=sector, t=turno: agregar_fila(s, t))
                btn_agregar.pack(anchor='ne', pady=0, padx=300)

                if key in datos_por_sector_turno:
                    for id_val, operario in datos_por_sector_turno[key]:
                        agregar_fila(sector, turno, id_val, operario)
                else:
                    agregar_fila(sector, turno)
       
    def guardar():
        cursor = conexion.cursor()
        semana_sel = semana_var.get()

        for (id_entry, operario_cb) in filas_widgets:
            id_text = id_entry.get().strip()
            operario_text = operario_cb.get().strip()
            if operario_text:
                try:
                    id_val = int(id_text)
                except ValueError:
                    continue

                parent_frame = id_entry.master.master
                for (sector, turno), frame in sector_frames.items():
                    if frame == parent_frame:
                        cursor.execute("""
                            UPDATE modymoi
                            SET operario = ?, Horario = ?, Sector = ?, Planta = 'Chocolates', semana = ?
                            WHERE id = ?
                        """, (operario_text, turno, sector, semana_sel, id_val))
                        break
                for (sector, turno), frame in sector_frames.items():
                    if frame == parent_frame:
                        cursor.execute("""
                            UPDATE modymoi
                            SET operario = ?, Horario = ?, Sector = ?, Planta = 'Chocolates', semana = ?
                            WHERE id = ?
                        """, (operario_text, turno, sector, semana_sel, id_val))
                        break

        conexion.commit()
        messagebox.showinfo("Guardado", "Datos actualizados correctamente.")
        cargar_datos_semana(semana_sel)

    guardar_btn.config(command=guardar)
    cargar_btn.config(command=lambda: cargar_datos_semana(semana_var.get()))

    contenedor = ttk.Frame(ventana)
    contenedor.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(contenedor, bg=bg_color)
    scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for sector in sectores:
        for turno in turnos:
            frame = tk.LabelFrame(scrollable_frame, text=f"{sector} - {turno}",
                                  font=("Segoe UI", 10, "bold"), fg="#004080", bg=bg_color)
            frame.pack(fill=tk.X, padx=10, pady=5)
            sector_frames[(sector, turno)] = frame
   

    cargar_datos_semana(semana_actual)
