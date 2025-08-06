from app import app, db
from app.models import User, Task

# Comando para crear la base de datos y las tablas
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}

if __name__ == '__main__':
    app.run(debug=True)