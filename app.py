import requests
import json
import pprint

accuweatherAPIKey = 'R1A8ZJsN5a79QcXpGtVVL1UgdWWtBJ8m'

current_condition_url = 'http://dataservice.accuweather.com/currentconditions/v1/'

r = requests.get("http://www.geoplugin.net/json.gp")

if(r.status_code != 200):
    print('Não foi possível obter a localização!')
else:
    localizacao = json.loads(r.text)
    latitude = localizacao['geoplugin_latitude']
    longitude = localizacao['geoplugin_longitude']
    #latitude = "-22.758020"
    #longitude = "-43.457593"
    
payload = {
    'q' : latitude + "," + longitude,
    'apikey' : accuweatherAPIKey,
    'language' : 'pt-BR',
}

locationAPIUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'

r2 = requests.get(locationAPIUrl, params=payload)

#http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=R1A8ZJsN5a79QcXpGtVVL1UgdWWtBJ8m&q=-23.627%2C-46.635&language=pt-BR

if(r2.status_code != 200):
    print('Não foi possível obter o código do local!')
else:
    location_info = json.loads(r2.text)
    local = location_info['ParentCity']['LocalizedName'] + ", " + location_info['AdministrativeArea']['LocalizedName'] + ". " +  location_info['Country']['LocalizedName']
    codigo_local = location_info['Key']
    payload_condition = {
        'apikey': 'R1A8ZJsN5a79QcXpGtVVL1UgdWWtBJ8m',
        'language': 'pt-br' 
    }
    url = current_condition_url + codigo_local
    r3 = requests.get(url, params=payload_condition)

    if r3.status_code != 200:
        print('Não foi possível obter a previsão do tempo.')
    else:
        current_condition_response = json.loads(r3.text)
        texto_clima = current_condition_response[0]['WeatherText']
        temperatura = current_condition_response[0]['Temperature']['Metric']['Value']
        print('Clima no momento: ', texto_clima)
        print('Temperatura: ' +  str(int(temperatura)) + 'ºC')