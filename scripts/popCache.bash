#!/bin/bash

my_dir="$(dirname $0)"

if [ "$#" -ne 1 ]
then
    echo "Usage: "
    echo "  $0 HEIGHT-RESOLUTION"
    exit 1
fi

height_res=$1
child_pids=""

# Populate temperature cache
$my_dir/helperPopCache.bash "temperature" $height_res &> /dev/null &
child_pids="$!"

# Populate precipitation cache
$my_dir/helperPopCache.bash "precipitation" $height_res &> /dev/null & 
child_pids="$child_pids $!"

echo "Populating cache. In order to stop populating cache, please kill the processes with:"
echo "  kill $child_pids"
