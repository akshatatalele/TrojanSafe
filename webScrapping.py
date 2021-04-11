import requests
from bs4 import BeautifulSoup
import sqlite3

#function to set up db connection
def get_connection():
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    return connection

def update_location_coordinates():
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.027906453327,-118.2749037790", 1))
    connection.execute("Update crime_data set crime_lat = ?, crime_long = ? where crime_id = ?", ( , 2))
    connection.execute("Update crime_data set crime_lat = ?, crime_long = ? where crime_id = ?", ( , 3))
    connection.execute("Update crime_data set crime_lat = ?, crime_long = ? where crime_id = ?", ( , 4))
    connection.execute("Update crime_data set crime_lat = ?, crime_long = ? where crime_id = ?", ( , 5))


def get_crime_details(url_string, crime_nos, connection):
    
    crime_title = ""
    crime_alert_date = ""
    location = ""
    timestamp = ""
    url = ""

    for i in range(1, crime_nos): 

        #Create valid URL
        URL = url_string+str(i)+'/';
        page = requests.get(URL)
        html = page.content
        soup = BeautifulSoup(html, 'html.parser')
        
        #Extract crime data
        if(soup.find("h1", class_="entry-title")):
            crime_title = soup.find("h1",class_="entry-title").text

            if(soup.find("div",class_="entry-meta")):
                crime_alert_date = soup.find("div",class_="entry-meta").text
            if(soup.find("div",class_="entry-content")):
                crime_details = soup.find("div",class_="entry-content")
            if(crime_details.find_all('p')):
                crime_in_depth = crime_details.find_all('p')
                url = URL
                
                # Extract crime time stamp and location
                for j in range(0,3):
                    crime_desc = crime_in_depth[j].text
                    crime_desc = crime_desc.split(":", 1)
                    
                    if j == 1 and crime_desc[0].lower().find("time") != -1:
                        timestamp = crime_desc[1]

                    elif j == 2 and crime_desc[0].lower().find("location") != -1:
                        location = crime_desc[1]

                # insert unique data into db
                db_timeStamp = connection.execute('Select * from crime_data where crime_timeStamp = ?', (timestamp,)) 
                if len(db_timeStamp.fetchall()) == 0:
                    connection.execute("Insert into crime_data(crime_title, crime_alert_date, crime_location, crime_timeStamp, crime_url) values(?, ?, ?, ?, ?)", (crime_title, crime_alert_date, location, timestamp, url))

    update_location_coordinates()
    
                
def main():
    connection = get_connection()
    get_crime_details('https://dps.usc.edu/robbery-', 56, connection)
    get_crime_details('https://dps.usc.edu/aggravated-assault-', 4, connection)
    get_crime_details('https://dps.usc.edu/attempted-robbery-', 5, connection)
    get_crime_details('https://dps.usc.edu/sexual-assault-', 4, connection)
    get_crime_details('https://dps.usc.edu/burglary-', 7, connection)
    get_crime_details('https://dps.usc.edu/sexual-battery-', 12, connection)
    connection.commit()
    connection.close()
      

if __name__ == "__main__":
    main()
