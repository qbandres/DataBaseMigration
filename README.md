# DataBaseMigration
Proyecto para exportar una excel o csv a postgres y Mysql

DataBaseMigration 🛠️📂

DataBaseMigration es una herramienta desarrollada en Python que permite la importación de datos desde archivos Excel y CSV a bases de datos PostgreSQL y MySQL. Facilita la conexión a bases de datos, la configuración de tipos de datos antes de la importación y la gestión de la estructura de tablas.

🚀 Características Principales
	•	✅ Conexión a bases de datos PostgreSQL y MySQL con validación previa.
	•	✅ Carga de archivos CSV o Excel con detección automática de columnas.
	•	✅ Configuración personalizada de columnas, permitiendo definir tipos de datos, claves primarias y restricciones NULL.
	•	✅ Visualización de detalles del archivo importado, como tamaño, cantidad de registros y columnas.
	•	✅ Importación de datos a la base de datos, generando la estructura de la tabla automáticamente.


DataBaseMigration/
│── main.py          # Punto de entrada de la aplicación
│── tabs/            # Carpeta con los módulos principales
│   ├── connection.py   # Módulo para la conexión a la base de datos
│   ├── import_data.py  # Módulo para la importación de datos
│── requirements.txt # Dependencias del proyecto
│── README.md        # Documentación del proyecto

⚙️ Requisitos
	•	Python 3.8+
	•	Dependencias (instalar con pip install -r requirements.txt):

		altgraph==0.17.4
		et_xmlfile==2.0.0
		macholib==1.16.3
		modulegraph==0.19.6
		mysql-connector-python==9.2.0
		numpy==2.2.2
		openpyxl==3.1.5
		packaging==24.2
		pandas==2.2.3
		psycopg2-binary==2.9.10
		pyinstaller==6.11.1
		pyinstaller-hooks-contrib==2025.0
		python-dateutil==2.9.0.post0
		pytz==2024.2
		setuptools==75.8.0
		six==1.17.0
		SQLAlchemy==2.0.37
		typing_extensions==4.12.2
		tzdata==2025.1

🗄️ Conexión a la Base de Datos
	1.	Definir los datos de conexión (host, puerto, usuario, contraseña y nombre de la base de datos).
	2.	Seleccionar el tipo de base de datos (PostgreSQL o MySQL).
	3.	Probar la conexión antes de continuar.

📊 Importación de Datos
	1.	Seleccionar un archivo CSV o Excel.
	2.	Configurar los tipos de datos para cada columna antes de la importación.
	3.	Definir si una columna será PRIMARY KEY o permitirá valores NULL.
	4.	Ingresar un nombre para la tabla en la base de datos.
	5.	Importar los datos.

🛠 Futuras Mejoras
	•	Exportación de datos desde la base de datos a archivos CSV/Excel.
	•	Soporte para más tipos de bases de datos.
	•	Mejor manejo de errores y logs.

Para pyinstaller usar
pyinstaller --onefile --windowed --icon=icon.icns --name=DataBaseMigration main.py

📄 Licencia

Este proyecto está bajo la licencia MIT.