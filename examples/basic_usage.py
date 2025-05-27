"""
Basic usage examples for PyObfuscator
"""

from pyobfuscator import Obfuscator, quick_obfuscate

def example_1_basic_obfuscation():
    """Example 1: Basic obfuscation"""
    print("Example 1: Basic Obfuscation")
    print("=" * 40)
    
    # Sample code to obfuscate
    code = '''
def hello_world():
    print("Hello, World!")
    return "Success"

if __name__ == "__main__":
    result = hello_world()
    print(f"Result: {result}")
'''
    
    # Create obfuscator
    obfuscator = Obfuscator()
    
    # Obfuscate using fast_xor technique
    result = obfuscator.obfuscate(code, technique='fast_xor', layers=2)
    
    print(f"Original size: {result['original_size']} bytes")
    print(f"Obfuscated size: {result['obfuscated_size']} bytes")
    print(f"Technique: {result['technique']}")
    print(f"Layers: {result['layers']}")
    
    # Create standalone file
    standalone_code = obfuscator.create_standalone_file(result)
    
    # Save to file
    with open('obfuscated_hello.py', 'w') as f:
        f.write(standalone_code)
    
    print("✅ Obfuscated file saved as 'obfuscated_hello.py'")
    print("   Run with: python obfuscated_hello.py")

def example_2_quick_obfuscation():
    """Example 2: Quick obfuscation using helper function"""
    print("\nExample 2: Quick Obfuscation")
    print("=" * 40)
    
    code = '''
import random

def generate_numbers():
    return [random.randint(1, 100) for _ in range(5)]

def main():
    numbers = generate_numbers()
    print(f"Generated numbers: {numbers}")
    print(f"Sum: {sum(numbers)}")

if __name__ == "__main__":
    main()
'''
    
    # Quick obfuscation - one line!
    standalone_code = quick_obfuscate(code, technique='fast_xor', layers=3)
    
    # Save to file
    with open('obfuscated_numbers.py', 'w') as f:
        f.write(standalone_code)
    
    print("✅ Quick obfuscated file saved as 'obfuscated_numbers.py'")

def example_3_multiple_techniques():
    """Example 3: Testing multiple techniques"""
    print("\nExample 3: Multiple Techniques")
    print("=" * 40)
    
    code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Fibonacci(10) = {fibonacci(10)}")
'''
    
    obfuscator = Obfuscator()
    techniques = ['fast_xor', 'fast_base64', 'fast_rotation']
    
    for technique in techniques:
        try:
            result = obfuscator.obfuscate(code, technique=technique, layers=1)
            ratio = result['obfuscated_size'] / result['original_size']
            print(f"{technique:<15} Size ratio: {ratio:.2f}")
        except Exception as e:
            print(f"{technique:<15} Error: {e}")

def example_4_deobfuscation():
    """Example 4: Obfuscation and deobfuscation"""
    print("\nExample 4: Obfuscation and Deobfuscation")
    print("=" * 40)
    
    original_code = '''
def secret_calculation(x, y):
    secret_key = 42
    return (x + y) * secret_key

result = secret_calculation(5, 10)
print(f"Secret result: {result}")
'''
    
    obfuscator = Obfuscator()
    
    # Obfuscate
    result = obfuscator.obfuscate(original_code, technique='fast_xor', layers=2)
    print("✅ Code obfuscated")
    
    # Deobfuscate
    deobfuscated_code = obfuscator.deobfuscate(result)
    print("✅ Code deobfuscated")
    
    # Verify integrity
    if deobfuscated_code.strip() == original_code.strip():
        print("✅ Integrity check passed!")
    else:
        print("❌ Integrity check failed!")

def main():
    """Run all examples"""
    print("PyObfuscator - Basic Usage Examples")
    print("=" * 50)
    
    try:
        example_1_basic_obfuscation()
        example_2_quick_obfuscation()
        example_3_multiple_techniques()
        example_4_deobfuscation()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("\nGenerated files:")
        print("- obfuscated_hello.py")
        print("- obfuscated_numbers.py")
        print("\nTry running them:")
        print("python obfuscated_hello.py")
        print("python obfuscated_numbers.py")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
