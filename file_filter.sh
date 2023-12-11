#!/bin/bash

# Set the directory path containing the log files
log_directory="/home/student/data/logs/*"

# Specify the phrase to search for in the log files
search_phrase="Attacker authenticated and is inside container"

# Specify the output file for filtered logs
output_file="/home/student/data/filteredlogs"

# Loop through each log file in the directory
for log_file in $log_directory; do
    # Check if the log file contains the search phrase
    if grep -q "$search_phrase" "$log_file"; then

      real_name=$(basename "$log_file")

        # If the phrase is found, append the log file name to the output file
        echo "$real_name" >> "$output_file"
    fi
done

echo "Filtered logs have been saved to $output_file"
