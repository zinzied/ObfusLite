"""
Steganographic Encoding for Python Code Obfuscation
Hides code within seemingly innocent data structures
"""

import random
import string
import base64
import json
import math
from typing import Dict, Any, List, Tuple
from obfuscator_core import BaseEncoder

class SteganographicEncoder(BaseEncoder):
    """
    Steganographic encoder that hides code within innocent-looking data
    such as fake configuration files, lorem ipsum text, or mathematical constants
    """
    
    def __init__(self):
        self.cover_types = {
            'lorem_ipsum': self._lorem_ipsum_cover,
            'config_file': self._config_file_cover,
            'math_constants': self._math_constants_cover,
            'fake_data': self._fake_data_cover,
            'poetry': self._poetry_cover
        }
        
        # Pre-generated cover text
        self.lorem_words = [
            'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
            'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
            'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
            'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
            'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate',
            'velit', 'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint',
            'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia',
            'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum'
        ]
        
    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode string data using steganographic techniques
        """
        # Convert to binary
        binary_data = ''.join(format(ord(char), '08b') for char in data)
        
        # Choose random cover type
        cover_type = random.choice(list(self.cover_types.keys()))
        
        # Generate cover data
        cover_data = self.cover_types[cover_type](binary_data)
        
        # Apply additional steganographic layers
        layered_data = self._apply_steganographic_layers(cover_data, binary_data)
        
        # Create decoy metadata
        decoy_metadata = self._generate_decoy_metadata(cover_type)
        
        # Encode as base64
        encoded_data = base64.b64encode(json.dumps({
            'cover_data': layered_data,
            'decoy_metadata': decoy_metadata
        }).encode()).decode()
        
        return {
            'encoded': encoded_data,
            'metadata': {
                'cover_type': cover_type,
                'original_length': len(data),
                'binary_length': len(binary_data),
                'steganographic_method': 'multi_layer'
            }
        }
        
    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode steganographically hidden data
        """
        # Decode from base64
        stego_data = json.loads(base64.b64decode(encoded_data.encode()).decode())
        
        # Extract cover data
        cover_data = stego_data['cover_data']
        cover_type = metadata['cover_type']
        
        # Reverse steganographic layers
        binary_data = self._extract_from_steganographic_layers(cover_data, cover_type)
        
        # Convert binary to string
        original_data = self._binary_to_string(binary_data, metadata['original_length'])
        
        return original_data
        
    def _lorem_ipsum_cover(self, binary_data: str) -> str:
        """Hide data in Lorem Ipsum text using word selection"""
        cover_text = []
        bit_index = 0
        
        # Generate enough text to hide all data
        while bit_index < len(binary_data):
            # Select word based on bit value
            if bit_index < len(binary_data):
                bit = binary_data[bit_index]
                if bit == '1':
                    # Choose word with odd length
                    word_candidates = [w for w in self.lorem_words if len(w) % 2 == 1]
                else:
                    # Choose word with even length
                    word_candidates = [w for w in self.lorem_words if len(w) % 2 == 0]
                    
                if word_candidates:
                    word = random.choice(word_candidates)
                else:
                    word = random.choice(self.lorem_words)
                    
                cover_text.append(word)
                bit_index += 1
                
            # Add some random words for naturalness
            if random.random() < 0.3:
                cover_text.append(random.choice(self.lorem_words))
                
        return ' '.join(cover_text) + '.'
        
    def _config_file_cover(self, binary_data: str) -> Dict[str, Any]:
        """Hide data in fake configuration file"""
        config = {
            'version': '1.0.0',
            'debug': False,
            'settings': {},
            'features': [],
            'metadata': {}
        }
        
        # Hide data in various config values
        bit_index = 0
        
        # Hide in version numbers
        version_parts = []
        for i in range(3):
            if bit_index + 3 < len(binary_data):
                bits = binary_data[bit_index:bit_index + 3]
                version_parts.append(str(int(bits, 2)))
                bit_index += 3
            else:
                version_parts.append(str(random.randint(0, 7)))
                
        config['version'] = '.'.join(version_parts)
        
        # Hide in boolean values
        bool_keys = ['debug', 'enabled', 'auto_update', 'logging', 'compression']
        for key in bool_keys:
            if bit_index < len(binary_data):
                config['settings'][key] = binary_data[bit_index] == '1'
                bit_index += 1
                
        # Hide in array lengths
        while bit_index + 4 < len(binary_data):
            bits = binary_data[bit_index:bit_index + 4]
            array_length = int(bits, 2)
            feature_name = f"feature_{len(config['features'])}"
            config['features'].extend([feature_name] * array_length)
            bit_index += 4
            
        # Hide remaining bits in metadata
        while bit_index < len(binary_data):
            key = f"param_{len(config['metadata'])}"
            if bit_index + 8 < len(binary_data):
                bits = binary_data[bit_index:bit_index + 8]
                config['metadata'][key] = int(bits, 2)
                bit_index += 8
            else:
                remaining_bits = binary_data[bit_index:]
                config['metadata'][key] = int(remaining_bits.ljust(8, '0'), 2)
                break
                
        return config
        
    def _math_constants_cover(self, binary_data: str) -> Dict[str, float]:
        """Hide data in mathematical constants"""
        constants = {
            'pi': math.pi,
            'e': math.e,
            'golden_ratio': (1 + math.sqrt(5)) / 2,
            'sqrt_2': math.sqrt(2),
            'sqrt_3': math.sqrt(3)
        }
        
        # Modify constants to encode data
        bit_index = 0
        
        for name, value in constants.items():
            if bit_index >= len(binary_data):
                break
                
            # Convert to string and modify decimal places
            value_str = f"{value:.15f}"
            decimal_part = value_str.split('.')[1]
            
            # Modify digits based on binary data
            modified_digits = []
            for i, digit in enumerate(decimal_part):
                if bit_index < len(binary_data):
                    bit = binary_data[bit_index]
                    # Modify digit based on bit
                    if bit == '1':
                        new_digit = str((int(digit) + 1) % 10)
                    else:
                        new_digit = digit
                    modified_digits.append(new_digit)
                    bit_index += 1
                else:
                    modified_digits.append(digit)
                    
            # Reconstruct number
            integer_part = value_str.split('.')[0]
            constants[name] = float(f"{integer_part}.{''.join(modified_digits)}")
            
        return constants
        
    def _fake_data_cover(self, binary_data: str) -> List[Dict[str, Any]]:
        """Hide data in fake database records"""
        records = []
        bit_index = 0
        
        names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry']
        cities = ['New York', 'London', 'Tokyo', 'Paris', 'Berlin', 'Sydney', 'Toronto']
        
        while bit_index < len(binary_data):
            record = {
                'id': len(records) + 1,
                'name': random.choice(names),
                'city': random.choice(cities),
                'active': True,
                'score': 0.0
            }
            
            # Hide data in various fields
            if bit_index < len(binary_data):
                record['active'] = binary_data[bit_index] == '1'
                bit_index += 1
                
            if bit_index + 7 < len(binary_data):
                bits = binary_data[bit_index:bit_index + 7]
                record['score'] = int(bits, 2) / 100.0
                bit_index += 7
                
            records.append(record)
            
            # Limit number of records
            if len(records) >= 20:
                break
                
        return records
        
    def _poetry_cover(self, binary_data: str) -> List[str]:
        """Hide data in poetry structure"""
        poem_lines = []
        bit_index = 0
        
        # Word pools for different syllable counts
        one_syllable = ['cat', 'dog', 'sun', 'moon', 'tree', 'sea', 'sky', 'bird']
        two_syllable = ['happy', 'garden', 'mountain', 'river', 'flower', 'dancing']
        three_syllable = ['beautiful', 'wonderful', 'amazing', 'fantastic']
        
        while bit_index < len(binary_data) and len(poem_lines) < 10:
            line_words = []
            line_bits = 0
            
            # Create line with 8-12 syllables
            target_syllables = random.randint(8, 12)
            current_syllables = 0
            
            while current_syllables < target_syllables and bit_index < len(binary_data):
                if bit_index + 1 < len(binary_data):
                    bits = binary_data[bit_index:bit_index + 2]
                    bit_index += 2
                    
                    # Choose word based on bits
                    if bits == '00':
                        word = random.choice(one_syllable)
                        syllables = 1
                    elif bits == '01':
                        word = random.choice(two_syllable)
                        syllables = 2
                    elif bits == '10':
                        word = random.choice(three_syllable)
                        syllables = 3
                    else:
                        word = random.choice(one_syllable)
                        syllables = 1
                        
                    if current_syllables + syllables <= target_syllables:
                        line_words.append(word)
                        current_syllables += syllables
                        
            poem_lines.append(' '.join(line_words))
            
        return poem_lines
        
    def _apply_steganographic_layers(self, cover_data: Any, binary_data: str) -> Any:
        """Apply additional steganographic layers"""
        # Convert cover data to string for processing
        if isinstance(cover_data, dict):
            cover_str = json.dumps(cover_data, sort_keys=True)
        elif isinstance(cover_data, list):
            cover_str = json.dumps(cover_data)
        else:
            cover_str = str(cover_data)
            
        # Apply LSB steganography to character codes
        modified_chars = []
        bit_index = 0
        
        for char in cover_str:
            char_code = ord(char)
            
            # Modify LSB if we have data to hide
            if bit_index < len(binary_data):
                bit = int(binary_data[bit_index])
                # Set LSB
                char_code = (char_code & 0xFE) | bit
                bit_index += 1
                
            modified_chars.append(chr(char_code))
            
        return ''.join(modified_chars)
        
    def _extract_from_steganographic_layers(self, cover_data: str, cover_type: str) -> str:
        """Extract data from steganographic layers"""
        binary_bits = []
        
        # Extract LSBs from character codes
        for char in cover_data:
            char_code = ord(char)
            lsb = char_code & 1
            binary_bits.append(str(lsb))
            
        return ''.join(binary_bits)
        
    def _generate_decoy_metadata(self, cover_type: str) -> Dict[str, Any]:
        """Generate fake metadata to throw off analysis"""
        return {
            'format': cover_type,
            'created': '2024-01-01T00:00:00Z',
            'author': 'System Generator',
            'checksum': random.randint(1000000, 9999999),
            'compression': 'none',
            'encoding': 'utf-8'
        }
        
    def _binary_to_string(self, binary_data: str, original_length: int) -> str:
        """Convert binary data back to string"""
        # Ensure binary data is multiple of 8
        while len(binary_data) % 8 != 0:
            binary_data += '0'
            
        chars = []
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                try:
                    chars.append(chr(int(byte, 2)))
                except ValueError:
                    chars.append('\x00')
                    
        result = ''.join(chars)
        return result[:original_length]
