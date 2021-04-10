DROP TABLE IF EXISTS crime_data;

CREATE TABLE crime_data (
    crime_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crime_title TEXT NOT NULL,
    crime_alert_date NUMERIC NOT NULL,
    crime_location TEXT NOT NULL,
    crime_incident_description TEXT NOT NULL,
    crime_timeStamp NUMERIC NOT NULL,
    crime_lat REAL NOT NULL,
    crime_long REAL NOT NULL
);