# 📝 Gestión de Tareas con Flask + Rick and Morty API

Este proyecto es una aplicación web Full Stack desarrollada con **Flask (Python)** que permite gestionar tareas personales con autenticación de usuarios.  
Además, integra la **Rick and Morty API** para asociar personajes a las tareas.

---

## 🚀 Funcionalidades

### 🔑 Autenticación de usuarios
- Registro de nuevos usuarios con email y contraseña.
- Inicio y cierre de sesión seguro (Flask-Login y hashing de contraseñas con Werkzeug).

### ✅ CRUD de Tareas
- Crear, editar y eliminar tareas personales.
- Cada tarea incluye:
  - **Título**
  - **Descripción**
  - **Fecha de vencimiento**
  - **Estado**: Pendiente / En progreso / Completada.

### 👾 Integración con Rick and Morty API
- Listado paginado de personajes de la API externa.
- Posibilidad de **asociar un personaje** a una tarea específica.
- Visualización del personaje asociado (imagen y nombre) dentro de la tarea.

### 🛡 Validaciones y Seguridad
- Validaciones en backend para campos requeridos.
- Manejo de sesiones con `Flask-Login`.
- Contraseñas encriptadas usando `generate_password_hash`.

---

## 🛠️ Tecnologías utilizadas

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python)
- **Base de Datos**: PostgreSQL (usando SQLAlchemy ORM)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Autenticación**: Flask-Login
- **Consumo de API**: `requests` (Rick and Morty API)
- **Gestor de dependencias**: pip / venv

---

## 📂 Estructura del proyecto
```bash
api_rick
├── app/
│ ├── init.py # Configuración principal de la app (Flask, DB, LoginManager)
│ ├── models.py # Modelos de la base de datos (User, Task)
│ ├── routes.py # Rutas (autenticación, tareas, API externa)
│ ├── templates/ # Archivos HTML (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── tasks.html
│   ├── create_task.html
│   ├── edit_task.html
│   └── characters.html
│ 
├── tasks.sql # Script de la base de datos (tablas + datos de prueba)
├── run.py # Punto de entrada de la aplicación
├── requirements.txt # Dependencias del proyecto
└── README.md # Documentación
```

   ### 🗄️ Base de datos
   
   El proyecto utiliza **PostgreSQL**.  
   Las tablas principales son:
   
   - `users`: Almacena los datos de los usuarios (email, contraseña encriptada).
   - `tasks`: Contiene las tareas de cada usuario, con su estado y fecha de vencimiento.
   - Relación: **1 usuario → muchas tareas**.
   - Cada tarea puede tener asociado el `id` de un personaje de la Rick and Morty API.
   
   Incluye el archivo `tasks.sql` con:
   - Creación de tablas.
   - Relaciones (`FK` de tareas a usuarios).
   - Datos de prueba.
   
   ---
   
   ## 🔧 Instalación y uso
   
   ### 1. Clonar el repositorio:
   ```bash
   git clone https://github.com/FernanDeHoyos/api_rick.git
   cd proyecto-tareas
```

### 2. Crear entorno virtual e instalar dependencias::
   ```bash
   python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno:
   ```bash
  export DATABASE_URL=postgresql://usuario:password@localhost:5432/tasks
export SECRET_KEY=una_clave_secreta_segura
```

### 4. Inicializar la base de datos:
   ```bash
  psql -U postgres -d tasks -f tasks.sql
```

### 5. IEjecutar la aplicacion:
   ```bash
  flask run
  o
  python run.py

  Abrir en el navegador: http://localhost:5000
```
### Usuario demo:

email: fernandehoyos93@gmail.com   
password: fernan135 
