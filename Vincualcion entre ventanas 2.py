import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os
import subprocess
import datetime
import re

def validar_solo_numeros(text):
    return text.isdigit() or text == ""

def validar_solo_letras(text):
    return re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]*$", text) is not None

def validar_celular(text):
    return len(text) <= 10 and text.isdigit()

def actualizar_cantones(event):
    provincia_seleccionada = provincia_combobox.get()
    if provincia_seleccionada in cantones_por_provincia:
        canton_combobox['values'] = cantones_por_provincia[provincia_seleccionada]
        canton_combobox.set("Seleccione un Cantón")
    else:
        canton_combobox['values'] = []
        canton_combobox.set("Seleccione un Cantón")

def validar_y_calcular():
    try:
        # Ponderación antes del simulacro (Puntaje A)
        va = int(opcion1.get()) + int(opcion2.get()) + int(opcion3.get()) + int(opcion4.get()) + int(opcion5.get()) + int(opcion6.get()) + int(opcion7.get()) + int(opcion8.get()) + int(opcion9.get()) + int(opcion10.get())
        
        # Ponderación durante el simulacro (Puntaje B)
        vb = int(opcion11.get()) + int(opcion12.get()) + int(opcion13.get()) + int(opcion14.get()) + int(opcion15.get()) + int(opcion16.get()) + int(opcion17.get()) + int(opcion18.get()) + int(opcion19.get()) + int(opcion20.get())

        # Ponderación después del simulacro (Puntaje C)
        vc = int(opcion21.get()) + int(opcion22.get()) + int(opcion23.get()) + int(opcion24.get()) + int(opcion25.get()) + int(opcion26.get()) + int(opcion27.get()) + int(opcion28.get())

        valor_a_label.config(text=str(va))
        valor_b_label.config(text=str(vb))
        valor_c_label.config(text=str(vc))

        # Fórmulas de Calificación según el PDF
        # Calificación A: (VA * 10) / 36
        ca = (va * 10) / 36
        # Calificación B: (VB * 10) / 28
        cb = (vb * 10) / 28
        # Calificación C: (VC * 10) / 16
        cc = (vc * 10) / 16

        calificacion_a_label.config(text=f"{ca:.2f}")
        calificacion_b_label.config(text=f"{cb:.2f}")
        calificacion_c_label.config(text=f"{cc:.2f}")

        # Cálculos de Totales según el PDF
        # Puntaje Total: PT = VA + VB + VC
        pt = va + vb + vc
        # Calificación Total: CT = (PT * 10) / 80
        ct = (pt * 10) / 80
        
        puntaje_total_label.config(text=f"{pt}")
        calificacion_total_label.config(text=f"{ct:.2f}")
        
        clasificacion = "N/A"
        if ct > 9.0:
            clasificacion = "Excelente"
        elif ct >= 7.0 and ct <= 9.0:
            clasificacion = "Muy Bueno"
        elif ct >= 5.0 and ct < 7.0:
            clasificacion = "Bueno"
        elif ct >= 3.0 and ct < 5.0:
            clasificacion = "Regular"
        else:
            clasificacion = "Deficiente"
        
        clasificacion_label.config(text=clasificacion)

        return True
    except (ValueError, IndexError):
        messagebox.showerror("Error", "Por favor, complete todas las opciones de puntuación con valores válidos.")
        return False

