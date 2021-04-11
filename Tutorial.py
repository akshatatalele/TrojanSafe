from flask import Flask, redirect, url_for, render_template, request, flash
import sqlite3
from werkzeug.exceptions import abort
import csv
from googlemaps import Client
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'BoostIsTheSecretOfMyEnergy'
API_KEY = 'AIzaSyD-9pwUGx6xkzP2pbIbuwT_DWgE3jT_Gj4'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    crimes = get_recent_crimes()
    return render_template("index.html", crimes= crimes)

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

# get recent 5 crimes 
def get_recent_crimes():
    conn = get_db_connection()
    cur = conn.cursor()
    crimes = cur.execute('SELECT * FROM crime_data order by crime_alert_date Limit 5').fetchall()
    conn.close()
    if crimes is None:
        abort(404)
    return crimes

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

def get_coordinates(address):
    gmaps = Client(API_KEY)
    geo_result = gmaps.geocode(address)
    lat = json.dumps(geo_result[0]['geometry']['location']['lat'])
    lng = json.dumps(geo_result[0]['geometry']['location']['lng'])
    return str(lat)+','+str(lng)
    
def get_all_danger_coordinates():
    conn = get_db_connection()
    crime_location_coordinate = conn.execute('select crime_location_coordinate from crime_data').fetchall()
    crime_location_list=[]
    for crime_location in crime_location_coordinate:
        crime_location_list.append(crime_location['crime_location_coordinate'])
    conn.commit()
    conn.close()
    return crime_location_list

def check_destination_safety(source_address,destination_address):
    start_coordinates = get_coordinates(source_address)
    end_coordinates = get_coordinates(destination_address)
    danger_locations = get_all_danger_coordinates()
    print(danger_locations)

if __name__ == "__main__":
    app.run(debug=True)
