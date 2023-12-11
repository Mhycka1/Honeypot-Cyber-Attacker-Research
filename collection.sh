#!/bin/bash

#calls a script to filter out files that haven't been entered
echo "filtering log files now"

/home/student/file_filter

cat /home/student/data/filteredlogs | grep text > /home/student/textLogs
cat /home/student/data/filteredlogs | grep mp4 > /home/student/mp4Logs
cat /home/student/data/filteredlogs | grep mp3 > /home/student/mp3Logs
cat /home/student/data/filteredlogs | grep no_files > /home/student/noFilesLogs

#this stuff is untouched
file=$( cat /home/student/fileNames )

for logType in $file
do
  currFile=$( cat $logType )

  # Determine the type based on the current log file
  if echo "$currFile" | grep -q "text"; then
    file_type="text"
  elif echo "$currFile" | grep -q "mp4"; then
    file_type="mp4"
  elif echo "$currFile" | grep -q "mp3"; then
    file_type="mp3"
  elif echo "$currFile" | grep -q "no_files"; then
    file_type="no"
  fi

  echo "Collecting data for type: $file_type"
  for mitmlog in $currFile
  do
    /home/student/par "/home/student/data/logs/$mitmlog" "$file_type"
    /home/student/malware_collector "/home/student/data/logs/$mitmlog" "$file_type"
  done
done

echo "done"

exit 0
