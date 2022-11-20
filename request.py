import os
import pprint
import json
from bs4 import BeautifulSoup
import requests
import subprocess
import shlex
import pandas as pd
import numpy as np

DATA_OPTS = {
    'lifeForm': 0,
    'habit': 0,
    'category': 0,
    'lifeSpan': 0,
    'plantAttribute': 0,
    'opt': 1,
    'minTemperature': '',
    'maxTemperature': '',
    'minRainfall': '',
    'maxRainfall': '',
    'minSoilPh': '',
    'maxSoilPh': '',
    'minLightIntensity': 0,
    'maxLightIntensity': 0,
    'climateZone': 0,
    'photoperiod': 0,
    'latitude': '',
    'altitude': '',
    'availableFieldDays': '',
    'soilDepth': 0,
    'soilTexture': 0,
    'soilFertility': 0,
    'soilSalinity': 0,
    'soilDrainage': 0,
    'mainUse': 2,
    'detailedUse': 0,
    'usedPart': 0,
    'quantity': 5
}

# DATA_TEMPLATE = 'lifeForm=0&habit=0&category=0&lifeSpan=0&plantAttribute=0&opt=1&minTemperature=&maxTemperature=&minRainfall=&maxRainfall=&minSoilPh=&maxSoilPh=&minLightIntensity=0&maxLightIntensity=0&climateZone=0&photoperiod=0&latitude=&altitude=&availableFieldDays=&soilDepth=0&soilTexture=0&soilFertility=0&soilSalinity=0&soilDrainage=0&mainUse=2&detailedUse=0&usedPart=0&quantity=5'



# MASTER_OPTS = {
#     'authority':'ecocrop.review.fao.org',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh;q=0.6',
#     'cache-control': 'max-age=0',
#     'content-type': 'application/x-www-form-urlencoded',
#     'dnt': 1,
#     'origin': 'https://ecocrop.review.fao.org',
#     'referer': 'https://ecocrop.review.fao.org/ecocrop/srv/en/cropSearchForm',
#     'data-raw': f"'{DATA_RAW}'",
# }

def find_plants(options):
    results = []

    DOMAIN = 'https://ecocrop.review.fao.org'
    ADDRESS = "https://ecocrop.review.fao.org/ecocrop/srv/en/cropSearch"

    FLAGS = " \
    -H 'authority: ecocrop.review.fao.org' \
    -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
    -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh;q=0.6' \
    -H 'cache-control: max-age=0' \
    -H 'content-type: application/x-www-form-urlencoded' \
    -H 'dnt: 1' \
    -H 'origin: https://ecocrop.review.fao.org' \
    -H 'referer: https://ecocrop.review.fao.org/ecocrop/srv/en/cropSearchForm'"

    DATA_RAW = ''
    for opt in options:
        DATA_RAW += opt+'='+str(options[opt])+'&'

    DATA_RAW = DATA_RAW.rstrip('&')

    REQUEST_TEMPLATE = f"curl '{ADDRESS}' {FLAGS} --data-raw '{DATA_RAW}' --compressed"
    proc = subprocess.Popen(shlex.split(REQUEST_TEMPLATE), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    (request_result, err) = proc.communicate()
    if request_result:
        result = BeautifulSoup(request_result, 'html.parser')
        # print(result.find_all('table')[0].find_all('a')[0]['href'])
        try:
            crops = [x['href'][len('javascript:load(%22'):-len('%22)')] for x in result.find_all('table')[0].find_all('a')]
            for crop in crops:
                data = subprocess.Popen(shlex.split(f"curl '{DOMAIN}{crop}'"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
                (request_result, err) = data.communicate()
                if request_result:
                    result = BeautifulSoup(request_result, 'html.parser')
                    sciname = result.find_all('h2')[0].text
                    data_table = result.find_all('table')[0]
                    # humname = data_table.find_all('td')[5].text
                    code = data_table.find_all('td')[-1].text
                    # print(sciname, code)
                    results.append(int(code))
                else:
                    print(f'Getting data for crop with url "{crop}" failed. Please try again.')
        except IndexError:
            print('No crops found in search, or response was malformed. Please try again.')
    else:
        print('Search for given parameters failed. Please try again.')
    return results

def find(id='', name=''):
    r = requests.get(f'https://ecocrop.review.fao.org/ecocrop/srv/en/cropListDetails?code={id}&relation=beginsWith&name={name}&quantity=1')
    try:
        result = BeautifulSoup(r.text, 'html.parser')
        data = result.find_all('table')[0].find_all('td')
        return data[-1].find_all('button')[0]['onclick'][len('load("/ecocrop/srv/en/cropView?id='):-len('")')], data[0].find_all('a')[0].text, data[2].text
    except IndexError:
        print('Search failed.')
        
def find_detailed(id=''):
    r = requests.get(f'https://ecocrop.review.fao.org/ecocrop/srv/en/dataSheet?id={id}')
    try:
        result = BeautifulSoup(r.text, 'lxml')
        table = result.find_all('table')
        df = pd.read_html(str(table))
        data = [df[0].iloc[:, :2]]
        data.append(df[0].iloc[:, 2:])
        data.append(df[1].iloc[:, :5])
        data.append(df[1].iloc[:-1, 5:])
        data.append(df[2].iloc[:, :2])
        data.append(df[2].iloc[:-1, 2:])
        d = df[5]['Uses'].filter(["Main use", "Detailed use"])
        nutrients_list = d[d['Main use'] == 'food & beverage'].drop_duplicates()["Detailed use"].values.tolist()
        return data, nutrients_list
    except IndexError:
            print('Search failed.')

if __name__ == '__main__':
    print(find_plants(DATA_OPTS))
    print(find(id=289))
