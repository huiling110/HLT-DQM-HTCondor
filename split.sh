#!/bin/bash
input="list"
i=0
j=0
while IFS= read -r line
do
  echo "$line"
  let i=i+1

  if [ $i -eq 1 ]
  then
     file1=$line
  fi

  if [ $i -eq 2 ]
  then
    file2=$line
  fi

  if [ $i -eq 3 ]
  then
    file3=$line
  fi

  if [ $i -eq 4 ]
  then
    file4=$line
  fi

  if [ $i -eq 5 ]
  then
    file5=$line
  fi

  if [ $i -eq 6 ]
  then
    file6=$line
  fi

  if [ $i -eq 7 ]
  then
    file7=$line
  fi

  if [ $i -eq 8 ]
  then
    file8=$line
  fi

  if [ $i -eq 9 ]
  then
    file9=$line
  fi

  if [ $i -eq 10 ]
  then
    file=filelist.py.$j
    file10=$line
cat > $file <<@EOI
filelist = ['$file1',
'$file2',
'$file3',
'$file4',
'$file5',
'$file6',
'$file7',
'$file8',
'$file9',
'$file10']
@EOI
    i=0
    let j=j+1
  fi

done < "$input"
