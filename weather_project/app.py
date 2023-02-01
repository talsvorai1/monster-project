#Python final project
#1. create website to take input and return city name:
from flask import Flask, render_template, request
import requests
from get_city_info import get_city_info
from get_forecast_info import get_city_forecast
from flask import send_from_directory, url_for
import json
import os
import datetime
############^
import logging
#############^
#set logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
#create a logger
logger = logging.getLogger(__name__)
#set log filename and filemode
log_file = 'app.log'
log_mode = 'w'
#set log file handler
handler = logging.FileHandler(log_file, mode=log_mode)
#add log file handler to logger
logger.addHandler(handler)
#log a message
logger.debug('This is a debugging message')
############V
############V

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])                 #make web for user to input
def index():                                             #creating index view file 
    if request.method == "POST":
        city = request.form["city"]
        ############
        logger.debug('Received request for city: %s', city)
        ############
        print("city returned is: ", city)

        #getting city coordinates and name
        city_info = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=4f724a0afd15a1ce336d71860da0bc59"
        ############
        try:
            response1 = requests.get(city_info)
            city_data = response1.json()
        except Exeption as e:
            logger.error('Error retrieving city data: %s', e)
        else:        
            #print("city JSON is:", json.dumps(city_data, indent=4))
            name, lattitude, longitude, country = get_city_info(city_data)
            print("our city name, lattitude longitude and country are: ", name, lattitude, longitude, country)
            logger.debug('Country is: %s', country)
        ############    
        #inserting coordinates to get forecast JSON:
        city_forecast = f"http://api.weatherunlocked.com/api/forecast/{lattitude},{longitude}?app_id=5e0a3737&app_key=38b8a656b02b1870cad1c1e7ab6b6044"
        response2 = requests.get(city_forecast)
        forecast_data = response2.json()
        #print("forecast info JSON is:", json.dumps(forecast_data, indent=4))
        date_list, max_list, min_list, humidity_list = get_city_forecast(forecast_data)
        ################
        logger.debug('Min temp for %s is %s', city, min_list)
        logger.debug('Max temp for %s is %s', city, max_list)
        ################
        save_search_data(name, country, min_list, max_list, humidity_list, date_list)


        if name == 0:
            return render_template('invalid_name.html')
        else:
            return render_template('result.html', len=len(date_list), \
                               date_list=date_list, max_list=max_list, \
                               min_list=min_list, humidity_list=humidity_list, \
                               city=name, country=country)
    else:
  
        return render_template('index.html')
def save_search_data(name, country, min_list, max_list, humidity_list, date_list):
    # Create a dictionary to store the search data
    search_data = {
        "city" : name,
        "country" : country,
        "min" : min_list,
        "max" : max_list,
        "humidity" : humidity_list,
        "dates" : date_list
    }

    directory = "history_downloads"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Parse the date string into a datetime object
    date = datetime.datetime.strptime(date_list[0], "%d/%m/%Y")
    # Convert the date to the desired format
    date = date.strftime("%d-%m-%Y")
    # Save file by search name and date        
    filename = f"history_downloads/{name}_{date}.json"
    with open(filename, "w") as file:
        # Write the search data to the file as JSON
        json.dump(search_data, file, indent=4) 

@app.route('/downloads')
def show_downloads():
    #list file in directory
    files = os.listdir("history_downloads")
    return render_template('history.html', files=files)

@app.route('/downloads/<filename>')
def download_file(filename):

    #send file to user as download
    directory = "history_downloads"
    return send_from_directory(directory, filename, as_attachment=True)    




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)

