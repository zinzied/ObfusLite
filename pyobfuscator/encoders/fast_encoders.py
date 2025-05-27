"""
Fast and Memory-Efficient Encoders for Python Code Obfuscation
Optimized versions that are lightweight and fast
"""

import base64
import json
import random
import string
import hashlib
import zlib
from typing import Dict, Any, List
from .base import BaseEncoder

class FastXOREncoder(BaseEncoder):
    """Fast XOR-based encoder with multiple keys"""

    def encode(self, data: str) -> Dict[str, Any]:
        # Generate multiple XOR keys
        keys = [random.randint(1, 255) for _ in range(4)]

        # Convert to bytes
        data_bytes = data.encode('utf-8')

        # Apply multiple XOR operations
        encoded_bytes = bytearray(data_bytes)
        for i, byte in enumerate(encoded_bytes):
            key_index = i % len(keys)
            encoded_bytes[i] = byte ^ keys[key_index]

        # Compress and encode
        compressed = zlib.compress(bytes(encoded_bytes))
        encoded_b64 = base64.b64encode(compressed).decode('ascii')

        return {
            'encoded': encoded_b64,
            'metadata': {
                'keys': keys,
                'original_length': len(data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        keys = metadata['keys']

        # Decode and decompress
        compressed = base64.b64decode(encoded_data.encode('ascii'))
        encoded_bytes = bytearray(zlib.decompress(compressed))

        # Reverse XOR operations
        for i, byte in enumerate(encoded_bytes):
            key_index = i % len(keys)
            encoded_bytes[i] = byte ^ keys[key_index]

        return bytes(encoded_bytes).decode('utf-8')

class FastBase64Encoder(BaseEncoder):
    """Fast Base64 encoder with character substitution"""

    def encode(self, data: str) -> Dict[str, Any]:
        # Create random character mapping
        chars = string.ascii_letters + string.digits + '+/='
        shuffled_chars = list(chars)
        random.shuffle(shuffled_chars)
        char_map = dict(zip(chars, shuffled_chars))

        # Encode to base64
        encoded_bytes = base64.b64encode(data.encode('utf-8'))
        encoded_str = encoded_bytes.decode('ascii')

        # Apply character substitution
        substituted = ''.join(char_map.get(c, c) for c in encoded_str)

        return {
            'encoded': substituted,
            'metadata': {
                'char_map': char_map,
                'original_length': len(data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        char_map = metadata['char_map']

        # Reverse character mapping
        reverse_map = {v: k for k, v in char_map.items()}
        original_b64 = ''.join(reverse_map.get(c, c) for c in encoded_data)

        # Decode from base64
        decoded_bytes = base64.b64decode(original_b64.encode('ascii'))
        return decoded_bytes.decode('utf-8')

class FastRotationEncoder(BaseEncoder):
    """Fast rotation cipher with multiple rounds"""

    def encode(self, data: str) -> Dict[str, Any]:
        # Generate rotation parameters
        rotations = [random.randint(1, 25) for _ in range(3)]

        encoded = data
        for rotation in rotations:
            # Apply Caesar cipher rotation
            result = []
            for char in encoded:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    rotated = chr((ord(char) - base + rotation) % 26 + base)
                    result.append(rotated)
                else:
                    result.append(char)
            encoded = ''.join(result)

        # Encode to base64 for safe storage
        encoded_b64 = base64.b64encode(encoded.encode('utf-8')).decode('ascii')

        return {
            'encoded': encoded_b64,
            'metadata': {
                'rotations': rotations,
                'original_length': len(data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        rotations = metadata['rotations']

        # Decode from base64
        encoded = base64.b64decode(encoded_data.encode('ascii')).decode('utf-8')

        # Reverse rotations in reverse order
        for rotation in reversed(rotations):
            result = []
            for char in encoded:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    rotated = chr((ord(char) - base - rotation) % 26 + base)
                    result.append(rotated)
                else:
                    result.append(char)
            encoded = ''.join(result)

        return encoded

class FastHashEncoder(BaseEncoder):
    """Fast hash-based encoder with lookup table"""

    def encode(self, data: str) -> Dict[str, Any]:
        # Split data into chunks
        chunk_size = 8
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        # Create hash mapping
        hash_map = {}
        encoded_hashes = []

        for chunk in chunks:
            # Create hash for chunk
            chunk_hash = hashlib.md5(chunk.encode()).hexdigest()[:8]
            hash_map[chunk_hash] = chunk
            encoded_hashes.append(chunk_hash)

        return {
            'encoded': '|'.join(encoded_hashes),
            'metadata': {
                'hash_map': hash_map,
                'original_length': len(data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        hash_map = metadata['hash_map']

        # Split encoded hashes
        hashes = encoded_data.split('|')

        # Reconstruct original data
        chunks = [hash_map[h] for h in hashes if h in hash_map]
        return ''.join(chunks)

class FastBinaryEncoder(BaseEncoder):
    """Fast binary encoder with bit manipulation"""

    def encode(self, data: str) -> Dict[str, Any]:
        # Convert to binary
        binary = ''.join(format(ord(char), '08b') for char in data)

        # Apply bit shifts
        shift = random.randint(1, 7)
        shifted_bits = []

        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                # Shift bits
                shifted = byte[shift:] + byte[:shift]
                shifted_bits.append(shifted)

        # Convert back to characters
        shifted_binary = ''.join(shifted_bits)
        encoded_chars = []

        for i in range(0, len(shifted_binary), 8):
            byte = shifted_binary[i:i+8]
            if len(byte) == 8:
                encoded_chars.append(chr(int(byte, 2)))

        encoded_str = ''.join(encoded_chars)
        encoded_b64 = base64.b64encode(encoded_str.encode('latin-1')).decode('ascii')

        return {
            'encoded': encoded_b64,
            'metadata': {
                'shift': shift,
                'original_length': len(data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        shift = metadata['shift']

        # Decode from base64
        encoded_str = base64.b64decode(encoded_data.encode('ascii')).decode('latin-1')

        # Convert to binary
        binary = ''.join(format(ord(char), '08b') for char in encoded_str)

        # Reverse bit shifts
        original_bits = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                # Reverse shift
                original = byte[-shift:] + byte[:-shift]
                original_bits.append(original)

        # Convert back to characters
        original_binary = ''.join(original_bits)
        chars = []

        for i in range(0, len(original_binary), 8):
            byte = original_binary[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))

        return ''.join(chars)

class FastLookupEncoder(BaseEncoder):
    """Fast lookup table encoder"""

    def encode(self, data: str) -> Dict[str, Any]:
        # Create character lookup table
        unique_chars = list(set(data))
        random.shuffle(unique_chars)

        # Create mapping
        lookup_table = {}
        for i, char in enumerate(unique_chars):
            lookup_table[char] = f"#{i:04d}#"

        # Encode using lookup table
        encoded_parts = [lookup_table[char] for char in data]
        encoded_str = ''.join(encoded_parts)

        return {
            'encoded': encoded_str,
            'metadata': {
                'lookup_table': lookup_table,
                'original_length': len(data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        lookup_table = metadata['lookup_table']

        # Reverse lookup table
        reverse_table = {v: k for k, v in lookup_table.items()}

        # Decode using reverse lookup
        decoded_chars = []
        i = 0
        while i < len(encoded_data):
            if encoded_data[i] == '#':
                # Find the complete token
                end = encoded_data.find('#', i + 1)
                if end != -1:
                    token = encoded_data[i:end+1]
                    if token in reverse_table:
                        decoded_chars.append(reverse_table[token])
                    i = end + 1
                else:
                    i += 1
            else:
                i += 1

        return ''.join(decoded_chars)

# Registry of fast encoders
FAST_ENCODERS = {
    'fast_xor': FastXOREncoder,
    'fast_base64': FastBase64Encoder,
    'fast_rotation': FastRotationEncoder,
    'fast_hash': FastHashEncoder,
    'fast_binary': FastBinaryEncoder,
    'fast_lookup': FastLookupEncoder
}
