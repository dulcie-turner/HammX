import os
import pprint
import json
from bs4 import BeautifulSoup
import requests
import subprocess
import shlex

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

DATA_RAW = ''
for opt in DATA_OPTS:
    DATA_RAW += opt+'='+str(DATA_OPTS[opt])+'&'

DATA_RAW = DATA_RAW.rstrip('&')

REQUEST_TEMPLATE = f"curl '{ADDRESS}' {FLAGS} --data-raw '{DATA_RAW}' --compressed"

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
                print(sciname, code)
            else:
                print(f'Getting data for crop with url "{crop}" failed. Please try again.')
    except IndexError:
        print('No crops found in search, or response was malformed. Please try again.')
else:
    print('Search for given parameters failed. Please try again.')
