"""
Generator module for creating all possible Float_4E3M objects.

This module provides functions to generate all 256 possible Float_4E3M objects
corresponding to all possible 8-bit patterns.
"""

from typing import List
from float_4e3m import Float_4E3M


def generate_all_float_4e3m() -> List[Float_4E3M]:
    """
    Generate all possible 256 Float_4E3M objects for all 8-bit patterns (0-255).
    
    Returns:
        List[Float_4E3M]: List containing all 256 possible Float_4E3M objects
    """
    all_floats = []
    
    for bit_pattern in range(256):
        float_obj = Float_4E3M.from_bits(bit_pattern)
        all_floats.append(float_obj)
    
    return all_floats


def print_all_representations(float_list: List[Float_4E3M], max_display: int = 20) -> None:
    """
    Print a sample of Float_4E3M representations for inspection.
    
    Args:
        float_list (List[Float_4E3M]): List of Float_4E3M objects
        max_display (int): Maximum number of objects to display
    """
    print(f"Total Float_4E3M objects: {len(float_list)}")
    print(f"Displaying first {min(max_display, len(float_list))} objects:")
    print("-" * 60)
    print("Bit Pattern | Sign | Exp | Mant |     Value")
    print("-" * 60)
    
    for i, float_obj in enumerate(float_list[:max_display]):
        bit_str = float_obj.to_bitstring()
        print(f"{bit_str}   |  {float_obj.sign}   |  {float_obj.exponent:2d} |  {float_obj.mantissa}  | {float_obj.value:10.6f}")
    
    if len(float_list) > max_display:
        print(f"... and {len(float_list) - max_display} more objects")


def analyze_value_distribution(float_list: List[Float_4E3M]) -> None:
    """
    Analyze the distribution of values in the Float_4E3M representation.
    
    Args:
        float_list (List[Float_4E3M]): List of Float_4E3M objects to analyze
    """
    values = [f.value for f in float_list]
    
    print("\nValue Distribution Analysis:")
    print("-" * 40)
    print(f"Total unique values: {len(set(values))}")
    print(f"Minimum value: {min(values)}")
    print(f"Maximum value: {max(values)}")
    print(f"Value range: {max(values) - min(values)}")
    
    # Count positive and negative values
    positive_count = sum(1 for v in values if v > 0)
    negative_count = sum(1 for v in values if v < 0)
    zero_count = sum(1 for v in values if v == 0)
    
    print(f"Positive values: {positive_count}")
    print(f"Negative values: {negative_count}")
    print(f"Zero values: {zero_count}")


if __name__ == "__main__":
    # Generate all possible Float_4E3M objects
    all_floats = generate_all_float_4e3m()
    
    # Display sample representations
    print_all_representations(all_floats)
    
    # Analyze value distribution
    analyze_value_distribution(all_floats)
    
    # Verify we have exactly 256 objects
    assert len(all_floats) == 256, f"Expected 256 objects, got {len(all_floats)}"
    print(f"\n✓ Successfully generated all {len(all_floats)} Float_4E3M objects")

    