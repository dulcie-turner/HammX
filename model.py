from request import find_plants, find, find_detailed
from crop_freqs import load_plant_data
import random
import pprint
from climateData import getData as get_climate_data
import math

CAMB_COORDS = (52.2053,0.1218)
TIMESCALE = 'short'
short_clim_data = {
    'avgTemperature': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tas")-273,
    'minTemperature': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tasmin")-273,  # Kelvin -273 ~= Celsius
    'maxTemperature': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tasmax")-273,
    'minRainfall': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "pr") * 31557600 -1,  # Rainfall flux (kg/m2/s) * 31557600 = annual rainfall (mm)
    'maxRainfall': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "pr") * 31557600 +1,
}
pprint.pprint(short_clim_data)

TIMESCALE = 'medium'
med_clim_data = {
    'avgTemperature': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tas")-273,
    'minTemperature': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tasmin")-273,  # Kelvin -273 ~= Celsius
    'maxTemperature': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tasmax")-273,
    'minRainfall': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "pr") * 31557600 -1,  # Rainfall flux (kg/m2/s) * 31557600 = annual rainfall (mm)
    'maxRainfall': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "pr") * 31557600 +1,
}
pprint.pprint(med_clim_data)

TIMESCALE = 'long'
long_clim_data = {
    'avgTemperature': int(round(get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tas")-273)),
    'minTemperature': int(round(get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tasmin")-273)),  # Kelvin -273 ~= Celsius
    'maxTemperature': int(round(get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "tasmax")-273)),
    'minRainfall': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "pr") * 31557600 -1,  # Rainfall flux (kg/m2/s) * 31557600 = annual rainfall (mm)
    'maxRainfall': get_climate_data(CAMB_COORDS[1], CAMB_COORDS[0], TIMESCALE, "pr") * 31557600 +1,
}
pprint.pprint(long_clim_data)

DATA_PATH = 'Crop_Map_of_England_2020_Cambridgeshire.json'
CONV_PATH = 'lucode_to_epcode.txt'

CONV_LOOKUP ={}

with open(CONV_PATH) as f:
    for line in f.readlines():
        lucode = line.split(' ')[0]
        ids = [int(x) for x in ' '.join(line.split(' ')[1:]).split(',')]
        CONV_LOOKUP[lucode] = ids

DATA_OPTS = {
    'lifeForm': 0,
    'habit': 0,
    'category': 0, # 2 = cereals & pseudocereals, 3 = pulses (grain legumes), 6 = fruits & nuts, 7 = vegetables,
    'lifeSpan': 0,
    'plantAttribute': 0,
    'opt': 2,
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
    'quantity': 100
}

trunc_names = lambda x: ', '.join([_.strip() for _ in random.sample(x.split(','), len(x.split(',')))[:min(len(x.split(',')), 3)]])+'...'

def find_alt_plants(curr_plants: dict, conv_lookup: dict, proj_clim: dict, search_opts: dict,  food_groups: dict = [2,3,6,7]):
    existing_group = []
    # Build existing group of plants
    for name in curr_plants:
        try:
            existing_group += conv_lookup[name]
        except KeyError:
            print('No equivalence found for LUCODE', name)

    # Apply projected climate conditions to search
    for cond in proj_clim:
        search_opts[cond] = proj_clim[cond]
    print(search_opts)
    
    new_group = []
    # Search once for each food group
    for group in food_groups:
        # search_opts['category'] = group
        new_plants = find_plants(search_opts)
        for plant in new_plants:  # each plant is returned in [name, id] format
            if plant not in new_group:
                new_group.append(plant)

    overlap_group = []
    out_group = []
    recc_group = []

    for elem in existing_group:
        if elem in new_group:
            overlap_group.append(elem)
        else:
            out_group.append(elem)
    for plant in new_group:
        if plant not in overlap_group:
            recc_group.append(plant)
    print(f'\nThese {len(overlap_group)} plants remain viable:')
    for plant in overlap_group:
        id, name, common_names = find(id=plant)
        print(name, 'also known as', trunc_names(common_names))
    print(f'\nThese {len(out_group)} plants are no longer viable:')
    for plant in out_group:
        id, name, common_names = find(id=plant)
        print(name, 'also known as', trunc_names(common_names))
    print(f'\nThese {len(recc_group)} plants are recommended for projected climate conditions:')
    for plant in recc_group:
        id, name, common_names = find(id=plant)
        print(name, 'also known as', trunc_names(common_names))
    
    return {'out': out_group,'recc': recc_group, 'overlap': overlap_group}

def order_by_weight(grouped_ids, resistance_to_change=0.9, optimal_pref_factor=0.7, scale_pref_factor=0.7):
    viable = {}
    for id in grouped_ids['recc']:
        viable[id] = find_detailed(id)[0]

    weight_factors = {'current':{}, 'optimal_temp':{}, 'optimal_avg_temp':{}, 'optimal_rain':{}, 'scale':{}}

    is_current = np.isin(grouped_ids['recc'], grouped_ids['overlap'])
    is_current = np.invert(is_current)
    weight_factors['current'] = dict(zip(grouped_ids['recc'], is_current))

    for id in grouped_ids['recc']: #parallelise?
        t_min = float(viable[id][2]['Ecology']['Optimal'][1]) #opt min temp
        t_max = float(viable[id][2]['Ecology']['Optimal.1'][1]) #opt max temp
        r_min = float(viable[id][2]['Ecology']['Optimal'][2]) #opt min rain
        r_max = float(viable[id][2]['Ecology']['Optimal.1'][2]) #opt max rain
        if (t_min <= long_clim_data['minTemperature']) and (long_clim_data['maxTemperature'] <= t_max):
            weight_factors['optimal_temp'][id] = True
        else:
            weight_factors['optimal_temp'][id] = False
        if (t_min <= long_clim_data['avgTemperature']) and (long_clim_data['avgTemperature'] <= t_max):
            weight_factors['optimal_avg_temp'][id] = True
        else:
            weight_factors['optimal_avg_temp'][id] = False
        if (long_clim_data['minRainfall'] >= r_min) and (long_clim_data['maxRainfall'] <= r_max):
            weight_factors['optimal_rain'][id] = True
        else:
            weight_factors['optimal_rain'][id] = False

        if (viable[id][1]['Description.3'][2] == 'grown on large scale'):
            weight_factors['scale'][id] = True
        else:
            weight_factors['scale'][id] = False

    #calculate weights
    ids = np.array(grouped_ids['recc'])
    ws_l = []
    for id in ids:
        w = (weight_factors['current'][id] * resistance_to_change) # favour original crops over new ones by resistance_to_change
        w += (weight_factors['scale'][id] * scale_pref_factor)  # favour those with plant_attributes='grown on large scale'
        w += (weight_factors['optimal_temp'][id] * optimal_pref_factor) # favour [min+max in optimal] temperature over [avg in optimal] over neither
        w += (weight_factors['optimal_avg_temp'][id] * optimal_pref_factor)
        w += (weight_factors['optimal_rain'][id] * optimal_pref_factor) # favour [min+max in optimal] rainfall over neither
        ws_l.append(w)
    ws = np.array(ws_l)
        
    # order ids by ws
    inds = ws.argsort()
    ids = ids[inds]
    return np.flip(ids)

def find_cond_violation(id, conds):
    data, nutrients = find_detailed(id)
    violations =[]
    t_min = float(data[2]['Ecology']['Absolute'][1]) #opt min temp
    t_max = float(data[2]['Ecology']['Absolute.1'][1]) #opt max temp
    r_min = float(data[2]['Ecology']['Absolute'][2]) #opt min rain
    r_max = float(data[2]['Ecology']['Absolute.1'][2]) #opt max rain
    if 'minTemperature' in conds:
        if conds['minTemperature'] < t_min:
            violations.append('Minimum temperature too low.')
    if 'maxTemperature' in conds:
        if conds['maxTemperature'] > t_max:
            violations.append('Maximum temperature too high.')
    if 'minRainfall' in conds:
        if conds['minRainfall'] < r_min:
            violations.append('Minimum rainfall too low.')
    if 'maxRainfall' in conds:
        if conds['maxRainfall'] > r_max:
            violations.append('Maximum rainfall too high.')
    return violations

current_plants = load_plant_data(DATA_PATH)

del short_clim_data['avgTemperature']
short_clim_data['maxRainfall']
short_clim_data['minRainfall']
grouped_ids = find_alt_plants(current_plants, CONV_LOOKUP, short_clim_data, DATA_OPTS)
ids_ordered = order_by_weight(grouped_ids)