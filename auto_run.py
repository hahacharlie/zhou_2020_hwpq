import os
import subprocess


def run_vivado_tcl_script():
    # Run the Vivado TCL script
    subprocess.run(["vivado", "-mode", "tcl", "-source", "clock_frequencies.tcl"])


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
    tcl_script_path = "clock_frequencies.tcl"
    verilog_file_path = (
        "zhou_2020_hwpq.srcs/sources_1/imports/my_hwpq/open_list_queue.sv"
    )

    # Initial run with default QUEUE_SIZE
    run_vivado_tcl_script()

    # List of new QUEUE_SIZE values
    queue_sizes = [8, 16, 32, 64, 128, 256, 512, 1024]

    for size in queue_sizes:
        # Update the QUEUE_SIZE in the Verilog file
        update_queue_size(verilog_file_path, size)

        # Rerun the Vivado TCL script
        run_vivado_tcl_script()


if __name__ == "__main__":
    main()
