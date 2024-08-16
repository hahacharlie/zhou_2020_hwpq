# Open the project (you may need to adjust the project path)
open_project ./zhou_2020_hwpq.xpr

# Define the design top level and clock signal
set top_module "open_list_queue"
set clock_port "CLK"

# Define a list of frequencies to test in (MHz)
# set frequency_list {25 50 100 120 130 140 150}

# Loop through the list of frequencies
for {set freq 50} {$freq <= 200} {incr freq 5} {

    # Calculate clock period in nanoseconds
    set period_ns [expr 1000.0 / $freq]

    # Update constraints
    # write_xdc -force ./zhou_2020_hwpq.srcs/constrs_1/imports/Downloads/Basys3_Master.xdc

    # Run synthesis and implementation
    reset_run synth_1
    launch_runs synth_1 -jobs 12
    wait_on_run synth_1
    open_run synth_1

    # Create a timing constraint
    create_clock -name sys_clk -period $period_ns [get_ports $clock_port]

    # Run implementation
    reset_run impl_1
    launch_runs impl_1 -jobs 12
    wait_on_run impl_1

    open_run impl_1

    # Report timing summary and get the Worst Negative Slack (WNS)
    set timing_report [report_timing_summary -delay_type max -significant_digits 3]

    # Extract WNS from the timing summary
    set wns [get_property SLACK [get_timing_paths]]

    # Print or log the frequency and the corresponding WNS
    puts "Frequency: ${freq} MHz -> WNS: ${wns} ns"

    # Optionally, you can save the WNS data to a file
    set log_file "wns_results.txt"
    set fileId [open $log_file "a"]
    puts $fileId "Frequency: ${freq} MHz -> WNS: ${wns} ns"
    close $fileId
}

# Close the project
close_project
