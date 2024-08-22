import os
import matplotlib.pyplot as plt


def parse_achieved_frequencies(file_path):
    """
    Parse achieved frequency data from a file.

    This function reads a file containing achieved frequency data in the format:
    "Frequency: X MHz -> Achieved Frequency: Y MHz"
    It extracts these values and returns them as separate lists.

    Args:
        file_path (str): The path to the file containing the data.

    Returns:
        tuple: A tuple containing two lists:
            - frequencies (list of float): The parsed frequency values in MHz.
            - achieved_frequencies (list of float): The parsed achieved frequency values in MHz.
    """
    frequencies = []
    achieved_frequencies = []

    with open(file_path, "r") as file:
        for line in file:
            if "Frequency" in line and "Achieved Frequency" in line:
                freq_part = line.split("->")[0].strip().split(" ")[1]
                achieved_freq_part = line.split("->")[1].strip().split(" ")[2]
                frequencies.append(float(freq_part))
                achieved_frequencies.append(float(achieved_freq_part))

    return frequencies, achieved_frequencies


# Directory containing the log files
log_dir = "zhou_2020_hwpq.logs"

# Dictionary to store data from all files
all_data = {}

# Iterate over all files in the directory
for file_name in sorted(
    os.listdir(log_dir), key=lambda x: int(x.split("_")[-1].split(".")[0])
):
    if file_name.startswith("pq_analysis_") and file_name.endswith(".txt"):
        queue_size = file_name.split("_")[-1].split(".")[0]
        file_path = os.path.join(log_dir, file_name)
        frequencies, achieved_frequencies = parse_achieved_frequencies(file_path)
        all_data[queue_size] = (frequencies, achieved_frequencies)

# Plotting all achieved frequencies in a single figure
plt.figure(figsize=(10, 6))

for queue_size, (frequencies, achieved_frequencies) in all_data.items():
    plt.plot(
        frequencies,
        achieved_frequencies,
        marker="o",
        label=f"QUEUE_SIZE = {queue_size}",
    )

plt.xlabel("Frequency (MHz)")
plt.ylabel("Achieved Frequency (MHz)")
plt.title("Achieved Frequency vs Frequency for Different QUEUE_SIZE")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