def guardar_excel():
    if not validar_y_calcular():
        return

    data = {
        "Evento/hipótesis": [evento_hipotesis_entry.get()],
        "Hora": [hora_label.cget("text")],
        "Fecha": [fecha_label.cget("text")],
        "Nombre de la institución": [nombre_de_la_institucion_entry.get()],
        "Jornada": [jornada_entry.get()],
        "Dirección de la institución": [direccion_de_la_institucion_entry.get()],
        "Sostenimiento": [sostenimiento_entry.get()],
        "Zona": [zona_entry.get()],
        "Distrito": [distrito_entry.get()],
        "AMIE": [amie_entry.get()],
        "Provincia": [provincia_combobox.get()],
        "Cantón": [canton_combobox.get()],
        "Máxima Autoridad": [maxima_entry.get()],
        "Celular (Máxima)": [celular_maxima_entry.get()],
        "Coordinador del ejercicio": [coordinado_entry.get()],
        "Evaluador": [evalua_entry.get()],
        "Celular (Evaluador)": [celular_evalua_entry.get()],
        "Cargo/Puesto": [cargo_entry.get()],
        "Institución": [institucion_entry.get()],
        "Estudiantes": [participantes_entry_frame.winfo_children()[0].get()],
        "Docentes": [participantes_entry_frame.winfo_children()[1].get()],
        "Administrativos": [participantes_entry_frame.winfo_children()[2].get()],
        "Funcionarios": [participantes_entry_frame.winfo_children()[3].get()],
        "Atención Prioritaria": [participantes_entry_frame.winfo_children()[4].get()],
        "Duración Estimado": [duracion_entry_frame.winfo_children()[0].get()],
        "Duración Real": [duracion_entry_frame.winfo_children()[1].get()],
        "Organización Comité de Gestión de Riesgo": [opcion1.get()],
        "Plan Institucional para la Reducción de Riesgos (PIRR)": [opcion2.get()],
        "Plan de trabajo (ficha técnica) y guion elaborados": [opcion3.get()],
        "Distribución de roles de acuerdo a las funciones": [opcion4.get()],
        "Reuniones pre operaciones realizadas": [opcion5.get()],
        "Mapa de riesgos, evacuación y recursos correctamente ubicado": [opcion6.get()],
        "Grupos de atención prioritaria identificados": [opcion7.get()],
        "Evaluación de situaciones peligrosas": [opcion8.get()],
        "Ejercicios de simulación previos": [opcion9.get()],
        "Elementos de escenografía debidamente organizados": [opcion10.get()],
        "Alarma fue escuchada": [opcion11.get()],
        "Medios y flujo de comunicación": [opcion12.get()],
        "Procedimientos establecidos": [opcion13.get()],
        "Ejecución acorde al guion": [opcion14.get()],
        "Recursos considerados en la planificación": [opcion15.get()],
        "Grupos de atención prioritaria con apoyo": [opcion16.get()],
        "Tiempo de respuesta": [opcion17.get()],
        "Organización distributiva": [opcion18.get()],
        "Verificación de actores": [opcion19.get()],
        "Coordinación y trabajo en equipo": [opcion20.get()],
        "Participación del Equipo Organizador": [opcion21.get()],
        "Reunión post operacional": [opcion22.get()],
        "Asumió su función de líder": [opcion23.get()],
        "Instrucciones claras y concretas": [opcion24.get()],
        "Brigadas realizaron sus funciones": [opcion25.get()],
        "Brigadas con sistema de identificación": [opcion26.get()],
        "Actividades lúdicas en el punto de encuentro": [opcion27.get()],
        "Se encontraron presentes con sus estudiantes": [opcion28.get()],
        "Valoración (A)": [valor_a_label.cget("text")],
        "Calificación (A)": [calificacion_a_label.cget("text")],
        "Valoración (B)": [valor_b_label.cget("text")],
        "Calificación (B)": [calificacion_b_label.cget("text")],
        "Valoración (C)": [valor_c_label.cget("text")],
        "Calificación (C)": [calificacion_c_label.cget("text")],
        "Puntaje Total": [puntaje_total_label.cget("text")],
        "Calificación Total": [calificacion_total_label.cget("text")],
        "Clasificación": [clasificacion_label.cget("text")],
        "Observaciones del Evaluador": [observaciones_text.get("1.0", tk.END).strip()],
        "Firma Máxima Autoridad": [firma_maxima_entry.get()],
        "Firma Evaluador": [firma_evaluador_entry.get()]
    }

    df = pd.DataFrame(data)
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    excel_path = os.path.join(downloads_path, "Resultados_evaluacion.xlsx")

    if os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            existing_df = pd.read_excel(excel_path)
            startrow = existing_df.shape[0] + 1
            df.to_excel(writer, index=False, header=False, startrow=startrow)
    else:
        df.to_excel(excel_path, index=False)

    messagebox.showinfo("Éxito", "Los datos se han guardado correctamente en el archivo de Excel.")
    subprocess.Popen(['start', 'excel', excel_path], shell=True)


ventana = tk.Tk()
ventana.title("Plantilla Evaluación de riesgo")
ventana.state('zoomed')
def accion_opcion1_pestaña1():
    try:
        subprocess.run(["python","formulario de registro.py"])
        ventana.destroy()
    except FileNotFoundError:
        messagebox.showerror("!!CUIDADO!!","No se encuentra el arhivo")
main_frame = tk.Frame(ventana)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame)
canvas.pack(fill="both", expand=True, side="left")

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

form_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=form_frame, anchor="nw", width=ventana.winfo_screenwidth())

form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# 1. Datos Generales
datos_generales = tk.Frame(form_frame, relief="solid", bg="#58595B")
datos_generales.pack(fill="x", pady=(10,0))
tk.Label(datos_generales, text="1. Datos Generales", bg="#58595B", fg="white").pack(side=tk.LEFT, padx=5)

frame1 = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
frame1.pack(fill="x")
tk.Label(frame1, text="Evento/hipótesis", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
evento_hipotesis_entry = tk.Entry(frame1, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_letras), "%P"))
evento_hipotesis_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame1, text="Hora:", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
hora_label = tk.Label(frame1, text=datetime.datetime.now().strftime("%H:%M:%S"), bg="white", relief="solid", borderwidth=1, width=15)
hora_label.pack(side=tk.LEFT, padx=5, pady=5)
tk.Label(frame1, text="Fecha:", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
fecha_label = tk.Label(frame1, text=datetime.date.today().strftime("%d/%m/%Y"), bg="white", relief="solid", borderwidth=1, width=15)
fecha_label.pack(side=tk.LEFT, padx=5, pady=5)

frame2 = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
frame2.pack(fill="x")
tk.Label(frame2, text="Nombre de la Institución", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
nombre_de_la_institucion_entry = tk.Entry(frame2, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_letras), "%P"))
nombre_de_la_institucion_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame2, text="Jornada", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
jornada_entry = tk.Entry(frame2, bg="white")
jornada_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)

