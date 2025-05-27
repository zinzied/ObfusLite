"""
Simple XOR-based encoder for testing the obfuscation framework
This is a basic but reliable encoder for demonstration purposes
"""

import base64
import json
import random
from typing import Dict, Any
from .base import BaseEncoder

class SimpleEncoder(BaseEncoder):
    """
    Simple XOR-based encoder for testing purposes
    This encoder is reliable and easy to debug
    """

    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode string data using XOR with a random key
        """
        # Generate a random key
        key = random.randint(1, 255)

        # Convert string to bytes and XOR with key
        data_bytes = data.encode('utf-8')
        encoded_bytes = bytes([b ^ key for b in data_bytes])

        # Encode as base64 for safe storage
        encoded_b64 = base64.b64encode(encoded_bytes).decode('ascii')

        return {
            'encoded': encoded_b64,
            'metadata': {
                'key': key,
                'original_length': len(data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode XOR-encoded data back to original string
        """
        # Get the key from metadata
        key = metadata['key']

        # Decode from base64
        encoded_bytes = base64.b64decode(encoded_data.encode('ascii'))

        # XOR with key to get original bytes
        original_bytes = bytes([b ^ key for b in encoded_bytes])

        # Convert back to string
        original_data = original_bytes.decode('utf-8')

        return original_data
