# -*- coding: utf-8 -*-
import requests
import jsonUtil
import key

base_url = 'https://00b501df.ngrok.io/RestfulService_war_exploded/restresources'
mensa_info_url = base_url + '/cafeterias'
menu_info_url = base_url + '/cafeteria/{}/menu'

r = requests.get(mensa_info_url)
mensa_info = jsonUtil.json_loads_byteified(r.text)
mensa_names = [x['info']['name'] for x in mensa_info]
mensa_name_loc = {x['info']['name']: x['info']['coordinates'] for x in mensa_info}


def getInfoMensa(name):
    match = [x for x in mensa_info if x['info']['name']==name]
    if match:
        entry = match[0]
        address = entry['info']['address']
        capacity = entry['capacity']
        takenSeats = entry['takenSeats']
        orario_lunch = entry['info']['launch']["start"] + ' - ' + entry['info']['launch']["end"]
        orario_dinner = entry['info']['dinner']["start"] + ' - ' + entry['info']['dinner']["end"]
        #freeSeats = capacity-takenSeats
        return "*Nome*: {}\n" \
               "*Indirizzo*: {}\n" \
               "*Capacità*: {}\n" \
               "*Orario Pranzo:* {}\n" \
               "*Orario Cena:* {}".format(name, address, capacity, orario_lunch, orario_dinner)
    return None


def getMenuInfo(name):
    if name not in mensa_names:
        return None
    index = mensa_names.index(name)
    url = menu_info_url.format(index)
    r = requests.get(url)
    menu = jsonUtil.json_loads_byteified(r.text)
    primi = menu['first_plate']
    primi_piatti = [str_plate(x) for x in primi]
    secondi = menu['second_plate']
    secondi_piatti = [str_plate(x) for x in secondi]
    return '\n'.join(["1️⃣ *PRIMI*:\n---------", '\n'.join(primi_piatti), "\n\n2️⃣ *SECONDI*:\n---------", '\n'.join(secondi_piatti)])


def str_plate(dict):
    return '\n'.join([
        '*{}*'.format(dict['name']),
        "  Gluten-Free: {}".format(checkbox(dict['glutenFree'])),
        "  Piatto Unico: {}".format(checkbox(dict['piatto_unico'])),
    ])

def checkbox(boolean):
    return '✅' if boolean else '❌'

BASE_MAP_IMG_URL = "http://maps.googleapis.com/maps/api/staticmap?" + \
                   "&size=400x400" + "&maptype=roadmap" + \
                   "&key=" + key.GOOGLE_API_KEY


MAX_THRESHOLD_RATIO = 2

def getFermateNearPosition(lat, lon, radius):
    import geoUtils
    import params
    nearby_fermate_dict = {}
    centralPoint = (lat, lon)
    min_distance = None
    for f,lat_lon in mensa_name_loc.iteritems():
        refPoint = (lat_lon['latitude'], lat_lon['longitude'])
        d = geoUtils.distance(refPoint, centralPoint)
        if d < radius:
            if min_distance is None or d < min_distance:
                min_distance = d
            #k = v['stop']
            nearby_fermate_dict[f] = {
                'loc': refPoint,
                'dist': d
            }
    min_distance = max(min_distance, 1) # if it's less than 1 km use 1 km as a min distance
    nearby_fermate_dict = {k:v for k,v in nearby_fermate_dict.items() if v['dist'] <= MAX_THRESHOLD_RATIO*min_distance}
    max_results = params.MAX_FERMATE_NEAR_LOCATION
    nearby_fermated_sorted_dict = sorted(nearby_fermate_dict.items(), key=lambda k: k[1]['dist'])[:max_results]
    return nearby_fermated_sorted_dict


def getMenseNearPositionImgUrl(lat, lon, radius=10):
    from utility import format_distance
    nearby_fermated_sorted_dict = getFermateNearPosition(lat, lon, radius)
    if nearby_fermated_sorted_dict:
        fermate_number = len(nearby_fermated_sorted_dict)
        img_url = BASE_MAP_IMG_URL + \
                  "&markers=color:red|{},{}".format(lat, lon) + \
                  ''.join(["&markers=color:blue|label:{}|{},{}".format(num, v['loc'][0], v['loc'][1])
                           for num, (f, v) in enumerate(nearby_fermated_sorted_dict, 1)])
        text = 'Ho trovato *1 mensa* ' if fermate_number == 1 else 'Ho trovato *{} mensa* '.format(
            fermate_number)
        text += "in prossimità dalla posizione inserita:\n"
        text += '\n'.join(
            '{}. {}: {}'.format(num, f, format_distance(v['dist']))
            for num, (f, v) in enumerate(nearby_fermated_sorted_dict, 1))
    else:
        img_url = None
        text = 'Nessuna fermata trovata nel raggio di {} km dalla posizione inserita.'.format(radius)
    return img_url, text

