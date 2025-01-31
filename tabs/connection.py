import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine  # Importar create_engine para conexiones a la BD
import logging

# Configuración de logging que NO guarda en un archivo
logging.basicConfig(
    level=logging.INFO,  # Sigue permitiendo mostrar mensajes en la interfaz
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_tab(tab_control, db_credentials, update_connection_status):
    """Crea la pestaña de conexión a la base de datos."""
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Conexión')

    ttk.Label(tab, text="Tipo de Base de Datos:").grid(row=0, column=0, padx=10, pady=5)
    db_type = tk.StringVar(value="postgres")
    db_credentials["db_type"] = db_type  # Guardar en las credenciales

    postgres_radio = ttk.Radiobutton(tab, text="PostgreSQL", variable=db_type, value="postgres", command=lambda: update_port())
    mysql_radio = ttk.Radiobutton(tab, text="MySQL", variable=db_type, value="mysql", command=lambda: update_port())
    postgres_radio.grid(row=0, column=1, sticky="w")
    mysql_radio.grid(row=0, column=2, sticky="w")

    ttk.Label(tab, text="Host (Render URL):").grid(row=1, column=0, padx=10, pady=5)
    host_entry = ttk.Entry(tab, width=40)
    host_entry.grid(row=1, column=1, columnspan=2)
    host_entry.insert(0, "localhost")  # Valor por defecto

    ttk.Label(tab, text="Puerto:").grid(row=2, column=0, padx=10, pady=5)
    port_entry = ttk.Entry(tab, width=30)
    port_entry.grid(row=2, column=1)
    port_entry.insert(0, "5432")

    ttk.Label(tab, text="Usuario:").grid(row=3, column=0, padx=10, pady=5)
    user_entry = ttk.Entry(tab, width=30)
    user_entry.grid(row=3, column=1)
    user_entry.insert(0, "postgres")

    ttk.Label(tab, text="Contraseña:").grid(row=4, column=0, padx=10, pady=5)
    password_entry = ttk.Entry(tab, width=30, show="*")
    password_entry.grid(row=4, column=1)

    ttk.Label(tab, text="Base de Datos:").grid(row=5, column=0, padx=10, pady=5)
    db_entry = ttk.Entry(tab, width=30)
    db_entry.grid(row=5, column=1)

    # Etiqueta para mostrar mensajes informativos
    info_label = ttk.Label(tab, text="", foreground="green", wraplength=400, justify="left")
    info_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="w")

    #Aqui actualizamos los valores del puerto y tambien aprobechamos para lel username
    def update_port():
        """Actualiza el puerto y el usuario según el tipo de base de datos seleccionado."""
        port_entry.delete(0, tk.END)
        user_entry.delete(0, tk.END)

        if db_type.get() == "mysql":
            port_entry.insert(0, "3306")
            user_entry.insert(0, "root")  # Usuario por defecto en MySQL
        else:
            port_entry.insert(0, "5432")
            user_entry.insert(0, "postgres")  # Usuario por defecto en PostgreSQL

    def display_message(message, level="info"):
        """Muestra mensajes en la etiqueta informativa y los registra en el archivo de logs."""
        info_label.config(text=message)
        if level == "info":
            logging.info(message)
        elif level == "error":
            logging.error(message)

    def test_connection():
        """Prueba la conexión a la base de datos y actualiza db_credentials."""
        host = host_entry.get()
        port = port_entry.get()
        user = user_entry.get()
        password = password_entry.get()
        database = db_entry.get()

        # Validar campos obligatorios
        if not host:
            display_message("Fallo de conexión: El campo 'Host' no puede estar vacío.", level="error")
            return
        if not port:
            display_message("Fallo de conexión: El campo 'Puerto' no puede estar vacío.", level="error")
            return
        if not user:
            display_message("Fallo de conexión: El campo 'Usuario' no puede estar vacío.", level="error")
            return
        if not password:
            display_message("Fallo de conexión: El campo 'Contraseña' no puede estar vacío.", level="error")
            return
        if not database:
            display_message("Fallo de conexión: El campo 'Base de Datos' no puede estar vacío.", level="error")
            return

        try:
            port = int(port)  # Asegurarse de que el puerto sea un entero

            # Crear la conexión según el tipo de base de datos
            if db_type.get() == "postgres":
                engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
            elif db_type.get() == "mysql":
                engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

            # Probar conexión
            conn = engine.connect()
            conn.close()

            # Actualizar db_credentials
            db_credentials["host"] = host
            db_credentials["port"] = port
            db_credentials["user"] = user
            db_credentials["password"] = password
            db_credentials["database"] = database
            db_credentials["connected"] = True  # Marcar como conectado

            # Actualizar el estado de la conexión en el cuadro informativo
            update_connection_status()

            display_message(f"Conexión exitosa a {db_type.get()} - Host: {host}, Base de Datos: {database}", level="info")
        except Exception as e:
            db_credentials["connected"] = False  # Marcar como desconectado
            update_connection_status()
            display_message(f"Fallo de conexión: {str(e)}", level="error")

    connect_button = ttk.Button(tab, text="Probar Conexión", command=test_connection)
    connect_button.grid(row=6, column=1, pady=10)