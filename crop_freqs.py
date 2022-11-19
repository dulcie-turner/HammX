import json

DATA_PATH = 'Crop_Map_of_England_2020_Cambridgeshire.json'

def load_plant_data(map_path, reference_path='lucode_crop_reference.txt',return_names=False):
    reference_dict = {}
    # Load LUCODE -> Crop type conversion
    with open(reference_path) as f:
        reference_list = [[_.split()[0].strip(), ' '.join(_.split()[1:]).strip()] for _ in f.readlines()]
        for item in reference_list:
            reference_dict[item[0]] = item[1]

    print('loaded crop references')
    # print(reference_dict)

    with open(map_path) as f:
            map_data = json.load(f)

    print('loaded map data')
    crop_freqs = {}
    for item in reference_list:
        crop_freqs[item[0]] = 0

    not_found = []
    unfound_freq = 0
    for feature in map_data['features']:
        try:
            crop_freqs[feature['attributes']['lucode']] += 1
        except KeyError:
            if feature['attributes']['lucode'] not in not_found:
                not_found.append(feature['attributes']['lucode'])
            unfound_freq += 1

    for code in not_found:
        print('Reference for LUCODE', code, 'not found')

    # crop_freqs = {'AC01': 97260, 'AC03': 30689, 'AC04': 0, 'AC05': 0, 'AC06': 0, 'AC07': 0, 'AC09': 0, 'AC10': 0, 'AC14': 0, 'AC15': 5233, 'AC16': 4542, 'AC17': 36043, 'AC18': 0, 'AC19': 8977, 'AC20': 3691, 'AC22': 0, 'AC23': 0, 'AC24': 0, 'AC26': 0, 'AC27': 0, 'AC30': 0, 'AC32': 48057, 'AC34': 2, 'AC35': 0, 'AC36': 0, 'AC37': 0, 'AC38': 0, 'AC41': 0, 'AC44': 34031, 'AC45': 0, 'AC50': 0, 'AC52': 0, 'AC58': 0, 'AC59': 0, 'AC60': 0, 'AC61': 0, 'AC62': 0, 'AC63': 31806, 'AC64': 0, 'AC65': 6475, 'AC66': 149138, 'AC67': 38539, 'AC68': 6740, 'AC69': 0, 'AC70': 0, 'AC71': 0, 'AC72': 0, 'AC74': 0, 'AC81': 0, 'AC88': 0, 'AC90': 0, 'AC92': 0, 'AC94': 0, 'AC100': 0, 'CA02': 0, 'LG01': 0, 'LG02': 0, 'LG03': 53633, 'LG04': 0, 'LG06': 0, 'LG07': 10725, 'LG09': 0, 'LG08': 0, 'LG11': 21019, 'LG13': 0, 'LG14': 266, 'LG15': 0, 'LG16': 0, 'LG20': 51418, 'LG21': 0, 'SR01': 0, 'FA01': 21284, 'HE02': 67, 'PG01': 62182, 'NA01': 46730, 'WA00': 4411, 'TC01': 0, 'NU01': 0, 'WO12': 45553, 'AC00': 0}
    total = unfound_freq
    output = []
    for elem in crop_freqs:
        if crop_freqs[elem] != 0:
            total += crop_freqs[elem]
            output.append([elem, crop_freqs[elem]])

    output.sort(key=lambda x: x[1], reverse=True)
    percent_total = 0
    percent_dict = {}
    for crop in output:
        print(reference_dict[crop[0]], (crop[1]/total)*100)
        if return_names:
            percent_dict[reference_dict[crop[0]]] = (crop[1]/total)*100 
        else:
            percent_dict[crop[0]] = (crop[1]/total)*100
        percent_total += (crop[1]/total)*100
    print('Accounted for', percent_total, '%')
    return percent_dict

if __name__ == '__main__':
    load_plant_data(DATA_PATH)
        