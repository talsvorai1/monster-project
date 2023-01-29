def get_city_info(my_city):
    """this function takes a json list
    and finds name, country, lat and lon,
    prints them and returns them"""
    name = 0
    lattitude = 0
    longitude = 0
    country = 0
    for i in my_city:
        name = i['name']
        if name != 0:
            break
        else:
            continue
    for i in my_city:
        lattitude = i['lat']
        if lattitude != 0:
            break
        else:
            continue
    for i in my_city:
        longitude = i['lon']
        if lattitude != 0:
            break
        else:
            continue
    for i in my_city:
        country = i['country']
        if country != 0:
            break
        else:
            continue
    return name, lattitude, longitude, country