import cdsapi
from datetime import date, datetime, timedelta
import xarray as xr
import numpy as np
import tempfile

gribFile = tempfile.NamedTemporaryFile()
gribFilename = gribFile.name
latestValidDate = (datetime.now() - timedelta(days = 5)).date()

def fetchData(dates, location):
    # saves data to file

    # time inputs: list of (padded to 2 digit) numbers
    # location input: a pair of lat / long coords

    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'grib',
            'variable': ['surface_solar_radiation_downwards', '2m_temperature'],
            'date': dates,
            'time': [f"{i:02}:00" for i in range(24)],
            'area': [location[0], location[1], location[0], location[1]],
        },
        gribFilename)

def getDates(startDate, endDate):
    # get list of dates between start and end date (excluding invalid ones where data has not yet arrived)
    delta = timedelta(days=1)
    dateCounter = startDate
    dates = []
    while dateCounter <= endDate:
        if (dateCounter < latestValidDate):
            dates.append(str(dateCounter))
        dateCounter += delta
    return dates

def main(dateInput):
    print("Running climateData.py at", datetime.now())

    dates = getDates(dateInput[0], dateInput[1])
    if len(dates) == 0:
        raise Exception(f"No dates to fetch. Start date must be earlier than {latestValidDate}")

    fetchData(dates, [-2.308799982070923, 53.593101501464844])

    # needs to be done separately to mitigate API bug
    temp_ds = xr.open_dataset(gribFilename, engine="cfgrib", backend_kwargs={'filter_by_keys': {'shortName': '2t'}})
    sol_ds = xr.open_dataset(gribFilename, engine="cfgrib", backend_kwargs={'filter_by_keys': {'shortName': 'ssrd'}})
    temp_df = temp_ds.to_dataframe()
    sol_df = sol_ds.to_dataframe()

if __name__ == "__main__":
    main([(datetime.now() - timedelta(days=30)).date(), (datetime.now() - timedelta(days=29)).date()])
    
