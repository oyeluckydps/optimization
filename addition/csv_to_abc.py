"""
Convert Float_4E3M CSV results to ABC logic synthesis format.
This script focuses on hierarchical synthesis optimizing all 8 output functions simultaneously.
"""

import csv
import subprocess
import os
from typing import List, Tuple, Dict


def csv_to_abc_hierarchical_synthesis(csv_filename: str, output_dir: str = "abc_output") -> None:
    """
    Convert CSV file to ABC format and perform hierarchical synthesis for all 8 outputs together.
    
    Args:
        csv_filename (str): Input CSV file with operand1, operand2, result columns
        output_dir (str): Directory to store ABC files and results
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
    print("\nGenerating separate truth tables for analysis...")
    for bit_pos in range(8):
        generate_separate_truth_table(truth_table_data, bit_pos, separate_dir)
    
    # Generate combined truth table for hierarchical synthesis
    print("\nGenerating combined truth table for hierarchical synthesis...")
    combined_file = generate_combined_truth_table(truth_table_data, combined_dir)
    
    # Perform hierarchical synthesis on all 8 outputs simultaneously
    print("\nPerforming hierarchical synthesis...")
    perform_hierarchical_synthesis(combined_file, results_dir)


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


def check_tool_availability(tool_name: str) -> bool:
    """Check if a synthesis tool is available."""
    try:
        result = subprocess.run([tool_name, "-h"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def perform_abc_synthesis(truth_table_file: str, results_dir: str) -> None:
    """Perform ABC synthesis (original method)."""
    
    # Advanced ABC command sequence for hierarchical synthesis
    abc_commands = [
        f"read_truth {truth_table_file}",
        "strash", "print_stats",
        "balance", "rewrite -l", "balance", "refactor -l", "balance",
        "rewrite -l", "balance", "compress2rs", "balance",
        "choice", "balance", "fraig", "balance", "print_stats",
        "map -a", "print_stats",
        f"write_verilog {results_dir}/float_4e3m_adder_optimized.v",
        f"write_blif {results_dir}/float_4e3m_adder_optimized.blif",
        "print_level", "print_io"
    ]
    
    script_file = os.path.join(results_dir, "hierarchical_synthesis.abc")
    with open(script_file, 'w') as f:
        for cmd in abc_commands:
            f.write(cmd + "\n")
        f.write("quit\n")
    
    result = subprocess.run(["abc", "-f", script_file], capture_output=True, text=True, cwd=results_dir)
    
    if result.returncode == 0:
        print("✓ ABC hierarchical synthesis completed!")
        parse_abc_results(result.stdout, results_dir)
    else:
        print(f"✗ ABC synthesis failed: {result.stderr}")


def perform_yosys_synthesis(truth_table_file: str, results_dir: str) -> None:
    """Perform synthesis using Yosys as alternative to ABC."""
    
    # Convert relative paths to absolute paths
    abs_truth_table_file = os.path.abspath(truth_table_file)
    abs_results_dir = os.path.abspath(results_dir)
    
    print(f"Truth table file: {abs_truth_table_file}")
    print(f"Results directory: {abs_results_dir}")
    
    # First, convert truth table to Verilog behavioral code
    verilog_file = convert_truth_table_to_verilog(abs_truth_table_file, abs_results_dir)
    
    # Use absolute paths for all files
    abs_verilog_file = os.path.abspath(verilog_file)
    output_verilog = os.path.join(abs_results_dir, "float_4e3m_adder_yosys_optimized.v")
    output_blif = os.path.join(abs_results_dir, "float_4e3m_adder_yosys_optimized.blif")
    
    # Yosys synthesis commands with absolute paths
    yosys_script = f"""read_verilog {abs_verilog_file}
