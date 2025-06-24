"""
Operations module for Float_4E3M arithmetic.

This module provides arithmetic operations for Float_4E3M objects.
Currently implements addition, with structure for future operations.
Includes functionality to save results in text and CSV formats.
"""

import csv
from typing import List, Tuple, Dict
import itertools
from float_4e3m import Float_4E3M


class Float4E3MOperations:
    """
    Class containing arithmetic operations for Float_4E3M numbers.
    Designed to be easily extensible for future operations.
    """
    
    @staticmethod
    def add(a: Float_4E3M, b: Float_4E3M) -> Float_4E3M:
        """
        Add two Float_4E3M numbers.
        
        Args:
            a (Float_4E3M): First operand
            b (Float_4E3M): Second operand
            
        Returns:
            Float_4E3M: Result of a + b
        """
        return a + b  # Uses the __add__ method defined in Float_4E3M
    
    @staticmethod
    def subtract(a: Float_4E3M, b: Float_4E3M) -> Float_4E3M:
        """
        Subtract two Float_4E3M numbers.
        
        Args:
            a (Float_4E3M): First operand
            b (Float_4E3M): Second operand
            
        Returns:
            Float_4E3M: Result of a - b
        """
        # Convert to regular floats, subtract, then convert back
        result_value = a.value - b.value
        return Float_4E3M.from_value(result_value)
    
    @staticmethod
    def multiply(a: Float_4E3M, b: Float_4E3M) -> Float_4E3M:
        """
        Multiply two Float_4E3M numbers.
        
        Args:
            a (Float_4E3M): First operand
            b (Float_4E3M): Second operand
            
        Returns:
            Float_4E3M: Result of a * b
        """
        result_value = a.value * b.value
        return Float_4E3M.from_value(result_value)
    
    @staticmethod
    def divide(a: Float_4E3M, b: Float_4E3M) -> Float_4E3M:
        """
        Divide two Float_4E3M numbers.
        
        Args:
            a (Float_4E3M): Dividend
            b (Float_4E3M): Divisor
            
        Returns:
            Float_4E3M: Result of a / b
            
        Raises:
            ZeroDivisionError: If b.value is zero
        """
        if b.value == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        result_value = a.value / b.value
        return Float_4E3M.from_value(result_value)


def save_addition_results_to_files(list1: List[Float_4E3M], list2: List[Float_4E3M], 
                                   text_filename: str = "addition_results.txt",
                                   csv_filename: str = "addition_results.csv",
                                   decimal_places: int = 10) -> List[Tuple[str, str, str]]:
    """
    Generate addition table and save results to both text and CSV files.
    
    Args:
        list1 (List[Float_4E3M]): First list of Float_4E3M objects
        list2 (List[Float_4E3M]): Second list of Float_4E3M objects
        text_filename (str): Name for the text output file
        csv_filename (str): Name for the CSV output file
        decimal_places (int): Number of decimal places to show in text file (default: 10)
        
    Returns:
        List[Tuple[str, str, str]]: List of (bitstream1, bitstream2, result_bitstream) tuples
    """
    addition_results = []
    
    # Prepare data for both formats
    text_lines = []
    csv_data = []
    
    # Header for text file (width depends on decimal places)
    separator_width = 50 + (decimal_places + 6) * 3  # Adjust width based on decimal places
    text_header = "Operand 1  | Operand 2  | Result     | Values"
    text_separator = "-" * separator_width
    text_lines.append(text_header)
    text_lines.append(text_separator)
    
    # Header for CSV file
    csv_header = ["operand1", "operand2", "result", "value1", "value2", "result_value"]
    csv_data.append(csv_header)
    
    # Generate all combinations and format results
    for x1 in list1:
        for x2 in list2:
            # Perform addition
            result = Float4E3MOperations.add(x1, x2)
            
            # Get bitstreams
            bits1 = x1.to_bitstring()
            bits2 = x2.to_bitstring()
            result_bits = result.to_bitstring()
            
            # Get values
            val1 = x1.value
            val2 = x2.value
            result_val = result.value
            
            # Store for return
            addition_results.append((bits1, bits2, result_bits))
            
            # Format for text file with configurable decimal places
            field_width = decimal_places + 6  # Add space for sign, digits before decimal, and decimal point
            format_str = f"{{val:.{decimal_places}f}}"
            
            val1_str = f"{val1:{field_width}.{decimal_places}f}"
            val2_str = f"{val2:{field_width}.{decimal_places}f}"
            result_str = f"{result_val:{field_width}.{decimal_places}f}"
            
            text_line = f"{bits1} | {bits2} | {result_bits} | {val1_str} + {val2_str} = {result_str}"
            text_lines.append(text_line)
            
            # Format for CSV file
            csv_row = [bits1, bits2, result_bits, val1, val2, result_val]
            csv_data.append(csv_row)
    
    # Write text file
    try:
        with open(text_filename, 'w', encoding='utf-8') as f:
            for line in text_lines:
                f.write(line + '\n')
        print(f"✓ Text results saved to: {text_filename}")
    except Exception as e:
        print(f"✗ Error writing text file: {e}")
    
    # Write CSV file
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
        print(f"✓ CSV results saved to: {csv_filename}")
    except Exception as e:
        print(f"✗ Error writing CSV file: {e}")
    
    return addition_results


