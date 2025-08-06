from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# CALLBACK PARA FLASK-LOGIN
# ============================================================
@login_manager.user_loader
def load_user(user_id):
    """
    Cargar un usuario desde la base de datos dado su ID.
    Flask-Login utiliza esta función para mantener la sesión del usuario.
    """
    return User.query.get(int(user_id))


# ============================================================
# MODELO: USER (USUARIO)
# ============================================================
class User(UserMixin, db.Model):
    """
    Representa a un usuario registrado en el sistema.
    """
    __tablename__ = 'users'

    # -------------------------
    # CAMPOS DE LA TABLA
    # -------------------------
    id = db.Column(db.Integer, primary_key=True)  # ID único del usuario (PK)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)  # Email único para login
    password_hash = db.Column(db.String(256))  # Contraseña en formato hash seguro (no texto plano)

    # -------------------------
    # RELACIONES
    # -------------------------
    tasks = db.relationship('Task', backref='author', lazy='dynamic')  
    # Un usuario puede tener múltiples tareas (relación 1 a N)

    # -------------------------
    # MÉTODOS DE LA CLASE
    # -------------------------
    def set_password(self, password):
        """Genera y almacena un hash seguro para la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña ingresada coincide con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Representación del usuario (útil para depuración)."""
        return f'<User {self.email}>'


# ============================================================
# MODELO: TASK (TAREA)
# ============================================================
class Task(db.Model):
    """
    Representa una tarea creada por un usuario.
    Puede estar asociada opcionalmente a un personaje de Rick and Morty.
    """
    __tablename__ = 'tasks'

    # -------------------------
    # CAMPOS DE LA TABLA
    # -------------------------
    id = db.Column(db.Integer, primary_key=True)  # ID único de la tarea (PK)
    title = db.Column(db.String(100), nullable=False)  # Título obligatorio de la tarea
    description = db.Column(db.Text)  # Descripción opcional
    due_date = db.Column(db.Date)  # Fecha de vencimiento (puede ser nula)
    status = db.Column(db.String(20), default='Pendiente')  # Estado: Pendiente / En progreso / Completada
    character_id = db.Column(db.Integer, nullable=True)  # ID del personaje (Rick & Morty API)

    # -------------------------
    # RELACIONES
    # -------------------------
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    # FK hacia la tabla de usuarios (cada tarea pertenece a un usuario)

    # -------------------------
    # MÉTODOS DE LA CLASE
    # -------------------------
    def __repr__(self):
        """Representación de la tarea (útil para depuración)."""
        return f'<Task {self.title}>'
