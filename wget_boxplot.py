import re
import matplotlib.pyplot as plt
import pandas as pd

# Function to parse the log file and extract relevant information
def parse_log_file(file_path):
    data = {"mp4": {"commands": [], "total": 0},
            "mp3": {"commands": [], "total": 0},
            "text": {"commands": [], "total": 0},
            "no": {"commands": [], "total": 0}}

    with open(file_path, 'r') as file:
        for line in file:
            match_command = re.match(r'(\d+) (\w+)', line)
            if match_command:
                num_commands = int(match_command.group(1))
                data_type = match_command.group(2)
                data[data_type]["commands"].append(num_commands)
                data[data_type]["total"] += num_commands

    return data

# Function to create a boxplot from the parsed data
def create_boxplot(parsed_data):
    labels = list(parsed_data.keys())
    data_values = [parsed_data[label]["commands"] for label in labels]

    # Calculate statistics using pandas describe function
    statistics = {label: pd.Series(commands).describe() for label, commands in zip(labels, data_values)}

    for label, stat in statistics.items():
        print(f"Statistics for {label}:")
        print(f"  Max: {int(stat['max'])}")
        print(f"  75%: {int(stat['75%'])}")
        print(f"  Median: {int(stat['50%'])}")
        print(f"  25%: {int(stat['25%'])}")
        print(f"  Min: {int(stat['min'])}")
        print(f"  Mean: {int(stat['mean'])}")
        print(f"  Total Occurrences: {parsed_data[label]['total']}")
        print()

    # Plot the boxplot
    fig, ax = plt.subplots()
    boxplot = ax.boxplot(data_values, labels=labels)
    plt.title('Occurrences of "wget" Command for Each Container Type')
    plt.xlabel('Container Type')
    plt.ylabel('Number of "wget" Commands')
    plt.show()

# Example usage
log_file_path = 'C:\\Users\\Michael\\Desktop\\HACS200\\wgetCommandsData Dec 2'
parsed_data = parse_log_file(log_file_path)
create_boxplot(parsed_data)
