# PyObfuscator - Advanced Python Code Obfuscation Library

A comprehensive Python code obfuscation library featuring novel encoding techniques that go beyond traditional methods. This library provides multiple innovative obfuscation algorithms designed to protect your Python code before compilation with PyInstaller.

## 🚀 Features

### ⚡ Performance Optimized
- **3 Performance Modes**: Fast, Balanced, Full
- **Ultra-Fast Encoders**: 100x faster than complex algorithms
- **Low Memory Usage**: < 1MB RAM for most operations
- **No More Freezing**: Instant processing even for large files

### 🔧 Fast Obfuscation Techniques

1. **Fast XOR Encoding** - Multi-key XOR with compression (Recommended)
2. **Fast Base64 Encoding** - Base64 with character substitution
3. **Fast Rotation Cipher** - Multi-round Caesar cipher
4. **Fast Hash Encoding** - Hash-based chunk encoding
5. **Fast Binary Manipulation** - Bit shifting operations
6. **Fast Lookup Tables** - Character mapping encoding

### 🔬 Advanced Obfuscation Techniques

1. **Quantum-Inspired Encoding** - Uses quantum gate operations and superposition concepts
2. **DNA Sequence Mapping** - Maps code to biological DNA sequences with genetic mutations
3. **Fractal Pattern Encoding** - Encodes data using mathematical fractals and chaos theory
4. **Neural Network Weight Encoding** - Stores code as neural network weights and biases
5. **Steganographic Hiding** - Hides code within innocent-looking data structures
6. **Runtime Reconstruction** - Creates self-modifying code that rebuilds at runtime
7. **Multi-dimensional Tensor Encoding** - Uses tensor operations and linear algebra

### Key Benefits

- ✅ **Lightning Fast** - Process large files in milliseconds
- ✅ **Memory Efficient** - Minimal RAM usage, no more crashes
- ✅ **PyInstaller Compatible** - Generates standalone code ready for .exe compilation
- ✅ **Multi-layer Protection** - Apply multiple obfuscation layers for enhanced security
- ✅ **Reversible** - Complete deobfuscation capability for legitimate use
- ✅ **Novel Algorithms** - Unique techniques not found in traditional obfuscators
- ✅ **GUI Interface** - User-friendly graphical interface included
- ✅ **Modular Design** - Easy to extend with new techniques

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install pyobfuscator
```

### From Source

```bash
git clone https://github.com/yourusername/pyobfuscator.git
cd pyobfuscator
pip install -e .
```

### Optional Dependencies

```bash
# For GUI interface
pip install pyobfuscator[gui]

# For development
pip install pyobfuscator[dev]
```

### Required Files

Ensure all these files are in your project directory:
- `obfuscator_core.py` - Main obfuscation engine
- `quantum_encoder.py` - Quantum-inspired encoding
- `dna_encoder.py` - DNA sequence mapping
- `fractal_encoder.py` - Fractal pattern encoding
- `neural_encoder.py` - Neural network encoding
- `steganographic_encoder.py` - Steganographic hiding
- `runtime_reconstructor.py` - Runtime reconstruction
- `tensor_encoder.py` - Tensor-based encoding
- `Obfusc8.py` - GUI application
- `example_usage.py` - Usage examples

## 🎯 Quick Start

### Command Line Interface

```bash
# Obfuscate a Python file
pyobfuscator obfuscate input.py -o output.py -t fast_xor -l 2

# List available techniques
pyobfuscator list-techniques

# Get help
pyobfuscator --help
```

### GUI Interface

```bash
# Launch GUI
pyobfuscator-gui
```

### Python API

```python
from pyobfuscator import Obfuscator, quick_obfuscate

# Quick obfuscation (one line!)
standalone_code = quick_obfuscate(your_code, technique='fast_xor', layers=2)

# Advanced usage
obfuscator = Obfuscator()
result = obfuscator.obfuscate(code, technique='fast_xor', layers=2)
standalone_code = obfuscator.create_standalone_file(result)

# Save and run
with open('obfuscated_app.py', 'w') as f:
    f.write(standalone_code)
