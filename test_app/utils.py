"""
Utility functions for the test application
"""

import datetime

def helper_function(message):
    """Helper function that processes a message"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {message}"

def calculate_sum(numbers):
    """Calculate sum of a list of numbers"""
    if not numbers:
        return 0
    
    total = sum(numbers)
    print(f"🧮 Calculating sum of {len(numbers)} numbers...")
    return total

def format_output(data):
    """Format data for output"""
    if isinstance(data, dict):
        return "\n".join([f"{k}: {v}" for k, v in data.items()])
    elif isinstance(data, list):
        return ", ".join(map(str, data))
    else:
        return str(data)
