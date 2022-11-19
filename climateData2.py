from netCDF4 import Dataset
import numpy as np

climatePath = "data\\tas_EUR-11_MOHC-HadGEM2-ES_rcp85_r1i1p1_MOHC-HadREM3-GA7-05_v1_sem_202101-203010.nc"

# a function to find the index of the point closest pt
# (in squared distance) to give lat/lon value.
def getclosest_ij(lats,lons,latpt,lonpt):
  # find squared distance of every point on grid
  """dist_sq = (lats-latpt)**2 + (lons-lonpt)**2
  # 1D index of minimum dist_sq element
  minindex_flattened = dist_sq.argmin()
  # Get 2D index for latvals and lonvals arrays from 1D index
  print(np.unravel_index(minindex_flattened, lats.shape))
  return np.unravel_index(minindex_flattened, lats.shape)"""

  geo_idx = (np.abs(lons  - lonpt)).argmin()
  #print(f"{min(lons)} {max(lons)} - {min(lats)} {max(lats)}")
  return [(np.abs(lats  - latpt)).argmin(), (np.abs(lons  - lonpt)).argmin()]

def main():
    rootgrp = Dataset(climatePath, "r")
    #print(rootgrp.variables.keys())
    temps, lats, lons = rootgrp['tas'], rootgrp['latitude'], rootgrp['longitude']
    print(temps)
    #print(rootgrp["rlat"])
    iy_min, ix_min = getclosest_ij(lats[:][1], lons[:][0], -2.308799982070923, 53.593101501464844)
    #print(iy_min)
    #print(ix_min)
    rootgrp.close()

if __name__ == "__main__":
    main()