def save_operation_results_to_files(list1: List[Float_4E3M], list2: List[Float_4E3M], 
                                   operation: str = 'add',
                                   text_filename: str = None,
                                   csv_filename: str = None,
                                   decimal_places: int = 10) -> List[Tuple[str, str, str]]:
    """
    Generate operation table for any operation and save results to both text and CSV files.
    
    Args:
        list1 (List[Float_4E3M]): First list of Float_4E3M objects
        list2 (List[Float_4E3M]): Second list of Float_4E3M objects
        operation (str): Operation to perform ('add', 'subtract', 'multiply', 'divide')
        text_filename (str): Name for the text output file (auto-generated if None)
        csv_filename (str): Name for the CSV output file (auto-generated if None)
        decimal_places (int): Number of decimal places to show in text file (default: 10)
        
    Returns:
        List[Tuple[str, str, str]]: List of (bitstream1, bitstream2, result_bitstream) tuples
    """
    # Generate default filenames if not provided
    if text_filename is None:
        text_filename = f"{operation}_results.txt"
    if csv_filename is None:
        csv_filename = f"{operation}_results.csv"
    
    # Map operations to functions and symbols
    operations_map = {
        'add': (Float4E3MOperations.add, '+'),
        'subtract': (Float4E3MOperations.subtract, '-'),
        'multiply': (Float4E3MOperations.multiply, '*'),
        'divide': (Float4E3MOperations.divide, '/')
    }
    
    if operation not in operations_map:
        raise ValueError(f"Unsupported operation: {operation}")
    
    op_func, op_symbol = operations_map[operation]
    operation_results = []
    
    # Prepare data for both formats
    text_lines = []
    csv_data = []
    
    # Header for text file (width depends on decimal places)
    separator_width = 50 + (decimal_places + 6) * 3  # Adjust width based on decimal places
    text_header = "Operand 1  | Operand 2  | Result     | Values"
    text_separator = "-" * separator_width
    text_lines.append(text_header)
    text_lines.append(text_separator)
    
    # Header for CSV file
    csv_header = ["operand1", "operand2", "result", "value1", "value2", "result_value"]
    csv_data.append(csv_header)
    
    # Generate all combinations and format results
    for x1 in list1:
        for x2 in list2:
            try:
                # Skip division by zero
                if operation == 'divide' and x2.value == 0:
                    continue
                
                # Perform operation
                result = op_func(x1, x2)
                
                # Get bitstreams
                bits1 = x1.to_bitstring()
                bits2 = x2.to_bitstring()
                result_bits = result.to_bitstring()
                
                # Get values
                val1 = x1.value
                val2 = x2.value
                result_val = result.value
                
                # Store for return
                operation_results.append((bits1, bits2, result_bits))
                
                # Format for text file with configurable decimal places
                field_width = decimal_places + 6  # Add space for sign, digits before decimal, and decimal point
                
                val1_str = f"{val1:{field_width}.{decimal_places}f}"
                val2_str = f"{val2:{field_width}.{decimal_places}f}"
                result_str = f"{result_val:{field_width}.{decimal_places}f}"
                
                text_line = f"{bits1} | {bits2} | {result_bits} | {val1_str} {op_symbol} {val2_str} = {result_str}"
                text_lines.append(text_line)
                
                # Format for CSV file
                csv_row = [bits1, bits2, result_bits, val1, val2, result_val]
                csv_data.append(csv_row)
                
            except (ZeroDivisionError, OverflowError) as e:
                # Skip problematic operations
                continue
    
    # Write text file
    try:
        with open(text_filename, 'w', encoding='utf-8') as f:
            for line in text_lines:
                f.write(line + '\n')
        print(f"✓ Text results saved to: {text_filename}")
    except Exception as e:
        print(f"✗ Error writing text file: {e}")
    
    # Write CSV file
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
        print(f"✓ CSV results saved to: {csv_filename}")
    except Exception as e:
        print(f"✗ Error writing CSV file: {e}")
    
    return operation_results


