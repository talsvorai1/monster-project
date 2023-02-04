#Python final project
#1. create website to take input and return city name:
from flask import Flask, render_template, request
import requests
from get_city_info import get_city_info
from get_forecast_info import get_city_forecast

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])                 #make web for user to input
def index():                                             #creating index view file
    if request.method == "POST":
        city = request.form["city"]
        print("city returned is: ", city)

        #getting city coordinates and name
        city_info = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=4f724a0afd15a1ce336d71860da0bc59"
        response1 = requests.get(city_info)
        city_data = response1.json()
        #print("city JSON is:", json.dumps(city_data, indent=4))
        name, lattitude, longitude, country = get_city_info(city_data)
        print("our city name, lattitude longitude and country are: ", name, lattitude, longitude, country)

        #inserting coordinates to get forecast JSON:
        city_forecast = f"http://api.weatherunlocked.com/api/forecast/{lattitude},{longitude}?app_id=5e0a3737&app_key=38b8a656b02b1870cad1c1e7ab6b6044"
        response2 = requests.get(city_forecast)
        forecast_data = response2.json()
        #print("forecast info JSON is:", json.dumps(forecast_data, indent=4))
        date_list, max_list, min_list, humidity_list = get_city_forecast(forecast_data)
        if name == 0:
            return render_template('invalid_name.html')
        else:
            return render_template('result.html', len=len(date_list), \
                               date_list=date_list, max_list=max_list, \
                               min_list=min_list, humidity_list=humidity_list, \
                               city=name, country=country)
    else:
        return render_template('index.html')

