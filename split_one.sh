#!/bin/bash
input=$1
i=0
while IFS= read -r line
do
  echo "$line"

  # file1=$line
  echo filelist = [\"$line\"] > filelist.py.$i

  let i=i+1

done < "$input"