def generate_addition_table(list1: List[Float_4E3M], list2: List[Float_4E3M]) -> List[Tuple[str, str, str]]:
    """
    Generate addition table for all combinations of two Float_4E3M lists.
    
    Args:
        list1 (List[Float_4E3M]): First list of Float_4E3M objects
        list2 (List[Float_4E3M]): Second list of Float_4E3M objects
        
    Returns:
        List[Tuple[str, str, str]]: List of (bitstream1, bitstream2, result_bitstream) tuples
    """
    addition_results = []
    
    for x1 in list1:
        for x2 in list2:
            result = Float4E3MOperations.add(x1, x2)
            addition_results.append((
                x1.to_bitstring(),
                x2.to_bitstring(),
                result.to_bitstring()
            ))
    
    return addition_results


def create_operation_matrix(list1: List[Float_4E3M], list2: List[Float_4E3M], 
                          operation: str = 'add') -> Dict:
    """
    Create a comprehensive operation matrix for analysis.
    
    Args:
        list1 (List[Float_4E3M]): First operand list
        list2 (List[Float_4E3M]): Second operand list
        operation (str): Operation to perform ('add', 'subtract', 'multiply', 'divide')
        
    Returns:
        Dict: Dictionary containing operation results and statistics
    """
    operations_map = {
        'add': Float4E3MOperations.add,
        'subtract': Float4E3MOperations.subtract,
        'multiply': Float4E3MOperations.multiply,
        'divide': Float4E3MOperations.divide
    }
    
    if operation not in operations_map:
        raise ValueError(f"Unsupported operation: {operation}")
    
    op_func = operations_map[operation]
    results = []
    overflow_count = 0
    underflow_count = 0
    
    for x1 in list1:
        for x2 in list2:
            try:
                if operation == 'divide' and x2.value == 0:
                    continue  # Skip division by zero
                
                result = op_func(x1, x2)
                
                # Check for potential overflow/underflow by comparing
                # the exact mathematical result with the quantized result
                exact_result = getattr(x1.value, f"__{operation}__")(x2.value) if operation != 'divide' else x1.value / x2.value
                
                if abs(exact_result) > abs(result.value) * 2:  # Rough overflow detection
                    overflow_count += 1
                elif abs(exact_result) > 0 and abs(result.value) < abs(exact_result) / 2:  # Rough underflow detection
                    underflow_count += 1
                
                results.append({
                    'operand1_bits': x1.to_bitstring(),
                    'operand1_value': x1.value,
                    'operand2_bits': x2.to_bitstring(),
                    'operand2_value': x2.value,
                    'result_bits': result.to_bitstring(),
                    'result_value': result.value,
                    'exact_result': exact_result,
                    'quantization_error': abs(exact_result - result.value)
                })
            
            except (ZeroDivisionError, OverflowError) as e:
                # Handle exceptions gracefully
                continue
    
    return {
        'operation': operation,
        'total_operations': len(results),
        'results': results,
        'overflow_count': overflow_count,
        'underflow_count': underflow_count,
        'unique_results': len(set(r['result_bits'] for r in results))
    }