frame3 = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
frame3.pack(fill="x")
tk.Label(frame3, text="Dirección de la Institución", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
direccion_de_la_institucion_entry = tk.Entry(frame3, bg="white")
direccion_de_la_institucion_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame3, text="Sostenimiento", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
sostenimiento_entry = tk.Entry(frame3, bg="white")
sostenimiento_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)

frame4 = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
frame4.pack(fill="x")
tk.Label(frame4, text="Zona", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
zona_entry = tk.Entry(frame4, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
zona_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame4, text="Distrito", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
distrito_entry = tk.Entry(frame4, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
distrito_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame4, text="AMIE", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
amie_entry = tk.Entry(frame4, bg="white")
amie_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame4, text="Provincia", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
provincias_ecuador = ["Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo", "Cotopaxi", "El Oro", "Esmeraldas", "Galápagos", "Guayas", "Imbabura", "Loja", "Los Ríos", "Manabí", "Morona Santiago", "Napo", "Orellana", "Pastaza", "Pichincha", "Santa Elena", "Santo Domingo de los Tsáchilas", "Sucumbíos", "Tungurahua", "Zamora Chinchipe"]
cantones_por_provincia = {
    "Azuay": ["Cuenca", "Girón", "Gualaceo", "Nabón", "Paute", "Pucará", "San Fernando", "Santa Isabel", "Sigsig", "Chordeleg", "El Pan", "Sevilla de Oro", "Guachapala", "Camilo Ponce Enríquez", "Oña"],
    "Bolívar": ["Guaranda", "Chillanes", "San Miguel", "Echeandía", "Caluma", "Las Naves", "Chimbo"],
    "Cañar": ["Azogues", "Biblián", "Cañar", "La Troncal", "El Tambo", "Déleg", "Suscal"],
    "Carchi": ["Tulcán", "Bolívar", "Espejo", "Mira", "Montúfar", "San Pedro de Huaca"],
    "Chimborazo": ["Riobamba", "Alausi", "Colta", "Chunchi", "Guamote", "Guano", "Pallatanga", "Penipe", "Cumandá", "Chambo"],
    "Cotopaxi": ["Latacunga", "La Maná", "Pangua", "Pujilí", "Salcedo", "Saquisilí", "Sigchos"],
    "El Oro": ["Machala", "Arenillas", "Atahualpa", "Balsas", "Chilla", "El Guabo", "Huaquillas", "Las Lajas", "Pasaje", "Piñas", "Portovelo", "Santa Rosa", "Zaruma", "Marcabelí"],
    "Esmeraldas": ["Esmeraldas", "Eloy Alfaro", "Muisne", "Quinindé", "San Lorenzo", "Atacames", "Rioverde"],
    "Galápagos": ["San Cristóbal", "Isabela", "Santa Cruz"],
    "Guayas": ["Guayaquil", "Alfredo Baquerizo Moreno (Juján)", "Balao", "Balzar", "Colimes", "Daule", "Durán", "El Empalme", "El Triunfo", "General Antonio Elizalde (Bucay)", "Isidro Ayora", "Lomas de Sargentillo", "Marcelino Maridueña", "Milagro", "Naranjal", "Naranjito", "Nobol", "Palestina", "Pedro Carbo", "Playas", "Salitre (Urbina Jado)", "Samborondón", "Santa Lucía", "Simón Bolívar", "Yaguachi"],
    "Imbabura": ["Ibarra", "Antonio Ante", "Cotacachi", "Otavalo", "Pimampiro", "San Miguel de Urcuquí"],
    "Loja": ["Loja", "Calvas", "Catamayo", "Celica", "Chaguarpamba", "Espíndola", "Gonzanamá", "Macará", "Paltas", "Pindal", "Puyango", "Quilanga", "Saraguro", "Sozoranga", "Zapotillo", "Olmedo"],
    "Los Ríos": ["Babahoyo", "Baba", "Montalvo", "Puebloviejo", "Quevedo", "Vinces", "Ventanas", "Palenque", "Urdaneta", "Quinsaloma", "Mocache", "Valencia", "Buena Fe"],
    "Manabí": ["Portoviejo", "Bolívar", "Chone", "El Carmen", "Flavio Alfaro", "Jipijapa", "Junín", "Manta", "Montecristi", "Olmedo", "Paján", "Pedernales", "Pichincha", "Rocafuerte", "Santa Ana", "Sucre", "24 de Mayo", "Tosagua", "Jaramijó", "Puerto López", "Jama", "San Vicente"],
    "Morona Santiago": ["Macas", "Morona", "Gualaquiza", "Limón Indanza", "Palora", "Santiago", "Sucúa", "Huamboya", "San Juan Bosco", "Taisha", "Logroño", "Pablo VI"],
    "Napo": ["Tena", "Archidona", "El Chaco", "Quijos", "Carlos Julio Arosemena Tola"],
    "Orellana": ["Francisco de Orellana (Coca)", "Aguarico", "La Joya de los Sachas", "Loreto"],
    "Pastaza": ["Puyo", "Arajuno", "Mera", "Santa Clara"],
    "Pichincha": ["Quito", "Cayambe", "Mejía", "Pedro Moncayo", "Pedro Vicente Maldonado", "Puerto Quito", "Rumiñahui", "San Miguel de los Bancos"],
    "Santa Elena": ["Santa Elena", "La Libertad", "Salinas"],
    "Santo Domingo de los Tsáchilas": ["Santo Domingo", "La Concordia"],
    "Sucumbíos": ["Nueva Loja", "Cascales", "Cuyabeno", "Gonzalo Pizarro", "Lago Agrio", "Putumayo", "Shushufindi"],
    "Tungurahua": ["Ambato", "Baños de Agua Santa", "Cevallos", "Mocha", "Patate", "Pelileo", "Píllaro", "Quero", "Tisaleo"],
    "Zamora Chinchipe": ["Zamora", "Yacuambi", "Yantzaza", "Chinchipe", "Nangaritza", "El Pangui", "Centinela del Cóndor", "Palanda", "Paquisha"]
}
provincia_combobox = ttk.Combobox(frame4, values=provincias_ecuador, state="readonly")
provincia_combobox.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
provincia_combobox.set("Seleccione una Provincia")
tk.Label(frame4, text="Cantón", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
canton_combobox = ttk.Combobox(frame4, state="readonly")
canton_combobox.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
provincia_combobox.bind("<<ComboboxSelected>>", actualizar_cantones)

frame5 = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
frame5.pack(fill="x")
tk.Label(frame5, text="Máxima Autoridad", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
maxima_entry = tk.Entry(frame5, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_letras), "%P"))
maxima_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame5, text="Celular", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
celular_maxima_entry = tk.Entry(frame5, bg="white", validate="key", validatecommand=(ventana.register(validar_celular), "%P"))
celular_maxima_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)

frame6 = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
frame6.pack(fill="x")
tk.Label(frame6, text="Cargo/Puesto", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
cargo_entry = tk.Entry(frame6, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_letras), "%P"))
cargo_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame6, text="Institución", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
institucion_entry = tk.Entry(frame6, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_letras), "%P"))
institucion_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)

