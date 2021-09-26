#!/bin/bash
# Make sure you edit config.txt file before running this script, and have the appropriate conda environment active.

echo "Downloading ASOS data..."
python3 download_asos.py
echo "Generating climatology figures..."
python3 get_climatology.py
echo "Downloading MOS data..."
python3 scrape_mos.py
python3 scrape_mos_cld.py
echo "Generating verification figures..."
python3 recent_verification.py
