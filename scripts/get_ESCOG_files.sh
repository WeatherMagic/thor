#! /bin/bash

#Checks if ncFiles exists, empties it if it does and creates it if it dosen't

curr_dir=$(pwd)
dir="$(dirname $0)/../ncFiles" #Default folder for net cdf files

echo "* Creating directory $dir"
mkdir -p $dir

cd $dir
#Downloads the choosen amount of ncFiles to the ncFiles folder
while true; do 
    read -p "* What data should I get? (hist/all/ext) " RESP
    if [ "$RESP" = "hist" ]; then
        echo "* Begining Downloading $RESP data."
        ../scripts/wget-ncFilesHist.sh
        break
    elif [ "$RESP" = "all" ]; then
        echo "* Begining Downloading $RESP data."
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