frame7 = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
frame7.pack(fill="x")
tk.Label(frame7, text="Coordinador del Ejercicio", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
coordinado_entry = tk.Entry(frame7, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_letras), "%P"))
coordinado_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame7, text="Evaluador", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
evalua_entry = tk.Entry(frame7, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_letras), "%P"))
evalua_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(frame7, text="Celular", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
celular_evalua_entry = tk.Entry(frame7, bg="white", validate="key", validatecommand=(ventana.register(validar_celular), "%P"))
celular_evalua_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)

# Participantes
participantes_frame = tk.Frame(form_frame, relief="solid", bg="#58595B")
participantes_frame.pack(fill="x", pady=(10,0))
tk.Label(participantes_frame, text="Participantes (Actores sistema educativo)", bg="#58595B", fg="white").pack(fill="x")

participantes_header = tk.Frame(form_frame, relief="solid", bg="#BFBFBF")
participantes_header.pack(fill="x")
tk.Label(participantes_header, text="Estudiantes", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(participantes_header, text="Docentes", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(participantes_header, text="Administrativos", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(participantes_header, text="Funcionarios", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(participantes_header, text="Atención Prioritaria", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

participantes_entry_frame = tk.Frame(form_frame, bg="white", relief="solid")
participantes_entry_frame.pack(fill="x")
estudiantes_entry = tk.Entry(participantes_entry_frame, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
estudiantes_entry.pack(side=tk.LEFT, fill="x", expand=True)
docentes_entry = tk.Entry(participantes_entry_frame, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
docentes_entry.pack(side=tk.LEFT, fill="x", expand=True)
administrativos_entry = tk.Entry(participantes_entry_frame, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
administrativos_entry.pack(side=tk.LEFT, fill="x", expand=True)
funcionarios_entry = tk.Entry(participantes_entry_frame, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
funcionarios_entry.pack(side=tk.LEFT, fill="x", expand=True)
atencion_prioritaria_entry = tk.Entry(participantes_entry_frame, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
atencion_prioritaria_entry.pack(side=tk.LEFT, fill="x", expand=True)

# Duración
duracion_frame = tk.Frame(form_frame, relief="solid", bg="#58595B")
duracion_frame.pack(fill="x", pady=(10,0))
tk.Label(duracion_frame, text="Duración", bg="#58595B", fg="white").pack(fill="x")

duracion_header = tk.Frame(form_frame, relief="solid", bg="#BFBFBF")
duracion_header.pack(fill="x")
tk.Label(duracion_header, text="Estimado", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(duracion_header, text="Real", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

duracion_entry_frame = tk.Frame(form_frame, bg="white", relief="solid")
duracion_entry_frame.pack(fill="x")
duracion_estimado_entry = tk.Entry(duracion_entry_frame, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
duracion_estimado_entry.pack(side=tk.LEFT, fill="x", expand=True)
duracion_real_entry = tk.Entry(duracion_entry_frame, bg="white", validate="key", validatecommand=(ventana.register(validar_solo_numeros), "%P"))
duracion_real_entry.pack(side=tk.LEFT, fill="x", expand=True)

# Ponderación
ponderacion_frame = tk.Frame(form_frame, relief="solid", bg="#58595B")
ponderacion_frame.pack(fill="x", pady=(10,0))
tk.Label(ponderacion_frame, text="Ponderación", bg="#58595B", fg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(ponderacion_frame, text="Asignar el puntaje según lo indicado", bg="#BFBFBF").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(ponderacion_frame, text="(2) S", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(ponderacion_frame, text="(1) PARCIAL", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(ponderacion_frame, text="(0) NO", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

# 2. Antes del Simulacro
antes_simulacro = tk.Frame(form_frame, relief="solid", bg="#58595B")
antes_simulacro.pack(fill="x", pady=(10,0))
tk.Label(antes_simulacro, text="2. Antes del simulacro", bg="#58595B", fg="white").pack(side=tk.LEFT)

headers_a = tk.Frame(form_frame, bg="#BFBFBF")
headers_a.pack(fill="x")
tk.Label(headers_a, text="Organización", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(headers_a, text="Verificable", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(headers_a, text="Puntaje", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

opcion1 = tk.StringVar(value="0")
container1 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container1.pack(fill="x")
tk.Label(container1, text="Comité Institucional de Gestión de Riesgos / Brigadas conformadas y organizadas.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container1, text="Acta o Certificado de conformación", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame1 = tk.Frame(container1, bg="white")
puntaje_frame1.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame1, text="2", variable=opcion1, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame1, text="1", variable=opcion1, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame1, text="0", variable=opcion1, value="0").pack(side=tk.LEFT)

opcion2 = tk.StringVar(value="0")
container2 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container2.pack(fill="x")
tk.Label(container2, text="Plan Institucional para la Reducción de Riesgos (PIRR) / Plan de Institucional (actualizado).", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container2, text="Documento revisado/aprobado", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame2 = tk.Frame(container2, bg="white")
puntaje_frame2.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame2, text="2", variable=opcion2, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame2, text="1", variable=opcion2, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame2, text="0", variable=opcion2, value="0").pack(side=tk.LEFT)

opcion3 = tk.StringVar(value="0")
container3 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container3.pack(fill="x")
tk.Label(container3, text="Plan de trabajo (ficha técnica) y guion elaborados.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container3, text="Documentos aprobados", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame3 = tk.Frame(container3, bg="white")
puntaje_frame3.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame3, text="2", variable=opcion3, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame3, text="1", variable=opcion3, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame3, text="0", variable=opcion3, value="0").pack(side=tk.LEFT)

opcion4 = tk.StringVar(value="0")
container4 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container4.pack(fill="x")
tk.Label(container4, text="Distribución de roles de acuerdo a las funciones establecidas.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container4, text="Observación directa", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame4 = tk.Frame(container4, bg="white")
puntaje_frame4.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame4, text="2", variable=opcion4, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame4, text="1", variable=opcion4, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame4, text="0", variable=opcion4, value="0").pack(side=tk.LEFT)

opcion5 = tk.StringVar(value="0")
container5 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container5.pack(fill="x")
tk.Label(container5, text="Reuniones pre operaciones realizadas.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container5, text="Documento verificable / registro fotográfico", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame5 = tk.Frame(container5, bg="white")
puntaje_frame5.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame5, text="2", variable=opcion5, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame5, text="1", variable=opcion5, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame5, text="0", variable=opcion5, value="0").pack(side=tk.LEFT)

opcion6 = tk.StringVar(value="0")
container6 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container6.pack(fill="x")
tk.Label(container6, text="Mapa de riesgos, evacuación y recursos correctamente ubicado.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container6, text="Observación directa", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame6 = tk.Frame(container6, bg="white")
puntaje_frame6.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame6, text="2", variable=opcion6, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame6, text="1", variable=opcion6, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame6, text="0", variable=opcion6, value="0").pack(side=tk.LEFT)

opcion7 = tk.StringVar(value="0")
container7 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container7.pack(fill="x")
tk.Label(container7, text="Grupos de atención prioritaria identificados.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container7, text="Observación directa", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame7 = tk.Frame(container7, bg="white")
puntaje_frame7.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame7, text="2", variable=opcion7, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame7, text="1", variable=opcion7, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame7, text="0", variable=opcion7, value="0").pack(side=tk.LEFT)

opcion8 = tk.StringVar(value="0")
container8 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container8.pack(fill="x")
tk.Label(container8, text="Evaluación de situaciones peligrosas que puedan afectar el desarrollo del ejercicio.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container8, text="Informe", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame8 = tk.Frame(container8, bg="white")
puntaje_frame8.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame8, text="2", variable=opcion8, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame8, text="1", variable=opcion8, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame8, text="0", variable=opcion8, value="0").pack(side=tk.LEFT)

opcion9 = tk.StringVar(value="0")
container9 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container9.pack(fill="x")
tk.Label(container9, text="Se realizaron ejercicios de simulación previos.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container9, text="Informe", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame9 = tk.Frame(container9, bg="white")
puntaje_frame9.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame9, text="2", variable=opcion9, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame9, text="1", variable=opcion9, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame9, text="0", variable=opcion9, value="0").pack(side=tk.LEFT)

opcion10 = tk.StringVar(value="0")
container10 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container10.pack(fill="x")
tk.Label(container10, text="Elementos que conforman la escenografía debidamente organizados e instalados.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(container10, text="Observación directa", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame10 = tk.Frame(container10, bg="white")
puntaje_frame10.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame10, text="2", variable=opcion10, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame10, text="1", variable=opcion10, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame10, text="0", variable=opcion10, value="0").pack(side=tk.LEFT)

# 3. Durante el Simulacro
durante_simulacro = tk.Frame(form_frame, relief="solid", bg="#58595B")
durante_simulacro.pack(fill="x", pady=(10,0))
tk.Label(durante_simulacro, text="3. Durante el simulacro", bg="#58595B", fg="white").pack(side=tk.LEFT)

headers_b = tk.Frame(form_frame, bg="#BFBFBF")
headers_b.pack(fill="x")
tk.Label(headers_b, text="Ejecución", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(headers_b, text="Puntaje", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

opcion11 = tk.StringVar(value="0")
container11 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container11.pack(fill="x")
tk.Label(container11, text="La alarma fue escuchada por todos los actores del sistema educativo.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame11 = tk.Frame(container11, bg="white")
puntaje_frame11.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame11, text="2", variable=opcion11, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame11, text="1", variable=opcion11, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame11, text="0", variable=opcion11, value="0").pack(side=tk.LEFT)

opcion12 = tk.StringVar(value="0")
container12 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container12.pack(fill="x")
tk.Label(container12, text="Funcionaron los medios y flujo de comunicación instaurados.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame12 = tk.Frame(container12, bg="white")
puntaje_frame12.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame12, text="2", variable=opcion12, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame12, text="1", variable=opcion12, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame12, text="0", variable=opcion12, value="0").pack(side=tk.LEFT)

opcion13 = tk.StringVar(value="0")
container13 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container13.pack(fill="x")
tk.Label(container13, text="Se aplicaron los procedimientos establecidos al momento de la evacuación.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame13 = tk.Frame(container13, bg="white")
puntaje_frame13.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame13, text="2", variable=opcion13, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame13, text="1", variable=opcion13, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame13, text="0", variable=opcion13, value="0").pack(side=tk.LEFT)

opcion14 = tk.StringVar(value="0")
container14 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container14.pack(fill="x")
tk.Label(container14, text="La ejecución del ejercicio fue acorde al guion establecido.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame14 = tk.Frame(container14, bg="white")
puntaje_frame14.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame14, text="2", variable=opcion14, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame14, text="1", variable=opcion14, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame14, text="0", variable=opcion14, value="0").pack(side=tk.LEFT)

opcion15 = tk.StringVar(value="0")
container15 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container15.pack(fill="x")
tk.Label(container15, text="Los recursos considerados en la planificación fueron ocupados.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame15 = tk.Frame(container15, bg="white")
puntaje_frame15.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame15, text="2", variable=opcion15, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame15, text="1", variable=opcion15, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame15, text="0", variable=opcion15, value="0").pack(side=tk.LEFT)

opcion16 = tk.StringVar(value="0")
container16 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container16.pack(fill="x")
tk.Label(container16, text="Las personas identificadas pertenecientes a los grupos de atención prioritaria contaron con personal de apoyo asignado de acuerdo a sus necesidades.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame16 = tk.Frame(container16, bg="white")
puntaje_frame16.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame16, text="2", variable=opcion16, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame16, text="1", variable=opcion16, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame16, text="0", variable=opcion16, value="0").pack(side=tk.LEFT)

opcion17 = tk.StringVar(value="0")
container17 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container17.pack(fill="x")
tk.Label(container17, text="El tiempo de respuesta durante la evacuación fue el óptimo acorde a las características que presenta la institución.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame17 = tk.Frame(container17, bg="white")
puntaje_frame17.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame17, text="2", variable=opcion17, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame17, text="1", variable=opcion17, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame17, text="0", variable=opcion17, value="0").pack(side=tk.LEFT)

opcion18 = tk.StringVar(value="0")
container18 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container18.pack(fill="x")
tk.Label(container18, text="Se tuvo una organización distributiva de las personas evacuadas en el punto de encuentro o zona segura.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame18 = tk.Frame(container18, bg="white")
puntaje_frame18.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame18, text="2", variable=opcion18, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame18, text="1", variable=opcion18, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame18, text="0", variable=opcion18, value="0").pack(side=tk.LEFT)

opcion19 = tk.StringVar(value="0")
container19 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container19.pack(fill="x")
tk.Label(container19, text="Se realizó una verificación de actores del sistema educativo evacuados en el punto de encuentro o zona segura.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame19 = tk.Frame(container19, bg="white")
puntaje_frame19.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame19, text="2", variable=opcion19, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame19, text="1", variable=opcion19, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame19, text="0", variable=opcion19, value="0").pack(side=tk.LEFT)

opcion20 = tk.StringVar(value="0")
container20 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container20.pack(fill="x")
tk.Label(container20, text="Se visualizó coordinación y trabajo en equipo por parte de los participantes.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame20 = tk.Frame(container20, bg="white")
puntaje_frame20.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame20, text="2", variable=opcion20, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame20, text="1", variable=opcion20, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame20, text="0", variable=opcion20, value="0").pack(side=tk.LEFT)

# 4. Después del Simulacro
despues_simulacro = tk.Frame(form_frame, relief="solid", bg="#58595B")
despues_simulacro.pack(fill="x", pady=(10,0))
tk.Label(despues_simulacro, text="4. Después del simulacro", bg="#58595B", fg="white").pack(side=tk.LEFT)

headers_c = tk.Frame(form_frame, bg="#BFBFBF")
headers_c.pack(fill="x")
tk.Label(headers_c, text="Equipo Organizador (Comité Institucional de Gestion de Riesgos)", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(headers_c, text="Puntaje", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

opcion21 = tk.StringVar(value="0")
container21 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container21.pack(fill="x")
tk.Label(container21, text="La participación de los integrantes del Equipo Organizador fue activa.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame21 = tk.Frame(container21, bg="white")
puntaje_frame21.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame21, text="2", variable=opcion21, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame21, text="1", variable=opcion21, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame21, text="0", variable=opcion21, value="0").pack(side=tk.LEFT)

opcion22 = tk.StringVar(value="0")
container22 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container22.pack(fill="x")
tk.Label(container22, text="Se realizó una reunión post operacional a fin de intercambiar las observaciones encontradas.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame22 = tk.Frame(container22, bg="white")
puntaje_frame22.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame22, text="2", variable=opcion22, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame22, text="1", variable=opcion22, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame22, text="0", variable=opcion22, value="0").pack(side=tk.LEFT)

headers_d = tk.Frame(form_frame, bg="#BFBFBF")
headers_d.pack(fill="x")
tk.Label(headers_d, text="Responsable del Ejercicio", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(headers_d, text="Puntaje", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

opcion23 = tk.StringVar(value="0")
container23 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container23.pack(fill="x")
tk.Label(container23, text="Asumió su función de líder durante la ejecución del ejercicio.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame23 = tk.Frame(container23, bg="white")
puntaje_frame23.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame23, text="2", variable=opcion23, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame23, text="1", variable=opcion23, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame23, text="0", variable=opcion23, value="0").pack(side=tk.LEFT)

opcion24 = tk.StringVar(value="0")
container24 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container24.pack(fill="x")
tk.Label(container24, text="Impartió instrucciones claras y concretas a los participantes.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame24 = tk.Frame(container24, bg="white")
puntaje_frame24.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame24, text="2", variable=opcion24, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame24, text="1", variable=opcion24, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame24, text="0", variable=opcion24, value="0").pack(side=tk.LEFT)

headers_e = tk.Frame(form_frame, bg="#BFBFBF")
headers_e.pack(fill="x")
tk.Label(headers_e, text="Brigadas", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(headers_e, text="Puntaje", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

opcion25 = tk.StringVar(value="0")
container25 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container25.pack(fill="x")
tk.Label(container25, text="Realizaron sus funciones acorde a lo establecido.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame25 = tk.Frame(container25, bg="white")
puntaje_frame25.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame25, text="2", variable=opcion25, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame25, text="1", variable=opcion25, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame25, text="0", variable=opcion25, value="0").pack(side=tk.LEFT)

opcion26 = tk.StringVar(value="0")
container26 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container26.pack(fill="x")
tk.Label(container26, text="Cuentan con un sistema de identificación.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame26 = tk.Frame(container26, bg="white")
puntaje_frame26.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame26, text="2", variable=opcion26, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame26, text="1", variable=opcion26, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame26, text="0", variable=opcion26, value="0").pack(side=tk.LEFT)

headers_f = tk.Frame(form_frame, bg="#BFBFBF")
headers_f.pack(fill="x")
tk.Label(headers_f, text="Actores Educativos (Aplica solo para docentes)", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)
tk.Label(headers_f, text="Puntaje", bg="#BFBFBF", relief="solid", borderwidth=0.5).pack(side=tk.LEFT, fill="x", expand=True)

opcion27 = tk.StringVar(value="0")
container27 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container27.pack(fill="x")
tk.Label(container27, text="Realizaron actividades lúdicas en el punto de encuentro o zona segura.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame27 = tk.Frame(container27, bg="white")
puntaje_frame27.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame27, text="2", variable=opcion27, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame27, text="1", variable=opcion27, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame27, text="0", variable=opcion27, value="0").pack(side=tk.LEFT)

opcion28 = tk.StringVar(value="0")
container28 = tk.Frame(form_frame, relief="solid", borderwidth=1, bg="white")
container28.pack(fill="x")
tk.Label(container28, text="Se encontraron presentes con sus estudiantes a cargo todo el tiempo.", bg="white").pack(side=tk.LEFT, fill="x", expand=True)
puntaje_frame28 = tk.Frame(container28, bg="white")
puntaje_frame28.pack(side=tk.LEFT, fill="x", expand=True)
ttk.Radiobutton(puntaje_frame28, text="2", variable=opcion28, value="2").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame28, text="1", variable=opcion28, value="1").pack(side=tk.LEFT)
ttk.Radiobutton(puntaje_frame28, text="0", variable=opcion28, value="0").pack(side=tk.LEFT)

# Resumen de Valoración y Calificación
resumen_frame = tk.Frame(form_frame, relief="solid", bg="#58595B")
resumen_frame.pack(fill="x", pady=(10,0))
tk.Label(resumen_frame, text="Resumen de Valoración y Calificación", bg="#58595B", fg="white").pack(fill="x")

valores_a = tk.Frame(form_frame, bg="#BFBFBF")
valores_a.pack(fill="x")
tk.Label(valores_a, text="Valoración (A)", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
valor_a_label = tk.Label(valores_a, text="0", bg="white", relief="solid", width=15)
valor_a_label.pack(side=tk.LEFT)
tk.Label(valores_a, text="Calificación (A)", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
calificacion_a_label = tk.Label(valores_a, text="0", bg="white", relief="solid", width=15)
calificacion_a_label.pack(side=tk.LEFT)

valores_b = tk.Frame(form_frame, bg="#BFBFBF")
valores_b.pack(fill="x")
tk.Label(valores_b, text="Valoración (B)", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
valor_b_label = tk.Label(valores_b, text="0", bg="white", relief="solid", width=15)
valor_b_label.pack(side=tk.LEFT)
tk.Label(valores_b, text="Calificación (B)", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
calificacion_b_label = tk.Label(valores_b, text="0", bg="white", relief="solid", width=15)
calificacion_b_label.pack(side=tk.LEFT)

valores_c = tk.Frame(form_frame, bg="#BFBFBF")
valores_c.pack(fill="x")
tk.Label(valores_c, text="Valoración (C)", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
valor_c_label = tk.Label(valores_c, text="0", bg="white", relief="solid", width=15)
valor_c_label.pack(side=tk.LEFT)
tk.Label(valores_c, text="Calificación (C)", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
calificacion_c_label = tk.Label(valores_c, text="0", bg="white", relief="solid", width=15)
calificacion_c_label.pack(side=tk.LEFT)

totales = tk.Frame(form_frame, bg="#BFBFBF")
totales.pack(fill="x")
tk.Label(totales, text="Puntaje Total", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
puntaje_total_label = tk.Label(totales, text="0", bg="white", relief="solid", width=15)
puntaje_total_label.pack(side=tk.LEFT)
tk.Label(totales, text="Calificación Total", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
calificacion_total_label = tk.Label(totales, text="0", bg="white", relief="solid", width=15)
calificacion_total_label.pack(side=tk.LEFT)
tk.Label(totales, text="Clasificación", bg="#BFBFBF", width=30).pack(side=tk.LEFT)
clasificacion_label = tk.Label(totales, text="N/A", bg="white", relief="solid", width=15)
clasificacion_label.pack(side=tk.LEFT)

# Campo 5: Firma
firma_frame = tk.Frame(form_frame, relief="solid", bg="#58595B")
firma_frame.pack(fill="x", pady=(10,0))
tk.Label(firma_frame, text="Campo 5: Firma", bg="#58595B", fg="white").pack(side=tk.LEFT, padx=5)

observaciones_frame = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
observaciones_frame.pack(fill="x")
tk.Label(observaciones_frame, text="Observaciones del Evaluador", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
observaciones_text = tk.Text(observaciones_frame, bg="white", height=5)
observaciones_text.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)

firmas_frame = tk.Frame(form_frame, bg="#BFBFBF", relief="solid", borderwidth=1)
firmas_frame.pack(fill="x")
tk.Label(firmas_frame, text="Firma Máxima Autoridad", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
firma_maxima_entry = tk.Entry(firmas_frame, bg="white")
firma_maxima_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
tk.Label(firmas_frame, text="Firma Evaluador", bg="#BFBFBF").pack(side=tk.LEFT, padx=5, pady=5)
firma_evaluador_entry = tk.Entry(firmas_frame, bg="white")
firma_evaluador_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)


# Botones
button_frame = tk.Frame(form_frame)
button_frame.pack(pady=20)
tk.Button(button_frame, text="Calcular", command=validar_y_calcular, bg="#58595B", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Guardar en Excel", command=guardar_excel, bg="#58595B", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Registrar", command=accion_opcion1_pestaña1, bg="#58595B", fg="white").pack(side=tk.LEFT, padx=10)

ventana.mainloop()