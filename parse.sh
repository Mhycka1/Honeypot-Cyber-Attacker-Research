#!/bin/bash

log_file="$1"  # Get the log file as the first argument
file_type="$2"

if [ -z "$log_file" ]; then
    echo "Usage: $0 <log_file>"
    exit 1
fi

command_count=0
time_spent=0

while IFS= read -r line; do
    if [[ $line == *"Attacker authenticated and is inside container"* ]]; then
        start_time=$(date -d "$(echo "$line" | awk '{print $1 " " $2}' | sed 's/\[//')" "+%s.%N")
    elif [[ $line == *"[EXEC] Noninteractive mode attacker command:"* ]]; then
        ((command_count++))
    fi
    if [[ $line == *"Attacker closed connection"* ]]; then
        end_time=$(date -d "$(echo "$line" | awk '{print $1 " " $2}' | sed 's/\[//')" "+%s.%N")
        time_spent=$(bc <<< "$time_spent + ($end_time - $start_time)")
    fi
done < $log_file

printf "%d %s\n" "$command_count" "$file_type" >> commandsUsedData
printf "%.3f %s\n" "$time_spent" "$file_type" >> timeSpentData
