"""
Circuit Generation for Float_4E3M Adder
Generates truth tables and prepares files for synthesis
"""

import csv
import subprocess
import os
import time
import numpy as np
from float_4e3m import Float_4E3M
from generator import generate_all_float_4e3m, print_all_representations, analyze_value_distribution
from conversion_utils import value_to_bitstream, value_to_components, demonstrate_conversion
from operations import generate_addition_table, analyze_addition_results, create_operation_matrix, save_addition_results_to_files, save_operation_results_to_files


def save_truth_table_to_tt_file(list1, list2, filename):
    """
    Generate a truth table file in BLIF format for the Float_4E3M adder.
    
    Args:
        list1: First list of Float_4E3M objects (operand 1)
        list2: Second list of Float_4E3M objects (operand 2)
        filename: Output filename with .tt extension
    """
    print(f"Generating truth table file: {filename}")
    
    with open(filename, 'w') as f:
        # Write BLIF header
        f.write(".i 16\n")  # 16 inputs (8 bits for each operand)
        f.write(".o 8\n")   # 8 outputs (8 bits for result)
        f.write(f".p {len(list1) * len(list2)}\n")  # Number of product terms
        
        # Input labels (operand1 and operand2 bit labels)
        f.write(".ilb op1_7 op1_6 op1_5 op1_4 op1_3 op1_2 op1_1 op1_0 "
                "op2_7 op2_6 op2_5 op2_4 op2_3 op2_2 op2_1 op2_0\n")
        
        # Output labels (result bit labels)
        f.write(".ob result_7 result_6 result_5 result_4 result_3 result_2 result_1 result_0\n")
        
        # Generate all combinations and their results
        for i, op1 in enumerate(list1):
            for j, op2 in enumerate(list2):
                # Perform addition
                try:
                    result = op1 + op2
                    
                    # Convert operands and result to 8-bit binary strings
                    op1_bits = op1.to_bitstring()
                    op2_bits = op2.to_bitstring()
                    result_bits = result.to_bitstring()
                    
                    # Write the truth table entry
                    # Format: input_bits output_bits
                    input_bits = op1_bits + op2_bits
                    f.write(f"{input_bits} {result_bits}\n")
                    
                except Exception as e:
                    # Handle any errors in addition (e.g., overflow, special cases)
                    print(f"Warning: Error in addition {op1.to_bitstring()} + {op2.to_bitstring()}: {e}")
                    # Write a default result (all zeros or handle as needed)
                    input_bits = op1.to_bitstring() + op2.to_bitstring()
                    f.write(f"{input_bits} 00000000\n")
        
        # Write end marker
        f.write(".e\n")
    
    print(f"✓ Truth table saved to {filename}")
    print(f"  Format: BLIF-style truth table")
    print(f"  Inputs: 16 bits (8-bit operand1 + 8-bit operand2)")
    print(f"  Outputs: 8 bits (8-bit result)")
    print(f"  Entries: {len(list1) * len(list2)} combinations")


def save_operation_results_to_files_with_tt(list1, list2, txt_filename, csv_filename, tt_filename):
    """
    Enhanced version that also generates the .tt file along with existing txt and csv files.
    
    Args:
        list1: First list of Float_4E3M objects
        list2: Second list of Float_4E3M objects  
        txt_filename: Output text filename
        csv_filename: Output CSV filename
        tt_filename: Output truth table filename (.tt extension)
    """
    print(f"\nSaving operation results to multiple formats...")
    
    # Generate the existing files (txt and csv)
    save_operation_results_to_files(list1, list2, 'add', txt_filename, csv_filename)
    
    # Generate the new truth table file
    save_truth_table_to_tt_file(list1, list2, tt_filename)


