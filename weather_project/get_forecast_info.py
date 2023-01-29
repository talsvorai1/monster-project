
def get_city_forecast(forecast_info):
    """this function takes a json list
    and finds max/min temp in celcius,
    date, humidity"""
#assigning week varibales with values

    date_list = []
    max_list = []
    min_list = []
    humidity_list = []
    for i in forecast_info['Days']:
        date = i['date']
        date_list.append(date)
        max = i['temp_max_c']
        max_list.append(max)
        min = i['temp_min_c']
        min_list.append(min)
        for j in i['Timeframes']:
            humidity = j['humid_pct']
            break
        humidity_list.append(humidity)

    return date_list, max_list, min_list, humidity_list

