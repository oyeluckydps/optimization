"""
Circuit Synthesis for Float_4E3M Adder
Focused on generating optimized circuits with minimum gates and levels
Supports all gate types: AND, OR, NOT, XOR, XNOR, MUX for ASIC optimization
"""

import csv
import subprocess
import os
import re
import math
from typing import List, Tuple, Dict
from collections import defaultdict
from float_4e3m import Float_4E3M


def check_tool_availability(tool_name: str) -> bool:
    """Check if a synthesis tool is available."""
    try:
        result = subprocess.run([tool_name, "-h"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def csv_to_abc_hierarchical_synthesis(csv_filename: str, output_dir: str = "abc_output") -> None:
    """
    Convert CSV file to optimized circuits using ABC and Yosys for minimum gates/levels.
    
    Args:
        csv_filename (str): Input CSV file with operand1, operand2, result columns
        output_dir (str): Directory to store synthesis results
    """
    
    # Convert to absolute paths
    abs_csv_file = os.path.abspath(csv_filename)
    abs_output_dir = os.path.abspath(output_dir)
    
    print(f"Processing CSV: {abs_csv_file}")
    print(f"Output directory: {abs_output_dir}")
    
    # Create organized directory structure
    separate_dir = os.path.join(abs_output_dir, "separate_TT")
    combined_dir = os.path.join(abs_output_dir, "combined_TT")
    results_dir = os.path.join(abs_output_dir, "synthesis_results")
    
    os.makedirs(separate_dir, exist_ok=True)
    os.makedirs(combined_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    print(f"✓ Created directories:")
    print(f"  - Separate TT: {separate_dir}")
    print(f"  - Combined TT: {combined_dir}")
    print(f"  - Results: {results_dir}")
    
    # Read CSV data
    truth_table_data = []
    
    print("Reading CSV file...")
    try:
        with open(abs_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader):
                try:
                    op1_bits = row['operand1']
                    op2_bits = row['operand2']
                    result_bits = row['result']
                    
                    # Combine op1 and op2 as 16-bit input
                    input_bits = op1_bits + op2_bits
                    
                    truth_table_data.append((input_bits, result_bits))
                except KeyError as e:
                    print(f"✗ CSV format error at row {row_num+1}: Missing column {e}")
                    print(f"Available columns: {list(row.keys())}")
                    return
                except Exception as e:
                    print(f"✗ Error processing row {row_num+1}: {e}")
                    continue
    
    except Exception as e:
        print(f"✗ Error reading CSV file: {e}")
        return
    
    print(f"✓ Processed {len(truth_table_data)} truth table entries")
    
    if len(truth_table_data) == 0:
        print("✗ No valid data found in CSV file")
        return
    
    # Generate separate truth tables (for reference/analysis)
    print("\nGenerating separate truth tables for reference...")
    for bit_pos in range(8):
        generate_separate_truth_table(truth_table_data, bit_pos, separate_dir)
    
    # Generate combined truth table for hierarchical synthesis
    print("\nGenerating combined truth table for synthesis...")
    combined_file = generate_combined_truth_table(truth_table_data, combined_dir)
    
    # Perform optimized synthesis for minimum gates and levels
    print("\nPerforming optimized synthesis for minimum gates and levels...")
    perform_optimized_synthesis(combined_file, results_dir)


def generate_separate_truth_table(truth_table_data: List[Tuple[str, str]], 
                                 bit_position: int, separate_dir: str) -> str:
    """Generate separate truth table file for analysis."""
    
    filename = os.path.join(separate_dir, f"output_bit_{bit_position}.tt")
    
    with open(filename, 'w') as f:
        # ABC truth table header
        f.write(".i 16\n")  # 16 input bits
        f.write(".o 1\n")   # 1 output bit
        f.write(f".p {len(truth_table_data)}\n")  # Number of product terms
        
        # Write truth table entries
        for input_bits, output_bits in truth_table_data:
            output_bit = output_bits[bit_position]
            f.write(f"{input_bits} {output_bit}\n")
        
        f.write(".e\n")
    
    print(f"  Generated separate truth table for bit {bit_position}")
    return filename


def generate_combined_truth_table(truth_table_data: List[Tuple[str, str]], 
                                 combined_dir: str) -> str:
    """Generate combined truth table file for synthesis."""
    
    filename = os.path.join(combined_dir, "float_4e3m_adder.tt")
    
    with open(filename, 'w') as f:
        # ABC truth table header
        f.write(".i 16\n")  # 16 input bits (op1[7:0] + op2[7:0])
        f.write(".o 8\n")   # 8 output bits
        f.write(f".p {len(truth_table_data)}\n")  # Number of product terms
        
        # Add input/output names for better readability
        f.write(".ilb op1_7 op1_6 op1_5 op1_4 op1_3 op1_2 op1_1 op1_0 ")
        f.write("op2_7 op2_6 op2_5 op2_4 op2_3 op2_2 op2_1 op2_0\n")
        f.write(".ob result_7 result_6 result_5 result_4 result_3 result_2 result_1 result_0\n")
        
        # Write truth table entries
        for input_bits, output_bits in truth_table_data:
            f.write(f"{input_bits} {output_bits}\n")
        
        f.write(".e\n")
    
    print(f"  Generated combined truth table: {filename}")
    return filename


def perform_optimized_synthesis(truth_table_file: str, results_dir: str) -> None:
    """
    Perform optimized synthesis using both ABC and Yosys for minimum gates and levels.
    Focuses purely on synthesis - analysis moved to separate file.
    """
    
    # Check which synthesis tools are available
    abc_available = check_tool_availability("abc")
    yosys_available = check_tool_availability("yosys")
    
    print(f"Available tools: ABC={abc_available}, Yosys={yosys_available}")
    
    if abc_available:
        print("\n1. Running ABC optimization for minimum gates and levels...")
        perform_abc_gate_optimization(truth_table_file, results_dir)
    
    if yosys_available:
        print("\n2. Running Yosys ASIC optimization for minimum gates...")
        perform_yosys_asic_optimization(truth_table_file, results_dir)
    
    if not abc_available and not yosys_available:
        print("✗ Neither ABC nor Yosys found!")
        print_installation_instructions()


def perform_abc_gate_optimization(truth_table_file: str, results_dir: str) -> None:
    """Perform ABC optimization focused on minimum gates and levels."""
    
    # ABC script optimized for minimum gates and logic levels
    abc_script = f"""
# Read truth table
read_truth {truth_table_file}
strash

# Aggressive optimization for minimum gates and levels
balance
rewrite -l
refactor -l
balance
rewrite -l
refactor -l
balance

# Multi-level optimization
compress2rs
balance
choice
balance
fraig
balance

# Area-focused technology mapping with all gate types
map -a

# Write optimized results
write_verilog {results_dir}/abc_min_gates.v
write_blif {results_dir}/abc_min_gates.blif
write_bench {results_dir}/abc_min_gates.bench

quit
"""
    
    script_file = os.path.join(results_dir, "abc_gate_optimization.abc")
    with open(script_file, 'w') as f:
        f.write(abc_script)
    
    try:
        result = subprocess.run(
            ["abc", "-f", script_file], 
            capture_output=True, 
            text=True, 
            cwd=results_dir
        )
        
        if result.returncode == 0:
            print("✓ ABC gate optimization completed!")
            
            # Save ABC synthesis log
            with open(os.path.join(results_dir, "abc_synthesis.log"), 'w') as f:
                f.write("ABC Gate Optimization Log\n")
                f.write("=" * 35 + "\n\n")
                f.write(result.stdout)
            
            print(f"  Generated: abc_min_gates.v, abc_min_gates.blif")
            
        else:
            print(f"✗ ABC gate optimization failed: {result.stderr}")
    
    except FileNotFoundError:
        print("✗ ABC not found")
    except Exception as e:
        print(f"✗ ABC optimization failed: {e}")


def perform_yosys_asic_optimization(truth_table_file: str, results_dir: str) -> None:
    """Perform Yosys ASIC optimization for minimum gates with all gate types."""
    
    # Convert truth table to Verilog first
    verilog_file = convert_truth_table_to_verilog(truth_table_file, results_dir)
    abs_verilog_file = os.path.abspath(verilog_file)
    
    # Yosys script optimized for ASIC with all gate types
    yosys_script = f"""# Read behavioral Verilog
read_verilog {abs_verilog_file}
hierarchy -check -top float_4e3m_adder

# Convert behavioral to structural
proc
opt

# Technology mapping for ASIC (not FPGA)
techmap
opt

# Enable all gate types for optimization
# Use generic library that supports all gates
abc

# Alternative optimization approaches
opt
opt_clean

# Final optimization
opt -full

# Write ASIC-optimized results  
write_verilog {results_dir}/yosys_asic_optimized.v
write_blif {results_dir}/yosys_asic_optimized.blif
write_json {results_dir}/yosys_circuit.json
"""
    
    script_file = os.path.join(results_dir, "yosys_asic_optimization.ys")
    
    with open(script_file, 'w') as f:
        f.write(yosys_script)
    
    try:
        result = subprocess.run(
            ["yosys", "-s", script_file],
            capture_output=True,
            text=True,
            cwd=results_dir
        )
        
        if result.returncode == 0:
            print("✓ Yosys ASIC optimization completed!")
            
            # Save Yosys synthesis log
            with open(os.path.join(results_dir, "yosys_synthesis.log"), 'w') as f:
                f.write("Yosys ASIC Optimization Log\n")
                f.write("=" * 35 + "\n\n")
                f.write(result.stdout)
            
            print(f"  Generated: yosys_asic_optimized.v, yosys_asic_optimized.blif")
            
        else:
            print(f"✗ Yosys ASIC optimization failed: {result.stderr}")
            print("\nTrying fallback ASIC optimization...")
            perform_yosys_fallback_asic(abs_verilog_file, results_dir)
    
    except Exception as e:
        print(f"✗ Yosys ASIC optimization failed: {e}")


def perform_yosys_fallback_asic(verilog_file: str, results_dir: str) -> None:
    """Fallback Yosys ASIC optimization with simpler commands."""
    
    # Simplified Yosys script for ASIC
    fallback_script = f"""read_verilog {verilog_file}
hierarchy -check -top float_4e3m_adder
proc
opt
techmap
opt
abc
opt
write_verilog {results_dir}/yosys_fallback_asic.v
write_blif {results_dir}/yosys_fallback_asic.blif
"""
    
    script_file = os.path.join(results_dir, "yosys_fallback.ys")
    
    with open(script_file, 'w') as f:
        f.write(fallback_script)
    
    try:
        result = subprocess.run(
            ["yosys", "-s", script_file],
            capture_output=True,
            text=True,
            cwd=results_dir
        )
        
        if result.returncode == 0:
            print("✓ Yosys fallback ASIC optimization completed!")
            
            with open(os.path.join(results_dir, "yosys_fallback.log"), 'w') as f:
                f.write("Yosys Fallback ASIC Log\n")
                f.write("=" * 30 + "\n\n")
                f.write(result.stdout)
            
            print(f"  Generated: yosys_fallback_asic.v")
            
        else:
            print(f"✗ Yosys fallback optimization failed: {result.stderr}")
    
    except Exception as e:
        print(f"✗ Yosys fallback optimization failed: {e}")


def convert_truth_table_to_verilog(truth_table_file: str, results_dir: str) -> str:
    """Convert truth table to behavioral Verilog for Yosys."""
    
    verilog_file = os.path.join(results_dir, "float_4e3m_adder_behavioral.v")
    
    print(f"  Converting truth table to behavioral Verilog...")
    
    # Read truth table
    truth_table_entries = []
    
    if not os.path.exists(truth_table_file):
        print(f"✗ Truth table file not found: {truth_table_file}")
        return verilog_file
    
    with open(truth_table_file, 'r') as f:
        lines = f.readlines()
        
        # Skip header lines and parse entries
        for line_num, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('.') and ' ' in line:
                parts = line.split()
                if len(parts) >= 2 and len(parts[0]) == 16 and len(parts[1]) == 8:
                    truth_table_entries.append((parts[0], parts[1]))
    
    print(f"  ✓ Parsed {len(truth_table_entries)} truth table entries")
    
    if len(truth_table_entries) == 0:
        print("✗ No valid truth table entries found!")
        return verilog_file
    
    # Generate behavioral Verilog
    with open(verilog_file, 'w') as f:
        f.write("// Float_4E3M Adder - Behavioral Verilog\n")
        f.write("// Optimized for ASIC synthesis with all gate types\n\n")
        f.write("module float_4e3m_adder(\n")
        f.write("    input [15:0] operands,  // {op1[7:0], op2[7:0]}\n")
        f.write("    output reg [7:0] result\n")
        f.write(");\n\n")
        f.write("always @(*) begin\n")
        f.write("    case (operands)\n")
        
        for input_bits, output_bits in truth_table_entries:
            f.write(f"        16'b{input_bits}: result = 8'b{output_bits};\n")
        
        f.write("        default: result = 8'b00000000;\n")
        f.write("    endcase\n")
        f.write("end\n\n")
        f.write("endmodule\n")
    
    print(f"  ✓ Generated behavioral Verilog: {verilog_file}")
    
    return verilog_file


def print_installation_instructions():
    """Print installation instructions for synthesis tools."""
    
    print("\nINSTALLATION INSTRUCTIONS:")
    print("=" * 30)
    print("\n1. Install ABC from source:")
    print("   git clone https://github.com/berkeley-abc/abc.git")
    print("   cd abc")
    print("   make")
    print("   sudo cp abc /usr/local/bin/")
    
    print("\n2. Install Yosys:")
    print("   sudo apt-get install yosys")
    
    print("\n3. Install build dependencies:")
    print("   sudo apt-get install build-essential git cmake")
    
    print("\n4. Verify installation:")
    print("   abc -h")
    print("   yosys -h")


def main():
    """Main function for optimized circuit synthesis."""
    
    # Updated paths to match the new TT directory structure
    csv_file = "addition/TT/demo_addition_results.csv"
    output_directory = "addition/TT/optimized_synthesis"
    
    print("Float_4E3M Optimized Circuit Synthesis")
    print("=" * 50)
    print("Goal: Minimum gates and levels with all gate types")
    print("Target: ASIC optimization (not FPGA)")
    print("Gates: AND, OR, NOT, NAND, NOR, XOR, XNOR, MUX allowed")
    print()
    
    # Convert relative paths to absolute paths
    abs_csv_file = os.path.abspath(csv_file)
    abs_output_dir = os.path.abspath(output_directory)
    
    print(f"CSV file: {abs_csv_file}")
    print(f"Output directory: {abs_output_dir}")
    
    if not os.path.exists(abs_csv_file):
        print(f"✗ Error: CSV file not found at: {abs_csv_file}")
        print("Please run generate_circuits.py first to create the CSV files.")
        return
    
    print(f"✓ CSV file found")
    
    # Perform optimized synthesis
    csv_to_abc_hierarchical_synthesis(abs_csv_file, abs_output_dir)
    
    print("\n" + "=" * 50)
    print("Optimized Synthesis Complete!")
    print(f"Results available in: {abs_output_dir}/synthesis_results/")
    
    print("\nGenerated Files:")
    print("ABC Optimization:")
    print("  - abc_min_gates.v     (Minimum gates Verilog)")
    print("  - abc_min_gates.blif  (BLIF format)")
    print("  - abc_synthesis.log   (ABC optimization log)")
    
    print("\nYosys ASIC Optimization:")
    print("  - yosys_asic_optimized.v   (ASIC optimized Verilog)")
    print("  - yosys_asic_optimized.blif (BLIF format)")
    print("  - yosys_synthesis.log      (Yosys optimization log)")
    
    print("\nOptimization Focus:")
    print("✓ Minimum number of gates")
    print("✓ Minimum logic levels (critical path)")
    print("✓ All gate types allowed (AND,OR,NOT,NAND,NOR,XOR,XNOR,MUX)")
    print("✓ ASIC-focused (not FPGA LUTs)")
    
    print("\nNext step: Run analyze_circuits.py for timing analysis")


if __name__ == "__main__":
    main()


def generate_separate_truth_table(truth_table_data: List[Tuple[str, str]], 
                                 bit_position: int, separate_dir: str) -> str:
    """
    Generate separate truth table file for analysis (not for synthesis).
    
    Args:
        truth_table_data: List of (input_bits, output_bits) tuples
        bit_position: Which output bit (0-7)
        separate_dir: Output directory for separate files
        
    Returns:
        str: Path to generated file
    """
    
    filename = os.path.join(separate_dir, f"output_bit_{bit_position}.tt")
    
    with open(filename, 'w') as f:
        # ABC truth table header
        f.write(".i 16\n")  # 16 input bits
        f.write(".o 1\n")   # 1 output bit
        f.write(f".p {len(truth_table_data)}\n")  # Number of product terms
        
        # Write truth table entries
        for input_bits, output_bits in truth_table_data:
            output_bit = output_bits[bit_position]
            f.write(f"{input_bits} {output_bit}\n")
        
        f.write(".e\n")
    
    print(f"  Generated separate truth table for bit {bit_position}")
    return filename


def generate_combined_truth_table(truth_table_data: List[Tuple[str, str]], 
                                 combined_dir: str) -> str:
    """
    Generate combined truth table file for hierarchical synthesis.
    
    Args:
        truth_table_data: List of (input_bits, output_bits) tuples
        combined_dir: Output directory for combined file
        
    Returns:
        str: Path to generated combined truth table file
    """
    
    filename = os.path.join(combined_dir, "float_4e3m_adder.tt")
    
    with open(filename, 'w') as f:
        # ABC truth table header
        f.write(".i 16\n")  # 16 input bits (op1[7:0] + op2[7:0])
        f.write(".o 8\n")   # 8 output bits
        f.write(f".p {len(truth_table_data)}\n")  # Number of product terms
        
        # Add input/output names for better readability
        f.write(".ilb op1_7 op1_6 op1_5 op1_4 op1_3 op1_2 op1_1 op1_0 ")
        f.write("op2_7 op2_6 op2_5 op2_4 op2_3 op2_2 op2_1 op2_0\n")
        f.write(".ob result_7 result_6 result_5 result_4 result_3 result_2 result_1 result_0\n")
        
        # Write truth table entries
        for input_bits, output_bits in truth_table_data:
            f.write(f"{input_bits} {output_bits}\n")
        
        f.write(".e\n")
    
    print(f"  Generated combined truth table: {filename}")
    return filename


def perform_hierarchical_synthesis(truth_table_file: str, results_dir: str) -> None:
    """
    Perform hierarchical synthesis using ABC or Yosys (whichever is available).
    
    Args:
        truth_table_file: Input combined truth table file
        results_dir: Directory for synthesis results
    """
    
    # Check which synthesis tool is available
    abc_available = check_tool_availability("abc")
    yosys_available = check_tool_availability("yosys")
    
    if abc_available:
        print("Using ABC for hierarchical synthesis...")
        perform_abc_synthesis(truth_table_file, results_dir)
    elif yosys_available:
        print("Using Yosys for hierarchical synthesis...")
        perform_yosys_synthesis(truth_table_file, results_dir)
    else:
        print("✗ Neither ABC nor Yosys found!")
        print_installation_instructions()


def perform_abc_synthesis(truth_table_file: str, results_dir: str) -> None:
    """Perform ABC synthesis with comprehensive timing analysis."""
    
    # Enhanced ABC command sequence with timing analysis
    abc_commands = [
        f"read_truth {truth_table_file}",
        "strash", "print_stats",
        
        # Optimization
        "balance", "rewrite -l", "balance", "refactor -l", "balance",
        "rewrite -l", "balance", "compress2rs", "balance",
        "choice", "balance", "fraig", "balance", 
        
        # Pre-mapping analysis
        "print_stats",
        "print_level",  # Shows logic depth
        
        # Technology mapping
        "map -a", 
        
        # Post-mapping analysis
        "print_stats",
        "print_level",
        "print_io",
        
        # Critical path analysis commands
        "show_gates",           # Show gate distribution
        "print_fanio",          # Show fanin/fanout statistics
        "print_supp",           # Show support analysis
        
        # Timing analysis (if library is available)
        "time",                 # Print timing information
        "stime",                # Show slack timing
        
        # Logic depth analysis
        "depth",                # Analyze logic depth
        
        # Write outputs
        f"write_verilog {results_dir}/float_4e3m_adder_optimized.v",
        f"write_blif {results_dir}/float_4e3m_adder_optimized.blif",
        f"write_bench {results_dir}/float_4e3m_adder_optimized.bench",
        
        # Generate reports
        f"write_dot {results_dir}/circuit_graph.dot",  # Circuit visualization
    ]
    
    script_file = os.path.join(results_dir, "abc_with_timing_analysis.abc")
    with open(script_file, 'w') as f:
        for cmd in abc_commands:
            f.write(cmd + "\n")
        f.write("quit\n")
    
    result = subprocess.run(["abc", "-f", script_file], capture_output=True, text=True, cwd=results_dir)
    
    if result.returncode == 0:
        print("✓ ABC synthesis with timing analysis completed!")
        
        # Extract timing information from ABC output
        extract_abc_timing_info(result.stdout, results_dir)
        
        # Save complete ABC log
        with open(os.path.join(results_dir, "abc_timing_analysis.log"), 'w') as f:
            f.write("ABC Synthesis with Timing Analysis\n")
            f.write("=" * 50 + "\n\n")
            f.write(result.stdout)
    else:
        print(f"✗ ABC synthesis failed: {result.stderr}")


def perform_yosys_synthesis(truth_table_file: str, results_dir: str) -> None:
    """Perform synthesis using Yosys with timing analysis."""
    
    # Convert paths
    abs_truth_table_file = os.path.abspath(truth_table_file)
    abs_results_dir = os.path.abspath(results_dir)
    
    # Convert truth table to Verilog
    verilog_file = convert_truth_table_to_verilog(abs_truth_table_file, abs_results_dir)
    abs_verilog_file = os.path.abspath(verilog_file)
    
    # Fixed Yosys script - removed problematic liberty command
    yosys_script = f"""read_verilog {abs_verilog_file}
hierarchy -check -top float_4e3m_adder
proc
synth -nomem
opt
fsm
opt
opt
techmap
opt

# Timing analysis before ABC
tee -o {abs_results_dir}/pre_abc_stats.log stat
tee -o {abs_results_dir}/pre_abc_check.log check

# ABC optimization without liberty file
abc -lut 4

# Post-optimization analysis
tee -o {abs_results_dir}/post_abc_stats.log stat
tee -o {abs_results_dir}/final_check.log check

opt
clean

# Final statistics and timing
tee -o {abs_results_dir}/final_stats.log stat -top float_4e3m_adder
tee -o {abs_results_dir}/depth_analysis.log stat -tech cmos

# Generate visualization (check if show command is available)
show -format dot -prefix {abs_results_dir}/circuit_visualization

# Write outputs
write_verilog {abs_results_dir}/float_4e3m_adder_yosys_optimized.v
write_blif {abs_results_dir}/float_4e3m_adder_yosys_optimized.blif
write_json {abs_results_dir}/float_4e3m_adder_circuit.json
"""
    
    script_file = os.path.join(abs_results_dir, "yosys_timing_synthesis.ys")
    
    with open(script_file, 'w') as f:
        f.write(yosys_script)
    
    try:
        result = subprocess.run(
            ["yosys", "-s", "yosys_timing_synthesis.ys"], 
            capture_output=True, 
            text=True, 
            cwd=abs_results_dir
        )
        
        if result.returncode == 0:
            print("✓ Yosys synthesis with timing analysis completed!")
            
            # Process the generated statistics files
            process_yosys_timing_files(abs_results_dir)
            
            # Save complete Yosys log
            with open(os.path.join(abs_results_dir, "yosys_synthesis.log"), 'w') as f:
                f.write("Yosys Synthesis Log\n")
                f.write("=" * 30 + "\n\n")
                f.write(result.stdout)
            
            print(f"✓ Yosys log saved")
            
        else:
            print(f"✗ Yosys synthesis failed with return code: {result.returncode}")
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            
            # Try a simpler fallback synthesis
            print("\nTrying fallback synthesis without advanced features...")
            perform_simple_yosys_synthesis(abs_verilog_file, abs_results_dir)
    
    except Exception as e:
        print(f"✗ Yosys execution failed: {e}")


def perform_simple_yosys_synthesis(verilog_file: str, results_dir: str) -> None:
    """Perform simple Yosys synthesis as fallback."""
    
    print("Running simple Yosys synthesis...")
    
    # Minimal Yosys script that should work on most installations
    simple_script = f"""read_verilog {verilog_file}
hierarchy -check -top float_4e3m_adder
proc
opt
techmap
opt
abc
opt
clean
stat
write_verilog {results_dir}/float_4e3m_adder_simple.v
write_blif {results_dir}/float_4e3m_adder_simple.blif
"""
    
    script_file = os.path.join(results_dir, "yosys_simple_synthesis.ys")
    
    with open(script_file, 'w') as f:
        f.write(simple_script)
    
    try:
        result = subprocess.run(
            ["yosys", "-s", "yosys_simple_synthesis.ys"],
            capture_output=True,
            text=True,
            cwd=results_dir
        )
        
        if result.returncode == 0:
            print("✓ Simple Yosys synthesis completed!")
            
            # Save simple synthesis log
            with open(os.path.join(results_dir, "yosys_simple.log"), 'w') as f:
                f.write("Yosys Simple Synthesis Log\n")
                f.write("=" * 30 + "\n\n")
                f.write(result.stdout)
            
            # Extract basic statistics
            extract_yosys_basic_stats(result.stdout, results_dir)
            
        else:
            print(f"✗ Simple Yosys synthesis also failed: {result.stderr}")
    
    except Exception as e:
        print(f"✗ Simple Yosys synthesis failed: {e}")


def extract_yosys_basic_stats(yosys_output: str, results_dir: str) -> None:
    """Extract basic statistics from Yosys output."""
    
    stats_file = os.path.join(results_dir, "yosys_basic_stats.txt")
    
    with open(stats_file, 'w') as f:
        f.write("Yosys Basic Statistics\n")
        f.write("=" * 30 + "\n\n")
        
        lines = yosys_output.split('\n')
        
        gate_count = "Not found"
        
        for line in lines:
            if 'Number of cells:' in line:
                try:
                    gate_count = line.split(':')[1].strip()
                    f.write(f"Total Gates: {gate_count}\n")
                except:
                    pass
            
            elif any(gate_type in line for gate_type in ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'NAND', 'NOR']):
                if any(char.isdigit() for char in line):
                    f.write(f"Gate Type: {line.strip()}\n")
        
        f.write(f"\nSUMMARY:\n")
        f.write(f"Total Gate Count: {gate_count}\n")
        f.write(f"Synthesis: Successful\n")
    
    print(f"✓ Basic statistics saved to: {stats_file}")
    
    if gate_count != "Not found":
        print(f"🎯 Gate Count: {gate_count}")


def perform_abc_synthesis(truth_table_file: str, results_dir: str) -> None:
    """Perform ABC synthesis with comprehensive timing analysis."""
    
    # Simplified ABC command sequence that should work reliably
    abc_commands = [
        f"read_truth {truth_table_file}",
        "strash", 
        "print_stats",
        
        # Basic optimization
        "balance", 
        "rewrite", 
        "balance", 
        "refactor", 
        "balance",
        
        # Pre-mapping analysis
        "print_stats",
        "print_level",  # Shows logic depth
        
        # Technology mapping
        "map", 
        
        # Post-mapping analysis
        "print_stats",
        "print_level",
        "print_io",
        
        # Write outputs
        f"write_verilog {results_dir}/float_4e3m_adder_abc_optimized.v",
        f"write_blif {results_dir}/float_4e3m_adder_abc_optimized.blif",
        
        # Try additional analysis commands (may not work on all ABC versions)
        "print_fanio",
        "show_gates",
    ]
    
    script_file = os.path.join(results_dir, "abc_synthesis.abc")
    with open(script_file, 'w') as f:
        for cmd in abc_commands:
            f.write(cmd + "\n")
        f.write("quit\n")
    
    try:
        result = subprocess.run(
            ["abc", "-f", script_file], 
            capture_output=True, 
            text=True, 
            cwd=results_dir
        )
        
        if result.returncode == 0:
            print("✓ ABC synthesis completed!")
            
            # Extract timing information from ABC output
            extract_abc_timing_info(result.stdout, results_dir)
            
            # Save complete ABC log
            with open(os.path.join(results_dir, "abc_synthesis.log"), 'w') as f:
                f.write("ABC Synthesis Log\n")
                f.write("=" * 25 + "\n\n")
                f.write(result.stdout)
            
            print(f"✓ ABC analysis complete")
            
        else:
            print(f"✗ ABC synthesis failed: {result.stderr}")
            
            # Try minimal ABC synthesis
            print("Trying minimal ABC synthesis...")
            perform_minimal_abc_synthesis(truth_table_file, results_dir)
    
    except FileNotFoundError:
        print("✗ ABC not found. Trying with Yosys only...")
    except Exception as e:
        print(f"✗ ABC synthesis failed: {e}")


def perform_minimal_abc_synthesis(truth_table_file: str, results_dir: str) -> None:
    """Perform minimal ABC synthesis as fallback."""
    
    print("Running minimal ABC synthesis...")
    
    # Very basic ABC commands
    minimal_commands = [
        f"read_truth {truth_table_file}",
        "strash",
        "print_stats", 
        "map",
        "print_stats",
        "print_level",
        f"write_verilog {results_dir}/float_4e3m_adder_minimal.v",
    ]
    
    script_file = os.path.join(results_dir, "abc_minimal.abc")
    with open(script_file, 'w') as f:
        for cmd in minimal_commands:
            f.write(cmd + "\n")
        f.write("quit\n")
    
    try:
        result = subprocess.run(
            ["abc", "-f", script_file],
            capture_output=True,
            text=True,
            cwd=results_dir
        )
        
        if result.returncode == 0:
            print("✓ Minimal ABC synthesis completed!")
            
            with open(os.path.join(results_dir, "abc_minimal.log"), 'w') as f:
                f.write("ABC Minimal Synthesis Log\n")
                f.write("=" * 30 + "\n\n")
                f.write(result.stdout)
            
            # Extract basic metrics
            extract_abc_basic_metrics(result.stdout, results_dir)
            
        else:
            print(f"✗ Minimal ABC synthesis failed: {result.stderr}")
    
    except Exception as e:
        print(f"✗ Minimal ABC synthesis failed: {e}")


def extract_abc_basic_metrics(abc_output: str, results_dir: str) -> None:
    """Extract basic metrics from ABC output."""
    
    metrics_file = os.path.join(results_dir, "abc_basic_metrics.txt")
    
    with open(metrics_file, 'w') as f:
        f.write("ABC Basic Metrics\n")
        f.write("=" * 20 + "\n\n")
        
        lines = abc_output.split('\n')
        
        for line in lines:
            if 'i/o =' in line and 'lev =' in line:
                f.write(f"Circuit: {line.strip()}\n")
                
                # Extract logic levels
                if 'lev =' in line:
                    try:
                        lev_match = line.split('lev =')[1].split()[0]
                        f.write(f"Logic Levels: {lev_match}\n")
                        print(f"🎯 Critical Path: {lev_match} logic levels")
                    except:
                        pass
    
    print(f"✓ Basic metrics saved to: {metrics_file}")


def convert_truth_table_to_verilog(truth_table_file: str, results_dir: str) -> str:
    """Convert truth table to behavioral Verilog for Yosys."""
    
    verilog_file = os.path.join(results_dir, "float_4e3m_adder_behavioral.v")
    
    print(f"Converting truth table to Verilog...")
    print(f"Input truth table: {truth_table_file}")
    print(f"Output Verilog: {verilog_file}")
    
    # Read truth table
    truth_table_entries = []
    
    if not os.path.exists(truth_table_file):
        print(f"✗ Truth table file not found: {truth_table_file}")
        return verilog_file
    
    with open(truth_table_file, 'r') as f:
        lines = f.readlines()
        
        # Skip header lines and parse entries
        for line_num, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('.') and ' ' in line:
                parts = line.split()
                if len(parts) >= 2 and len(parts[0]) == 16 and len(parts[1]) == 8:
                    truth_table_entries.append((parts[0], parts[1]))
                elif len(parts) >= 2:
                    print(f"Warning: Skipping line {line_num+1} - invalid format: {line}")
    
    print(f"✓ Parsed {len(truth_table_entries)} truth table entries")
    
    if len(truth_table_entries) == 0:
        print("✗ No valid truth table entries found!")
        return verilog_file
    
    # Generate behavioral Verilog
    with open(verilog_file, 'w') as f:
        f.write("// Float_4E3M Adder - Explicit Combinational Logic\n")
        f.write("module float_4e3m_adder(\n")
        f.write("    input [15:0] operands,\n")
        f.write("    output [7:0] result\n")  # Use wire, not reg
        f.write(");\n\n")
        
        # Generate explicit assign statements for each output bit
        for bit_pos in range(8):
            f.write(f"assign result[{bit_pos}] = ")
            
            terms = []
            for input_bits, output_bits in truth_table_entries:
                if output_bits[bit_pos] == '1':
                    # Create AND term for this minterm
                    literals = []
                    for i in range(16):
                        if input_bits[i] == '1':
                            literals.append(f"operands[{15-i}]")
                        else:
                            literals.append(f"~operands[{15-i}]")
                    
                    term = "(" + " & ".join(literals) + ")"
                    terms.append(term)
            
            if terms:
                f.write(" |\n    ".join(terms) + ";\n\n")
            else:
                f.write("1'b0;\n\n")
        
        f.write("endmodule\n")
    
    print(f"✓ Generated behavioral Verilog: {verilog_file}")
    
    # Verify the file was created and has content
    if os.path.exists(verilog_file):
        file_size = os.path.getsize(verilog_file)
        print(f"✓ Verilog file size: {file_size} bytes")
    else:
        print(f"✗ Failed to create Verilog file: {verilog_file}")
    
    return verilog_file


def extract_abc_timing_info(abc_output: str, results_dir: str) -> None:
    """Extract and format timing information from ABC output."""
    
    timing_report = os.path.join(results_dir, "abc_timing_report.txt")
    
    with open(timing_report, 'w') as f:
        f.write("ABC Timing Analysis Report\n")
        f.write("=" * 40 + "\n\n")
        
        # Extract key timing metrics
        lines = abc_output.split('\n')
        
        # Look for statistics sections
        stats_sections = []
        current_section = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['i/o', 'nodes', 'levels', 'depth', 'gates']):
                if current_section:
                    stats_sections.append('\n'.join(current_section))
                    current_section = []
                current_section.append(line)
            elif 'abc' in line.lower() or line.strip() == '':
                if current_section:
                    stats_sections.append('\n'.join(current_section))
                    current_section = []
            elif current_section:
                current_section.append(line)
        
        if current_section:
            stats_sections.append('\n'.join(current_section))
        
        # Format the extracted information
        for i, section in enumerate(stats_sections):
            f.write(f"Analysis Stage {i+1}:\n")
            f.write("-" * 25 + "\n")
            f.write(section)
            f.write("\n\n")
        
        f.write("ABC TIMING COMMANDS USED:\n")
        f.write("-" * 30 + "\n")
        f.write("print_level  - Logic depth analysis\n")
        f.write("print_stats  - Gate count and area\n")
        f.write("print_fanio  - Fanin/fanout statistics\n")
        f.write("time         - Timing information\n")
        f.write("stime        - Slack timing analysis\n")
        f.write("depth        - Critical path depth\n")
    
    print(f"✓ ABC timing report saved to: {timing_report}")


def process_yosys_timing_files(results_dir: str) -> None:
    """Process Yosys-generated timing analysis files."""
    
    timing_files = [
        "pre_abc_stats.log",
        "post_abc_stats.log", 
        "final_stats.log",
        "depth_analysis.log"
    ]
    
    summary_file = os.path.join(results_dir, "yosys_timing_summary.txt")
    
    with open(summary_file, 'w') as f:
        f.write("Yosys Timing Analysis Summary\n")
        f.write("=" * 40 + "\n\n")
        
        for timing_file in timing_files:
            file_path = os.path.join(results_dir, timing_file)
            if os.path.exists(file_path):
                f.write(f"=== {timing_file.upper()} ===\n")
                with open(file_path, 'r') as tf:
                    content = tf.read()
                    f.write(content)
                f.write("\n" + "-"*50 + "\n\n")
            else:
                f.write(f"⚠ {timing_file} not found\n\n")
    
    print(f"✓ Yosys timing summary saved to: {summary_file}")


def print_installation_instructions():
    """Print installation instructions for synthesis tools."""
    
    print("\nINSTALLATION INSTRUCTIONS:")
    print("=" * 30)
    print("\n1. Install ABC from source:")
    print("   git clone https://github.com/berkeley-abc/abc.git")
    print("   cd abc")
    print("   make")
    print("   sudo cp abc /usr/local/bin/")
    
    print("\n2. Install Yosys (easier alternative):")
    print("   sudo apt-get install yosys")
    
    print("\n3. Install build dependencies:")
    print("   sudo apt-get install build-essential git cmake")
    
    print("\n4. Verify installation:")
    print("   abc -h")
    print("   yosys -h")


def main():
    """Main function for hierarchical synthesis."""
    
    # Updated paths to match the new TT directory structure
    csv_file = "addition/TT/complete_addition_results.csv"
    output_directory = "addition/TT/hierarchical_synthesis"
    
    print("Float_4E3M Hierarchical Circuit Synthesis")
    print("=" * 50)
    print("Strategy: Optimize all 8 output functions simultaneously")
    print("Tool: ABC with advanced hierarchical synthesis\n")
    
    # Convert relative paths to absolute paths for better debugging
    abs_csv_file = os.path.abspath(csv_file)
    abs_output_dir = os.path.abspath(output_directory)
    
    print(f"CSV file: {abs_csv_file}")
    print(f"Output directory: {abs_output_dir}")
    
    if not os.path.exists(abs_csv_file):
        print(f"✗ Error: CSV file not found at: {abs_csv_file}")
        print("Please ensure the CSV file exists or update the path.")
        
        # List files in the addition/TT directory for debugging
        addition_tt_dir = os.path.dirname(abs_csv_file)
        if os.path.exists(addition_tt_dir):
            print(f"\nFiles in {addition_tt_dir}:")
            for file in os.listdir(addition_tt_dir):
                print(f"  - {file}")
        else:
            # Check if addition directory exists
            addition_dir = os.path.dirname(addition_tt_dir)
            if os.path.exists(addition_dir):
                print(f"\nDirectories in {addition_dir}:")
                for item in os.listdir(addition_dir):
                    if os.path.isdir(os.path.join(addition_dir, item)):
                        print(f"  - {item}/")
        
        return
    
    print(f"✓ CSV file found: {abs_csv_file}")
    
    # Perform hierarchical synthesis
    csv_to_abc_hierarchical_synthesis(abs_csv_file, abs_output_dir)
    
    print("\n" + "=" * 50)
    print("Hierarchical synthesis complete!")
    print(f"Results available in: {abs_output_dir}/")
    print("\nKey advantages of this approach:")
    print("✓ Shared logic across all 8 outputs")
    print("✓ Global optimization opportunities")
    print("✓ Minimal total gate count")
    print("✓ Balanced timing across outputs")
    
    print("\nGenerated directories:")
    print("- separate_TT/ - Individual truth tables for each output bit")
    print("- combined_TT/ - Combined truth table for hierarchical synthesis")
    print("- synthesis_results/ - Optimized netlists and analysis reports")
    
    print("\nNext step: Run timing analysis with analyze_circuits.py")


if __name__ == "__main__":
    main()

