import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# Declaración global para almacenar la configuración de columnas
column_config = {}



def create_tab(tab_control, db_credentials):
    """Crea la pestaña de importación de datos."""
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Importar Datos')

    df = None  # DataFrame global para almacenar los datos
    table_name_entry = None  # Campo para nombre de tabla

    # Widgets
    ttk.Label(tab, text="Archivo Excel/CSV:").grid(row=0, column=0, padx=10, pady=5)
    file_entry = ttk.Entry(tab, width=50)
    file_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

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
                messagebox.showinfo("Éxito", f"Archivo cargado correctamente.\nTamaño: {size_mb:.2f} MB\nRegistros: {len(df)}")
                configure_columns()
            except Exception as e:
                messagebox.showerror("Error", f"Falló la carga del archivo: {e}")

    browse_button = ttk.Button(tab, text="📂 Examinar", command=browse_file)
    browse_button.grid(row=0, column=3, padx=5, pady=5)

    # Tabla para configurar columnas
    columns_frame = ttk.LabelFrame(tab, text="Configuración de Columnas")
    columns_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    # Inicializar variables globales al inicio del script o del método donde corresponda
    table_name_entry = None
    reset_button = None

    def configure_columns():
        """Configura los tipos de datos para las columnas."""
        nonlocal table_name_entry, reset_button

        # Limpiar cualquier configuración previa en el marco
        for widget in columns_frame.winfo_children():
            widget.destroy()

        if df is None:
            messagebox.showerror("Error", "No se ha cargado ningún archivo.")
            return

        ttk.Label(columns_frame, text="Columna").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(columns_frame, text="Tipo de Dato").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(columns_frame, text="Primary Key").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(columns_frame, text="Permitir NULL").grid(row=0, column=3, padx=5, pady=5)

        config_widgets = []  # Lista para almacenar los widgets configurables

        for i, column in enumerate(df.columns):
            if column not in column_config:
                column_config[column] = {
                    "type": tk.StringVar(value="VARCHAR"),  # Valor por defecto
                    "primary_key": tk.BooleanVar(value=False),
                    "nullable": tk.BooleanVar(value=True),
                }

            # Etiqueta para el nombre de la columna
            ttk.Label(columns_frame, text=column).grid(row=i + 1, column=0, padx=5, pady=5)

            # Selector de tipo de dato
            type_menu = ttk.Combobox(columns_frame, textvariable=column_config[column]["type"], values=[
                "INT", "VARCHAR", "DATE", "TIMESTAMP", "FLOAT", "BOOLEAN", "TEXT"], state="readonly")
            type_menu.grid(row=i + 1, column=1, padx=5, pady=5)
            config_widgets.append(type_menu)

            # Checkbutton para Primary Key
            pk_check = ttk.Checkbutton(columns_frame, variable=column_config[column]["primary_key"])
            pk_check.grid(row=i + 1, column=2, padx=5, pady=5)
            config_widgets.append(pk_check)

            # Checkbutton para Permitir NULL
            null_check = ttk.Checkbutton(columns_frame, variable=column_config[column]["nullable"])
            null_check.grid(row=i + 1, column=3, padx=5, pady=5)
            config_widgets.append(null_check)

        ttk.Label(tab, text="Nombre de la Tabla:").grid(row=2, column=0, padx=10, pady=5)
        table_name_entry = ttk.Entry(tab, width=30)
        table_name_entry.grid(row=2, column=1, padx=5, pady=5)

        def lock_widgets():
            """Bloquea los selectores para indicar que ya están configurados."""
            for widget in config_widgets:
                widget.configure(state="disabled")  # Bloquea los widgets
            reset_button.grid(row=4, column=0, columnspan=4, pady=10)  # Muestra el botón de restablecer
            messagebox.showinfo("Configuración", "La configuración de columnas ha sido bloqueada.")

        def reset_configuration():
            """Restablece los selectores para permitir modificaciones."""
            for widget in config_widgets:
                widget.configure(state="normal")  # Desbloquea los widgets
            reset_button.grid_remove()  # Oculta el botón de restablecer
            messagebox.showinfo("Configuración", "La configuración de columnas ha sido restablecida.")

        # Botón para bloquear los selectores
        lock_button = ttk.Button(tab, text="Configurar Columnas", command=lock_widgets)
        lock_button.grid(row=3, column=1, padx=5, pady=5)

        # Botón para restablecer configuración (inicialmente oculto)
        reset_button = ttk.Button(tab, text="Restablecer Configuración", command=reset_configuration)
        reset_button.grid(row=4, column=0, columnspan=4, pady=10)
        reset_button.grid_remove()

        def import_data():
            """Importa los datos a la base de datos con la configuración definida."""
            if df is None:
                messagebox.showerror("Error", "No se ha cargado ningún archivo.")
                return

            table_name = table_name_entry.get()
            if not table_name:
                messagebox.showerror("Error", "Debe proporcionar un nombre para la tabla.")
                return

            user = db_credentials.get("user", "")
            password = db_credentials.get("password", "")
            host = db_credentials.get("host", "")
            port = db_credentials.get("port", "")
            database = db_credentials.get("database", "")

            if not all([user, password, host, port, database]):
                messagebox.showerror("Error", "Faltan datos de conexión a la base de datos.")
                return

            try:
                # Convertir columnas con tipo DATE
                for column, config in column_config.items():
                    if config["type"].get() == "DATE":
                        df[column] = pd.to_datetime(df[column]).dt.date  # Convertir a solo fecha

                # Crear tabla
                columns = [f"{column} {config['type'].get()} {'PRIMARY KEY' if config['primary_key'].get() else ''} {'NOT NULL' if not config['nullable'].get() else ''}"
                        for column, config in column_config.items()]
                create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
                engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
                with engine.connect() as conn:
                    conn.execute(text(create_table_query))
                df.to_sql(table_name, engine, if_exists='append', index=False)
                messagebox.showinfo("Éxito", f"Datos importados correctamente a la tabla '{table_name}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Falló la importación: {e}")

        import_button = ttk.Button(tab, text="Importar Datos", command=import_data)
        import_button.grid(row=3, column=2, padx=5, pady=5)