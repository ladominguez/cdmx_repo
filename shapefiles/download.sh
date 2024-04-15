#!/bin/bash
# Author: Diego Valle-Jones
# Web: http://www.diegovalle.net
# Purpose: Download shapefiles of manzanas (blocks), agebs (census areas), ejes
# viales (streets), interesting areas and a whole bunch of other stuff

# Note that you'll need a recent version of innoextract
# http://constexpr.org/innoextract/, one that can work with files
# created by version 5.5 of Inno Setup, the one in Ubuntu universe is
# not recent enough.  The version available at
# https://launchpad.net/~arx/+archive/release is good enough.

# sudo add-apt-repository ppa:arx/release
# sudo apt-get update
# sudo apt-get install innoextract
# chmod +x download-census-shp.sh

# As of now, this script has not been tested on Windows and Mac
# systems, only on Ubuntu. The script will create a directory
# called 'shps' where all the shapefiles are located, if something
# goes wrong when dowloading be sure to delete it and try again

set -e
# Projection compatible with Google Maps
PROJECTION="+proj=longlat +ellps=WGS84 +no_defs +towgs84=0,0,0"
# wget command
CURL="curl -fsS --retry 3  "

# The list of shapefiles of manzanas, agebs, etc
declare -a files=("ageb_urb" "eje_vial" "estatal" "loc_rur" "loc_urb"
    "manzanas" "municipal" "servicios_a" "servicios_l" "servicios_p")

# List of files for the national (not state level) data
declare -a national_files=("estatal" "loc_urb" "nacional" "loc_rur" "municipal" "zonas_metro")

# State abbreviations
declare -a states=("national" "ags" "bc" "bcs" "camp" "coah" "col" "chis" "chih"
    "df" "dgo" "gto" "gro" "hgo" "jal" "mex" "mich" "mor" "nay" "nl" "oax"
    "pue" "qro" "qroo" "slp" "sin" "son" "tab" "tamps" "tlax" "ver" "yuc"
    "zac");

# Use gdal to reproject, and then rename the shapefiles to include
# a user friendly abbreviation instead of a number
# First argument: directory of shapefiles shps/state_abbreviation
# Second argument: the state abbreviation
# TODO: convert the encoding from windows-1252 to utf-8
function reproject {
  name="$3[@]"
  arr=("${!name}")
  for i in "${arr[@]}"
  do
    ogr2ogr "$1/$2_$i.shp" "$1"/$i.shp -t_srs "$PROJECTION"
    rm "$1"/$i*
  done
  # rename the extra census data that comes with the shapefiles
  cd "$1/tablas"
  rename "s/^cpv2010/$2_cpv2010/" cpv2010*
  rm -rf cpv2010*
  cd ../../..
}

# For each of the 32 states (and national data == 00) download and reproject
for i in $(seq 0 32);
do
   # The INEGI uses a leading zero for all one digit numbers
   if [ "$i" -lt 10 ]
   then
     FILENUM="0$i"
   else
     FILENUM="$i"
   fi
   # download the files from the inegi server. 'idusr' is the id you get
   # when you register at the INEGI (yes, I'm 12 years old)
   $CURL "http://www.inegi.org.mx/est/scince/scince2010.aspx?_file=/est/scince/scince2010/Scince2010_$FILENUM.exe&idusr=80085" -o ${states[$i]}_scince.exe
   # Extract the shapefiles from the inno setup installer windows
   # executable (note that it doesn't allow you to specify the
   # directory to extract the files)
   innoextract --lowercase --silent ${states[$i]}_scince.exe
   # Create a directory called "shps" to store the shapefiles
   mkdir -p shps/${states[$i]}
   # Copy the shapefiles to the new directory
   cp -r app/"$FILENUM"/* shps/${states[$i]}
   # Delete the temp files from innoextract
   rm -rf app
   rm -rf tmp
   rm -rf ${states[$i]}_scince.exe
   # call the reproject function above
   if [ "$i" -eq 0 ]
   then
     reproject shps/${states[$i]} ${states[$i]} national_files
   else
     reproject shps/${states[$i]} ${states[$i]} files
   fi
   # give the server a rest before downloading the next file
   sleep 20
done

# You could use the code below to merge all the states into one giant
# shapefile of Mexico. Change '_manzanas' to '_agebs' or '_eje_vial' or whatever
#for file in $(find shps -maxdepth 2 -name "*_manzanas.shp"  )
#do
#  ogr2ogr -update -append mexico_manzanas.shp $file  -f "esri shapefile" -nln merge
#done
# Filter attributes (e.g. only include total population in the dbf)
#ogr2ogr -select POB1 mexico_manazanas.shp merge.shp
