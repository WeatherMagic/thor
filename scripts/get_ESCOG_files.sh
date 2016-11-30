#! /bin/bash

#Checks if ncFiles exists, empties it if it does and creates it if it dosen't

curr_dir=$(pwd)
dir="$(dirname $0)/../ncFiles" #Default folder for net cdf files

echo "* Creating directory $dir"
mkdir -p $dir

cd $dir
#Downloads the choosen amount of ncFiles to the ncFiles folder
while true; do 
    read -p "* How much data should I get? (min/med/max/maxi/ext) " RESP
    if [ "$RESP" = "min" ]; then
        echo "* Begining Downloading $RESP amount of data."
        ../scripts/wget-ncFilesMin.sh
        break
    elif [ "$RESP" = "med" ]; then
        echo "* Begining Downloading $RESP amount of data."
        ../scripts/wget-ncFilesMedium.sh
        break
    elif [ "$RESP" = "max" ]; then
        echo "* Begining Downloading $RESP amount of data."
        ../scripts/wget-ncFilesMax.sh
        break
    elif [ "$RESP" = "maxi" ]; then
        echo "* Begining Downloading $RESP amount of data."
        ../scripts/wget-ncFilesMax-i.sh
        break
    elif [ "$RESP" = "ext" ]; then
        echo "* Exiting."
        break
    else
        echo "* $RESP is not a valid input pls help me help you."
    fi
done

cd $curr_dir
