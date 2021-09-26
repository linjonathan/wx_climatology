# wx_climatology

## Installation
You will first need to set up the python environment. The easiest way to do this is to use the supplied environment.yml file:
```
conda env create -f environment.yml
```
To install the packages yourself, with the most up to date software, create the environment yourself:
```
conda create -n wx_challenge python numpy matplotlib beautifulsoup4 requests lxml
conda activate wx_challenge
pip install windrose
```

## Generating Climatology and Verification
You will need to edit the *config.txt* file to adjust for the station ID and state of the station. See the file for more details.

Finally, to run the scripts that download the ASOS + MOS data, and generate climatology and verification:
```
bash run.sh
```

