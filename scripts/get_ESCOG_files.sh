#! /bin/bash

#Checks if ncFiles exists, empties it if it does and creates it if it dosen't

dir="ncFiles" #Default folder dor net cdf files

if [ -d "../$dir" ]; then
    #Folder exists and is empty
    echo "*"
else
    echo "* Creating directory ncFiles."
    mkdir ../$dir
fi

#Changeing folder to get the wget files in the right place
cd ../$dir

#Downloads the choosen amount of ncFiles to the ncFiles folder
while true; do 
    read -p "* How much data should I get? (min/med/max/ext) " RESP
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
    elif [ "$RESP" = "ext" ]; then
        echo "* Exiting."
        break
    else
        echo "* $RESP is not a valid input pls help me help you."
    fi
done
