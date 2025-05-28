#!/usr/bin/env python3
"""
Test main application file
"""

from utils import helper_function, calculate_sum
from config import get_config

def main():
    """Main application function"""
    print("🚀 Starting Test Application")
    
    config = get_config()
    print(f"📋 Config: {config}")
    
    result = helper_function("Hello from main!")
    print(f"📝 Helper result: {result}")
    
    numbers = [1, 2, 3, 4, 5]
    total = calculate_sum(numbers)
    print(f"🔢 Sum of {numbers} = {total}")
    
    print("✅ Application completed successfully!")

if __name__ == "__main__":
    main()