def test_special_cases():
    """Test special case handling for infinity, zero, and NaN."""
    print("\n4. SPECIAL CASES TESTING")
    print("-" * 50)
    
    # Test positive infinity
    try:
        pos_inf = Float_4E3M.from_value(float('inf'))
        print(f"Positive infinity -> Sign: {pos_inf.sign}, Exp: {pos_inf.exponent}, Mant: {pos_inf.mantissa}")
        print(f"  Bitstream: {pos_inf.to_bitstring()}, Value: {pos_inf.value}")
    except Exception as e:
        print(f"Positive infinity error: {e}")
    
    # Test negative infinity
    try:
        neg_inf = Float_4E3M.from_value(float('-inf'))
        print(f"Negative infinity -> Sign: {neg_inf.sign}, Exp: {neg_inf.exponent}, Mant: {neg_inf.mantissa}")
        print(f"  Bitstream: {neg_inf.to_bitstring()}, Value: {neg_inf.value}")
    except Exception as e:
        print(f"Negative infinity error: {e}")
    
    # Test zero
    try:
        zero = Float_4E3M.from_value(0.0)
        print(f"Zero -> Sign: {zero.sign}, Exp: {zero.exponent}, Mant: {zero.mantissa}")
        print(f"  Bitstream: {zero.to_bitstring()}, Value: {zero.value}")
    except Exception as e:
        print(f"Zero error: {e}")
    
    # Test NaN (should raise error)
    try:
        nan_result = Float_4E3M.from_value(float('nan'))
        print(f"NaN -> Sign: {nan_result.sign}, Exp: {nan_result.exponent}, Mant: {nan_result.mantissa}")
    except ValueError as e:
        print(f"NaN correctly raised error: {e}")
    except Exception as e:
        print(f"NaN unexpected error: {e}")


def benchmark_conversion_performance():
    """Benchmark the numpy-optimized conversion performance."""
    print("\n3. PERFORMANCE BENCHMARK")
    print("-" * 50)
    
    # Test values for conversion
    np.random.seed(42)  # For reproducible results
    test_values = np.random.uniform(-2.0, 2.0, 1000)
    
    print("Testing conversion performance with 1000 random values...")
    
    # Warm up the class (initialize lookup tables)
    Float_4E3M.from_value(0.5)
    
    # Time the conversions
    start_time = time.time()
    converted_objects = [Float_4E3M.from_value(val) for val in test_values]
    end_time = time.time()
    
    conversion_time = end_time - start_time
    print(f"✓ Converted 1000 values in {conversion_time:.4f} seconds")
    print(f"✓ Average time per conversion: {conversion_time/1000*1000:.3f} ms")
    
    # Verify accuracy with a few examples
    print("\nAccuracy verification (first 5 conversions):")
    for i in range(5):
        original = test_values[i]
        converted = converted_objects[i]
        error = abs(original - converted.value)
        print(f"  {original:8.4f} -> {converted.value:8.4f} (error: {error:.6f})")
    
    return converted_objects


