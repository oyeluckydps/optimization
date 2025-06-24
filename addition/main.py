"""
Main demonstration script for Float_4E3M implementation.

This script demonstrates all the functionality requested:
1. Float_4E3M class with proper value calculation
2. Generation of all 256 possible objects
3. Value to bitstream conversion (optimized with numpy)
4. Addition operations between all combinations
"""

import time
import numpy as np
from float_4e3m import Float_4E3M
from generator import generate_all_float_4e3m, print_all_representations, analyze_value_distribution
from conversion_utils import value_to_bitstream, value_to_components, demonstrate_conversion
from operations import generate_addition_table, analyze_addition_results, create_operation_matrix, save_addition_results_to_files, save_operation_results_to_files


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


def main():
    """Main demonstration function."""
    
    print("=" * 70)
    print("Float_4E3M: Custom 8-bit Floating Point Implementation")
    print("Format: 1 Sign + 4 Exponent + 3 Mantissa bits")
    print("Formula: (-1)^s * 2^(-exponent) * ((8+mantissa)/8)")
    print("Optimized with NumPy for fast conversion")
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

    