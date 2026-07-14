'''
--------------------------------
   RANDOM STRING GENERATOR A 

version: 02
Created by Gemini in 2026-06-16
Altered by Vin Calil in 2026-06-20
--------------------------------
'''

# The code uses standard Python libraries. It uses the secrets module for secure, 
#   uniform random selection. It uses the unicodedata module to handle UTF-8 
#   accented characters correctly.

'''
How This Code Works:
 * Fisher-Yates Scrambling Algorithm: The _scramble_string method rearranges the final combined strings securely without losing array index properties.
 * Unicode Support: Character check evaluations use unicodedata.category(). It correctly handles non-English alphabet tokens (like á, ó, ç), classifying them under letter-based Unicode boundaries (L).
 * Warning Delivery Flow: Duplicate items trigger standard Python UserWarning elements right before output string returns. This fulfills the requirement to return the generated output string while showing the warning.

Usage:
 * from Random_string_generator_Char import RandomStringGenerator;
   RandomStringGenerator.generate(26, 18, 4, 4, special=" _@*^%!#")   # special="#@%()_="
   RandomStringGenerator.generate_formatted(format_str="aAIIIIIIIIIIIIIIII0000####",  special=" _@*^%!#", scramble=True)

'''

import string
import secrets
import warnings
import unicodedata
from typing import Optional, Tuple, List, Dict, Final

# == Custom Exception for Validation Errors
class StringGeneratorError(Exception):
    """Custom exception for string generation validation errors."""
    pass

