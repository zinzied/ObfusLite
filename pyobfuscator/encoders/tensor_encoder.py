"""
Multi-dimensional Tensor Encoding for Python Code Obfuscation
Uses tensor operations and linear algebra for encoding
"""

import numpy as np
import base64
import json
from typing import Dict, Any, List, Tuple
from obfuscator_core import BaseEncoder

class TensorEncoder(BaseEncoder):
    """
    Tensor-based encoder that uses multi-dimensional arrays
    and linear algebra operations for obfuscation
    """
    
    def __init__(self):
        self.tensor_operations = {
            'matrix_multiplication': self._matrix_mult_encode,
            'tensor_decomposition': self._tensor_decomp_encode,
            'fourier_transform': self._fourier_encode,
            'wavelet_transform': self._wavelet_encode,
            'singular_value_decomposition': self._svd_encode
        }
        
    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode string data using tensor operations
        """
        # Convert to binary
        binary_data = ''.join(format(ord(char), '08b') for char in data)
        
        # Convert binary to numerical array
        data_array = np.array([float(bit) for bit in binary_data])
        
        # Choose tensor operation
        operation = np.random.choice(list(self.tensor_operations.keys()))
        
        # Apply tensor encoding
        tensor_data = self.tensor_operations[operation](data_array)
        
        # Apply additional tensor transformations
        transformed_tensors = self._apply_tensor_transformations(tensor_data)
        
        # Create tensor metadata
        tensor_metadata = self._generate_tensor_metadata(data_array.shape, operation)
        
        # Encode as base64
        encoded_data = base64.b64encode(json.dumps({
            'tensors': self._serialize_tensors(transformed_tensors),
            'metadata': tensor_metadata
        }).encode()).decode()
        
        return {
            'encoded': encoded_data,
            'metadata': {
                'operation': operation,
                'original_length': len(data),
                'data_shape': data_array.shape,
                'tensor_dimensions': len(transformed_tensors)
            }
        }
        
    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode tensor-encoded data back to original string
        """
        # Decode from base64
        tensor_info = json.loads(base64.b64decode(encoded_data.encode()).decode())
        
        # Deserialize tensors
        tensors = self._deserialize_tensors(tensor_info['tensors'])
        
        # Reverse tensor transformations
        original_tensors = self._reverse_tensor_transformations(tensors)
        
        # Reverse tensor operation
        operation = metadata['operation']
        data_array = self._reverse_tensor_operation(original_tensors, operation, metadata)
        
        # Convert back to binary
        binary_data = ''.join([str(int(round(bit))) for bit in data_array])
        
        # Convert binary to string
        original_data = self._binary_to_string(binary_data, metadata['original_length'])
        
        return original_data
        
    def _matrix_mult_encode(self, data_array: np.ndarray) -> Dict[str, np.ndarray]:
        """Encode using matrix multiplication"""
        # Reshape data into matrix
        size = len(data_array)
        matrix_size = int(np.ceil(np.sqrt(size)))
        
        # Pad data to fit matrix
        padded_data = np.pad(data_array, (0, matrix_size**2 - size), mode='constant')
        data_matrix = padded_data.reshape(matrix_size, matrix_size)
        
        # Create random transformation matrices
        transform_matrix_1 = np.random.randn(matrix_size, matrix_size)
        transform_matrix_2 = np.random.randn(matrix_size, matrix_size)
        
        # Apply transformations
        encoded_matrix = transform_matrix_1 @ data_matrix @ transform_matrix_2
        
        return {
            'encoded_matrix': encoded_matrix,
            'transform_1': transform_matrix_1,
            'transform_2': transform_matrix_2,
            'original_shape': data_array.shape,
            'matrix_size': matrix_size
        }
        
    def _tensor_decomp_encode(self, data_array: np.ndarray) -> Dict[str, np.ndarray]:
        """Encode using tensor decomposition"""
        # Reshape into 3D tensor
        size = len(data_array)
        tensor_dim = int(np.ceil(size**(1/3)))
        
        # Pad data
        padded_data = np.pad(data_array, (0, tensor_dim**3 - size), mode='constant')
        data_tensor = padded_data.reshape(tensor_dim, tensor_dim, tensor_dim)
        
        # Apply random rotations to each dimension
        rotation_matrices = []
        for dim in range(3):
            angle = np.random.uniform(0, 2*np.pi)
            rotation = self._create_rotation_matrix_3d(tensor_dim, dim, angle)
            rotation_matrices.append(rotation)
            
        # Apply rotations
        encoded_tensor = data_tensor.copy()
        for i, rotation in enumerate(rotation_matrices):
            encoded_tensor = np.tensordot(rotation, encoded_tensor, axes=([1], [i]))
            encoded_tensor = np.moveaxis(encoded_tensor, 0, i)
            
        return {
            'encoded_tensor': encoded_tensor,
            'rotations': rotation_matrices,
            'original_shape': data_array.shape,
            'tensor_dim': tensor_dim
        }
        
    def _fourier_encode(self, data_array: np.ndarray) -> Dict[str, np.ndarray]:
        """Encode using Fourier transform"""
        # Apply FFT
        fft_data = np.fft.fft(data_array)
        
        # Separate real and imaginary parts
        real_part = fft_data.real
        imag_part = fft_data.imag
        
        # Apply random phase shifts
        phase_shifts = np.random.uniform(0, 2*np.pi, len(data_array))
        shifted_fft = fft_data * np.exp(1j * phase_shifts)
        
        # Create frequency domain mask
        mask = np.random.choice([0, 1], size=len(data_array), p=[0.3, 0.7])
        masked_fft = shifted_fft * mask
        
        return {
            'masked_fft': masked_fft,
            'phase_shifts': phase_shifts,
            'frequency_mask': mask,
            'original_shape': data_array.shape
        }
        
    def _wavelet_encode(self, data_array: np.ndarray) -> Dict[str, np.ndarray]:
        """Encode using wavelet-like transform"""
        # Simple Haar wavelet-like transform
        def haar_transform(signal):
            n = len(signal)
            if n == 1:
                return signal
                
            # Ensure even length
            if n % 2 == 1:
                signal = np.append(signal, 0)
                n += 1
                
            # Compute averages and differences
            averages = (signal[::2] + signal[1::2]) / 2
            differences = (signal[::2] - signal[1::2]) / 2
            
            # Recursively transform averages
            transformed_averages = haar_transform(averages)
            
            return np.concatenate([transformed_averages, differences])
            
        # Apply wavelet transform
        wavelet_coeffs = haar_transform(data_array)
        
        # Apply random scaling to coefficients
        scales = np.random.uniform(0.5, 2.0, len(wavelet_coeffs))
        scaled_coeffs = wavelet_coeffs * scales
        
        # Quantize coefficients
        quantization_levels = np.random.randint(2, 16, len(wavelet_coeffs))
        quantized_coeffs = np.round(scaled_coeffs * quantization_levels) / quantization_levels
        
        return {
            'quantized_coeffs': quantized_coeffs,
            'scales': scales,
            'quantization_levels': quantization_levels,
            'original_shape': data_array.shape
        }
        
    def _svd_encode(self, data_array: np.ndarray) -> Dict[str, np.ndarray]:
        """Encode using Singular Value Decomposition"""
        # Reshape into matrix
        size = len(data_array)
        rows = int(np.ceil(np.sqrt(size)))
        cols = int(np.ceil(size / rows))
        
        # Pad and reshape
        padded_data = np.pad(data_array, (0, rows * cols - size), mode='constant')
        data_matrix = padded_data.reshape(rows, cols)
        
        # Apply SVD
        U, s, Vt = np.linalg.svd(data_matrix, full_matrices=False)
        
        # Modify singular values
        modified_s = s + np.random.normal(0, 0.1, len(s))
        
        # Randomly permute components
        perm_indices = np.random.permutation(len(s))
        U_perm = U[:, perm_indices]
        s_perm = modified_s[perm_indices]
        Vt_perm = Vt[perm_indices, :]
        
        return {
            'U': U_perm,
            'singular_values': s_perm,
            'Vt': Vt_perm,
            'permutation': perm_indices,
            'original_shape': data_array.shape,
            'matrix_shape': (rows, cols)
        }
        
    def _apply_tensor_transformations(self, tensor_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Apply additional tensor transformations"""
        transformed = {}
        
        for key, tensor in tensor_data.items():
            if isinstance(tensor, np.ndarray):
                # Apply random linear transformation
                if tensor.ndim == 1:
                    # Vector transformation
                    transform_matrix = np.random.randn(len(tensor), len(tensor))
                    transformed[key] = transform_matrix @ tensor
                    transformed[f'{key}_transform'] = transform_matrix
                elif tensor.ndim == 2:
                    # Matrix transformation
                    left_transform = np.random.randn(tensor.shape[0], tensor.shape[0])
                    right_transform = np.random.randn(tensor.shape[1], tensor.shape[1])
                    transformed[key] = left_transform @ tensor @ right_transform
                    transformed[f'{key}_left_transform'] = left_transform
                    transformed[f'{key}_right_transform'] = right_transform
                else:
                    # Higher-order tensor - apply mode-wise transformations
                    transformed_tensor = tensor.copy()
                    transforms = []
                    for mode in range(tensor.ndim):
                        mode_size = tensor.shape[mode]
                        mode_transform = np.random.randn(mode_size, mode_size)
                        transformed_tensor = np.tensordot(mode_transform, transformed_tensor, 
                                                        axes=([1], [mode]))
                        transformed_tensor = np.moveaxis(transformed_tensor, 0, mode)
                        transforms.append(mode_transform)
                    transformed[key] = transformed_tensor
                    transformed[f'{key}_transforms'] = transforms
            else:
                transformed[key] = tensor
                
        return transformed
        
    def _reverse_tensor_transformations(self, tensors: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Reverse tensor transformations"""
        original = {}
        
        for key, tensor in tensors.items():
            if key.endswith('_transform') or key.endswith('_transforms'):
                continue
                
            if isinstance(tensor, np.ndarray):
                if tensor.ndim == 1 and f'{key}_transform' in tensors:
                    # Reverse vector transformation
                    transform_matrix = tensors[f'{key}_transform']
                    original[key] = np.linalg.solve(transform_matrix, tensor)
                elif tensor.ndim == 2 and f'{key}_left_transform' in tensors:
                    # Reverse matrix transformation
                    left_transform = tensors[f'{key}_left_transform']
                    right_transform = tensors[f'{key}_right_transform']
                    original[key] = np.linalg.solve(left_transform, tensor) @ np.linalg.inv(right_transform)
                elif f'{key}_transforms' in tensors:
                    # Reverse higher-order tensor transformations
                    transforms = tensors[f'{key}_transforms']
                    reversed_tensor = tensor.copy()
                    for mode, transform in enumerate(reversed(transforms)):
                        mode_idx = len(transforms) - 1 - mode
                        reversed_tensor = np.tensordot(np.linalg.inv(transform), reversed_tensor,
                                                     axes=([1], [mode_idx]))
                        reversed_tensor = np.moveaxis(reversed_tensor, 0, mode_idx)
                    original[key] = reversed_tensor
                else:
                    original[key] = tensor
            else:
                original[key] = tensor
                
        return original
        
    def _create_rotation_matrix_3d(self, size: int, axis: int, angle: float) -> np.ndarray:
        """Create 3D rotation matrix"""
        rotation = np.eye(size)
        
        if size >= 3:
            if axis == 0:  # Rotation around x-axis
                rotation[1, 1] = np.cos(angle)
                rotation[1, 2] = -np.sin(angle)
                rotation[2, 1] = np.sin(angle)
                rotation[2, 2] = np.cos(angle)
            elif axis == 1:  # Rotation around y-axis
                rotation[0, 0] = np.cos(angle)
                rotation[0, 2] = np.sin(angle)
                rotation[2, 0] = -np.sin(angle)
                rotation[2, 2] = np.cos(angle)
            else:  # Rotation around z-axis
                rotation[0, 0] = np.cos(angle)
                rotation[0, 1] = -np.sin(angle)
                rotation[1, 0] = np.sin(angle)
                rotation[1, 1] = np.cos(angle)
                
        return rotation
        
    def _serialize_tensors(self, tensors: Dict[str, np.ndarray]) -> Dict[str, Any]:
        """Serialize tensors for JSON storage"""
        serialized = {}
        for key, value in tensors.items():
            if isinstance(value, np.ndarray):
                serialized[key] = {
                    'data': value.tolist(),
                    'shape': value.shape,
                    'dtype': str(value.dtype)
                }
            elif isinstance(value, list) and all(isinstance(item, np.ndarray) for item in value):
                serialized[key] = [
                    {
                        'data': item.tolist(),
                        'shape': item.shape,
                        'dtype': str(item.dtype)
                    } for item in value
                ]
            else:
                serialized[key] = value
        return serialized
        
    def _deserialize_tensors(self, serialized: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """Deserialize tensors from JSON storage"""
        tensors = {}
        for key, value in serialized.items():
            if isinstance(value, dict) and 'data' in value:
                tensors[key] = np.array(value['data']).reshape(value['shape'])
            elif isinstance(value, list) and all(isinstance(item, dict) and 'data' in item for item in value):
                tensors[key] = [np.array(item['data']).reshape(item['shape']) for item in value]
            else:
                tensors[key] = value
        return tensors
        
    def _generate_tensor_metadata(self, data_shape: Tuple, operation: str) -> Dict[str, Any]:
        """Generate metadata for tensor operations"""
        return {
            'operation': operation,
            'data_shape': data_shape,
            'tensor_rank': len(data_shape),
            'compression_ratio': np.random.uniform(0.1, 0.9),
            'noise_level': np.random.uniform(0.01, 0.1)
        }
        
    def _reverse_tensor_operation(self, tensors: Dict[str, np.ndarray], 
                                operation: str, metadata: Dict[str, Any]) -> np.ndarray:
        """Reverse the specific tensor operation"""
        if operation == 'matrix_multiplication':
            return self._reverse_matrix_mult(tensors)
        elif operation == 'tensor_decomposition':
            return self._reverse_tensor_decomp(tensors)
        elif operation == 'fourier_transform':
            return self._reverse_fourier(tensors)
        elif operation == 'wavelet_transform':
            return self._reverse_wavelet(tensors)
        elif operation == 'singular_value_decomposition':
            return self._reverse_svd(tensors)
        else:
            # Fallback
            return np.array([0])
            
    def _reverse_matrix_mult(self, tensors: Dict[str, np.ndarray]) -> np.ndarray:
        """Reverse matrix multiplication encoding"""
        encoded_matrix = tensors['encoded_matrix']
        transform_1 = tensors['transform_1']
        transform_2 = tensors['transform_2']
        original_shape = tensors['original_shape']
        
        # Reverse transformations
        data_matrix = np.linalg.solve(transform_1, encoded_matrix) @ np.linalg.inv(transform_2)
        
        # Flatten and trim to original size
        data_array = data_matrix.flatten()[:original_shape[0]]
        
        return data_array
        
    def _reverse_tensor_decomp(self, tensors: Dict[str, np.ndarray]) -> np.ndarray:
        """Reverse tensor decomposition encoding"""
        encoded_tensor = tensors['encoded_tensor']
        rotations = tensors['rotations']
        original_shape = tensors['original_shape']
        
        # Reverse rotations
        data_tensor = encoded_tensor.copy()
        for i, rotation in enumerate(reversed(rotations)):
            data_tensor = np.tensordot(np.linalg.inv(rotation), data_tensor, axes=([1], [i]))
            data_tensor = np.moveaxis(data_tensor, 0, i)
            
        # Flatten and trim
        data_array = data_tensor.flatten()[:original_shape[0]]
        
        return data_array
        
    def _reverse_fourier(self, tensors: Dict[str, np.ndarray]) -> np.ndarray:
        """Reverse Fourier transform encoding"""
        masked_fft = tensors['masked_fft']
        phase_shifts = tensors['phase_shifts']
        frequency_mask = tensors['frequency_mask']
        
        # Reverse masking (approximate)
        unmasked_fft = masked_fft / (frequency_mask + 1e-10)
        
        # Reverse phase shifts
        original_fft = unmasked_fft * np.exp(-1j * phase_shifts)
        
        # Inverse FFT
        data_array = np.fft.ifft(original_fft).real
        
        return data_array
        
    def _reverse_wavelet(self, tensors: Dict[str, np.ndarray]) -> np.ndarray:
        """Reverse wavelet transform encoding"""
        quantized_coeffs = tensors['quantized_coeffs']
        scales = tensors['scales']
        
        # Reverse scaling
        wavelet_coeffs = quantized_coeffs / scales
        
        # Inverse Haar transform (simplified)
        def inverse_haar_transform(coeffs):
            n = len(coeffs)
            if n == 1:
                return coeffs
                
            # Split into averages and differences
            mid = n // 2
            averages = coeffs[:mid]
            differences = coeffs[mid:]
            
            # Recursively inverse transform averages
            if len(averages) > 1:
                averages = inverse_haar_transform(averages)
                
            # Reconstruct signal
            signal = np.zeros(n)
            signal[::2] = averages + differences[:len(averages)]
            signal[1::2] = averages - differences[:len(averages)]
            
            return signal
            
        data_array = inverse_haar_transform(wavelet_coeffs)
        
        return data_array
        
    def _reverse_svd(self, tensors: Dict[str, np.ndarray]) -> np.ndarray:
        """Reverse SVD encoding"""
        U = tensors['U']
        s = tensors['singular_values']
        Vt = tensors['Vt']
        permutation = tensors['permutation']
        original_shape = tensors['original_shape']
        
        # Reverse permutation
        inverse_perm = np.argsort(permutation)
        U_orig = U[:, inverse_perm]
        s_orig = s[inverse_perm]
        Vt_orig = Vt[inverse_perm, :]
        
        # Reconstruct matrix
        data_matrix = U_orig @ np.diag(s_orig) @ Vt_orig
        
        # Flatten and trim
        data_array = data_matrix.flatten()[:original_shape[0]]
        
        return data_array
        
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
