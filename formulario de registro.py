import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess

ventana = tk.Tk()
ventana.title("Registro de Usuario")
ventana.geometry("320x550")

def iniciar_progreso():
    if barra_progreso["value"] < 100:
        barra_progreso["value"] += 33

def boton_1():
    # Ventana emergente para usuario y contraseña
    def guardar_credenciales():
        usuario = e_usuario.get().strip()
        clave = e_clave.get().strip()

        if not usuario or not clave:
            messagebox.showerror("Error", "Debes ingresar usuario y contraseña.")
            return

        # Guardar en bdUsuariosClaves.txt (ya existente)
        cred_path = "bdUsuariosClaves.txt"  # usa el archivo que ya tienes
        with open(cred_path, "a", encoding="utf-8") as f:
            f.write(f"{usuario},{clave}\n")

        # Guardar datos del formulario
        nombre = e_nombre.get()
        genero = opcion.get()
        estado_civil = opcion2.get()
        estado_laboral = opcion3.get()

        datos = (
            f"Usuario: {usuario}\n"
            f"Nombre: {nombre}\n"
            f"Género: {genero}\n"
            f"Estado Civil: {estado_civil}\n"
            f"Estado Laboral: {estado_laboral}\n"
            + "-"*40 + "\n"
        )

        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        txt_path = os.path.join(downloads_path, "Resultados_evaluacion.txt")
        with open(txt_path, "a", encoding="utf-8") as file:
            file.write(datos)

        messagebox.showinfo("Éxito", "El usuario fue registrado correctamente.")

        ventana_cred.destroy()

        # Abrir los archivos
        subprocess.Popen(['notepad', cred_path])
        subprocess.Popen(['notepad', txt_path])

    ventana_cred = tk.Toplevel(ventana)
    ventana_cred.title("Crear credenciales")
    ventana_cred.geometry("300x200")

    tk.Label(ventana_cred, text="Nuevo Usuario:").pack(pady=5)
    e_usuario = ttk.Entry(ventana_cred)
    e_usuario.pack(pady=5)

    tk.Label(ventana_cred, text="Nueva Contraseña:").pack(pady=5)
    e_clave = ttk.Entry(ventana_cred, show="*")
    e_clave.pack(pady=5)

    ttk.Button(ventana_cred, text="Guardar", command=guardar_credenciales).pack(pady=15)


# Nombre
f_nombre = tk.Frame(ventana, relief="solid")
f_nombre.pack()

tk.Label(f_nombre, text="Nombre:").pack(side=tk.LEFT)
e_nombre = ttk.Entry(f_nombre)
e_nombre.pack(side=tk.RIGHT)

ttk.Separator(ventana, orient="horizontal").pack(fill="x", pady=5)

# Género
f_genero = tk.Frame(ventana)
f_genero.pack()
tk.Label(f_genero, text="Género: ").pack(side=tk.LEFT)

opcion = tk.StringVar()
opcion.set("Opcion")

f_generos = ttk.Frame(f_genero, relief="solid")
f_generos.pack(padx=5, pady=5, side=tk.RIGHT)

ttk.Radiobutton(f_generos, text="Hombre", variable=opcion, value="Hombre", command=iniciar_progreso).pack(anchor="w")
ttk.Radiobutton(f_generos, text="Mujer", variable=opcion, value="Mujer", command=iniciar_progreso).pack(anchor="w")
ttk.Radiobutton(f_generos, text="Otros", variable=opcion, value="Otro", command=iniciar_progreso).pack(anchor="w")

ttk.Separator(ventana, orient="horizontal").pack(fill="x", pady=5)

# Estado civil
f_civil = tk.Frame(ventana)
f_civil.pack()
tk.Label(f_civil, text="Estado civil: ").pack(side=tk.LEFT)

opcion2 = tk.StringVar()
opcion2.set("Opcion")

f_civils = ttk.Frame(f_civil, relief="solid")
f_civils.pack(padx=5, pady=5, side=tk.RIGHT)

ttk.Radiobutton(f_civils, text="Soltero", variable=opcion2, value="Soltero", command=iniciar_progreso).pack(anchor="w")
ttk.Radiobutton(f_civils, text="Casado", variable=opcion2, value="Casado", command=iniciar_progreso).pack(anchor="w")
ttk.Radiobutton(f_civils, text="Divorciado", variable=opcion2, value="Divorciado", command=iniciar_progreso).pack(anchor="w")
ttk.Radiobutton(f_civils, text="Unión Libre", variable=opcion2, value="Unión libre", command=iniciar_progreso).pack(anchor="w")

ttk.Separator(ventana, orient="horizontal").pack(fill="x", pady=5)

# Estado laboral
f_laboral = tk.Frame(ventana)
f_laboral.pack()
tk.Label(f_laboral, text="Estado laboral: ").pack(side=tk.LEFT)

opcion3 = tk.StringVar()
opcion3.set("Opcion")

f_laborals = ttk.Frame(f_laboral, relief="solid")
f_laborals.pack(padx=5, pady=5, side=tk.RIGHT)

ttk.Radiobutton(f_laborals, text="Empleado", variable=opcion3, value="Empleado", command=iniciar_progreso).pack(anchor="w")
ttk.Radiobutton(f_laborals, text="Desempleado", variable=opcion3, value="Desempleado", command=iniciar_progreso).pack(anchor="w")

ttk.Separator(ventana, orient="horizontal").pack(fill="x", pady=5)

# Barra de progreso
barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=300, mode="determinate")
barra_progreso.pack()

ttk.Separator(ventana, orient="horizontal").pack(fill="x", pady=5)

# Botón registrar
boton = ttk.Button(ventana, text="Registrar", command=boton_1)
boton.pack()

ventana.mainloop()
