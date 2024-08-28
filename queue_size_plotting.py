import matplotlib.pyplot as plt


def parse_data_from_file(file_path):
    """
    Parse frequency, synthesis time, implementation time, power, WNS, Slice LUTs Util%, Slice Registers Util%, and Achieved Frequency data from a file.

    This function reads a file containing frequency, synthesis time, implementation time, power, WNS, Slice LUTs Util%, Slice Registers Util%, and Achieved Frequency data in the format:
    "Frequency: X MHz -> Synthesis: Ym Zs -> Ws"
    "Frequency: X MHz -> Implementation: Ym Zs -> Ws"
    "Frequency: X MHz -> Power: Y W"
    "Frequency: X MHz -> WNS: Y ns"
    "Frequency: X MHz -> Slice LUTs Util%: Y %"
    "Frequency: X MHz -> Slice Registers Util%: Y %"
    "Frequency: X MHz -> Achieved Frequency: Y MHz"
    It extracts these values and returns them as separate lists.

    Args:
        file_path (str): The path to the file containing the data.

    Returns:
        tuple: A tuple containing eight lists:
            - frequencies (list of float): The parsed frequency values in MHz.
            - synthesis_times (list of float): The parsed synthesis times in seconds.
            - implementation_times (list of float): The parsed implementation times in seconds.
            - power_values (list of float): The parsed power values in watts.
            - wns_values (list of float): The parsed WNS values in ns.
            - used_slice_luts (list of float): The parsed Slice LUTs Util% values.
            - used_slice_registers (list of float): The parsed Slice Registers Util% values.
            - achieved_frequencies (list of float): The parsed achieved frequency values in MHz.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file content is not in the expected format.
    """
    frequencies = []
    synthesis_times = []
    implementation_times = []
    power_values = []
    used_slice_luts = []
    wns_values = []
    achieved_frequencies = []

    with open(file_path, "r") as file:
        for line in file:
            if "Frequency" in line and "Synthesis" in line:
                freq_part = line.split("->")[0].strip().split(" ")[1]
                synth_part = line.split("->")[1].strip().split(" ")[1][:-1]
                frequencies.append(float(freq_part))
                synthesis_times.append(float(synth_part))
            elif "Frequency" in line and "Implementation" in line:
                impl_part = line.split("->")[1].strip().split(" ")[1][:-1]
                implementation_times.append(float(impl_part))
            elif "Frequency" in line and "Power" in line:
                power_part = line.split("->")[1].strip().split(" ")[1]
                power_values.append(float(power_part))
            elif "Frequency" in line and "WNS" in line:
                wns_part = line.split("->")[1].strip().split(" ")[1]
                wns_values.append(float(wns_part))
            elif "Frequency" in line and "LUTs Util%" in line:
                luts_part = line.split("->")[1].strip().split(" ")[2]
                used_slice_luts.append(float(luts_part))
            elif "Frequency" in line and "Achieved Frequency" in line:
                achieved_freq_part = line.split("->")[1].strip().split(" ")[2]
                achieved_frequencies.append(float(achieved_freq_part))

    return (
        frequencies,
        synthesis_times,
        implementation_times,
        power_values,
        wns_values,
        used_slice_luts,
        achieved_frequencies,
    )


# File path placeholder, this would be the path to the user's text file
file_path = (
    "/home/charlie-wu/Workspace/zhou_2020_hwpq/zhou_2020_hwpq.logs/pq_analysis_32.txt"
)

# Parse the data from the file
(
    frequencies,
    synthesis_times,
    implementation_times,
    power_values,
    wns_values,
    used_slice_luts,
    achieved_frequencies,
) = parse_data_from_file(file_path)

# Plotting all metrics in a single figure with 4 subplots
fig, axs = plt.subplots(3, 2, figsize=(14, 10))

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

# Plotting Frequency vs Used Slice LUTs Percent
axs[2, 0].plot(frequencies, used_slice_luts, marker="o")
axs[2, 0].set_xlabel("Frequency (MHz)")
axs[2, 0].set_ylabel("Used Slice LUTs Percent (%)")
axs[2, 0].set_title("Used Slice LUTs Percent vs Frequency")
axs[2, 0].grid(True)

# Plotting Frequency vs Achieved Frequency
axs[2, 1].plot(frequencies, achieved_frequencies, marker="o")
axs[2, 1].set_xlabel("Frequency (MHz)")
axs[2, 1].set_ylabel("Achieved Frequency (MHz)")
axs[2, 1].set_title("Achieved Frequency vs Frequency")
axs[2, 1].grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.savefig("zhou_2020_hwpq.plots/new_queue_size_plot.png")
