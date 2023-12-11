import re
import matplotlib.pyplot as plt
import pandas as pd


# Function to parse the log file and extract relevant information
def parse_log_file(file_path):
    data = {"mp4": {"time_spent": [], "total_lines": 0},
            "mp3": {"time_spent": [], "total_lines": 0},
            "text": {"time_spent": [], "total_lines": 0},
            "no": {"time_spent": [], "total_lines": 0}}

    with open(file_path, 'r') as file:
        for line in file:
            match_time = re.match(r'([0-9.]+) (\w+)', line)
            if match_time:
                time_spent = float(match_time.group(1))
                data_type = match_time.group(2)
                data[data_type]["time_spent"].append(time_spent)
            data[data_type]["total_lines"] += 1

    return data


# Function to create a boxplot from the parsed data
def create_boxplot(parsed_data):
    labels = list(parsed_data.keys())
    data_values = [parsed_data[label]["time_spent"] for label in labels]

    fig, ax = plt.subplots()

    # Plot the boxplot
    boxplot = ax.boxplot(data_values, labels=labels)

    # Plot the average line
    averages = [sum(times) / len(times) for times in data_values]
    ax.scatter(labels, averages, color='green', marker='o', label='Average')

    # Annotate the total number of lines for each type
    for label in labels:
        total_line = parsed_data[label]["total_lines"]
        ax.text(labels.index(label) + 1, total_line + 1, str(total_line), ha='center', va='bottom', color='blue')

    plt.title('Time Spent Inside Each Container Type')
    plt.xlabel('Honey Type')
    plt.ylabel('Time Spent (seconds)')
    plt.legend()

    # Print total time spent, total zero time spent, and overall total time spent for each data type
    for label in labels:
        times = parsed_data[label]["time_spent"]
        total_time_spent = sum(times)
        total_zero_time_spent = times.count(0)

        print(f"Statistics for {label}:")
        print(f"  Total seconds spent: {total_time_spent:.3f} seconds")
        print(f"  Total times with 0.000 seconds spent: {total_zero_time_spent}")

        if times:  # Avoid division by zero for empty lists
            statistics = pd.Series(times).describe()
            print(f"  Min: {statistics['min']:.3f}")
            print(f"  25%: {statistics['25%']:.3f}")
            print(f"  Median: {statistics['50%']:.3f}")
            print(f"  75%: {statistics['75%']:.3f}")
            print(f"  Max: {statistics['max']:.3f}")
            print(f"  Mean: {statistics['mean']:.3f}")

        print()

    overall_total_time_spent = sum(sum(times) for times in data_values)
    print(f"Overall total time spent: {overall_total_time_spent:.3f} seconds")
    plt.show()

    # Flush the output
    import sys
    sys.stdout.flush()


# Example usage
log_file_path = 'C:\\Users\\Michael\\Desktop\\HACS200\\timeSpentData Dec 2'
parsed_data = parse_log_file(log_file_path)
create_boxplot(parsed_data)
