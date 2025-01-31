import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import os
import logging
from sqlalchemy import create_engine, types
from sqlalchemy.sql import text

# Configuración del logging
# Configuración de logging que NO guarda en un archivo
logging.basicConfig(
    level=logging.INFO,  # Sigue permitiendo mostrar mensajes en la interfaz
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Declaración global para almacenar la configuración de columnas
column_config = {}

def create_tab(tab_control, db_credentials, update_file_info):
    """Crea la pestaña de importación de datos."""
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Importar Datos')

    df = None  # DataFrame global para almacenar los datos
    table_name_entry = None  # Campo para nombre de tabla

    # Widgets
    ttk.Label(tab, text="Archivo Excel/CSV:").grid(row=0, column=0, padx=10, pady=5)
    file_entry = ttk.Entry(tab, width=50)
    file_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

    # Estado de importación
    status_label = ttk.Label(tab, text="Estado: Esperando archivo...", foreground="black")
    status_label.grid(row=0, column=4, padx=10, pady=5)

    # Label para mostrar interacciones del usuario
    interaction_label = ttk.Label(tab, text="", foreground="green")
    interaction_label.grid(row=5, column=0, columnspan=5, padx=10, pady=5)

    def exit_program():
        """Cierra la aplicación"""
        logging.info("Aplicación cerrada por el usuario")
        tab_control.winfo_toplevel().destroy()

    def browse_file():
        """Selecciona y carga un archivo Excel o CSV."""
        nonlocal df
        file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xls"), ("Archivos CSV", "*.csv")])
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)
            try:
                if file_path.endswith(".csv"):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)

                # Mostrar mensaje de éxito
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                records = len(df)
                columns = len(df.columns)

                # Actualizar los detalles del archivo en el cuadro informativo
                update_file_info(size_mb, records, columns)

                status_label.config(text="Archivo cargado correctamente", foreground="green")
                interaction_label.config(text=f"Archivo cargado: {os.path.basename(file_path)}", foreground="green")

                logging.info(f"Archivo cargado: {file_path}, Tamaño: {size_mb:.2f} MB, Registros: {records}, Columnas: {columns}")
                configure_columns()
            except Exception as e:
                status_label.config(text="Error al cargar archivo", foreground="red")
                interaction_label.config(text=f"Error: {str(e)}", foreground="red")
                logging.error(f"Error al cargar archivo: {str(e)}")

    browse_button = ttk.Button(tab, text="📂 Examinar", command=browse_file)
    browse_button.grid(row=0, column=3, padx=5, pady=5)

    # Marco principal con Scrollbar
    columns_frame = ttk.LabelFrame(tab, text="Configuración de Columnas")
    columns_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    canvas = tk.Canvas(columns_frame)
    scrollbar = ttk.Scrollbar(columns_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    table_name_entry = None
    reset_button = None
    confirm_button = None

    def configure_columns():
        """Configura los tipos de datos para las columnas."""
        nonlocal table_name_entry, reset_button, confirm_button

        # Limpiar cualquier configuración previa en el marco
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if df is None:
            status_label.config(text="No se ha cargado ningún archivo", foreground="red")
            interaction_label.config(text="Error: No hay archivo cargado", foreground="red")
            return

        ttk.Label(scrollable_frame, text="Columna").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(scrollable_frame, text="Tipo de Dato").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(scrollable_frame, text="Primary Key").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(scrollable_frame, text="Permitir NULL").grid(row=0, column=3, padx=5, pady=5)

        config_widgets = []

        for i, column in enumerate(df.columns):
            if column not in column_config:
                column_config[column] = {
                    "type": tk.StringVar(value="VARCHAR"),
                    "primary_key": tk.BooleanVar(value=False),
                    "nullable": tk.BooleanVar(value=True),
                }

            ttk.Label(scrollable_frame, text=column).grid(row=i + 1, column=0, padx=5, pady=5)

            type_menu = ttk.Combobox(scrollable_frame, textvariable=column_config[column]["type"], values=[
                "INT", "VARCHAR", "DATE", "TIMESTAMP", "FLOAT", "BOOLEAN", "TEXT"], state="readonly")
            type_menu.grid(row=i + 1, column=1, padx=5, pady=5)
            config_widgets.append(type_menu)

            pk_check = ttk.Checkbutton(scrollable_frame, variable=column_config[column]["primary_key"])
            pk_check.grid(row=i + 1, column=2, padx=5, pady=5)
            config_widgets.append(pk_check)

            null_check = ttk.Checkbutton(scrollable_frame, variable=column_config[column]["nullable"])
            null_check.grid(row=i + 1, column=3, padx=5, pady=5)
            config_widgets.append(null_check)

        ttk.Label(tab, text="Nombre de la Tabla:").grid(row=2, column=0, padx=10, pady=5)
        table_name_entry = ttk.Entry(tab, width=30)
        table_name_entry.grid(row=2, column=1, padx=5, pady=5)

        def lock_widgets():
            """Bloquea los selectores de columnas."""
            for widget in config_widgets:
                widget.configure(state="disabled")
            reset_button.grid()
            confirm_button.grid_remove()
            status_label.config(text="Columnas configuradas", foreground="blue")
            interaction_label.config(text="Configuración de columnas bloqueada", foreground="green")

        def reset_configuration():
            """Restablece la configuración de columnas."""
            for widget in config_widgets:
                widget.configure(state="normal")
            reset_button.grid_remove()
            confirm_button.grid()
            status_label.config(text="Configuración de columnas restablecida", foreground="black")
            interaction_label.config(text="Configuración de columnas restablecida", foreground="green")

        confirm_button = ttk.Button(tab, text="Confirmar Datos", command=lock_widgets)
        confirm_button.grid(row=3, column=1, padx=5, pady=5)

        reset_button = ttk.Button(tab, text="Restablecer Configuración", command=reset_configuration)
        reset_button.grid(row=4, column=0, columnspan=4, pady=10)
        reset_button.grid_remove()

    def import_data():
        """Importa los datos a la base de datos con la configuración definida."""
        if df is None:
            status_label.config(text="Error: No se ha cargado ningún archivo", foreground="red")
            interaction_label.config(text="Error: No hay archivo para importar", foreground="red")
            return

        table_name = table_name_entry.get()
        if not table_name:
            status_label.config(text="Error: Falta el nombre de la tabla", foreground="red")
            interaction_label.config(text="Error: Nombre de tabla no especificado", foreground="red")
            return

        user = db_credentials.get("user", "")
        password = db_credentials.get("password", "")
        host = db_credentials.get("host", "")
        port = db_credentials.get("port", "")
        database = db_credentials.get("database", "")

        if not all([user, password, host, port, database]):
            status_label.config(text="Error: Datos de conexión incompletos", foreground="red")
            interaction_label.config(text="Error: Credenciales de base de datos incompletas", foreground="red")
            return

        try:
            for column, config in column_config.items():
                if config["type"].get() == "DATE":
                    df[column] = pd.to_datetime(df[column]).dt.date
                elif config["type"].get() == "VARCHAR":
                    df[column] = df[column].astype(str)

            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
            df.to_sql(table_name, engine, if_exists='append', index=False)

            status_label.config(text="Importación exitosa", foreground="green")
            interaction_label.config(text=f"Datos importados exitosamente a la tabla '{table_name}'", foreground="green")
            logging.info(f"Datos importados correctamente a la tabla '{table_name}'.")

        except Exception as e:
            status_label.config(text="Error en importación", foreground="red")
            interaction_label.config(text=f"Error en importación: {str(e)}", foreground="red")
            logging.error(f"Error al importar datos: {str(e)}")

    # Botones de acción
    import_button = ttk.Button(tab, text="Importar Datos", command=import_data)
    import_button.grid(row=3, column=2, padx=5, pady=5)

    # Botón de salida
    exit_button = ttk.Button(tab, text="Salir", command=exit_program)
    exit_button.grid(row=3, column=3, padx=5, pady=5)