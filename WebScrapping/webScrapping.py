import requests
from bs4 import BeautifulSoup

def get_crime_details(url_string,crime_nos):
    for i in range(crime_nos,1,-1): 
        #Create valid URL
        URL = url_string+str(i)+'/';
        page = requests.get(URL)
        html = page.content

        soup = BeautifulSoup(html, 'html.parser')
        #Extract crime data
        if(soup.find("h1",class_="entry-title")):
            crime_type=soup.find("h1",class_="entry-title").text
            count+=1
            if(soup.find("div",class_="entry-meta")):
                crime_alert_date=soup.find("div",class_="entry-meta").text
            if(soup.find("div",class_="entry-content")):
                crime_details=soup.find("div",class_="entry-content")
            if(crime_details.find_all('p')):
                crime_in_depth = crime_details.find_all('p')

                # Extract crime data in more detail
                for i in crime_in_depth:
                    crime_desc = i.text
                
            
def main():
    get_crime_details('https://dps.usc.edu/robbery-',55)
    get_crime_details('https://dps.usc.edu/aggravated-assault-',4)
    get_crime_details('https://dps.usc.edu/attempted-robbery-',5)
    get_crime_details('https://dps.usc.edu/sexual-assault-',4)
    get_crime_details('https://dps.usc.edu/burglary-',7)
    get_crime_details('https://dps.usc.edu/sexual-battery-',12)
      

if __name__ == "__main__":
    main()


    