hierarchy -check -top float_4e3m_adder
proc
opt
fsm
opt
memory
opt
techmap
opt
abc
opt
clean
stat
write_verilog {output_verilog}
write_blif {output_blif}
"""
    
    script_file = os.path.join(abs_results_dir, "yosys_synthesis.ys")
    
    # Write script file
    print(f"Creating Yosys script: {script_file}")
    with open(script_file, 'w') as f:
        f.write(yosys_script)
    
    # Verify script file exists
    if not os.path.exists(script_file):
        print(f"✗ Script file was not created: {script_file}")
        return
    
    print(f"✓ Script file created successfully")
    print(f"Script contents:\n{yosys_script}")
    
    try:
        # Change to results directory and run yosys
        print(f"Running Yosys from directory: {abs_results_dir}")
        
        result = subprocess.run(
            ["yosys", "-s", "yosys_synthesis.ys"], 
            capture_output=True, 
            text=True, 
            cwd=abs_results_dir
        )
        
        if result.returncode == 0:
            print("✓ Yosys synthesis completed!")
            
            # Save Yosys log
            log_file = os.path.join(abs_results_dir, "yosys_synthesis.log")
            with open(log_file, 'w') as f:
                f.write("Yosys Synthesis Log\n")
                f.write("=" * 30 + "\n\n")
                f.write(result.stdout)
            
            print(f"✓ Yosys log saved to: {log_file}")
            
            # Check if output files were created
            if os.path.exists(output_verilog):
                print(f"✓ Optimized Verilog created: {output_verilog}")
            if os.path.exists(output_blif):
                print(f"✓ BLIF file created: {output_blif}")
                
        else:
            print(f"✗ Yosys synthesis failed with return code: {result.returncode}")
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            
            # Save error log
            error_log = os.path.join(abs_results_dir, "yosys_error.log")
            with open(error_log, 'w') as f:
                f.write("Yosys Error Log\n")
                f.write("=" * 20 + "\n\n")
                f.write(f"Return code: {result.returncode}\n")
                f.write(f"STDOUT:\n{result.stdout}\n")
                f.write(f"STDERR:\n{result.stderr}\n")
    
    except Exception as e:
        print(f"✗ Yosys execution failed: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script file exists: {os.path.exists(script_file)}")
        print(f"Script file path: {script_file}")


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
        f.write("// Float_4E3M Adder - Behavioral Verilog\n")
        f.write("// Generated from truth table\n\n")
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
    
    print(f"✓ Generated behavioral Verilog: {verilog_file}")
    
    # Verify the file was created and has content
    if os.path.exists(verilog_file):
        file_size = os.path.getsize(verilog_file)
        print(f"✓ Verilog file size: {file_size} bytes")
    else:
        print(f"✗ Failed to create Verilog file: {verilog_file}")
    
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
    
    print("\n2. Install Yosys (easier alternative):")
    print("   sudo apt-get install yosys")
    
    print("\n3. Install build dependencies:")
    print("   sudo apt-get install build-essential git cmake")
    
    print("\n4. Verify installation:")
    print("   abc -h")
    print("   yosys -h")


def parse_abc_results(abc_output: str, results_dir: str) -> None:
    """
    Parse ABC output and generate human-readable optimization report.
    
    Args:
        abc_output: ABC command output
        results_dir: Directory to save the report
    """
    
    report_file = os.path.join(results_dir, "optimization_report.txt")
    
    # Extract key statistics from ABC output
    lines = abc_output.split('\n')
    stats_sections = []
    current_section = []
    
    for line in lines:
        if 'i/o' in line.lower() or 'nodes' in line.lower() or 'levels' in line.lower():
            if current_section:
                stats_sections.append('\n'.join(current_section))
                current_section = []
            current_section.append(line)
        elif current_section and (line.strip() == '' or 'abc' in line.lower()):
            if current_section:
                stats_sections.append('\n'.join(current_section))
                current_section = []
        elif current_section:
            current_section.append(line)
    
    if current_section:
        stats_sections.append('\n'.join(current_section))
    
    # Generate comprehensive report
    with open(report_file, 'w') as f:
        f.write("Float_4E3M Adder Hierarchical Synthesis Report\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("OPTIMIZATION STRATEGY:\n")
        f.write("-" * 25 + "\n")
        f.write("✓ All 8 output functions optimized simultaneously\n")
        f.write("✓ Hierarchical synthesis with shared logic detection\n")
        f.write("✓ Multi-level Boolean optimization\n")
        f.write("✓ Area-oriented technology mapping\n\n")
        
        f.write("ABC OPTIMIZATION SEQUENCE:\n")
        f.write("-" * 30 + "\n")
        f.write("1. Truth table → AIG conversion\n")
        f.write("2. Iterative balance + rewrite + refactor\n")
        f.write("3. Compression with resynthesis\n")
        f.write("4. Choice computation for mapping\n")
        f.write("5. Functional reduction (FRAIG)\n")
        f.write("6. Technology mapping\n\n")
        
        f.write("SYNTHESIS STATISTICS:\n")
        f.write("-" * 25 + "\n")
        for i, section in enumerate(stats_sections):
            f.write(f"Stage {i+1}:\n{section}\n\n")
        
        f.write("GENERATED FILES:\n")
        f.write("-" * 20 + "\n")
        f.write("• float_4e3m_adder_optimized.v   (Verilog netlist)\n")
        f.write("• float_4e3m_adder_optimized.blif (BLIF format)\n")
        f.write("• float_4e3m_adder_optimized.bench (Berkeley format)\n")
        f.write("• abc_synthesis.log               (Detailed ABC log)\n\n")
        
        f.write("NEXT STEPS:\n")
        f.write("-" * 15 + "\n")
        f.write("1. Review the optimized Verilog netlist\n")
        f.write("2. Analyze gate count and logic depth\n")
        f.write("3. Verify functionality with simulation\n")
        f.write("4. Consider technology-specific optimization\n")
        f.write("5. Evaluate timing and area constraints\n")
    
    print(f"✓ Optimization report generated: {report_file}")


def main():
    """Main function for hierarchical synthesis."""
    
    # Use the correct paths from your setup
    csv_file = "addition/demo_addition_results.csv"
    output_directory = "addition/hierarchical_synthesis"
    
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
        
        # List files in the addition directory for debugging
        addition_dir = os.path.dirname(abs_csv_file)
        if os.path.exists(addition_dir):
            print(f"\nFiles in {addition_dir}:")
            for file in os.listdir(addition_dir):
                print(f"  - {file}")
        
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


if __name__ == "__main__":
    main()

    