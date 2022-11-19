from netCDF4 import Dataset
from cordex import rotated_coord_transform
from datetime import datetime, timedelta
import numpy as np
from warnings import filterwarnings
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')

filenames = {
  "tas": ["tas_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_202101-203010.nc", "tas_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_203101-204010.nc", "tas_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_204101-205010.nc"],
  "pr": ["pr_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_202101-203010.nc", "pr_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_203101-204010.nc", "pr_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_204101-205010.nc"],
  "hurs": ["hurs_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_202101-203010.nc","hurs_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_203101-204010.nc", "hurs_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_204101-205010.nc"]
}

# a function to find the index of the point closest pt
# (in squared distance) to give lat/lon value.
def getclosest_lonlat(lons,lats,lonpt,latpt):
  rotPt = rotated_coord_transform(lonpt, latpt,  -162, 39.25,direction='geo2rot')
  return [(np.abs(lons  - rotPt[0])).argmin(), (np.abs(lats  - rotPt[1])).argmin()]

def time_to_datetime(inp):
  return datetime(1949, 12, 1) + timedelta(days=int(inp))

def getData(lon, lat, timeframe, param):
    if timeframe == "now":
      timeIndex = 12
      climatePath = filenames[param][0]
    elif timeframe == "short":
      timeIndex = 22 # 5 years ahead
      climatePath = filenames[param][0]
    elif timeframe == "medium":
      timeIndex = 12 # 10 years ahead
      climatePath = filenames[param][1]
    elif timeframe == "long":
      timeIndex = 12 # 20 years ahead
      climatePath = filenames[param][2]

    rootgrp = Dataset("data\\" + climatePath, "r")

    # get the closest coordinate in the dataset
    lons, lats = rootgrp['rlon'], rootgrp['rlat']
    closeLon, closeLat = getclosest_lonlat(lons[:], lats[:], lon, lat)
   
    print(f"the avg {param} for lon: {lons[closeLat]} lat: {lats[closeLat]}  (at {time_to_datetime(rootgrp['time'][timeIndex])}) is {rootgrp[param][timeIndex, closeLon, closeLat] }")

    rootgrp.close()

if __name__ == "__main__":
    lon = -2.308799982070923
    lat = 53.593101501464844
    getData(lon, lat, "long", "hurs")

    """ TIME PARAMETERS:
        now - ...
        short - 5 years ahead
        medium - 10 years ahead
        long - 20 years ahead
        
        DATA PARAMETERS:
        tas - 2m temperature
        pr - mean precipitation flux (rain)
        hurs - relative humidity"""