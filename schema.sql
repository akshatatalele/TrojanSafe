DROP TABLE IF EXISTS crime_data;

CREATE TABLE crime_data (
    crime_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crime_title TEXT NOT NULL,
    crime_alert_date TEXT NOT NULL,
    crime_location TEXT NOT NULL,
    crime_timeStamp TEXT NOT NULL,
    crime_location_coordinate TEXT,
    crime_url TEXT NOT NULL
);