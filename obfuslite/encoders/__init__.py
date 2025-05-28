"""
Encoder modules for PyObfuscator

This module provides access to all available encoding techniques,
both fast and advanced algorithms.
"""

from typing import Dict, List, Optional, Type
from .base import BaseEncoder

# Import all encoders
from .fast_encoders import (
    FastXOREncoder, FastBase64Encoder, FastRotationEncoder,
    FastHashEncoder, FastBinaryEncoder, FastLookupEncoder
)
from .simple_encoder import SimpleEncoder

# Advanced encoders (optional imports to handle missing dependencies)
try:
    from .quantum_encoder import QuantumEncoder
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False

try:
    from .dna_encoder import DnaEncoder
    DNA_AVAILABLE = True
except ImportError:
    DNA_AVAILABLE = False

try:
    from .fractal_encoder import FractalEncoder
    FRACTAL_AVAILABLE = True
except ImportError:
    FRACTAL_AVAILABLE = False

try:
    from .neural_encoder import NeuralEncoder
    NEURAL_AVAILABLE = True
except ImportError:
    NEURAL_AVAILABLE = False

try:
    from .steganographic_encoder import SteganographicEncoder
    STEGANOGRAPHIC_AVAILABLE = True
except ImportError:
    STEGANOGRAPHIC_AVAILABLE = False

try:
    from .runtime_reconstructor import RuntimeReconstructor
    RUNTIME_AVAILABLE = True
except ImportError:
    RUNTIME_AVAILABLE = False

try:
    from .tensor_encoder import TensorEncoder
    TENSOR_AVAILABLE = True
except ImportError:
    TENSOR_AVAILABLE = False

# Registry of all available encoders
_ENCODER_REGISTRY: Dict[str, Type[BaseEncoder]] = {
    # Fast encoders (always available)
    'fast_xor': FastXOREncoder,
    'fast_base64': FastBase64Encoder,
    'fast_rotation': FastRotationEncoder,
    'fast_hash': FastHashEncoder,
    'fast_binary': FastBinaryEncoder,
    'fast_lookup': FastLookupEncoder,
    'simple': SimpleEncoder,
}

# Add advanced encoders if available
if QUANTUM_AVAILABLE:
    _ENCODER_REGISTRY['quantum'] = QuantumEncoder
if DNA_AVAILABLE:
    _ENCODER_REGISTRY['dna'] = DnaEncoder
if FRACTAL_AVAILABLE:
    _ENCODER_REGISTRY['fractal'] = FractalEncoder
if NEURAL_AVAILABLE:
    _ENCODER_REGISTRY['neural'] = NeuralEncoder
if STEGANOGRAPHIC_AVAILABLE:
    _ENCODER_REGISTRY['steganographic'] = SteganographicEncoder
if RUNTIME_AVAILABLE:
    _ENCODER_REGISTRY['runtime'] = RuntimeReconstructor
if TENSOR_AVAILABLE:
    _ENCODER_REGISTRY['tensor'] = TensorEncoder

def get_available_techniques() -> List[str]:
    """Get list of all available obfuscation techniques"""
    return list(_ENCODER_REGISTRY.keys())

def get_fast_techniques() -> List[str]:
    """Get list of fast obfuscation techniques"""
    return [
        'fast_xor', 'fast_base64', 'fast_rotation',
        'fast_hash', 'fast_binary', 'fast_lookup', 'simple'
    ]

def get_advanced_techniques() -> List[str]:
    """Get list of advanced obfuscation techniques"""
    advanced = []
    if QUANTUM_AVAILABLE:
        advanced.append('quantum')
    if DNA_AVAILABLE:
        advanced.append('dna')
    if FRACTAL_AVAILABLE:
        advanced.append('fractal')
    if NEURAL_AVAILABLE:
        advanced.append('neural')
    if STEGANOGRAPHIC_AVAILABLE:
        advanced.append('steganographic')
    if RUNTIME_AVAILABLE:
        advanced.append('runtime')
    if TENSOR_AVAILABLE:
        advanced.append('tensor')
    return advanced

def get_encoder_class(technique: str) -> Optional[Type[BaseEncoder]]:
    """Get encoder class for a specific technique"""
    return _ENCODER_REGISTRY.get(technique)

