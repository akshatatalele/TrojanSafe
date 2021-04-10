from flask import Flask, redirect, url_for, render_template, request, flash
import sqlite3
from werkzeug.exceptions import abort
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BoostIsTheSecretOfMyEnergy'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/alerts")
def alerts():
    conn = get_db_connection()
    crimes = conn.execute('SELECT * from crime_data').fetchall()
    conn.close()
    return render_template("alerts.html", crimes = crimes)


@app.route('/<int:crime_id>')
def crime(crime_id):
    crime = get_crime(crime_id)
    return render_template('crime.html', crime=crime)

def get_crime(crime_id):
    conn = get_db_connection()
    crime = conn.execute('SELECT * FROM crime_data WHERE crime_id = ?',
                        (crime_id,)).fetchone()
    conn.close()
    if crime is None:
        abort(404)
    return crime

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                        (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    crime = get_crime(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE crime_data SET crime_title = ?, crime_incident_description = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', crime=crime)

# @app.route('/<int:id>/delete', methods=('POST',))
# def delete(id):
#     post = get_post(id)
#     conn = get_db_connection()
#     conn.execute('DELETE FROM posts WHERE id = ?', (id,))
#     conn.commit()
#     conn.close()
#     flash('"{}" was successfully deleted!'.format(post['title']))
#     return redirect(url_for('index'))

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


if __name__ == "__main__":
    app.run(debug=True)
