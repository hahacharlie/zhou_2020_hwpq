# Open the project (you may need to adjust the project path)
open_project ./zhou_2020_hwpq.xpr

# Define the design top level and clock signal
set top_module "open_list_queue"
set clock_port "CLK"

set log_file "zhou_2020_hwpq.logs/pq_analysis_256.txt"
set fileId [open $log_file "a"]

# Loop through the list of frequencies
for {set freq 50} {$freq <= 400} {incr freq 10} {

    # Calculate clock period in nanoseconds
    set period_ns [expr 1000.0 / $freq]

    # Reset the previous synthesis result
    reset_run synth_1

    # Start a new synthesis and time how long it takes
    set synth_start_time [clock seconds]
    launch_runs synth_1 -jobs 12
    wait_on_run synth_1
    set synth_end_time [clock seconds]

    # Calculate the synthesis duration
    set synth_duration [expr $synth_end_time - $synth_start_time]
    if {$synth_duration > 60} {
        set minutes [expr int($synth_duration / 60)]
        set seconds [expr $synth_duration % 60]
        set synth_duration "${minutes}m ${seconds}s"
    } else {
        set synth_duration "${synth_duration}s"
    }

    # Open the synthesis result
    open_run synth_1

    # Create a timing constraint
    create_clock -name sys_clk -period $period_ns [get_ports $clock_port]

    # Reset the previous implementation result
    reset_run impl_1

    # Start a new implementation run and time how long it takes
    set impl_start_time [clock seconds]
    launch_runs impl_1 -jobs 12
    wait_on_run impl_1
    set impl_end_time [clock seconds]

    # Calculate the implementation duration
    set impl_duration [expr $impl_end_time - $impl_start_time]
    if {$impl_duration > 60} {
        set minutes [expr int($impl_duration / 60)]
        set seconds [expr $impl_duration % 60]
        set impl_duration "${minutes}m ${seconds}s"
    } else {
        set impl_duration "${impl_duration}s"
    }

    # Open the implementation result
    open_run impl_1

    # Extract the utilization report content
    # report_utilization -file utilization_${freq}.txt

    # Extract the utilization report content
    set utilization_report [report_utilization -return_string]

    # Initialize variables to store the extracted values
    # set clb_luts_util 0.0
    # set clb_registers_util 0.0

    # Extract the Util% of CLB LUTs and CLB Registers from the report
    set in_section_1 0
    foreach line [split $utilization_report "\n"] {
        if {[regexp {^1\. CLB Logic} $line]} {
            set in_section_1 1
        } elseif {[regexp {^\d+\.} $line]} {
            set in_section_1 0
        }

        if {$in_section_1} {
            if {[regexp {\|\s*CLB LUTs\s*\|\s*[0-9]+\s*\|\s*[0-9]+\s*\|\s*[0-9]+\s*\|\s*[0-9]+\s*\|\s*([0-9]+\.[0-9]+)\s*\|} $line match luts_util]} {
                set clb_luts_util $luts_util
            }
            if {[regexp {\|\s*CLB Registers\s*\|\s*[0-9]+\s*\|\s*[0-9]+\s*\|\s*[0-9]+\s*\|\s*[0-9]+\s*\|\s*([0-9]+\.[0-9]+)\s*\|} $line match registers_util]} {
                set clb_registers_util $registers_util
            }
        }
    }

    # Report power summary and get the total on-chip power
    set power_report [report_power -return_string]
    set match [regexp {\|\s*Total On-Chip Power \(W\)\s*\|\s*([0-9\.]+)\s*\|} $power_report full_match total_on_chip_power]

    # Report timing summary and get the Worst Negative Slack (WNS)
    set timing_report [report_timing_summary -delay_type max -significant_digits 3]

    # Extract WNS from the timing summary
    set wns [get_property SLACK [get_timing_paths]]

    # Calculate the achieved frequency using WNS and target frequency with 3 significant digits
    set achieved_frequency [format "%.3f" [expr {1000.0 / ($period_ns - $wns)}]]

    # Print the results to the log file
    puts $fileId "Frequency: ${freq} MHz -> Synthesis: ${synth_duration}"
    puts $fileId "Frequency: ${freq} MHz -> Implementation: ${impl_duration}"
    if ($match) {
        puts $fileId "Frequency: ${freq} MHz -> Power: ${total_on_chip_power} W"
    } else {
        puts $fileId "Frequency: ${freq} MHz -> Power: No power report"
    }
    puts $fileId "Frequency: ${freq} MHz -> LUTs Util%: ${clb_luts_util} %"
    puts $fileId "Frequency: ${freq} MHz -> Registers Util%: ${clb_registers_util} %"
    puts $fileId "Frequency: ${freq} MHz -> WNS: ${wns} ns"
    puts $fileId "Frequency: ${freq} MHz -> Achieved Frequency: ${achieved_frequency} MHz"
    puts $fileId "\n"

}

# Close the log file
close $fileId

# Close the project
close_project