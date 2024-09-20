#!/bin/bash
# Make sure you edit config.txt file before running this script, and have the appropriate conda environment active.

echo "Downloading ASOS data..."
/home/jl3658/.conda/envs/synoptic2/bin/python3 download_asos.py $1 $2
echo "Generating climatology figures..."
/home/jl3658/.conda/envs/synoptic2/bin/python3 get_climatology.py $2
echo "Downloading MOS data..."
/home/jl3658/.conda/envs/synoptic2/bin/python3 scrape_mos.py $2
/home/jl3658/.conda/envs/synoptic2/bin/python3 scrape_mos_cld.py $2
echo "Generating verification figures..."
/home/jl3658/.conda/envs/synoptic2/bin/python3 recent_verification.py $2