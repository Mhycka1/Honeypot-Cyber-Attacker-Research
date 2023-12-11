import re
from scipy.stats import kruskal

# Function to parse the log file and extract relevant information
def parse_log_file(file_path):
    data = {"mp4": [], "mp3": [], "text": [], "no": []}

    with open(file_path, 'r') as file:
        for line in file:
            match_data = re.match(r'(\d+) (\w+)', line)
            if match_data:
                value = int(match_data.group(1))
                data_type = match_data.group(2)
                data[data_type].append(value)

    return data

# Function to perform Kruskal-Wallis test
def perform_kruskal_wallis(data):
    result_statistic, result_pvalue = kruskal(data["mp4"], data["mp3"], data["text"], data["no"])
    return result_statistic, result_pvalue

# Example usage
log_file_path = 'C:\\Users\\Michael\\Desktop\\HACS200\\commandsUsedData Dec 2'
parsed_data = parse_log_file(log_file_path)

# Check if there is enough data to perform the test
if all(len(values) >= 3 for values in parsed_data.values()):
    kruskal_statistic, kruskal_pvalue = perform_kruskal_wallis(parsed_data)
    print("Kruskal-Wallis Test Result:")
    print(f"Statistic: {kruskal_statistic}")
    print(f"P-value: {kruskal_pvalue}")
else:
    print("Not enough data to perform the Kruskal-Wallis test.")