class RandomStringGenerator:
    # == Default character pools
    DEFAULT_NUMERIC = "0123456789"
    DEFAULT_SPECIAL = "-_@#"
    
    # == Define the minimum number of characters required in a pool so this pool can be used.
    PERMITTED_MIN: Final[int] = 2
   
    @classmethod
    def _get_default_alpha(cls) -> str:
        """Generates default UTF-8 alpha characters including basic ASCII."""
        # return (DEFAULT_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        return string.ascii_letters

    @classmethod
    def _analyze_pool(cls, pool: str, pool_type: str) -> Tuple[Dict[str, int], Dict[str, List[int]]]:
        """
        Analyzes a character pool for invalid and repeated characters.
        Returns cleaned pool, list of invalid chars, and a dict of repeat positions.
        """
        invalid_chars = dict()        
        repeat_positions = dict()
        seen_indices = dict() 
        
        is_invalid = bool()
        
        for idx, char in enumerate(pool):
            
            # == Track duplicates and their positions.
            if char in seen_indices:
                if char not in repeat_positions:
                    repeat_positions[char] = [seen_indices[char]]
                repeat_positions[char].append(idx)
            else:
                seen_indices[char] = idx

            # == Track invalid characters and their positions.
            # Check character type validity using Unicode categories
            # L = Letter, N = Number, P/S = Punctuation/Symbol (Special)
            cat = unicodedata.category(char)
            is_invalid = False
            if pool_type == "alpha" and not cat.startswith("L"):
                is_invalid = True
            elif pool_type == "numeric" and not cat.startswith("N"):
                is_invalid = True
            elif pool_type == "special" and (cat.startswith("L") or cat.startswith("N")):
                is_invalid = True

            if (is_invalid):
                # == Track only the frist time the invalid characters appears.
                if char not in invalid_chars:
                    invalid_chars[char] = idx

        return invalid_chars, repeat_positions

    @classmethod
    def _validate_pools(cls, alpha: Optional[str], numeric: Optional[str], special: Optional[str]) -> Tuple[str, str, str, List[str]]:
        """Validates all pools, throws errors for invalid types, collects warnings for duplicates."""
        # == Set defaults if not provided
        alpha_pool = alpha if alpha is not None else cls._get_default_alpha()
        numeric_pool = numeric if numeric is not None else cls.DEFAULT_NUMERIC
        special_pool = special if special is not None else cls.DEFAULT_SPECIAL

        # == Validate minimum permitted length of the pools
        if (len(alpha_pool) < cls.PERMITTED_MIN):
            raise StringGeneratorError(
                "ERROR: The minimum permitted length of 'valid alpha characters' input string is 2. "
            )
        if (len(numeric_pool) < cls.PERMITTED_MIN):
            raise StringGeneratorError(
                "ERROR: The minimum permitted length of 'valid numeric characters' input string is 2. "
            )            
        if (len(special_pool) < cls.PERMITTED_MIN):
            raise StringGeneratorError(
                "ERROR: The minimum permitted length of 'valid special characters' input string is 2. "
            )          
            
        pending_warnings = []
        
        # == Validate Alpha Pool
        inv_a, rep_a = cls._analyze_pool(alpha_pool, "alpha")
        if inv_a:
            raise StringGeneratorError(
                f"ERROR: Presence of non alpha characters in the 'valid alpha characters' input string is forbidden. "
                f"Invalid: {inv_a}. Positions detailed in exception context."
            )
        if rep_a:
            pending_warnings.append(("alpha", rep_a))
            
        # == Validate Numeric Pool
        inv_n, rep_n = cls._analyze_pool(numeric_pool, "numeric")
        if inv_n:
            raise StringGeneratorError(
                f"ERROR: Presence of non numeric characters in the 'valid numeric characters' input string is forbidden. "
                f"Invalid: {inv_n}. Positions detailed in exception context."
            )
        if rep_n:
            pending_warnings.append(("numeric", rep_n))
            
        # == Validate Special Pool
        inv_s, rep_s = cls._analyze_pool(special_pool, "special")
        if inv_s:
            raise StringGeneratorError(
                f"ERROR: Presence of non special characters in the 'valid special characters' input string is forbidden. "
                f"Invalid: {inv_s}. Positions detailed in exception context."
            )
        if rep_s:
            pending_warnings.append(("special", rep_s))
            
        return alpha_pool, numeric_pool, special_pool, pending_warnings

    @classmethod
    def _trigger_warnings(cls, pending_warnings: List[tuple], output_str: str):
        """Triggers warnings after the final string is calculated."""
        for pool_type, repeats in pending_warnings:
            warnings.warn(
                f"\nThere is repeated elements in the 'valid {pool_type} characters' input string.\n"
                f"Calculated Output String: {output_str}\n"
                f"Repeated Elements Map (char: positions): {repeats}\n",
                UserWarning
            )

    @classmethod
    def _scramble_string(cls, s: str) -> str:
        """Scrambles a string using cryptographically secure random indices."""
        chars = list(s)

        # == Fisher-Yates shuffle using secrets module
        for i in range(len(chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            chars[i], chars[j] = chars[j], chars[i]
        return "".join(chars)


    @classmethod
    def _analyze_alpha_subpools(cls, subpool: str, frmt_str: str, case_map: str, case_name: str):
        """
        Analyze whether an aplha sub-pool (whether lowercase or uppercase) has the
        minimum required number of characters to enable a random character choice. 
        """    
        if not subpool:           
            # == Track indices of frmt_str characters thas requires any 'case_map' characters.
            invalid_positions = dict()
            for idx, char in enumerate(frmt_str):
                for mapchar in case_map:
                    if char == mapchar:
                        if char not in invalid_positions:
                            invalid_positions[char] = [idx]
                        else :
                            invalid_positions[char].append(idx)            

            if invalid_positions :
                raise StringGeneratorError(
                    f"ERROR: The 'format_str' input string cannot have any character "
                    f"of the sequence '{case_map}' when the 'valid alpha characters' " 
                    f"input string has no {case_name} characters."
                    f"\nInvalid Formatting characters for '{case_name}' (char: positions): {invalid_positions}\n",
                    )
                
        elif (len(subpool) < cls.PERMITTED_MIN) :
            raise StringGeneratorError(
                f"ERROR: The minimum number of '{case_name}' characters in the 'valid "
                f"alpha characters' input string must be '{cls.PERMITTED_MIN}' when the "
                f"'format_str' input string has any character of the sequence '{case_map}'. "
            )           


    @classmethod
    def _validate_alpha_subpools(cls, a_low: str, a_upp: str, frmt_str: str):
        """
        Analyzes if the 'format_str' input string from the 'generate_formatted()'
        method has formatting characters that requires any alpha character from
        a sub-pool that is empty or has less elements than the minimum permitted.
        """

        low_map = "an@x"
        has_lowmap = set(frmt_str).intersection(low_map)
        if has_lowmap:
            # == Track indices of Format string characters thas requires lowercase characters.
            cls._analyze_alpha_subpools(a_low, frmt_str, low_map, "lowercase")
                # -- Note: even when there is no lowercase characters, the "I", "T", "&", and "Z" formats are still allowed.
    
        upp_map = "AN$X"
        has_uppmap = set(frmt_str).intersection(upp_map)
        if has_uppmap:
            # == Track indices of Format string characters thas requires uppercase characters.
            cls._analyze_alpha_subpools(a_upp, frmt_str, upp_map, "uppercase")
                # -- Note: even when there is no uppercase characters, the "I", "T", "&", and "Z" formats are still allowed.
        


    @classmethod
    def generate(cls, total: int, num_alpha: int, num_numeric: int, num_special: int, 
                    alpha: Optional[str] = None, numeric: Optional[str] = None, special: Optional[str] = None) -> str:
        """Version 1: Generates random string based on character counts."""
        # == Check sum restriction
        if num_alpha + num_numeric + num_special != total:
            raise StringGeneratorError(
                f"ERROR: the total number of characters is different from the summation of alpha, numeric and especial characters. "
                f"Parameters provided: [Total: {total}, Alpha: {num_alpha}, Numeric: {num_numeric}, Special: {num_special}]"
            )
            
        a_pool, n_pool, s_pool, pending_warnings = cls._validate_pools(alpha, numeric, special)
        
        # == Generate components using uniform distribution choice via secrets
        out_alpha = "".join(secrets.choice(a_pool) for _ in range(num_alpha))
        out_numeric = "".join(secrets.choice(n_pool) for _ in range(num_numeric))
        out_special = "".join(secrets.choice(s_pool) for _ in range(num_special))
        
        # == Concatenate and scramble
        combined = out_alpha + out_numeric + out_special
        final_str = cls._scramble_string(combined)
        
        cls._trigger_warnings(pending_warnings, final_str)
        return final_str

    @classmethod
    def generate_formatted(cls, format_str: str, alpha: Optional[str] = None, numeric: Optional[str] = None, 
                    special: Optional[str] = None, scramble: bool = False) -> str:
        """Formatted version: Generates random string based on a format mask string."""
        a_pool, n_pool, s_pool, pending_warnings = cls._validate_pools(alpha, numeric, special)
        
        # == Separate sub-pools for easy format mapping
        a_low = "".join([c for c in a_pool if unicodedata.category(c) == "Ll" or c.islower()])
        a_upp = "".join([c for c in a_pool if unicodedata.category(c) == "Lu" or c.isupper()])

#        print("sub-pool lower: ", a_low)        
#        print("sub-pool upper: ", a_upp)        

        # == Fallback to standard defaults if custom pool lacks a specific case
        # if not a_low: a_low = string.ascii_lowercase
        # if not a_upp: a_upp = string.ascii_uppercase
        
        # == Map tokens to their corresponding pool choices
        token_map = {
            "a": lambda: secrets.choice(a_low) if a_low else None,
            "A": lambda: secrets.choice(a_upp) if a_upp else None,
            "I": lambda: secrets.choice(a_pool),
            "0": lambda: secrets.choice(n_pool),
            "#": lambda: secrets.choice(s_pool),
            "n": lambda: secrets.choice(a_low + n_pool) if a_low else None,
            "N": lambda: secrets.choice(a_upp + n_pool) if a_upp else None,
            "T": lambda: secrets.choice(a_pool + n_pool),
            "@": lambda: secrets.choice(a_low + s_pool) if a_low else None,
            "$": lambda: secrets.choice(a_upp + s_pool) if a_upp else None,
            "&": lambda: secrets.choice(a_pool + s_pool),
            "x": lambda: secrets.choice(a_low + n_pool + s_pool) if a_low else None,
            "X": lambda: secrets.choice(a_upp + n_pool + s_pool) if a_upp else None,
            "Z": lambda: secrets.choice(a_pool + n_pool + s_pool),
        }
        
        cls._validate_alpha_subpools(a_low, a_upp, format_str)         
        
        output_chars = []
        for idx, char in enumerate(format_str):
            if char in token_map:
                output_chars.append(token_map[char]())
            else:
                raise StringGeneratorError(f"ERROR: Invalid character mask token '{char}' found in format string at index {idx}.")
                
        final_str = "".join(output_chars)
        
        if scramble:
            final_str = cls._scramble_string(final_str)
            
        cls._trigger_warnings(pending_warnings, final_str)
        return final_str

# = - = - = - = - = - = - = - = - = - = - = - = - 


 
