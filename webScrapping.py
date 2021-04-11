import requests
from bs4 import BeautifulSoup
import sqlite3

#function to set up db connection
def get_connection():
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    return connection

def update_location_coordinates(connection):
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.027906453327,-118.2749037790", 1))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.03430468199586,-118.28400709568707", 2))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.024850673098236,-118.28176814003838", 3))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.03311208160461,-118.27945309822908", 4))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02224681607721,-118.29167836920976", 5))

    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02753252915366,-118.28508509662556", 6))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02841583614427,-118.28397669961177", 7))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.0280902530464,-118.27917680787786", 8))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02521101686115,-118.2780044672892", 9))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02184862398057,-118.28023553542654", 10))

    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02964608601271,-118.28744337485861", 11))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("33.67254330951706,-117.972303150867", 12))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.023907979689774,-118.30022200835289", 13))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02545135250305,-118.28344519430684", 14))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.025425168142945,-118.28344479014247", 15))

    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.01858436088644,-118.28337755832518", 16))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.027487282376676,-118.30891797366498", 17))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.01847184158187,-118.2923165448302", 18))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02453411362622,-118.2812628159949", 19))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02733874040611,-118.289105258325", 20))
    
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.03299626362487,-118.28199000732457", 21))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.01810874230469,-118.2944354448302", 22))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02844546327014,-118.28422864482994", 23))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.06648564328661,-118.20198226353455", 24))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02819178643076,-118.2758524072807", 25))

    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.033671351114386,-118.28434963756283", 26))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.0188293865494,-118.28269509116915", 27))
    connection.execute("Update crime_data set crime_location_coordinate = ? where crime_id = ?", ("34.02747501645694,-118.2866917313349", 28))
    

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

    update_location_coordinates(connection)
    
                
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
