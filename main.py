import tkinter as tk
from tkinter import ttk
from tabs import connection, import_data  # Asegúrate de importar correctamente

def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Herramienta de Migración de Base de Datos")

    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")

    # Diccionario para almacenar las credenciales
    db_credentials = {
        "user": "",
        "password": "",
        "host": "",
        "port": "",
        "database": ""
    }

    # Crear pestañas
    connection.create_tab(tab_control, db_credentials)  # Pestaña de conexión
    import_data.create_tab(tab_control, db_credentials)  # Pestaña de importación

    root.mainloop()

if __name__ == "__main__":
    main()