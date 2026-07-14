'''
-------------------------------------------
   RANDOM STRING GENERATOR - BINARY VALUES

version: 01
Created by Gemini in 2026-06-16
-------------------------------------------
'''

# The code uses the secrets module for cryptographically secure, uniform 
# random integer generation. It uses the re (regular expression) module to cleanly 
# split the input format string into alternating numeric and non-numeric pieces.

r'''
How This Code Works:
 * Structural Tokenization: The expression re.split(r'(\d+)', value_format) breaks the layout into clean segments. For example, "100-abc-5" becomes ['100', '-abc-', '5']. This preserves the exact sequence spacing of non-numeric blocks.
 * Uniform Range Boundaries: The secrets.randbelow(max_val + 1) method ensures every number from 0 to the upper numeric value has an equal mathematical chance of being selected.
 * Custom Base Shifting: Standard conversions (hex(), oct(), bin()) naturally add default prefixes. The helper method strips these away ([2:]) and manually applies prefixes only if display_prefix evaluates to True.

Usage: 
   from Random_formatted_number_generator import RandomFormattedNumberGenerator, FormattedNumberGeneratorError ;
   RandomFormattedNumberGenerator.generate("23h59m59.999s")  # Random Time
   RandomFormattedNumberGenerator.generate("255.255.255.255") # Random IP Address
   RandomFormattedNumberGenerator.generate("255-255-255-255-255-255", base_format='hex') # Random MAC Address
   RandomFormattedNumberGenerator.generate("255", base_format='bin', display_prefix=True)  # Random bit stream up to 8 bits; decimal value = (2^8)-1 .
   RandomFormattedNumberGenerator.generate("7&11!13@17-21#23abc29.0", base_format='hex')     # Complex pattern

'''


import re
import secrets
from typing import Optional

class FormattedNumberGeneratorError(Exception):
    """Custom exception for verification and validation errors."""
    pass

class RandomFormattedNumberGenerator:
    # Set up valid base configurations: (base_number, prefix)
    VALID_BASES = {
        'hex': (16, '0x'),
        'oct': (8, '0'),
        'bin': (2, '0b'),
        'dec': (10, '')
    }

    @classmethod
    def _format_value(cls, value: int, base_format: str, display_prefix: bool) -> str:
        """Converts an integer to the requested string format with optional prefixes."""
        base_num, prefix = cls.VALID_BASES[base_format]

        # Convert to target base string representation
        if base_format == 'hex':
            # Remove default python prefix '0x' to handle custom prefix rules
            text_rep = hex(value)[2:]
        elif base_format == 'oct':
            text_rep = oct(value)[2:]
        elif base_format == 'bin':
            text_rep = bin(value)[2:]
        else:
            text_rep = str(value)

        # Apply prefix rules if display_prefix is explicitly requested
        if display_prefix:
            return f"{prefix}{text_rep}"
        return text_rep

    @classmethod
    def generate(cls, value_format: str, base_format: Optional[str] = None, display_prefix: bool = False) -> str:
        """
        Generates a string where numeric blocks are replaced by random values
        up to their original value, preserving non-numeric structures.
        """
        # 1. Parameter Validation & Defaults Setting
        if not value_format:
            raise FormattedNumberGeneratorError("ERROR: The 'value_format' string cannot be empty.")

        if base_format is None:
            base_format = 'dec'
            
        if base_format not in cls.VALID_BASES:
            raise FormattedNumberGeneratorError(
                f"ERROR: Invalid 'base_format' '{base_format}'. "
                f"Valid values are: {list(cls.VALID_BASES.keys())}"
            )

        # 2. Tokenize the String into Substrings
        # Regex captures consecutive digits (\d+) alternating with non-digits (\D+)
        tokens = re.split(r'(\d+)', value_format)
        
        output_segments = []

        # 3. Process and Replicate the Sequence
        for token in tokens:
            if not token:
                continue # Skip empty matches from regex split boundaries
                
            if token.isdigit():
                # Extract numerical value boundary
                max_val = int(token)
                
                # Generate random uniform value between 0 and max_val (inclusive)
                # secrets.randbelow(N) gives 0 to N-1, so we pass max_val + 1
                random_val = secrets.randbelow(max_val + 1)
                
                # Convert numeric token into target representation
                formatted_segment = cls._format_value(random_val, base_format, display_prefix)
                output_segments.append(formatted_segment)
            else:
                # Keep non-numeric structural chunks exactly as they are
                output_segments.append(token)

        return "".join(output_segments)
