import requests
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db
from app.models import User, Task

RICK_AND_MORTY_API_URL = "https://rickandmortyapi.com/api/character/"

# ============================================================
# CONTEXT PROCESSOR
# ============================================================
@app.context_processor
def inject_now():
    """
    Inyecta la variable 'year' con el año actual en todas las plantillas.
    """
    return {'year': datetime.now().year}


# ============================================================
# RUTA: LISTADO DE TAREAS
# ============================================================
@app.route('/')
@app.route('/tasks')
@login_required
def tasks():
    """
    Muestra todas las tareas del usuario autenticado.
    - Obtiene cada tarea del usuario actual.
    - Si hay un personaje asociado, consulta su información en la API de Rick and Morty.
    """
    tasks = current_user.tasks.all()
    tasks_with_characters = []

    for task in tasks:
        character_info = None
        if task.character_id:
            try:
                response = requests.get(f"{RICK_AND_MORTY_API_URL}{task.character_id}")
                response.raise_for_status()
                character_info = response.json()
            except requests.exceptions.RequestException:
                pass  # Si falla la API, solo mostramos la tarea sin personaje.

        tasks_with_characters.append({'task': task, 'character': character_info})

    return render_template('tasks.html', title='Mis Tareas', tasks_with_characters=tasks_with_characters)


# ============================================================
# RUTA: REGISTRO DE USUARIO
# ============================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Permite registrar un nuevo usuario.
    - Verifica si el email ya está registrado.
    - Crea el usuario con su contraseña encriptada.
    """
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar si el usuario ya existe
        user = User.query.filter_by(email=email).first()
        if user:
            flash('El email ya está registrado.', 'danger')
            return redirect(url_for('register'))

        # Crear nuevo usuario
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. ¡Inicia sesión!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registro')


# ============================================================
# RUTA: LOGIN DE USUARIO
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Permite iniciar sesión a un usuario registrado.
    - Verifica credenciales (email y contraseña).
    - Mantiene sesión activa con Flask-Login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validar usuario y contraseña
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Credenciales incorrectas.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('tasks'))

    return render_template('login.html', title='Login')


# ============================================================
# RUTA: LOGOUT DE USUARIO
# ============================================================
@app.route('/logout')
@login_required
def logout():
    """
    Cierra la sesión del usuario actual.
    """
    logout_user()
    return redirect(url_for('login'))


# ============================================================
# RUTA: CREAR NUEVA TAREA
# ============================================================
@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    """
    Permite crear una nueva tarea.
    - Requiere estar autenticado.
    - Guarda título, descripción, fecha de vencimiento y estado.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        status = request.form.get('status')

        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            user_id=current_user.id
        )

        db.session.add(new_task)
        db.session.commit()
        flash('Tarea creada exitosamente.', 'success')
        return redirect(url_for('tasks'))

    return render_template('create_task.html', title='Crear Tarea')


# ============================================================
# RUTA: EDITAR TAREA EXISTENTE
# ============================================================
@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """
    Permite editar una tarea existente.
    - Solo el dueño de la tarea puede modificarla.
    """
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('No tienes permiso para editar esta tarea.', 'danger')
        return redirect(url_for('tasks'))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        task.status = request.form.get('status')

        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

        db.session.commit()
        flash('Tarea actualizada exitosamente.', 'success')
        return redirect(url_for('tasks'))

    return render_template('edit_task.html', title='Editar Tarea', task=task)


# ============================================================
# RUTA: ELIMINAR TAREA
# ============================================================
@app.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """
    Permite eliminar una tarea existente.
    - Solo el dueño de la tarea puede eliminarla.
    """
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta tarea.', 'danger')
        return redirect(url_for('tasks'))

    db.session.delete(task)
    db.session.commit()
    flash('Tarea eliminada exitosamente.', 'success')
    return redirect(url_for('tasks'))


# ============================================================
# RUTA: LISTAR PERSONAJES (API RICK & MORTY)
# ============================================================
@app.route('/characters', methods=['GET'])
@login_required
def list_characters():
    """
    Obtiene personajes de la API de Rick and Morty.
    - Pagina los resultados.
    - Permite asociarlos a tareas existentes del usuario.
    """
    try:
        page = request.args.get('page', 1, type=int)
        response = requests.get(f"{RICK_AND_MORTY_API_URL}?page={page}")
        response.raise_for_status()

        data = response.json()
        characters = data.get('results', [])
        info = data.get('info', {})

        # Obtener las tareas del usuario para el modal
        tasks = current_user.tasks.all()
        tasks_with_characters = [{'task': task, 'character': None} for task in tasks]

        return render_template(
            'characters.html',
            characters=characters,
            info=info,
            tasks_with_characters=tasks_with_characters,
            title="Personajes de Rick and Morty"
        )

    except requests.exceptions.RequestException:
        flash('Error al obtener los personajes de la API.', 'danger')
        return redirect(url_for('tasks'))


# ============================================================
# RUTA: ASOCIAR PERSONAJE A TAREA
# ============================================================
@app.route('/task/associate_character/<int:task_id>/<int:character_id>', methods=['POST'])
@login_required
def associate_character(task_id, character_id):
    """
    Asocia un personaje (Rick and Morty API) a una tarea específica.
    - Solo el dueño de la tarea puede hacerlo.
    """
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('No tienes permiso para modificar esta tarea.', 'danger')
        return redirect(url_for('tasks'))

    task.character_id = character_id
    db.session.commit()

    flash('Personaje asociado exitosamente.', 'success')
    return redirect(url_for('tasks'))
