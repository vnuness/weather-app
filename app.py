import requests
import json
import pprint
import datetime
from datetime import date
import urllib.parse

# accuweatherAPIKey = 'R1A8ZJsN5a79QcXpGtVVL1UgdWWtBJ8m'
accuweatherAPIKey = 'Z4ZHcWI2TCOOwjW1lRVowLj2hgCl357j'
map_box_token = 'pk.eyJ1IjoidnNpbHZhbnVuZXMiLCJhIjoiY2szYzZteGozMGtxMDNvbnZzcXd0ZTZrYSJ9.ovUGOVQPu1M-0xzhuKuTQg'

current_condition_url = 'http://dataservice.accuweather.com/currentconditions/v1/'

days_of_week = ['Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado']

def pegar_coordenadas():

    r = requests.get("http://www.geoplugin.net/json.gp")

    if(r.status_code != 200):
        print('Não foi possível obter a localização!')
        return None
    else:
        try:
            localizacao = json.loads(r.text)
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long'] = localizacao['geoplugin_longitude']
            return coordenadas
            #latitude = "-22.758020"
            #longitude = "-43.457593"
        except :
            return None
    
        
def pegar_codigo_local(lat, longitude):

    payload = {
            'q' : lat + "," + longitude,
            'apikey' : accuweatherAPIKey,
            'language' : 'pt-BR',
        }

    locationAPIUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'

    r2 = requests.get(locationAPIUrl, params=payload)

    if(r2.status_code != 200):
        print('Não foi possível obter o código do local!')
        return None
    else:
        # try:
        location_info = json.loads(r2.text)
        local = {}
        local['info_local'] = location_info['ParentCity']['LocalizedName'] + ", " + location_info['AdministrativeArea']['LocalizedName'] + ". " +  location_info['Country']['LocalizedName']
        local['codigo_local'] = location_info['Key']
        return local
        # except: 
        # return None

def pegar_tempo_agora(codigo_local, nome_local):

    payload = {
        'apikey': accuweatherAPIKey,
        'language': 'pt-br' 
    }
    
    current_conditions_url = current_condition_url + codigo_local
    r3 = requests.get(current_conditions_url, params=payload)

    if r3.status_code != 200:
        print('Não foi possível obter a previsão do tempo.')
        return None
    else:
        try:
            current_condition_response = json.loads(r3.text)
            info_clima = {}
            info_clima['texto_clima'] = current_condition_response[0]['WeatherText']
            info_clima['temperatura'] = current_condition_response[0]['Temperature']['Metric']['Value']
            info_clima['nome_local'] = nome_local
            return info_clima
        except:
            return None

def pegar_previsao_proximos_dias(codigo_local, nome_local):

    url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'
    payload = {
        'apikey' : accuweatherAPIKey,
        'language': 'pt-br',
        'metric': 'true'
    }

    r = requests.get(url + codigo_local, params=payload)

    try:
        if(r.status_code != 200) :
            print('Não foi possível pegar a previsão dos próximos dias!')
            return None
        else :
            days = json.loads(r.text)['DailyForecasts']
            return days
    except:
        return None

def mostrar_previsao(latitude, longitude):
    # try:
    local = pegar_codigo_local(latitude, longitude)

    clima_atual = pegar_tempo_agora(local['codigo_local'], local['info_local'])
    previsao_proximos_dias = pegar_previsao_proximos_dias(local['codigo_local'], local['info_local'])
    print('Clima atual em: ', clima_atual['nome_local'])
    print(clima_atual['texto_clima'])
    print('Temperatura: ', str(int(clima_atual['temperatura'])) + '\xb0' + 'C' + '\n')
    print('Clima para hoje e para os próximos dias: ' + '\n')
    opcao = input('Deseja ver a previsão dos próximos dias? (s ou n): ').lower()
    while opcao != 'n':
        for key, value in enumerate(previsao_proximos_dias):
            if(int(key) == 0):
                print('Hoje')
            else:
                print(days_of_week[int(date.fromtimestamp(int(value['EpochDate'])).strftime('%w'))])
            print('Mínima: ' + str(value['Temperature']['Minimum']['Value']) + 'ºC')
            print('Máxima: ' + str(value['Temperature']['Maximum']['Value']) + 'ºC')
            print('Clima: ' + str(value['Day']['IconPhrase']))
            print('---------------------------------------------')
        opcao = input('Deseja ver a previsão dos próximos dias? (s ou n): ')

    # except:
    print('Erro ao processar a solicitação.')


def pesquisar_local(local):
    map_box_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + urllib.parse.quote(local.lower()) + '.json?access_token=' + map_box_token
    return json.loads(requests.get(map_box_url).text)['features'][0]['geometry']['coordinates']



## INICIO DO PROGRAMA

local = input('Digite o local que você deseja saber a previsão')

coordenadas = pesquisar_local(local)

mostrar_previsao(str(coordenadas[1]), str(coordenadas[0]))

coordenadas = pegar_coordenadas()
# mostrar_previsao(coordenadas['lat'], coordenadas['long'])

