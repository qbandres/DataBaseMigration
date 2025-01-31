import tkinter as tk
from tkinter import ttk
from tabs import connection, import_data  # Asegúrate de importar correctamente

def main():
    root = tk.Tk()
    root.geometry("900x600")
    root.title("Herramienta de Migración de Base de Datos")

    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")

    # Diccionario para almacenar las credenciales
    db_credentials = {
        "user": "",
        "password": "",
        "host": "",
        "port": "",
        "database": "",
        "connected": False  # Estado de la conexión
    }

    # Frame para el estado de la conexión y detalles del archivo
    status_frame = ttk.LabelFrame(root, text="Estado y Detalles")
    status_frame.pack(fill="x", padx=10, pady=10)

    # Variables para mostrar en el cuadro informativo
    connection_status = tk.StringVar(value="Desconectado")
    host_var = tk.StringVar(value="Host: -")
    port_var = tk.StringVar(value="Puerto: -")
    user_var = tk.StringVar(value="Usuario: -")
    db_var = tk.StringVar(value="Base de Datos: -")
    file_size_var = tk.StringVar(value="Tamaño del Archivo: -")
    file_records_var = tk.StringVar(value="Registros: -")
    file_columns_var = tk.StringVar(value="Columnas: -")

    # Labels para mostrar la información
    ttk.Label(status_frame, textvariable=connection_status, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=2, sticky="w")
    ttk.Label(status_frame, textvariable=host_var).grid(row=1, column=0, padx=5, pady=2, sticky="w")
    ttk.Label(status_frame, textvariable=port_var).grid(row=2, column=0, padx=5, pady=2, sticky="w")
    ttk.Label(status_frame, textvariable=user_var).grid(row=3, column=0, padx=5, pady=2, sticky="w")
    ttk.Label(status_frame, textvariable=db_var).grid(row=4, column=0, padx=5, pady=2, sticky="w")
    ttk.Label(status_frame, textvariable=file_size_var).grid(row=0, column=1, padx=5, pady=2, sticky="w")
    ttk.Label(status_frame, textvariable=file_records_var).grid(row=1, column=1, padx=5, pady=2, sticky="w")
    ttk.Label(status_frame, textvariable=file_columns_var).grid(row=2, column=1, padx=5, pady=2, sticky="w")

    # Función para actualizar el estado de la conexión
    def update_connection_status():
        if db_credentials["connected"]:
            connection_status.set("Conectado")
            host_var.set(f"Host: {db_credentials['host']}")
            port_var.set(f"Puerto: {db_credentials['port']}")
            user_var.set(f"Usuario: {db_credentials['user']}")
            db_var.set(f"Base de Datos: {db_credentials['database']}")
            # Activar pestaña de Importar Datos
            tab_control.tab(1, state="normal")


        else:
            connection_status.set("Desconectado")
            host_var.set("Host: -")
            port_var.set("Puerto: -")
            user_var.set("Usuario: -")
            db_var.set("Base de Datos: -")
            # Desactivar pestaña de Importar Datos
            tab_control.tab(1, state="disabled")

    # Función para actualizar los detalles del archivo
    def update_file_info(size_mb, records, columns):
        file_size_var.set(f"Tamaño del Archivo: {size_mb:.2f} MB")
        file_records_var.set(f"Registros: {records}")
        file_columns_var.set(f"Columnas: {columns}")

    # Crear pestañas y pasar las funciones de actualización
    connection.create_tab(tab_control, db_credentials, update_connection_status)
    import_data.create_tab(tab_control, db_credentials, update_file_info)

    # Desactivar pestaña de importar datos al inicio
    tab_control.tab(1, state="disabled")

    root.mainloop()

if __name__ == "__main__":
    main()