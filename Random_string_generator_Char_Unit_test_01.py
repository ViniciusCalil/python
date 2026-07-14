'''
----------------------------------------
   UNIT TEST PROGRAM FOR
   Random String Generator-Char-version 01.

version: 01
Created by Gemini in 2026-06-16
Altered by Vin Calil in 2026-06-20
----------------------------------------
'''

import unittest
import warnings
from Random_string_generator_Char import RandomStringGenerator, StringGeneratorError

class TestRandomStringGenerator(unittest.TestCase):

    def test_successful_generation(self):
        """Tests standard execution of Version 1 with standard boundaries."""
        total = 32
        result = RandomStringGenerator.generate(total=total, num_alpha=11, num_numeric=11, num_special=10)
        self.assertEqual(len(result), total)

    def test_summation_error(self):
        """Tests that version 1 throws an error if totals do not add up."""
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(total=10, num_alpha=2, num_numeric=2, num_special=2)
        self.assertIn("the total number of characters is different from the summation", str(ctx.exception))

    def test_utf8_and_duplicate_warnings(self):
        """Tests UTF-8 accented characters and ensures duplicate pools throw warnings."""
        # Using accented alpha pool containing intentional duplicates ('á', 'é')
        custom_alpha = "áéíóúáéé" 
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = RandomStringGenerator.generate(
                total=24, num_alpha=24, num_numeric=0, num_special=0, alpha=custom_alpha
            )
            # Verify the warning triggered for repeated character elements
            self.assertTrue(len(w) >= 1)
            self.assertIn("There is repeated elements in the 'valid alpha characters'", str(w[-1].message))
            self.assertEqual(len(result), 24)
