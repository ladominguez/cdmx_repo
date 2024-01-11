#!/bin/sh
#

input='DetectedFinal_All_20230501_20230531.dat'
output=$(echo $input | sed 's/dat/csv/g')
grep -v Date $input  | awk '{print $2, $1}'  | sed 's/\///g' | awk '{printf("DetectedFinal_%s_%02d.jpg\n",$1,$2)}' > filename.tmp
grep -v Date $input | awk '{print $2 "," $3 "," $4 "," $5 "," $6 "," $7 "," $8 "," $9}' | nl -s "," -w 3 > data.tmp
echo "No.,Date,time,latitutde,longitude,depth,magnitude,cc,MAD,waveforms" > $output
paste -d, data.tmp filename.tmp >> $output


rm filename.tmp data.tmp

