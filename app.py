from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get('LUMIA_DATA_DIR', str(BASE_DIR)))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / 'lumia.db'
app = Flask(__name__)
app.secret_key = os.environ.get('LUMIA_SECRET_KEY', 'lumia-web-chave-local-de-desenvolvimento')
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    with db() as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('teacher','student'))
        );
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            due_date TEXT,
            teacher_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(teacher_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            grade REAL,
            feedback TEXT,
            UNIQUE(activity_id, student_id),
            FOREIGN KEY(activity_id) REFERENCES activities(id) ON DELETE CASCADE,
            FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE
        );
        ''')
        if con.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
            con.execute('INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,?)',
                        ('Professor Demo', 'professor@lumia.com', generate_password_hash('123456'), 'teacher'))
            con.execute('INSERT INTO users(name,email,password_hash,role) VALUES(?,?,?,?)',
                        ('Aluno Demo', 'aluno@lumia.com', generate_password_hash('123456'), 'student'))


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if session.get('role') != role:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        with db() as con:
            user = con.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        flash('E-mail ou senha inválidos.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    with db() as con:
        if session['role'] == 'teacher':
            activities = con.execute('''SELECT a.*,
                (SELECT COUNT(*) FROM submissions s WHERE s.activity_id=a.id) AS total_submissions
                FROM activities a WHERE teacher_id=? ORDER BY a.created_at DESC''',
                (session['user_id'],)).fetchall()
            return render_template('teacher.html', activities=activities)
        activities = con.execute('''SELECT a.*, u.name AS teacher_name,
                s.id AS submission_id, s.grade, s.feedback, s.submitted_at
                FROM activities a JOIN users u ON u.id=a.teacher_id
                LEFT JOIN submissions s ON s.activity_id=a.id AND s.student_id=?
                ORDER BY a.created_at DESC''', (session['user_id'],)).fetchall()
        return render_template('student.html', activities=activities)


@app.route('/activity/new', methods=['GET', 'POST'])
@role_required('teacher')
def new_activity():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date') or None
        if not title or not description:
            flash('Preencha o título e a descrição.', 'error')
        else:
            with db() as con:
                con.execute('INSERT INTO activities(title,description,due_date,teacher_id) VALUES(?,?,?,?)',
                            (title, description, due_date, session['user_id']))
            flash('Atividade publicada com sucesso.', 'success')
            return redirect(url_for('dashboard'))
    return render_template('activity_form.html')


@app.route('/activity/<int:activity_id>/submit', methods=['GET', 'POST'])
@role_required('student')
def submit_activity(activity_id):
    with db() as con:
        activity = con.execute('SELECT * FROM activities WHERE id=?', (activity_id,)).fetchone()
        if not activity:
            abort(404)
        existing = con.execute('SELECT * FROM submissions WHERE activity_id=? AND student_id=?',
                               (activity_id, session['user_id'])).fetchone()
        if request.method == 'POST':
            answer = request.form.get('answer', '').strip()
            if not answer:
                flash('Escreva sua resposta antes de enviar.', 'error')
            else:
                con.execute('''INSERT INTO submissions(activity_id,student_id,answer) VALUES(?,?,?)
                    ON CONFLICT(activity_id,student_id) DO UPDATE SET answer=excluded.answer,
                    submitted_at=CURRENT_TIMESTAMP, grade=NULL, feedback=NULL''',
                    (activity_id, session['user_id'], answer))
                flash('Atividade enviada. Você pode consultar o feedback no painel.', 'success')
                return redirect(url_for('dashboard'))
    return render_template('submit.html', activity=activity, existing=existing)


@app.route('/activity/<int:activity_id>/submissions')
@role_required('teacher')
def view_submissions(activity_id):
    with db() as con:
        activity = con.execute('SELECT * FROM activities WHERE id=? AND teacher_id=?',
                               (activity_id, session['user_id'])).fetchone()
        if not activity:
            abort(404)
        submissions = con.execute('''SELECT s.*, u.name AS student_name, u.email
            FROM submissions s JOIN users u ON u.id=s.student_id
            WHERE s.activity_id=? ORDER BY s.submitted_at DESC''', (activity_id,)).fetchall()
    return render_template('submissions.html', activity=activity, submissions=submissions)


@app.route('/submission/<int:submission_id>/feedback', methods=['POST'])
@role_required('teacher')
def give_feedback(submission_id):
    grade_text = request.form.get('grade', '').strip()
    feedback = request.form.get('feedback', '').strip()
    try:
        grade = float(grade_text) if grade_text else None
        if grade is not None and not 0 <= grade <= 10:
            raise ValueError
    except ValueError:
        flash('A nota deve estar entre 0 e 10.', 'error')
        return redirect(request.referrer or url_for('dashboard'))
    with db() as con:
        row = con.execute('''SELECT s.id, a.teacher_id, a.id AS activity_id FROM submissions s
            JOIN activities a ON a.id=s.activity_id WHERE s.id=?''', (submission_id,)).fetchone()
        if not row or row['teacher_id'] != session['user_id']:
            abort(404)
        con.execute('UPDATE submissions SET grade=?, feedback=? WHERE id=?',
                    (grade, feedback, submission_id))
    flash('Feedback salvo.', 'success')
    return redirect(url_for('view_submissions', activity_id=row['activity_id']))


@app.errorhandler(403)
def forbidden(_):
    return render_template('error.html', code=403, message='Você não tem permissão para acessar esta página.'), 403


@app.errorhandler(404)
def not_found(_):
    return render_template('error.html', code=404, message='O conteúdo solicitado não foi encontrado.'), 404


init_db()
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
