import matplotlib.pyplot as plt


def parse_data_from_file(file_path):
    """
    Parse frequency, synthesis time, implementation time, power, and Worst Negative Slack (WNS) data from a file.

    This function reads a file containing frequency, synthesis time, implementation time, power, and WNS data in the format:
    "Frequency: X MHz -> Synthesis: Y s"
    "Frequency: X MHz -> Implementation: Y s"
    "Frequency: X MHz -> Power: Y W"
    "Frequency: X MHz -> WNS: Y ns"
    It extracts these values and returns them as separate lists.

    Args:
        file_path (str): The path to the file containing the data.

    Returns:
        tuple: A tuple containing five lists:
            - frequencies (list of float): The parsed frequency values in MHz.
            - synthesis_times (list of float): The parsed synthesis times in seconds.
            - implementation_times (list of float): The parsed implementation times in seconds.
            - power_values (list of float): The parsed power values in watts.
            - wns_values (list of float): The parsed WNS values in ns.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file content is not in the expected format.
    """
    frequencies = []
    synthesis_times = []
    implementation_times = []
    power_values = []
    wns_values = []

    with open(file_path, "r") as file:
        for line in file:
            if "Frequency" in line and "Synthesis" in line:
                freq_part = line.split("->")[0].strip().split(" ")[1]
                synth_part = line.split("->")[1].strip().split(" ")[1]
                frequencies.append(float(freq_part))
                synthesis_times.append(float(synth_part))
            elif "Frequency" in line and "Implementation" in line:
                impl_part = line.split("->")[1].strip().split(" ")[1]
                implementation_times.append(float(impl_part))
            elif "Frequency" in line and "Power" in line:
                power_part = line.split("->")[1].strip().split(" ")[1]
                power_values.append(float(power_part))
            elif "Frequency" in line and "WNS" in line:
                wns_part = line.split("->")[1].strip().split(" ")[1]
                wns_values.append(float(wns_part))

    return frequencies, synthesis_times, implementation_times, power_values, wns_values


# File path placeholder, this would be the path to the user's text file
file_path = (
    "/home/charlie/Workspace/pq_research/vivado_dir/zhou_2020_hwpq/pq_analysis.txt"
)

# Parse the data from the file
frequencies, synthesis_times, implementation_times, power_values, wns_values = (
    parse_data_from_file(file_path)
)

# Plotting all metrics in a single figure with 4 subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Plotting Frequency vs Synthesis Time
axs[0, 0].plot(frequencies, synthesis_times, marker="o")
axs[0, 0].set_xlabel("Frequency (MHz)")
axs[0, 0].set_ylabel("Synthesis Time (s)")
axs[0, 0].set_title("Synthesis Time vs Frequency")
axs[0, 0].grid(True)

# Plotting Frequency vs Implementation Time
axs[0, 1].plot(frequencies, implementation_times, marker="o")
axs[0, 1].set_xlabel("Frequency (MHz)")
axs[0, 1].set_ylabel("Implementation Time (s)")
axs[0, 1].set_title("Implementation Time vs Frequency")
axs[0, 1].grid(True)

# Plotting Frequency vs Power
axs[1, 0].plot(frequencies, power_values, marker="o")
axs[1, 0].set_xlabel("Frequency (MHz)")
axs[1, 0].set_ylabel("Power (W)")
axs[1, 0].set_title("Power vs Frequency")
axs[1, 0].grid(True)

# Plotting Frequency vs WNS
axs[1, 1].plot(frequencies, wns_values, marker="o")
axs[1, 1].set_xlabel("Frequency (MHz)")
axs[1, 1].set_ylabel("WNS (ns)")
axs[1, 1].set_title("WNS vs Frequency")
axs[1, 1].grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
