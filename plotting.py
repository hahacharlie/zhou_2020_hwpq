import matplotlib.pyplot as plt

"""
function to parse wns vs. frequency
"""
def parse_data_from_file(file_path):
    frequencies = []
    wns_values = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split('->')
            freq_part = parts[0].strip().split(' ')[1]
            wns_part = parts[1].strip().split(' ')[1]

            frequencies.append(float(freq_part))
            wns_values.append(float(wns_part))

    return frequencies, wns_values

# File path placeholder, this would be the path to the user's text file
file_path = '/home/charlie/Workspace/pq_research/vivado_dir/zhou_2020_hwpq/wns_results.txt'

# Parse the data from the file
frequencies, wns_values = parse_data_from_file(file_path)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(frequencies, wns_values, marker='o')
plt.xlabel('Frequency (MHz)')
plt.ylabel('WNS (ns)')
plt.title('WNS vs Frequency')
plt.grid(True)
plt.show()