#        print('result', result)

    def test_costum_pools(self):
        """Tests custom pools."""
        # Using accented alpha pool containing intentional duplicates ('á', 'é')
        custom_alpha = "vwxyz" 
        custom_numeric = "1357" 
        custom_special = "!@#""" 
        
        total = 32
        result = RandomStringGenerator.generate(total=total, num_alpha=11, 
            num_numeric=11, num_special=10, alpha=custom_alpha, 
            numeric=custom_numeric, special=custom_special)
        self.assertEqual(len(result), total)

   
    def test_invalid_pool_types(self):
        """Tests that mixing incorrect types into specialized pools raises exceptions."""
        # Mixing a number into an alpha pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, alpha="abc1")
        self.assertIn("Presence of non alpha characters in the 'valid alpha characters'", str(ctx.exception))
            
        # Mixing a special character into an alpha pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, alpha="abc#")
        self.assertIn("Presence of non alpha characters in the 'valid alpha characters'", str(ctx.exception))
            
        # Mixing an alpha into a numeric pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, numeric="123a")
        self.assertIn("Presence of non numeric characters in the 'valid numeric characters'", str(ctx.exception))

        # Mixing a special character into a numeric pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, numeric="123$")
        self.assertIn("Presence of non numeric characters in the 'valid numeric characters'", str(ctx.exception))

        # Mixing an alpha into a special pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, special="!@#a")
        self.assertIn("Presence of non special characters in the 'valid special characters'", str(ctx.exception))

        # Mixing a number into a special pool
        with self.assertRaises(StringGeneratorError):
            RandomStringGenerator.generate(3, 1, 1, 1, special="$%&5")
        self.assertIn("Presence of non special characters in the 'valid special characters'", str(ctx.exception))

    def test_small_pool_sizes(self):
        """Tests that minimum required number fo elemets in any pool."""
        # Empty alpha pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, alpha="")
        self.assertIn("The minimum permitted length of 'valid alpha characters'", str(ctx.exception))
            
        # Alpha pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, alpha="h")
        self.assertIn("The minimum permitted length of 'valid alpha characters'", str(ctx.exception))
            
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, numeric="")
        self.assertIn("The minimum permitted length of 'valid numeric characters'", str(ctx.exception))
            
        # Alpha pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, numeric="4")
        self.assertIn("The minimum permitted length of 'valid numeric characters'", str(ctx.exception))
            
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, special="")
        self.assertIn("The minimum permitted length of 'valid special characters'", str(ctx.exception))
            
        # Alpha pool
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate(3, 1, 1, 1, special="%")
        self.assertIn("The minimum permitted length of 'valid special characters'", str(ctx.exception))
            
            
    def test_v2_mask_replacements(self):
        """Tests that version 2 maps complex masked string profiles correctly."""
        # '0' must yield a number, '#' must yield a special character
        format_str = "00##aA"
        result = RandomStringGenerator.generate_formatted(format_str=format_str, scramble=False)
        
        self.assertEqual(len(result), 6)
        self.assertTrue(result[0].isdigit())
        self.assertTrue(result[1].isdigit())
        self.assertIn(result[2], "-_@#")
        self.assertIn(result[3], "-_@#")
        self.assertTrue(result[4].islower())
        self.assertTrue(result[5].isupper())
        
        format_str = "AIa"
        alpha = "VWXdef"
        result = RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha, scramble=False)
        self.assertEqual(len(result), 3)
        self.assertTrue(result[0].isupper() and result[1].isalpha() and result[2].islower())

        """ Scramble the output random string, but keeps number and type of characters defined in 'format_str'."""
        format_str = "AIa"
        alpha = "VWXdef"
        result = RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha, scramble=True)
        self.assertEqual(len(result), 3)
        chars_upp = True if (result[0].isupper() or result[1].isupper() or result[2].isupper()) else False
        chars_low = True if (result[0].islower() or result[1].islower() or result[2].islower()) else False
        self.assertTrue(chars_upp and chars_low)
        
        format_str = "AX"
        alpha = "VWXDEF"
        result = RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha, scramble=False)
        self.assertEqual(len(result), 2)        
        self.assertTrue(result[0].isupper())
        self.assertTrue(not result[1].islower())
        
    def test_v2_invalid_token(self):
        """Tests that version 2 throws an error if an unmapped format item is used."""
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate_formatted(format_str="aA0#_INVALID_TOKEN")
        self.assertIn("Invalid character mask token ", str(ctx.exception))

    def test_v2_lacking_token(self):
        """Tests that version 2 throws an error when an empty sub-pool token is required in format_str."""                
        format_str = "Xa"
        alpha = "abcdef"
        with self.assertRaises(StringGeneratorError) as ctx:
            result = RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha, scramble=False)
        self.assertIn("'format_str' input string cannot have any character", str(ctx.exception))
        self.assertIn("string has no uppercase characters", str(ctx.exception))
        
        format_str = "xA"
        alpha = "abcdef"
        with self.assertRaises(StringGeneratorError) as ctx:
            result = RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha, scramble=False)
        self.assertIn("'format_str' input string cannot have any character", str(ctx.exception))
        self.assertIn("string has no uppercase characters", str(ctx.exception))
        
        format_str = "xA"
        alpha = "ABCDEF"
        with self.assertRaises(StringGeneratorError) as ctx:
            result = RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha, scramble=False)
        self.assertIn("'format_str' input string cannot have any character", str(ctx.exception))
        self.assertIn("string has no lowercase characters", str(ctx.exception))
        
        format_str = "Xa"
        alpha = "ABCDEF"
        with self.assertRaises(StringGeneratorError) as ctx:
            result = RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha, scramble=False)
        self.assertIn("'format_str' input string cannot have any character", str(ctx.exception))
        self.assertIn("string has no lowercase characters", str(ctx.exception))
        
        """Tests that version 2 throws an error when a sub-pool has less 'PERMITTED_MIN'characters."""                
        format_str = "AXa"
        alpha = "Asdfg"
        with self.assertRaises(StringGeneratorError) as ctx:
            print("xxx >> ",RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha) )
        self.assertIn("The minimum number of 'uppercase' characters", str(ctx.exception))
        
        format_str = "AXa"
        alpha = "aSDFG"
        with self.assertRaises(StringGeneratorError) as ctx:
            RandomStringGenerator.generate_formatted(format_str=format_str, alpha=alpha)
        self.assertIn("The minimum number of 'lowercase' characters", str(ctx.exception))
        
    

if __name__ == "__main__":
    # Run the tests directly
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
