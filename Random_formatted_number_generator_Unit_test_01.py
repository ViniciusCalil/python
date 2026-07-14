'''
------------------------------------------------------
          UNIT TEST PROGRAM FOR 
   Random STRING GENERATOR - BINARY VALUES version 01

version: 01
Created by Gemini in 2026-06-16
------------------------------------------------------
'''

import unittest
import re
from Random_formatted_number_generator import RandomFormattedNumberGenerator, FormattedNumberGeneratorError

class TestRandomFormattedNumberGenerator(unittest.TestCase):

    def test_default_decimal_no_prefix(self):
        """Tests that omitting base_format defaults to 'dec' without a prefix."""
        # Max bounds are 10, 5, 20. Non-numeric structures match exactly.
        value_format = "10-5,;20"
        result = RandomFormattedNumberGenerator.generate(value_format)
        
        # Split output to verify random ranges
        tokens = re.split(r'[-–,;\s]+', result)
        self.assertEqual(len(tokens), 3)
        
        val1, val2, val3 = int(tokens[0]), int(tokens[1]), int(tokens[2])
        self.assertTrue(0 <= val1 <= 10)
        self.assertTrue(0 <= val2 <= 5)
        self.assertTrue(0 <= val3 <= 20)

    def test_hex_with_prefix(self):
        """Tests hexadecimal formatting profile containing prefixes."""
        value_format = "255abc15"
        result = RandomFormattedNumberGenerator.generate(value_format, base_format='hex', display_prefix=True)
        
        # Numeric blocks are separated by "abc"
        parts = result.split("abc")
        self.assertEqual(len(parts), 2)
        
        # Verify first segment starts with hex prefix '0x'
        self.assertTrue(parts[0].startswith("0x"))
        # Parse value back from hex string to verify it is within bounds
        val1 = int(parts[0], 16)
        self.assertTrue(0 <= val1 <= 255)

    def test_binary_without_prefix(self):
        """Tests binary formatting configuration without its standard prefix."""
        value_format = "7"
        result = RandomFormattedNumberGenerator.generate(value_format, base_format='bin', display_prefix=False)
        
        # It should contain only valid binary digits 0 and 1, no '0b'
        self.assertNotIn("0b", result)
        val = int(result, 2)
        self.assertTrue(0 <= val <= 7)

    def test_octal_with_prefix(self):
        """Tests octal configuration utilizing its prefix constraint."""
        value_format = "64"
        result = RandomFormattedNumberGenerator.generate(value_format, base_format='oct', display_prefix=True)
        
        self.assertTrue(result.startswith("0"))
        val = int(result, 8)
        self.assertTrue(0 <= val <= 64)

    def test_invalid_base_format_exception(self):
        """Verifies that an unmapped invalid base configuration string throws errors."""
        with self.assertRaises(FormattedNumberGeneratorError) as ctx:
            RandomFormattedNumberGenerator.generate("10", base_format="invalid_base")
        self.assertIn("Invalid 'base_format'", str(ctx.exception))

    def test_empty_format_string_exception(self):
        """Verifies that processing empty formatting items triggers failure paths."""
        with self.assertRaises(FormattedNumberGeneratorError):
            RandomFormattedNumberGenerator.generate("")

if __name__ == "__main__":
    # Execute the test framework configuration
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
