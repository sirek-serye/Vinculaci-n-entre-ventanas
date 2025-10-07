import tkinter as tk
from tkinter import messagebox
import os
import subprocess
def validate_login():
    filename = "bdUsuariosClaves.txt"
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Error de Archivo", f"No se pudo encontrar el archivo '{filename}'.")
        return
    entered_username = entry_username.get()
    entered_password = entry_password.get()
    user_found = False
    for line in lines:
        credentials = line.strip().split(',')
        if len(credentials) == 2:
            stored_username, stored_password = credentials
            if stored_username == entered_username and stored_password == entered_password:
                user_found = True
                break  # Si se encuentra, se detiene la búsqueda.
    if user_found:
        messagebox.showinfo("Login Exitoso", f"¡Bienvenido, {entered_username}!")
        login_window.destroy()  # Cierra la ventana de login
        os.system('python "Vincualcion entre ventanas 2.py"')
    else:
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")
def accion_opcion1_pestaña1():
    try:
        subprocess.run(["python","Vincualcion entre ventanas 2.py"])
    except FileNotFoundError:
        messagebox.showerror("!!CUIDADO!!","No se encuentra el arhivo")

login_window = tk.Tk()
login_window.title("Inicio de Sesión")
login_window.geometry("350x220")
login_window.resizable(False, False)
# --- Creación de los Widgets ---
main_label = tk.Label(login_window, text="Por favor, inicie sesión", font=("Arial", 14))
main_label.pack(pady=15)

label_username = tk.Label(login_window, text="Usuario:")
label_username.pack()
entry_username = tk.Entry(login_window, width=30)
entry_username.pack(pady=5)

label_password = tk.Label(login_window, text="Contraseña:")
label_password.pack()
entry_password = tk.Entry(login_window, width=30, show="*")
entry_password.pack(pady=5)

login_button = tk.Button(login_window, text="Ingresar", command=validate_login)
login_button.pack(pady=20)

login_window.mainloop()