def analyze_addition_results(addition_results: List[Tuple[str, str, str]]) -> None:
    """
    Analyze the results of addition operations.
    
    Args:
        addition_results: List of (bitstream1, bitstream2, result_bitstream) tuples
    """
    print("Addition Analysis")
    print("=" * 50)
    print(f"Total operations performed: {len(addition_results)}")
    
    # Count unique results
    unique_results = set(result[2] for result in addition_results)
    print(f"Unique result patterns: {len(unique_results)}")
    
    # Show sample results
    print("\nSample Addition Results:")
    print("-" * 60)
    print("Operand 1  | Operand 2  | Result     | Values")
    print("-" * 60)
    
    for i, (bits1, bits2, result_bits) in enumerate(addition_results[:10]):
        val1 = Float_4E3M.from_bits(int(bits1, 2)).value
        val2 = Float_4E3M.from_bits(int(bits2, 2)).value
        result_val = Float_4E3M.from_bits(int(result_bits, 2)).value
        
        print(f"{bits1} | {bits2} | {result_bits} | {val1:6.3f} + {val2:6.3f} = {result_val:6.3f}")
    
    if len(addition_results) > 10:
        print("... (showing first 10 results)")


if __name__ == "__main__":
    from generator import generate_all_float_4e3m
    
    # Generate all possible Float_4E3M objects
    print("Generating all Float_4E3M objects...")
    all_floats = generate_all_float_4e3m()
    
    # Create two identical lists as requested
    list1 = all_floats.copy()
    list2 = all_floats.copy()
    
    print(f"Created list1 with {len(list1)} objects")
    print(f"Created list2 with {len(list2)} objects")
    print(f"Total operations to perform: {len(list1)} × {len(list2)} = {len(list1) * len(list2)}")
    
    # Generate addition table
    print("\nGenerating addition table...")
    addition_results = generate_addition_table(list1, list2)
    
    # Analyze results
    analyze_addition_results(addition_results)
    
    # Create comprehensive operation matrix for addition
    print("\nCreating comprehensive addition matrix...")
    operation_matrix = create_operation_matrix(list1, list2, 'add')
    
    print(f"\nOperation Matrix Summary:")
    print(f"Operation: {operation_matrix['operation']}")
    print(f"Total operations: {operation_matrix['total_operations']}")
    print(f"Unique results: {operation_matrix['unique_results']}")
    print(f"Overflow occurrences: {operation_matrix['overflow_count']}")
    print(f"Underflow occurrences: {operation_matrix['underflow_count']}")
    
    print(f"\n✓ Successfully performed all {len(addition_results)} addition operations")
    print("✓ Results converted back to bitstream format")
    print("✓ Structure ready for additional operations (subtract, multiply, divide)")
    
    # Demonstrate file saving functionality
    print("\nDemonstrating file output functionality...")
    
    # Save addition results for a smaller subset to demonstrate format
    subset_size = 256  # Use smaller subset for demonstration
    list1_subset = all_floats[:subset_size]
    list2_subset = all_floats[:subset_size]
    
    print(f"Saving {subset_size}x{subset_size} addition results to files...")
    save_addition_results_to_files(list1_subset, list2_subset, 
                                  "addition/demo_addition_results.txt", 
                                  "addition/demo_addition_results.csv")
    
    print(f"\n✓ File output demonstration complete")
    print("✓ Full 256x256 results can be generated by calling:")
    print("   save_addition_results_to_files(all_floats, all_floats)")