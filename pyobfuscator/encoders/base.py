"""
Base encoder class for PyObfuscator

All encoding techniques inherit from this base class to ensure
consistent interface and behavior.
"""

import random
import string
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseEncoder(ABC):
    """
    Abstract base class for all encoding techniques
    
    All encoders must implement the encode() and decode() methods
    to provide consistent interface for the obfuscation system.
    """
    
    @abstractmethod
    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode the input data using the specific technique
        
        Args:
            data: String data to encode
            
        Returns:
            Dictionary containing:
            - 'encoded': The encoded data
            - 'metadata': Any metadata needed for decoding
        """
        pass
        
    @abstractmethod
    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode the encoded data back to original string
        
        Args:
            encoded_data: The encoded data to decode
            metadata: Metadata needed for decoding
            
        Returns:
            Original string data
        """
        pass
        
    def _generate_random_key(self, length: int = 32) -> str:
        """
        Generate a random key for encoding
        
        Args:
            length: Length of the key to generate
            
        Returns:
            Random string key
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
    def _generate_random_bytes(self, length: int = 16) -> bytes:
        """
        Generate random bytes for encoding
        
        Args:
            length: Number of bytes to generate
            
        Returns:
            Random bytes
        """
        return bytes(random.randint(0, 255) for _ in range(length))
        
    def _validate_input(self, data: str) -> None:
        """
        Validate input data
        
        Args:
            data: Input data to validate
            
        Raises:
            ValueError: If data is invalid
        """
        if not isinstance(data, str):
            raise ValueError("Input data must be a string")
        if not data.strip():
            raise ValueError("Input data cannot be empty")
            
    def _validate_metadata(self, metadata: Dict[str, Any], required_keys: list) -> None:
        """
        Validate metadata contains required keys
        
        Args:
            metadata: Metadata dictionary to validate
            required_keys: List of required keys
            
        Raises:
            ValueError: If required keys are missing
        """
        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary")
            
        missing_keys = [key for key in required_keys if key not in metadata]
        if missing_keys:
            raise ValueError(f"Missing required metadata keys: {missing_keys}")
            
    def get_info(self) -> Dict[str, str]:
        """
        Get information about this encoder
        
        Returns:
            Dictionary with encoder information
        """
        return {
            'name': self.__class__.__name__,
            'type': 'unknown',
            'description': 'Base encoder class',
            'speed': 'unknown',
            'security': 'unknown'
        }
