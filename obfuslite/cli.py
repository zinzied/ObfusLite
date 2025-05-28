"""
Command-line interface for ObfusLite

Provides command-line access to all obfuscation features.
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional

from . import Obfuscator, get_available_techniques, get_fast_techniques, __version__

def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser"""

    parser = argparse.ArgumentParser(
        prog='obfuslite',
        description='Advanced Python code obfuscation with novel encoding techniques',
        epilog='Examples:\n'
               '  obfuslite obfuscate input.py -o output.py\n'
               '  obfuslite obfuscate input.py -t fast_xor -l 3\n'
               '  obfuslite deobfuscate data.json -o original.py\n'
               '  obfuslite list-techniques\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--version', action='version', version=f'ObfusLite {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Obfuscate command
    obfuscate_parser = subparsers.add_parser(
        'obfuscate',
        help='Obfuscate Python code',
        description='Obfuscate Python source code using specified technique'
    )
    obfuscate_parser.add_argument(
        'input',
        help='Input Python file to obfuscate'
    )
    obfuscate_parser.add_argument(
        '-o', '--output',
        help='Output file for obfuscated code (default: input_obfuscated.py)'
    )
    obfuscate_parser.add_argument(
        '-t', '--technique',
        default='fast_xor',
        choices=get_available_techniques(),
        help='Obfuscation technique to use (default: fast_xor)'
    )
    obfuscate_parser.add_argument(
        '-l', '--layers',
        type=int,
        default=2,
        help='Number of obfuscation layers (default: 2)'
    )
    obfuscate_parser.add_argument(
        '-s', '--seed',
        type=int,
        help='Random seed for reproducible obfuscation'
    )
    obfuscate_parser.add_argument(
        '--save-data',
        help='Save obfuscation data to file for later deobfuscation'
    )
    obfuscate_parser.add_argument(
        '--standalone',
        action='store_true',
        help='Create standalone executable file (default behavior)'
    )

    # Deobfuscate command
    deobfuscate_parser = subparsers.add_parser(
        'deobfuscate',
        help='Deobfuscate code from obfuscation data',
        description='Restore original code from obfuscation data file'
    )
    deobfuscate_parser.add_argument(
        'data_file',
        help='Obfuscation data file (JSON format)'
    )
    deobfuscate_parser.add_argument(
        '-o', '--output',
        help='Output file for deobfuscated code (default: deobfuscated.py)'
    )

    # List techniques command
    list_parser = subparsers.add_parser(
        'list-techniques',
        help='List available obfuscation techniques',
        description='Show all available obfuscation techniques with descriptions'
    )
    list_parser.add_argument(
        '--fast-only',
        action='store_true',
        help='Show only fast techniques'
    )

    # Info command
    info_parser = subparsers.add_parser(
        'info',
        help='Show information about a technique',
        description='Display detailed information about an obfuscation technique'
    )
    info_parser.add_argument(
        'technique',
        choices=get_available_techniques(),
        help='Technique to get information about'
    )

    # Benchmark command
    benchmark_parser = subparsers.add_parser(
        'benchmark',
        help='Benchmark obfuscation techniques',
        description='Test performance of different obfuscation techniques'
    )
    benchmark_parser.add_argument(
        'input',
        help='Input Python file to benchmark with'
    )
    benchmark_parser.add_argument(
        '--techniques',
        nargs='+',
        default=get_fast_techniques(),
        help='Techniques to benchmark (default: all fast techniques)'
    )

    # GUI command
    gui_parser = subparsers.add_parser(
        'gui',
        help='Launch the enhanced GUI interface',
        description='Start the ObfusLite GUI with multi-file support'
    )

    return parser

def cmd_obfuscate(args) -> int:
    """Handle obfuscate command"""

    # Check input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1

    # Read input file
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        return 1

    # Determine output file
    if args.output:
        output_file = args.output
    else:
        input_path = Path(args.input)
        output_file = input_path.with_name(f"{input_path.stem}_obfuscated{input_path.suffix}")

    print(f"🔒 Obfuscating '{args.input}' using '{args.technique}' technique...")
    print(f"   Layers: {args.layers}")
    if args.seed:
        print(f"   Seed: {args.seed}")

    # Obfuscate
    try:
        obfuscator = Obfuscator()
        result = obfuscator.obfuscate(
            code,
            technique=args.technique,
            layers=args.layers,
            seed=args.seed
        )

        # Create standalone file
        standalone_code = obfuscator.create_standalone_file(result)

        # Save standalone file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(standalone_code)

        print(f"✅ Obfuscated file saved: {output_file}")
        print(f"   Original size: {result['original_size']} bytes")
        print(f"   Obfuscated size: {result['obfuscated_size']} bytes")
        print(f"   Compression: {(1 - result['obfuscated_size']/result['original_size'])*100:.1f}%")

        # Save obfuscation data if requested
        if args.save_data:
            with open(args.save_data, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"   Obfuscation data saved: {args.save_data}")

        print(f"\n🚀 Usage:")
        print(f"   Run: python {output_file}")
        print(f"   Create .exe: pyinstaller --onefile {output_file}")

        return 0

    except Exception as e:
        print(f"Error during obfuscation: {e}", file=sys.stderr)
        return 1

def cmd_deobfuscate(args) -> int:
    """Handle deobfuscate command"""

    # Check data file
    if not os.path.exists(args.data_file):
        print(f"Error: Data file '{args.data_file}' not found", file=sys.stderr)
        return 1

    # Determine output file
    output_file = args.output or 'deobfuscated.py'

    try:
        # Load obfuscation data
        with open(args.data_file, 'r', encoding='utf-8') as f:
            obfuscated_data = json.load(f)

        print(f"🔓 Deobfuscating from '{args.data_file}'...")

        # Deobfuscate
        obfuscator = Obfuscator()
        original_code = obfuscator.deobfuscate(obfuscated_data)

        # Save original code
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        print(f"✅ Original code restored: {output_file}")
        return 0

    except Exception as e:
        print(f"Error during deobfuscation: {e}", file=sys.stderr)
        return 1

def cmd_list_techniques(args) -> int:
    """Handle list-techniques command"""

    from .encoders import get_technique_info

    techniques = get_fast_techniques() if args.fast_only else get_available_techniques()
    technique_info = get_technique_info()

    print("🛡️  Available ObfusLite Techniques:")
    print("=" * 50)

    for technique in techniques:
        info = technique_info.get(technique, {})
        technique_type = info.get('type', 'unknown')
        description = info.get('description', 'No description available')
        speed = info.get('speed', 'unknown')
        security = info.get('security', 'unknown')

        print(f"\n📦 {technique}")
        print(f"   Type: {technique_type}")
        print(f"   Description: {description}")
        print(f"   Speed: {speed}")
        print(f"   Security: {security}")

    return 0

def cmd_info(args) -> int:
    """Handle info command"""

    from .encoders import get_technique_info

    technique_info = get_technique_info()
    info = technique_info.get(args.technique, {})

    print(f"📋 Technique: {args.technique}")
    print("=" * 30)
    print(f"Type: {info.get('type', 'unknown')}")
    print(f"Description: {info.get('description', 'No description available')}")
    print(f"Speed: {info.get('speed', 'unknown')}")
    print(f"Security: {info.get('security', 'unknown')}")

    return 0

def cmd_gui(args) -> int:
    """Handle GUI command"""
    try:
        from .gui import main as gui_main
        print("🖥️  Launching ObfusLite Enhanced GUI...")
        return gui_main()
    except ImportError:
        print("❌ GUI not available. Install PyQt6: pip install PyQt6", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error launching GUI: {e}", file=sys.stderr)
        return 1

def cmd_benchmark(args) -> int:
    """Handle benchmark command"""

    # Check input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1

    try:
        # Read input file
        with open(args.input, 'r', encoding='utf-8') as f:
            code = f.read()

        print(f"⚡ Benchmarking techniques with '{args.input}'...")
        print("=" * 60)
        print(f"{'Technique':<15} {'Time(s)':<10} {'Size Ratio':<12} {'Status':<10}")
        print("-" * 60)

        obfuscator = Obfuscator()

        for technique in args.techniques:
            if technique not in get_available_techniques():
                print(f"{technique:<15} {'N/A':<10} {'N/A':<12} {'Unknown':<10}")
                continue

            try:
                import time
                start_time = time.time()

                result = obfuscator.obfuscate(code, technique=technique, layers=1)

                end_time = time.time()
                duration = end_time - start_time
                ratio = result['obfuscated_size'] / result['original_size']

                print(f"{technique:<15} {duration:<10.3f} {ratio:<12.2f} {'Success':<10}")

            except Exception as e:
                print(f"{technique:<15} {'Error':<10} {'N/A':<12} {str(e)[:10]:<10}")

        return 0

    except Exception as e:
        print(f"Error during benchmark: {e}", file=sys.stderr)
        return 1

def main() -> int:
    """Main entry point for the CLI"""

    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to appropriate command handler
    if args.command == 'obfuscate':
        return cmd_obfuscate(args)
    elif args.command == 'deobfuscate':
        return cmd_deobfuscate(args)
    elif args.command == 'list-techniques':
        return cmd_list_techniques(args)
    elif args.command == 'info':
        return cmd_info(args)
    elif args.command == 'benchmark':
        return cmd_benchmark(args)
    elif args.command == 'gui':
        return cmd_gui(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
