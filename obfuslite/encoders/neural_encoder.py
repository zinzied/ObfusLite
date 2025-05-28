"""
Neural Network Weight Encoding for Python Code Obfuscation
Stores code as neural network weights and biases
"""

import numpy as np
import base64
import json
from typing import Dict, Any, List, Tuple
from obfuscator_core import BaseEncoder

class NeuralEncoder(BaseEncoder):
    """
    Neural network-based encoder that stores data as network weights
    and uses neural network operations for encoding/decoding
    """
    
    def __init__(self):
        self.activation_functions = {
            'sigmoid': self._sigmoid,
            'tanh': self._tanh,
            'relu': self._relu,
            'leaky_relu': self._leaky_relu,
            'swish': self._swish
        }
        
    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode string data as neural network weights
        """
        # Convert to binary
        binary_data = ''.join(format(ord(char), '08b') for char in data)
        
        # Convert binary to numerical array
        data_array = np.array([float(bit) for bit in binary_data])
        
        # Design neural network architecture
        architecture = self._design_network_architecture(len(data_array))
        
        # Create neural network weights that encode the data
        weights, biases = self._create_encoding_network(data_array, architecture)
        
        # Apply neural transformations
        transformed_weights = self._apply_neural_transformations(weights, biases, architecture)
        
        # Create activation patterns
        activation_patterns = self._generate_activation_patterns(data_array, architecture)
        
        # Encode as base64
        encoded_data = base64.b64encode(json.dumps({
            'weights': [w.tolist() for w in transformed_weights],
            'biases': [b.tolist() for b in biases],
            'activation_patterns': activation_patterns
        }).encode()).decode()
        
        return {
            'encoded': encoded_data,
            'metadata': {
                'architecture': architecture,
                'original_length': len(data),
                'binary_length': len(binary_data),
                'network_depth': len(architecture) - 1
            }
        }
        
    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode neural network weights back to original string
        """
        # Decode from base64
        network_data = json.loads(base64.b64decode(encoded_data.encode()).decode())
        
        # Reconstruct weights and biases
        weights = [np.array(w) for w in network_data['weights']]
        biases = [np.array(b) for b in network_data['biases']]
        activation_patterns = network_data['activation_patterns']
        
        # Reverse neural transformations
        original_weights = self._reverse_neural_transformations(
            weights, biases, metadata['architecture']
        )
        
        # Extract original data from network
        data_array = self._extract_data_from_network(
            original_weights, biases, activation_patterns, metadata['architecture']
        )
        
        # Convert back to binary
        binary_data = ''.join([str(int(round(bit))) for bit in data_array])
        
        # Convert binary to string
        original_data = self._binary_to_string(binary_data, metadata['original_length'])
        
        return original_data
        
    def _design_network_architecture(self, input_size: int) -> List[int]:
        """Design neural network architecture based on data size"""
        # Create a network that can encode the data efficiently
        layers = [input_size]
        
        # Add hidden layers with decreasing size
        current_size = input_size
        while current_size > 8:
            next_size = max(8, current_size // 2)
            layers.append(next_size)
            current_size = next_size
            
        # Add encoding layer (bottleneck)
        encoding_size = max(4, input_size // 16)
        layers.append(encoding_size)
        
        # Mirror for decoder
        decoder_layers = layers[:-1][::-1]
        layers.extend(decoder_layers[1:])
        
        return layers
        
    def _create_encoding_network(self, data_array: np.ndarray, 
                               architecture: List[int]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """Create neural network weights that encode the data"""
        weights = []
        biases = []
        
        # Initialize weights with data-dependent values
        for i in range(len(architecture) - 1):
            input_size = architecture[i]
            output_size = architecture[i + 1]
            
            # Create weight matrix
            weight_matrix = np.random.randn(input_size, output_size) * 0.1
            
            # Embed data into weights using various techniques
            if i == 0:  # First layer - embed raw data
                data_indices = np.random.choice(
                    weight_matrix.size, 
                    min(len(data_array), weight_matrix.size), 
                    replace=False
                )
                flat_weights = weight_matrix.flatten()
                flat_weights[data_indices[:len(data_array)]] = data_array
                weight_matrix = flat_weights.reshape(weight_matrix.shape)
                
            elif i == len(architecture) // 2:  # Middle layer - embed transformed data
                transformed_data = self._transform_data(data_array, 'fourier')
                if len(transformed_data) <= weight_matrix.size:
                    flat_weights = weight_matrix.flatten()
                    flat_weights[:len(transformed_data)] = transformed_data
                    weight_matrix = flat_weights.reshape(weight_matrix.shape)
                    
            weights.append(weight_matrix)
            
            # Create bias vector
            bias_vector = np.random.randn(output_size) * 0.1
            
            # Embed data checksum in biases
            data_checksum = np.sum(data_array) % output_size
            bias_vector[int(data_checksum)] += np.mean(data_array)
            
            biases.append(bias_vector)
            
        return weights, biases
        
    def _apply_neural_transformations(self, weights: List[np.ndarray], 
                                    biases: List[np.ndarray], 
                                    architecture: List[int]) -> List[np.ndarray]:
        """Apply neural network transformations to weights"""
        transformed_weights = []
        
        for i, weight_matrix in enumerate(weights):
            # Apply different transformations based on layer
            if i % 2 == 0:
                # Even layers: apply rotation transformation
                angle = np.pi / 4
                rotation_matrix = self._create_rotation_matrix(weight_matrix.shape[0])
                if rotation_matrix.shape[1] == weight_matrix.shape[0]:
                    transformed = rotation_matrix @ weight_matrix
                else:
                    transformed = weight_matrix
            else:
                # Odd layers: apply scaling transformation
                scale_factor = 1.0 + 0.1 * np.sin(np.arange(weight_matrix.shape[1]))
                transformed = weight_matrix * scale_factor
                
            # Apply activation-like transformation
            transformed = self._tanh(transformed)
            
            transformed_weights.append(transformed)
            
        return transformed_weights
        
    def _reverse_neural_transformations(self, weights: List[np.ndarray], 
                                      biases: List[np.ndarray], 
                                      architecture: List[int]) -> List[np.ndarray]:
        """Reverse the neural transformations"""
        original_weights = []
        
        for i, weight_matrix in enumerate(weights):
            # Reverse activation-like transformation
            transformed = self._inverse_tanh(weight_matrix)
            
            # Reverse layer-specific transformations
            if i % 2 == 0:
                # Reverse rotation
                angle = -np.pi / 4
                rotation_matrix = self._create_rotation_matrix(transformed.shape[0])
                if rotation_matrix.shape[1] == transformed.shape[0]:
                    original = rotation_matrix @ transformed
                else:
                    original = transformed
            else:
                # Reverse scaling
                scale_factor = 1.0 + 0.1 * np.sin(np.arange(transformed.shape[1]))
                original = transformed / scale_factor
                
            original_weights.append(original)
            
        return original_weights
        
    def _generate_activation_patterns(self, data_array: np.ndarray, 
                                    architecture: List[int]) -> List[List[float]]:
        """Generate activation patterns for data reconstruction"""
        patterns = []
        
        # Forward pass through network to generate patterns
        current_input = data_array
        
        for layer_size in architecture[1:]:
            # Simulate layer activation
            if len(current_input) > layer_size:
                # Downsample
                indices = np.linspace(0, len(current_input) - 1, layer_size, dtype=int)
                layer_output = current_input[indices]
            elif len(current_input) < layer_size:
                # Upsample
                layer_output = np.interp(
                    np.linspace(0, len(current_input) - 1, layer_size),
                    np.arange(len(current_input)),
                    current_input
                )
            else:
                layer_output = current_input.copy()
                
            # Apply activation function
            layer_output = self._sigmoid(layer_output)
            patterns.append(layer_output.tolist())
            current_input = layer_output
            
        return patterns
        
    def _extract_data_from_network(self, weights: List[np.ndarray], 
                                 biases: List[np.ndarray],
                                 activation_patterns: List[List[float]], 
                                 architecture: List[int]) -> np.ndarray:
        """Extract original data from neural network weights"""
        # Extract from first layer weights (primary storage)
        first_layer_weights = weights[0].flatten()
        
        # Extract from middle layer if available
        middle_idx = len(weights) // 2
        if middle_idx < len(weights):
            middle_weights = weights[middle_idx].flatten()
        else:
            middle_weights = np.array([])
            
        # Combine extraction methods
        extracted_data = []
        
        # Method 1: Direct extraction from first layer
        data_length = architecture[0]
        if len(first_layer_weights) >= data_length:
            extracted_data.extend(first_layer_weights[:data_length])
        
        # Method 2: Use activation patterns for validation
        if activation_patterns and len(activation_patterns[0]) > 0:
            pattern_data = np.array(activation_patterns[0])
            # Inverse sigmoid to get original values
            pattern_data = self._inverse_sigmoid(pattern_data)
            
            # Use as backup if primary extraction fails
            if len(extracted_data) < data_length:
                needed = data_length - len(extracted_data)
                extracted_data.extend(pattern_data[:needed])
                
        # Ensure we have the right amount of data
        while len(extracted_data) < data_length:
            extracted_data.append(0.0)
            
        return np.array(extracted_data[:data_length])
        
    def _transform_data(self, data: np.ndarray, method: str) -> np.ndarray:
        """Apply mathematical transformations to data"""
        if method == 'fourier':
            # Apply FFT
            fft_data = np.fft.fft(data)
            return np.concatenate([fft_data.real, fft_data.imag])
        elif method == 'wavelet':
            # Simple wavelet-like transform
            return np.convolve(data, [0.5, 0.5], mode='same')
        else:
            return data
            
    def _create_rotation_matrix(self, size: int) -> np.ndarray:
        """Create rotation matrix for weight transformation"""
        angle = np.pi / 4
        if size == 1:
            return np.array([[1.0]])
        elif size == 2:
            return np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]
            ])
        else:
            # For larger matrices, create block diagonal rotation
            matrix = np.eye(size)
            for i in range(0, size - 1, 2):
                matrix[i:i+2, i:i+2] = np.array([
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]
                ])
            return matrix
            
    # Activation functions
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        
    def _tanh(self, x):
        return np.tanh(x)
        
    def _relu(self, x):
        return np.maximum(0, x)
        
    def _leaky_relu(self, x):
        return np.where(x > 0, x, 0.01 * x)
        
    def _swish(self, x):
        return x * self._sigmoid(x)
        
    def _inverse_sigmoid(self, y):
        y = np.clip(y, 1e-7, 1 - 1e-7)
        return np.log(y / (1 - y))
        
    def _inverse_tanh(self, y):
        y = np.clip(y, -1 + 1e-7, 1 - 1e-7)
        return 0.5 * np.log((1 + y) / (1 - y))
        
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
