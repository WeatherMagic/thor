#!/bin/bash


if [ "$#" -ne 1 ]
then
    echo "Usage: "
    echo "  $0 HEIGHT-RESOLUTION"
    exit 1
fi

resolution=$1
models="ICHEC-EC-EARTH IPSL-IPSL-CM5A-MR CNRM-CERFACS-CNRM-CM5"
exhaustLevels="rcp45 rcp85"


for model in $models; do
    for exhaustLevel in $exhaustLevels; do
        for year in $(seq 2006 2100); do
            for month in $(seq 1 12); do
                curlString="http://thor.hfelo.se/api/temperature?to-latitude=90&month=$month&climate-model=$model&year=$year&height-resolution=$resolution&exhaust-level=$exhaustLevel&from-latitude=-90&from-longitude=-180&to-longitude=180" 
                echo "Fetching: "
                echo $curlString 
                curl $curlString > /dev/null
                echo ""
            done
        done
    done
done

# Historical as well
for model in $models; do
    for year in $(seq 1950 2005); do
        for month in $(seq 1 12); do
            curlString="http://thor.hfelo.se/api/temperature?to-latitude=90&month=$month&climate-model=$model&year=$year&height-resolution=$resolution&exhaust-level=historical&from-latitude=-90&from-longitude=-180&to-longitude=180" 
            echo "Fetching: "
            echo $curlString 
            curl $curlString > /dev/null
            echo ""
        done
    done
done

