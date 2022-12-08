import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file
from cv_pdf import create_pdf

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
users = {'admin': 'default', 'test': 'test'}

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key'))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(
        app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
@app.route('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('logged_in'):
        flash("You are already logged in. Redirected to archive.")
        return redirect('archive')
    if request.method == 'POST':
        if request.form['username'] not in users.keys():
            error = 'Invalid username'
        elif request.form['password'] != users[request.form['username']]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('archive'))
    return render_template('login.html', error=error)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if session.get('logged_in'):
        flash("You are already logged in. Redirected to archive.")
        return redirect('archive')
    error = None
    if request.method == 'POST':
        if request.form['username'] in users.keys():
            error = 'Имя пользователя уже занято'
        else:
            users[request.form['username']] = request.form['password']
            flash('You was registered and moved to login-page (like mov %ebp, %esp).')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    flash('You were logged out, wow')
    return redirect(url_for('login'))


@app.route('/archive')
def archive():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute(
        'select id, username, name, age, education, work_experience, '
        'skills, email, telephone, image from cvs order by id desc')
    cvs = cur.fetchall()
    return render_template('archive.html', cvs=cvs)


@app.route('/add_cv', methods=['POST', 'GET'])
def add_cv():
    if not session.get('logged_in'):
        abort(401)
    elif request.method == 'POST':
        db = get_db()
        db.execute(
            'insert into cvs (username, name, age, education, work_experience, '
            'skills, email, telephone, image) values (?,?,?,?,?,?,?,?,?)',
            [session['username'], request.form['name'], request.form['age'], request.form['education'],
             request.form['work_experience'], request.form['skills'], request.form['email'], request.form['telephone'],
             request.form['image']])
        db.commit()
        flash('New cv was successfully posted')

        return redirect(url_for('archive'))
    elif request.method == 'GET':
        return render_template('add_cv.html')


@app.route('/cv_<int:id>')
def one_cv(id):
    db = get_db()
    cur = db.execute(
        f'select id, username, name, age, education, work_experience, skills, email,'
        f' telephone, image from cvs where id="{id}" order by id desc')
    cv = cur.fetchall()
    return render_template('cv_number.html', cv=cv)


@app.route('/cv_download_<int:id>')
def download_cv(id):
    db = get_db()
    cur = db.execute(
        f'select id, username, name, age, education, work_experience, skills, email,'
        f' telephone, image from cvs where id="{id}" order by id desc')
    cv = cur.fetchall()
    print(cv)
    name = str(cv[0]['name'])
    age = str(cv[0]['age'])
    education = map(str, cv[0]['education'].split(','))
    work_experience = map(str, cv[0]['work_experience'].split(','))
    skills = map(str, cv[0]['skills'].split(','))
    email = str(cv[0]['email'])
    tel = str(cv[0]['telephone'])
    pict = cv[0]['image']
    print(pict)
    create_pdf(
        name=name,
        age=age,
        education=education,
        work_experience=work_experience,
        skills=skills,
        email=email,
        tel=tel,
        pict=pict
    )
    return send_file('resume.pdf')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
