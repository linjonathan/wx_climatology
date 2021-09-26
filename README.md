# wx_climatology

You will first need to set up the python environment. The easiest way to do this is to use the supplied environment.yml file:
```
conda env create -f environment.yml
```
However, this may become out of date in the future. To install the packages yourself, with the most up to date software, create the environment yourself:
```
conda create -n wx_challenge python numpy matplotlib beautifulsoup4 requests lxml
conda activate wx_challenge
pip install windrose
```
