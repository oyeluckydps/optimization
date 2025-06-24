"""
Conversion utilities for Float_4E3M format.

This module provides functions to convert between regular float values
and Float_4E3M bit representations, including rounding to the nearest
representable value.
"""

from typing import Tuple
from float_4e3m import Float_4E3M


def value_to_bitstream(value: float) -> str:
    """
    Convert a float value to Float_4E3M bitstream representation.
    
    This function finds the closest Float_4E3M representation for the given value
    by trying all possible combinations and selecting the one with minimum error.
    
    Args:
        value (float): The value to convert
        
    Returns:
        str: 8-bit binary string representation (e.g., "10110000")
    """
    float_4e3m = Float_4E3M.from_value(value)
    return float_4e3m.to_bitstring()


def value_to_components(value: float) -> Tuple[int, int, int]:
    """
    Convert a float value to Float_4E3M sign, exponent, and mantissa components.
    
    Args:
        value (float): The value to convert
        
    Returns:
        Tuple[int, int, int]: (sign, exponent, mantissa) components
    """
    float_4e3m = Float_4E3M.from_value(value)
    return float_4e3m.sign, float_4e3m.exponent, float_4e3m.mantissa


def bitstream_to_value(bitstream: str) -> float:
    """
    Convert a bitstream to its Float_4E3M value.
    
    Args:
        bitstream (str): 8-bit binary string (e.g., "10110000")
        
    Returns:
        float: The corresponding Float_4E3M value
    """
    if len(bitstream) != 8:
        raise ValueError("Bitstream must be exactly 8 bits")
    
    # Convert binary string to integer
    bits = int(bitstream, 2)
    float_4e3m = Float_4E3M.from_bits(bits)
    return float_4e3m.value


def demonstrate_conversion(test_values: list) -> None:
    """
    Demonstrate the conversion process for a list of test values.
    
    Args:
        test_values (list): List of float values to test
    """
    print("Value Conversion Demonstration")
    print("=" * 60)
    print("Original Value | Sign | Exp | Mant | Bitstream | Converted Value | Error")
    print("-" * 80)
    
    for value in test_values:
        # Convert to Float_4E3M
        float_4e3m = Float_4E3M.from_value(value)
        bitstream = float_4e3m.to_bitstring()
        converted_value = float_4e3m.value
        error = abs(value - converted_value)
        
        print(f"{value:13.6f} |  {float_4e3m.sign}   | {float_4e3m.exponent:2d}  |  {float_4e3m.mantissa}  | {bitstream} | {converted_value:14.6f} | {error:.6f}")


def find_conversion_errors(test_values: list) -> list:
    """
    Find conversion errors for a list of test values.
    
    Args:
        test_values (list): List of values to test
        
    Returns:
        list: List of tuples (original_value, converted_value, error)
    """
    errors = []
    
    for value in test_values:
        float_4e3m = Float_4E3M.from_value(value)
        converted_value = float_4e3m.value
        error = abs(value - converted_value)
        errors.append((value, converted_value, error))
    
    return errors


if __name__ == "__main__":
    # Test cases including the specific example from the problem
    test_values = [
        -0.25,    # Specific example from problem
        0.0,
        1.0,
        -1.0,
        0.5,
        -0.5,
        0.125,
        -0.125,
        2.0,
        -2.0,
        0.75,
        -0.75
    ]
    
    print("Testing conversion utilities...")
    print()
    
    # Demonstrate conversions
    demonstrate_conversion(test_values)
    
    print()
    print("Specific example: -0.25")
    print("-" * 30)
    
    # Handle the specific example
    value = -0.25
    sign, exponent, mantissa = value_to_components(value)
    bitstream = value_to_bitstream(value)
    
    print(f"Value: {value}")
    print(f"Sign: {sign}")
    print(f"Exponent: {exponent:04b} (binary) = {exponent} (decimal)")
    print(f"Mantissa: {mantissa:03b} (binary) = {mantissa} (decimal)")
    print(f"Complete bitstream: {bitstream}")
    
    # Verify round-trip conversion
    recovered_value = bitstream_to_value(bitstream)
    print(f"Recovered value: {recovered_value}")
    print(f"Conversion error: {abs(value - recovered_value)}")