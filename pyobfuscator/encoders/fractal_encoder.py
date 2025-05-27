"""
Fractal Pattern Encoding for Python Code Obfuscation
Uses mathematical fractals and chaos theory for encoding
"""

import numpy as np
import base64
import json
import math
from typing import Dict, Any, List, Tuple
from .base import BaseEncoder

class FractalEncoder(BaseEncoder):
    """
    Fractal-based encoder that uses mathematical fractals
    and chaos theory to encode data in fractal patterns
    """

    def __init__(self):
        self.fractal_types = {
            'mandelbrot': self._mandelbrot_encode,
            'julia': self._julia_encode,
            'sierpinski': self._sierpinski_encode,
            'dragon': self._dragon_encode,
            'lorenz': self._lorenz_encode
        }

    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode string data using fractal patterns
        """
        # Convert to binary
        binary_data = ''.join(format(ord(char), '08b') for char in data)

        # Choose random fractal type
        fractal_type = np.random.choice(list(self.fractal_types.keys()))

        # Generate fractal parameters
        fractal_params = self._generate_fractal_params(fractal_type)

        # Encode using selected fractal
        fractal_data = self.fractal_types[fractal_type](binary_data, fractal_params)

        # Apply chaos mapping for additional security
        chaos_data = self._apply_chaos_mapping(fractal_data)

        # Create fractal coordinate system
        coordinate_system = self._create_coordinate_system(len(binary_data))

        # Encode as base64
        encoded_data = base64.b64encode(json.dumps({
            'fractal_data': chaos_data,
            'coordinate_system': coordinate_system
        }).encode()).decode()

        return {
            'encoded': encoded_data,
            'metadata': {
                'fractal_type': fractal_type,
                'fractal_params': fractal_params,
                'original_length': len(data),
                'binary_length': len(binary_data)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode fractal-encoded data back to original string
        """
        # Decode from base64
        fractal_info = json.loads(base64.b64decode(encoded_data.encode()).decode())

        # Reverse chaos mapping
        fractal_data = self._reverse_chaos_mapping(fractal_info['fractal_data'])

        # Decode using fractal type
        fractal_type = metadata['fractal_type']
        fractal_params = metadata['fractal_params']

        binary_data = self._fractal_decode(fractal_data, fractal_type, fractal_params)

        # Convert binary to string
        original_data = self._binary_to_string(binary_data, metadata['original_length'])

        return original_data

    def _generate_fractal_params(self, fractal_type: str) -> Dict[str, Any]:
        """Generate parameters for the specified fractal type"""
        if fractal_type == 'mandelbrot':
            return {
                'max_iter': np.random.randint(50, 200),
                'escape_radius': np.random.uniform(2.0, 4.0),
                'zoom': np.random.uniform(0.5, 2.0),
                'center': (np.random.uniform(-2, 2), np.random.uniform(-2, 2))
            }
        elif fractal_type == 'julia':
            return {
                'c_real': np.random.uniform(-2, 2),
                'c_imag': np.random.uniform(-2, 2),
                'max_iter': np.random.randint(50, 200),
                'escape_radius': np.random.uniform(2.0, 4.0)
            }
        elif fractal_type == 'sierpinski':
            return {
                'iterations': np.random.randint(5, 15),
                'scale': np.random.uniform(0.3, 0.7),
                'rotation': np.random.uniform(0, 2 * np.pi)
            }
        elif fractal_type == 'dragon':
            return {
                'iterations': np.random.randint(8, 16),
                'angle': np.random.uniform(np.pi/3, 2*np.pi/3),
                'scale': np.random.uniform(0.5, 1.5)
            }
        elif fractal_type == 'lorenz':
            return {
                'sigma': np.random.uniform(8, 12),
                'rho': np.random.uniform(25, 30),
                'beta': np.random.uniform(2.5, 3.0),
                'dt': np.random.uniform(0.01, 0.02)
            }

    def _mandelbrot_encode(self, binary_data: str, params: Dict[str, Any]) -> List[Dict]:
        """Encode data using Mandelbrot set"""
        encoded_points = []

        for i, bit in enumerate(binary_data):
            # Map bit to complex plane position
            angle = (i / len(binary_data)) * 2 * np.pi
            radius = 0.5 if bit == '0' else 1.5

            # Create complex number
            c = complex(
                params['center'][0] + radius * np.cos(angle) * params['zoom'],
                params['center'][1] + radius * np.sin(angle) * params['zoom']
            )

            # Calculate Mandelbrot iterations
            z = 0
            iterations = 0
            while abs(z) < params['escape_radius'] and iterations < params['max_iter']:
                z = z*z + c
                iterations += 1

            # Encode the result
            encoded_points.append({
                'c_real': c.real,
                'c_imag': c.imag,
                'iterations': iterations,
                'final_z_real': z.real,
                'final_z_imag': z.imag
            })

        return encoded_points

    def _julia_encode(self, binary_data: str, params: Dict[str, Any]) -> List[Dict]:
        """Encode data using Julia set"""
        encoded_points = []
        c = complex(params['c_real'], params['c_imag'])

        for i, bit in enumerate(binary_data):
            # Map bit to initial z value
            angle = (i / len(binary_data)) * 2 * np.pi
            radius = 0.5 if bit == '0' else 1.5

            z = complex(radius * np.cos(angle), radius * np.sin(angle))

            # Calculate Julia iterations
            iterations = 0
            while abs(z) < params['escape_radius'] and iterations < params['max_iter']:
                z = z*z + c
                iterations += 1

            encoded_points.append({
                'z_real': z.real,
                'z_imag': z.imag,
                'iterations': iterations
            })

        return encoded_points

    def _sierpinski_encode(self, binary_data: str, params: Dict[str, Any]) -> List[Tuple]:
        """Encode data using Sierpinski triangle"""
        encoded_points = []

        # Define triangle vertices
        vertices = [
            (0, 0),
            (1, 0),
            (0.5, np.sqrt(3)/2)
        ]

        # Start at random point
        current_point = (np.random.random(), np.random.random())

        for bit in binary_data:
            # Choose vertex based on bit pattern
            vertex_index = int(bit)
            if len(encoded_points) > 0:
                # Use previous point for more complex mapping
                vertex_index = (vertex_index + len(encoded_points)) % 3

            target_vertex = vertices[vertex_index]

            # Move halfway to chosen vertex
            new_point = (
                (current_point[0] + target_vertex[0]) * params['scale'],
                (current_point[1] + target_vertex[1]) * params['scale']
            )

            # Apply rotation
            rotated_point = (
                new_point[0] * np.cos(params['rotation']) - new_point[1] * np.sin(params['rotation']),
                new_point[0] * np.sin(params['rotation']) + new_point[1] * np.cos(params['rotation'])
            )

            encoded_points.append(rotated_point)
            current_point = new_point

        return encoded_points

    def _dragon_encode(self, binary_data: str, params: Dict[str, Any]) -> List[Tuple]:
        """Encode data using Dragon curve"""
        encoded_points = []

        # Generate dragon curve sequence
        dragon_sequence = self._generate_dragon_sequence(len(binary_data))

        # Map binary data to dragon curve
        current_pos = (0, 0)
        current_angle = 0

        for i, bit in enumerate(binary_data):
            # Determine turn direction
            turn = 1 if bit == '1' else -1
            if i < len(dragon_sequence):
                turn *= dragon_sequence[i]

            # Update angle
            current_angle += turn * params['angle']

            # Move forward
            new_pos = (
                current_pos[0] + params['scale'] * np.cos(current_angle),
                current_pos[1] + params['scale'] * np.sin(current_angle)
            )

            encoded_points.append(new_pos)
            current_pos = new_pos

        return encoded_points

    def _lorenz_encode(self, binary_data: str, params: Dict[str, Any]) -> List[Tuple]:
        """Encode data using Lorenz attractor"""
        encoded_points = []

        # Initial conditions
        x, y, z = 1.0, 1.0, 1.0

        for bit in binary_data:
            # Lorenz equations
            dx = params['sigma'] * (y - x)
            dy = x * (params['rho'] - z) - y
            dz = x * y - params['beta'] * z

            # Update with Euler method
            x += dx * params['dt']
            y += dy * params['dt']
            z += dz * params['dt']

            # Perturb based on bit value
            if bit == '1':
                x += 0.1
                y += 0.1

            encoded_points.append((x, y, z))

        return encoded_points

    def _generate_dragon_sequence(self, length: int) -> List[int]:
        """Generate dragon curve turn sequence"""
        sequence = [1]

        while len(sequence) < length:
            # Dragon curve generation rule
            new_sequence = sequence + [1] + [-x for x in reversed(sequence)]
            sequence = new_sequence

        return sequence[:length]

    def _apply_chaos_mapping(self, fractal_data: List) -> str:
        """Apply chaotic mapping for additional obfuscation"""
        # Convert fractal data to string representation
        data_str = json.dumps(fractal_data, default=str)

        # Apply logistic map chaos
        x = 0.5  # Initial condition
        r = 3.9  # Chaos parameter

        chaotic_sequence = []
        for char in data_str:
            x = r * x * (1 - x)  # Logistic map
            chaotic_value = int((x * 256)) % 256
            encrypted_char = chr(ord(char) ^ chaotic_value)
            chaotic_sequence.append(encrypted_char)

        return ''.join(chaotic_sequence)

    def _reverse_chaos_mapping(self, chaos_data: str) -> List:
        """Reverse the chaotic mapping"""
        x = 0.5  # Same initial condition
        r = 3.9  # Same chaos parameter

        decrypted_sequence = []
        for char in chaos_data:
            x = r * x * (1 - x)
            chaotic_value = int((x * 256)) % 256
            decrypted_char = chr(ord(char) ^ chaotic_value)
            decrypted_sequence.append(decrypted_char)

        data_str = ''.join(decrypted_sequence)
        return json.loads(data_str)

    def _create_coordinate_system(self, data_length: int) -> Dict[str, Any]:
        """Create fractal coordinate system for mapping"""
        return {
            'origin': (np.random.uniform(-1, 1), np.random.uniform(-1, 1)),
            'scale_x': np.random.uniform(0.5, 2.0),
            'scale_y': np.random.uniform(0.5, 2.0),
            'rotation': np.random.uniform(0, 2 * np.pi),
            'data_length': data_length
        }

    def _fractal_decode(self, fractal_data: List, fractal_type: str, params: Dict[str, Any]) -> str:
        """Decode fractal data back to binary"""
        # This is a simplified decoding process
        # In practice, this would involve complex reverse mapping

        binary_bits = []

        for point_data in fractal_data:
            # Extract bit based on fractal properties
            if fractal_type == 'mandelbrot':
                bit = '1' if point_data['iterations'] % 2 == 1 else '0'
            elif fractal_type == 'julia':
                bit = '1' if point_data['iterations'] % 2 == 1 else '0'
            elif fractal_type in ['sierpinski', 'dragon', 'lorenz']:
                # For geometric fractals, use position-based decoding
                if isinstance(point_data, (list, tuple)) and len(point_data) >= 2:
                    bit = '1' if point_data[0] > point_data[1] else '0'
                else:
                    bit = '0'
            else:
                bit = '0'

            binary_bits.append(bit)

        return ''.join(binary_bits)

    def _binary_to_string(self, binary_data: str, original_length: int) -> str:
        """Convert binary data back to string"""
        # Ensure binary data is multiple of 8
        while len(binary_data) % 8 != 0:
            binary_data += '0'

        chars = []
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))

        result = ''.join(chars)
        return result[:original_length]
