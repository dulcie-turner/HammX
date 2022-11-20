# HammX
The GitHub repository for team HammX as part of the HackX Cambridge hackathon 2022.

## Requirements
```
pip install \
django \
netCDF4 \
py-cordex \
beautifulsoup4 \
pandas \
numpy \
lxml
```

## Technical Information
We rely on the following user inputs:
* Change resistance (favouring new plants)
* Soil conditions (optional)
* Target food groups/nutrients
* Local area (currently UK-limited, test is Cambridge)
* Projection timescale (short/medium/long)
* Other preferences (absolute/optimum yield, large scale planting…)

We compile the following data:

* Climate data for that area for that timescale
* Current crop distribution in that area

We provide:

* Existing crops that can still be planted after that time has passed
* Existing crops that are in danger of becoming non-viable due to climate change
* New crops that would be well placed for those new climate conditions (in a weighted list)

## Model Description
First we compile a set of existing plants in the area. Based on user preferences and climate projections, we compile a set of new plants that would be viable after the time set by the user is elapsed. 

We take the union of the two sets to find plants that are still viable, plants that are no longer viable, and new recommendations. Recommendations are then compared against a series of factors based on their growth requirements, whether they are scalable etc. to produce a weighted ranking of recommendations.

## Data Sources
* [Cordex](https://cordex.org/)
* [GAEZ Ecocrop](https://gaez.fao.org/pages/ecocrop-find-plant)
* [CROME 2020](https://www.data.gov.uk/dataset/be5d88c9-acfb-4052-bf6b-ee9a416cfe60/crop-map-of-england-crome-2020)