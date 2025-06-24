"""
Float_4E3M: A custom floating-point representation with 1 sign bit, 4 exponent bits, 3 mantissa bits.

Format: S EEEE MMM
- S: Sign bit (1 bit)
- E: Exponent bits (4 bits) 
- M: Mantissa bits (3 bits)

Value calculation: (-1)^s * 2^(-exponent) * ((8+mantissa)/8)
"""

import math
import numpy as np
from typing import Optional, Tuple


class Float_4E3M:
    """
    Custom 8-bit floating point format with 1 sign, 4 exponent, 3 mantissa bits.
    
    The value is calculated as: (-1)^s * 2^(-exponent) * ((8+mantissa)/8)
    where s is the sign bit, exponent is the 4-bit exponent value, 
    and mantissa is the 3-bit mantissa value.
    """
    
    # Class variables to store precomputed values for efficient conversion
    _all_values = None
    _all_components = None
    _initialized = False
    
    def __init__(self, sign: int, exponent: int, mantissa: int):
        """
        Initialize Float_4E3M with individual bit components.
        
        Args:
            sign (int): Sign bit (0 or 1)
            exponent (int): 4-bit exponent value (0-15)
            mantissa (int): 3-bit mantissa value (0-7)
        """
        # Validate input ranges
        if not (0 <= sign <= 1):
            raise ValueError("Sign bit must be 0 or 1")
        if not (0 <= exponent <= 15):
            raise ValueError("Exponent must be between 0 and 15 (4 bits)")
        if not (0 <= mantissa <= 7):
            raise ValueError("Mantissa must be between 0 and 7 (3 bits)")
        
        self.sign = sign
        self.exponent = exponent
        self.mantissa = mantissa
        
        # Initialize precomputed values if not already done
        if not Float_4E3M._initialized:
            Float_4E3M._initialize_lookup_tables()
    
    @classmethod
    def _initialize_lookup_tables(cls):
        """
        Initialize lookup tables with all possible Float_4E3M values for efficient conversion.
        Uses numpy for vectorized computation.
        """
        if cls._initialized:
            return
        
        # Create arrays for all possible bit patterns
        all_bits = np.arange(256, dtype=np.uint8)
        
        # Extract sign, exponent, and mantissa for all bit patterns
        signs = (all_bits >> 7) & 1
        exponents = (all_bits >> 3) & 0xF
        mantissas = all_bits & 0x7
        
        # Compute all values using vectorized operations
        # value = (-1)^s * 2^(-exponent) * ((8+mantissa)/8)
        sign_factors = np.where(signs == 0, 1.0, -1.0)
        exponent_factors = 2.0 ** (-exponents.astype(np.float64))
        mantissa_factors = (8 + mantissas.astype(np.float64)) / 8.0
        
        cls._all_values = sign_factors * exponent_factors * mantissa_factors
        cls._all_components = np.column_stack((signs, exponents, mantissas))
        cls._initialized = True
    @property
    def value(self) -> float:
        """
        Calculate the floating-point value using the formula:
        value = (-1)^s * 2^(-exponent) * ((8+mantissa)/8)
        
        Returns:
            float: The calculated floating-point value
        """
        sign_factor = (-1) ** self.sign
        exponent_factor = 2 ** (-self.exponent)
        mantissa_factor = (8 + self.mantissa) / 8
        
        return sign_factor * exponent_factor * mantissa_factor
    
    @classmethod
    def from_bits(cls, bits: int) -> 'Float_4E3M':
        """
        Create Float_4E3M from an 8-bit integer representation.
        
        Bit layout: SEEEMMM
        - Bit 7: Sign
        - Bits 6-3: Exponent
        - Bits 2-0: Mantissa
        
        Args:
            bits (int): 8-bit integer (0-255)
            
        Returns:
            Float_4E3M: New instance created from bit pattern
        """
        if not (0 <= bits <= 255):
            raise ValueError("Bits must be between 0 and 255 (8 bits)")
        
        sign = (bits >> 7) & 1
        exponent = (bits >> 3) & 0xF  # Extract bits 6-3
        mantissa = bits & 0x7         # Extract bits 2-0
        
        return cls(sign, exponent, mantissa)
    
    def to_bits(self) -> int:
        """
        Convert Float_4E3M to 8-bit integer representation.
        
        Returns:
            int: 8-bit integer representation
        """
        return (self.sign << 7) | (self.exponent << 3) | self.mantissa
    
    def to_bitstring(self) -> str:
        """
        Convert to binary string representation.
        
        Returns:
            str: 8-bit binary string (e.g., "10110101")
        """
        return f"{self.to_bits():08b}"
    
    @classmethod
    def from_value(cls, value: float) -> 'Float_4E3M':
        """
        Convert a regular float to Float_4E3M by finding the closest representation.
        Uses precomputed numpy arrays for efficient minimum distance calculation.
        
        Args:
            value (float): The value to convert
            
        Returns:
            Float_4E3M: Closest Float_4E3M representation
        """
        # Ensure lookup tables are initialized
        if not cls._initialized:
            cls._initialize_lookup_tables()
        
        # Handle special cases
        if np.isnan(value):
            raise ValueError("Cannot convert NaN to Float_4E3M representation")
        
        if np.isinf(value):
            if value > 0:
                # Positive infinity -> (0, 0, 7) - largest positive value
                return cls(0, 0, 7)
            else:
                # Negative infinity -> (1, 0, 7) - largest negative value
                return cls(1, 0, 7)
        
        if value == 0.0:
            # Zero -> (0, 15, 0) - smallest positive value with largest exponent
            return cls(0, 15, 0)
        
        # Find the index with minimum absolute difference
        differences = np.abs(cls._all_values - value)
        best_index = np.argmin(differences)
        
        # Extract the best components
        sign, exponent, mantissa = cls._all_components[best_index]
        
        return cls(int(sign), int(exponent), int(mantissa))
    
    def __str__(self) -> str:
        """String representation showing bit pattern and value."""
        return f"Float_4E3M({self.to_bitstring()}) = {self.value}"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"Float_4E3M(sign={self.sign}, exp={self.exponent}, mant={self.mantissa}, value={self.value})"
    
    def __add__(self, other: 'Float_4E3M') -> 'Float_4E3M':
        """
        Add two Float_4E3M numbers by converting to float, adding, then converting back.
        
        Args:
            other (Float_4E3M): The other number to add
            
        Returns:
            Float_4E3M: Result of addition converted back to Float_4E3M
        """
        if not isinstance(other, Float_4E3M):
            raise TypeError("Can only add Float_4E3M to Float_4E3M")
        
        result_value = self.value + other.value
        return Float_4E3M.from_value(result_value)
    
    def __eq__(self, other) -> bool:
        """Check equality based on bit representation."""
        if not isinstance(other, Float_4E3M):
            return False
        return self.to_bits() == other.to_bits()
    
    def __hash__(self) -> int:
        """Hash based on bit representation."""
        return hash(self.to_bits())