def create_encoder(technique: str) -> Optional[BaseEncoder]:
    """Create an encoder instance for a specific technique"""
    encoder_class = get_encoder_class(technique)
    if encoder_class:
        return encoder_class()
    return None

def get_technique_info() -> Dict[str, Dict[str, str]]:
    """Get information about all available techniques"""
    return {
        # Fast techniques
        'fast_xor': {
            'type': 'fast',
            'description': 'Multi-key XOR encoding with compression',
            'speed': 'very_fast',
            'security': 'good'
        },
        'fast_base64': {
            'type': 'fast',
            'description': 'Base64 with character substitution',
            'speed': 'very_fast',
            'security': 'basic'
        },
        'fast_rotation': {
            'type': 'fast',
            'description': 'Multi-round Caesar cipher rotation',
            'speed': 'very_fast',
            'security': 'good'
        },
        'fast_hash': {
            'type': 'fast',
            'description': 'Hash-based chunk encoding',
            'speed': 'very_fast',
            'security': 'good'
        },
        'fast_binary': {
            'type': 'fast',
            'description': 'Binary manipulation with bit shifting',
            'speed': 'very_fast',
            'security': 'good'
        },
        'fast_lookup': {
            'type': 'fast',
            'description': 'Character lookup table encoding',
            'speed': 'very_fast',
            'security': 'basic'
        },
        'simple': {
            'type': 'fast',
            'description': 'Simple XOR encoding',
            'speed': 'very_fast',
            'security': 'basic'
        },
        # Advanced techniques (if available)
        **({
            'quantum': {
                'type': 'advanced',
                'description': 'Quantum-inspired encoding with gate operations',
                'speed': 'slow',
                'security': 'very_high'
            }
        } if QUANTUM_AVAILABLE else {}),
        **({
            'dna': {
                'type': 'advanced',
                'description': 'DNA sequence mapping with genetic mutations',
                'speed': 'medium',
                'security': 'high'
            }
        } if DNA_AVAILABLE else {}),
        **({
            'fractal': {
                'type': 'advanced',
                'description': 'Fractal pattern encoding with chaos theory',
                'speed': 'slow',
                'security': 'very_high'
            }
        } if FRACTAL_AVAILABLE else {}),
        **({
            'neural': {
                'type': 'advanced',
                'description': 'Neural network weight encoding',
                'speed': 'very_slow',
                'security': 'very_high'
            }
        } if NEURAL_AVAILABLE else {}),
        **({
            'steganographic': {
                'type': 'advanced',
                'description': 'Steganographic hiding in innocent data',
                'speed': 'medium',
                'security': 'high'
            }
        } if STEGANOGRAPHIC_AVAILABLE else {}),
        **({
            'runtime': {
                'type': 'advanced',
                'description': 'Runtime reconstruction and self-modification',
                'speed': 'medium',
                'security': 'very_high'
            }
        } if RUNTIME_AVAILABLE else {}),
        **({
            'tensor': {
                'type': 'advanced',
                'description': 'Multi-dimensional tensor operations',
                'speed': 'very_slow',
                'security': 'very_high'
            }
        } if TENSOR_AVAILABLE else {})
    }

# Export main classes and functions
__all__ = [
    'BaseEncoder',
    'get_available_techniques',
    'get_fast_techniques',
    'get_advanced_techniques',
    'get_encoder_class',
    'create_encoder',
    'get_technique_info',
    # Fast encoders
    'FastXOREncoder',
    'FastBase64Encoder',
    'FastRotationEncoder',
    'FastHashEncoder',
    'FastBinaryEncoder',
    'FastLookupEncoder',
    'SimpleEncoder',
]

# Add advanced encoders to exports if available
if QUANTUM_AVAILABLE:
    __all__.append('QuantumEncoder')
if DNA_AVAILABLE:
    __all__.append('DnaEncoder')
if FRACTAL_AVAILABLE:
    __all__.append('FractalEncoder')
if NEURAL_AVAILABLE:
    __all__.append('NeuralEncoder')
if STEGANOGRAPHIC_AVAILABLE:
    __all__.append('SteganographicEncoder')
if RUNTIME_AVAILABLE:
    __all__.append('RuntimeReconstructor')
if TENSOR_AVAILABLE:
    __all__.append('TensorEncoder')