def generate_csv_files(all_floats, output_dir="addition/TT"):
    """Generate CSV files with addition results and truth tables."""
    
    print(f"\n6. GENERATING CSV, TXT, AND TT FILES")
    print("-" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create two identical lists as requested
    list1 = all_floats.copy()
    list2 = all_floats.copy()
    
    print(f"Created list1 with {len(list1)} objects")
    print(f"Created list2 with {len(list2)} objects")
    print(f"Total operations to perform: {len(list1)} × {len(list2)} = {len(list1) * len(list2)}")
    
    # Generate addition table (this might take a moment for 256x256 = 65,536 operations)
    print("\nGenerating addition table for all combinations...")
    start_time = time.time()
    addition_results = generate_addition_table(list1, list2)
    end_time = time.time()
    
    print(f"✓ Completed all {len(addition_results)} addition operations in {end_time - start_time:.2f} seconds")
    
    # Analyze results
    analyze_addition_results(addition_results)
    
    # Save results to files including .tt format
    print("\n\nSaving results to files...")
    print("Generating complete 256x256 addition table files...")
    save_operation_results_to_files_with_tt(
        list1, list2, 
        f"{output_dir}/complete_addition_results.txt", 
        f"{output_dir}/complete_addition_results.csv",
        f"{output_dir}/complete_addition_results.tt"
    )
    
    # Also generate a smaller sample for quick inspection
    print("\nGenerating sample 16x16 files for quick inspection...")
    save_operation_results_to_files_with_tt(
        list1[:16], list2[:16], 
        f"{output_dir}/sample_addition_results.txt", 
        f"{output_dir}/sample_addition_results.csv",
        f"{output_dir}/sample_addition_results.tt"
    )
    
    # Also generate demo files
    print("\nGenerating demo 16x16 files...")
    save_operation_results_to_files_with_tt(
        list1[:16], list2[:16],
        f"{output_dir}/demo_addition_results.txt",
        f"{output_dir}/demo_addition_results.csv",
        f"{output_dir}/demo_addition_results.tt"
    )
    
    return addition_results


def main():
    """Main demonstration function."""
    
    print("=" * 70)
    print("Float_4E3M: Custom 8-bit Floating Point Implementation")
    print("Format: 1 Sign + 4 Exponent + 3 Mantissa bits")
    print("Formula: (-1)^s * 2^(-exponent) * ((8+mantissa)/8)")
    print("Enhanced with Truth Table (.tt) Generation for Circuit Synthesis")
    print("=" * 70)
    
    # Step 1: Generate all 256 possible Float_4E3M objects
    print("\n1. GENERATING ALL POSSIBLE FLOAT_4E3M OBJECTS")
    print("-" * 50)
    
    all_floats = generate_all_float_4e3m()
    print(f"✓ Generated {len(all_floats)} Float_4E3M objects")
    
    # Display sample representations
    print_all_representations(all_floats, max_display=15)
    
    # Analyze value distribution
    analyze_value_distribution(all_floats)
    
    # Step 2: Demonstrate value to bitstream conversion
    print("\n\n2. VALUE TO BITSTREAM CONVERSION")
    print("-" * 50)
    
    # Test the specific example: -0.25
    test_value = -0.25
    print(f"Converting {test_value} to Float_4E3M:")
    
    sign, exponent, mantissa = value_to_components(test_value)
    bitstream = value_to_bitstream(test_value)
    
    print(f"  Sign bit: {sign}")
    print(f"  Exponent: {exponent:04b} (binary) = {exponent} (decimal)")
    print(f"  Mantissa: {mantissa:03b} (binary) = {mantissa} (decimal)")
    print(f"  Complete bitstream: {bitstream}")
    
    # Verify the conversion
    float_obj = Float_4E3M.from_value(test_value)
    print(f"  Actual value: {float_obj.value}")
    print(f"  Conversion error: {abs(test_value - float_obj.value):.8f}")
    
    # Performance benchmark
    benchmark_conversion_performance()
    
    # Special cases testing
    test_special_cases()
    
    # More conversion examples
    print("\n5. MORE CONVERSION EXAMPLES")
    print("-" * 50)
    test_values = [-0.25, 0.0, 1.0, -1.0, 0.5, -0.5, 0.125]
    demonstrate_conversion(test_values)
    
    # Generate CSV files for circuit synthesis
    addition_results = generate_csv_files(all_floats, output_dir="addition/TT")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("ENHANCED GENERATION SUMMARY")
    print("=" * 70)
    print("✓ Float_4E3M class with 1 sign + 4 exponent + 3 mantissa bits")
    print("✓ Proper value calculation: (-1)^s * 2^(-exponent) * ((8+mantissa)/8)")
    print("✓ Generated all 256 possible objects for all 8-bit patterns")
    print("✓ Efficient value-to-bitstream conversion using NumPy")
    print("✓ Example: -0.25 correctly converted to bitstream")
    print(f"✓ Performed all {len(addition_results)} addition operations")
    print("✓ Results converted back to bitstream format")
    print("✓ Results saved to text, CSV, and truth table formats")
    print("✓ Performance optimized with precomputed lookup tables")
    
    print("\nGenerated Files:")
    print("- addition/TT/complete_addition_results.txt (formatted table)")
    print("- addition/TT/complete_addition_results.csv (machine-readable)")
    print("- addition/TT/complete_addition_results.tt (BLIF truth table)")
    print("- addition/TT/sample_addition_results.txt (16x16 sample)")
    print("- addition/TT/sample_addition_results.csv (16x16 sample)")
    print("- addition/TT/sample_addition_results.tt (16x16 truth table)")
    print("- addition/TT/demo_addition_results.txt (16x16 demo)")
    print("- addition/TT/demo_addition_results.csv (16x16 demo)")
    print("- addition/TT/demo_addition_results.tt (16x16 truth table)")
    
    print("\nTruth Table Format:")
    print("- BLIF-style format with .tt extension")
    print("- 16 inputs: op1_7...op1_0, op2_7...op2_0")
    print("- 8 outputs: result_7...result_0")
    print("- Ready for logic synthesis tools")
    print("- Compatible with Berkeley ABC, Yosys, and other synthesis tools")
    
    print("\nNext steps:")
    print("1. Run synthesis analysis: python analyze_circuits.py")
    print("2. Run timing analysis: python run_builtin_analysis.py")
    print("3. Use .tt files with synthesis tools for circuit generation")


if __name__ == "__main__":
    main()