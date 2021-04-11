from flask import Flask, redirect, url_for, render_template, request, flash
import sqlite3
from werkzeug.exceptions import abort
import csv
from googlemaps import Client
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BoostIsTheSecretOfMyEnergy'
API_KEY = 'AIzaSyD-9pwUGx6xkzP2pbIbuwT_DWgE3jT_Gj4'
gmaps = Client(API_KEY)

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

@app.route('/get_safety_details')
def get_safety_details():
    source_address = request.args.get('source_address')
    destination_address = request.args.get('destination_address')
    status, start_coordinates, end_coordinates, unsafe_locations, is_destination_safe = check_destination_safety(source_address, destination_address)
    response = {
        "status" : status,
        "start_coordinates" : start_coordinates,
        "end_coordinates" : end_coordinates,
        "unsafe_locations" : unsafe_locations,
        "is_destination_safe" : is_destination_safe
    }
    return json.dumps(response)

def get_coordinates(address):
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
    is_destination_safe = True
    start_coordinates = get_coordinates(source_address)
    end_coordinates = get_coordinates(destination_address)
    danger_locations = get_all_danger_coordinates()

    unsafe_locations, status = get_unsafe_locations(end_coordinates, danger_locations)
    if len(unsafe_locations) > 0:
        is_destination_safe = False
    else:
        unsafe_locations = []
        is_destination_safe = True

    print("is_destination_safe" + str(is_destination_safe))
    return status, start_coordinates, end_coordinates, unsafe_locations, is_destination_safe

def get_unsafe_locations(end_coordinates, danger_locations):
    unsafe_locations = []
    for location in range(0, len(danger_locations)): 
        dist_matrix = gmaps.distance_matrix(end_coordinates,danger_locations[location])['rows'][0]['elements'][0]
        if dist_matrix['distance']['value'] < 528 :
            unsafe_locations.append(danger_locations[location])
    return unsafe_locations, dist_matrix['status']
    
if __name__ == "__main__":
    app.run(debug=True)