```

## 🔧 Usage with PyInstaller

1. **Obfuscate your code** using this library
2. **Save the standalone code** to a .py file
3. **Compile with PyInstaller**:
   ```bash
   pyinstaller --onefile obfuscated_app.py
   ```

The resulting .exe will contain your obfuscated code that reconstructs itself at runtime.

## 📚 Obfuscation Techniques Explained

### Quantum-Inspired Encoding
- Maps binary data to quantum state representations
- Uses quantum gate operations (Hadamard, Pauli-X, Y, Z)
- Applies superposition and entanglement concepts
- Encodes data in complex number amplitudes

### DNA Sequence Mapping
- Converts code to DNA base sequences (A, T, G, C)
- Applies genetic mutations for additional obfuscation
- Uses codon tables for amino acid encoding
- Includes intron sequences for steganographic hiding

### Fractal Pattern Encoding
- Utilizes mathematical fractals (Mandelbrot, Julia sets)
- Applies chaos theory and strange attractors
- Maps data to fractal coordinates
- Uses Lorenz attractor and Sierpinski triangle

### Neural Network Weight Encoding
- Stores code as neural network weights and biases
- Uses multiple layer architectures
- Applies activation functions for transformation
- Includes forward and backward propagation concepts

### Steganographic Hiding
- Hides code in innocent-looking data:
  - Lorem ipsum text
  - Configuration files
  - Mathematical constants
  - Fake database records
  - Poetry structures

### Runtime Reconstruction
- Creates self-modifying code
- Uses bytecode assembly
- AST (Abstract Syntax Tree) reconstruction
- Dynamic import mechanisms
- Function composition techniques

### Tensor Encoding
- Multi-dimensional array operations
- Matrix multiplication transformations
- Singular Value Decomposition (SVD)
- Fourier and wavelet transforms
- Linear algebra operations

## ⚙️ Configuration Options

### Obfuscation Parameters

- **Technique**: Choose from 7 available methods
- **Layers**: Apply 1-10 layers of obfuscation
- **Seed**: Set random seed for reproducible results
- **Compression**: Optional output compression

### Security Levels

- **Basic** (1-2 layers): Fast obfuscation for simple protection
- **Standard** (3-5 layers): Balanced security and performance
- **High** (6-10 layers): Maximum security for sensitive code

## 🔍 Examples

See `example_usage.py` for comprehensive examples including:

- Basic obfuscation/deobfuscation
- Advanced features demonstration
- PyInstaller preparation
- Technique comparison
- Security features showcase

## 🛡️ Security Considerations

### What This Library Protects Against

- ✅ Casual code inspection
- ✅ Simple reverse engineering attempts
- ✅ Automated code analysis tools
- ✅ Source code theft
- ✅ Algorithm discovery

### Limitations

- ❌ Not cryptographically secure against determined attackers
- ❌ Runtime performance overhead due to reconstruction
- ❌ Increased file size due to obfuscation data
- ❌ Debugging becomes more difficult

### Best Practices

1. **Combine multiple techniques** for enhanced security
2. **Use high layer counts** for sensitive code
3. **Keep obfuscation keys secure** if using seeds
4. **Test thoroughly** before deployment
5. **Consider performance impact** for time-critical applications

## 🔧 Extending the Library

### Adding New Techniques

1. Create a new encoder class inheriting from `BaseEncoder`
2. Implement `encode()` and `decode()` methods
3. Register with the obfuscator core
4. Add to GUI dropdown menu

Example:
```python
from obfuscator_core import BaseEncoder

class MyCustomEncoder(BaseEncoder):
    def encode(self, data: str) -> Dict[str, Any]:
        # Your encoding logic here
        pass

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        # Your decoding logic here
        pass

# Register the technique
obfuscator.register_technique('custom', MyCustomEncoder())
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all encoder files are in the same directory
2. **Memory Issues**: Reduce layer count for large files
3. **PyInstaller Errors**: Check that all dependencies are included
4. **Deobfuscation Fails**: Verify obfuscation data integrity

### Performance Optimization

- Use fewer layers for faster processing
- Choose simpler techniques for large codebases
- Enable multithreading in settings
- Consider output compression for storage

## 📄 License

This library is free to use for personal and commercial projects. No warranty is provided.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- New obfuscation techniques
- Performance optimizations
- Additional GUI features
- Better PyInstaller integration
- Documentation improvements

## 📞 Support

For issues, questions, or feature requests, please create an issue in the project repository.

---

**Note**: This obfuscation library is designed for legitimate code protection purposes. Users are responsible for complying with applicable laws and regulations in their jurisdiction.
