import os
import subprocess


def run_vivado_tcl_script():
    # Run the Vivado TCL script
    subprocess.run(
        [
            "vivado",
            "-mode",
            "batch",
            "-nolog",
            "-nojournal",
            "-source",
            "clock_frequencies.tcl",
        ]
    )


def update_queue_size(file_path, new_size):
    # Read the file content
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Update the QUEUE_SIZE parameter
    with open(file_path, "w") as file:
        for line in lines:
            if "parameter QUEUE_SIZE" in line:
                line = f"    parameter QUEUE_SIZE = {new_size},  // Number of slots in each queue\n"
            file.write(line)


def main():
    verilog_file_path = (
        "zhou_2020_hwpq.srcs/sources_1/imports/my_hwpq/open_list_queue.sv"
    )

    # Check the directory to see if there are log files, if so, erase them all
    log_dir = "zhou_2020_hwpq.logs"
    for file_name in os.listdir(log_dir):
        if file_name.startswith("pq_analysis_") and file_name.endswith(".txt"):
            file_path = os.path.join(log_dir, file_name)
            os.remove(file_path)

    # Create a log file for the default QUEUE_SIZE
    log_file_path = "zhou_2020_hwpq.logs/pq_analysis_4.txt"
    with open(log_file_path, "w") as log_file:
        log_file.write(f"Log for QUEUE_SIZE = 4\n")
        log_file.write(f"\n")

    # Initial run with default QUEUE_SIZE
    run_vivado_tcl_script()

    # List of new QUEUE_SIZE values
    queue_sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

    for i, size in enumerate(queue_sizes):
        # Start checking after index 0 since there's no previous size
        if i >= 1:
            # Get the size number that is 1 index before the current one
            last_size = queue_sizes[i - 1]
            last_log_file_path = f"zhou_2020_hwpq.logs/pq_analysis_{last_size}.txt"

            # Check the last log file for LUT Utilization
            with open(last_log_file_path, "r") as last_log_file:
                last_log_lines = last_log_file.readlines()

            # Check the first paragraph for LUT Utilization
            for line in last_log_lines:
                if "LUTs Util%" in line:
                    lut_utilization = float(line.split(":")[2].strip().split(" ")[0])
                    if lut_utilization > 50.0:
                        print(
                            f"LUT Utilization has gone above 50% ({lut_utilization}%). Exiting script."
                        )
                        break

        # Create a log file for the current QUEUE_SIZE
        log_file_path = f"zhou_2020_hwpq.logs/pq_analysis_{size}.txt"
        with open(log_file_path, "w") as log_file:
            log_file.write(f"Log for QUEUE_SIZE = {size}\n")
            log_file.write(f"\n")

        # Update the QUEUE_SIZE in the Verilog file
        update_queue_size(verilog_file_path, size)

        # Update the log_file name in the TCL script
        with open("clock_frequencies.tcl", "r") as tcl_file:
            tcl_lines = tcl_file.readlines()

        with open("clock_frequencies.tcl", "w") as tcl_file:
            log_file_updated = False
            for line in tcl_lines:
                if "set log_file" in line and not log_file_updated:
                    line = (
                        f'set log_file "zhou_2020_hwpq.logs/pq_analysis_{size}.txt"\n'
                    )
                    log_file_updated = True
                tcl_file.write(line)

        # Rerun the Vivado TCL script
        run_vivado_tcl_script()


if __name__ == "__main__":
    main()
