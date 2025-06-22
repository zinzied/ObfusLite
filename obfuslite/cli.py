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
               '  obfuslite list-techniques\n'
               '  obfuslite gui\n'
               '  obfuslite web --port 8080\n',
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

    # Combine command
    combine_parser = subparsers.add_parser(
        'combine',
        help='Combine multiple Python files into one',
        description='Combine multiple Python files into a single file for easier obfuscation'
    )
    combine_parser.add_argument(
        'main_file',
        help='Main Python file (entry point)'
    )
    combine_parser.add_argument(
        '-o', '--output',
        help='Output file for combined code (default: combined_app.py)'
    )
    combine_parser.add_argument(
        '--obfuscate',
        action='store_true',
        help='Automatically obfuscate the combined file'
    )
    combine_parser.add_argument(
        '-t', '--technique',
        default='fast_xor',
        choices=get_available_techniques(),
        help='Obfuscation technique to use if --obfuscate is specified (default: fast_xor)'
    )
    combine_parser.add_argument(
        '-l', '--layers',
        type=int,
        default=2,
        help='Number of obfuscation layers if --obfuscate is specified (default: 2)'
    )

    # GUI command
    gui_parser = subparsers.add_parser(
        'gui',
        help='Launch the enhanced GUI interface',
        description='Start the ObfusLite GUI with multi-file support'
    )

    # Web interface command
    web_parser = subparsers.add_parser(
        'web',
        help='Launch the web interface',
        description='Start the ObfusLite web interface in your browser'
    )
    web_parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind the web server to (default: 127.0.0.1)'
    )
    web_parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind the web server to (default: 5000)'
    )
    web_parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Do not automatically open browser'
    )
    web_parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )

    # Debug command
    debug_parser = subparsers.add_parser(
        'debug',
        help='Debug a combined Python file',
        description='Analyze a combined file for potential issues'
    )
    debug_parser.add_argument(
        'file',
        help='Combined Python file to debug'
    )
    debug_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed analysis'
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

def cmd_combine(args) -> int:
    """Handle combine command"""

    # Check input file
    if not os.path.exists(args.main_file):
        print(f"Error: Main file '{args.main_file}' not found", file=sys.stderr)
        return 1

    # Determine output file
    output_file = args.output or 'combined_app.py'

    print(f"🔗 Combining files starting from '{args.main_file}'...")

    try:
        # Import combine functionality
        from .core import combine_python_files

        # Combine files
        combined_file = combine_python_files(args.main_file, output_file)

        print(f"✅ Combined file created: {combined_file}")
        print(f"   Original files combined into single file")

        # Obfuscate if requested
        if args.obfuscate:
            print(f"\n🔒 Obfuscating combined file...")

            obfuscator = Obfuscator()

            # Read combined file
            with open(combined_file, 'r', encoding='utf-8') as f:
                code = f.read()

            # Obfuscate
            result = obfuscator.obfuscate(
                code,
                technique=args.technique,
                layers=args.layers
            )

            # Create standalone file
            standalone_code = obfuscator.create_standalone_file(result)

            # Save obfuscated file
            obfuscated_file = combined_file.replace('.py', '_obfuscated.py')
            with open(obfuscated_file, 'w', encoding='utf-8') as f:
                f.write(standalone_code)

            print(f"✅ Obfuscated file created: {obfuscated_file}")
            print(f"   Technique: {args.technique}")
            print(f"   Layers: {args.layers}")

            print(f"\n🚀 Usage:")
            print(f"   Run: python {obfuscated_file}")
            print(f"   Create .exe: pyinstaller --onefile {obfuscated_file}")
        else:
            print(f"\n🚀 Usage:")
            print(f"   Run: python {combined_file}")
            print(f"   Obfuscate: obfuslite obfuscate {combined_file}")
            print(f"   Create .exe: pyinstaller --onefile {combined_file}")

        return 0

    except Exception as e:
        print(f"Error during combine operation: {e}", file=sys.stderr)
        return 1

def cmd_debug(args) -> int:
    """Handle debug command"""

    # Check input file
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        return 1

    try:
        from .core import debug_combined_file

        print(f"🔍 Debugging combined file: {args.file}")
        print("=" * 50)

        debug_info = debug_combined_file(args.file)

        # Basic info
        print(f"📁 File exists: {'✅' if debug_info['file_exists'] else '❌'}")
        print(f"✅ Syntax valid: {'✅' if debug_info['syntax_valid'] else '❌'}")

        if debug_info['syntax_error']:
            error = debug_info['syntax_error']
            print(f"❌ Syntax Error:")
            print(f"   Line {error['line']}: {error['message']}")
            if error['text']:
                print(f"   Code: {error['text'].strip()}")

        # Statistics
        if debug_info['syntax_valid']:
            print(f"\n📊 Statistics:")
            print(f"   Imports: {len(debug_info['imports'])}")
            print(f"   Functions: {len(debug_info['functions'])}")
            print(f"   Classes: {len(debug_info['classes'])}")
            print(f"   Global variables: {len(debug_info['global_vars'])}")

        # Issues
        if debug_info['potential_issues']:
            print(f"\n⚠️  Potential Issues ({len(debug_info['potential_issues'])}):")
            for i, issue in enumerate(debug_info['potential_issues'], 1):
                print(f"   {i}. {issue}")
        else:
            print(f"\n✅ No obvious issues detected!")

        # Verbose output
        if args.verbose and debug_info['syntax_valid']:
            print(f"\n📋 Detailed Analysis:")

            if debug_info['imports']:
                print(f"\n🔗 Imports ({len(debug_info['imports'])}):")
                for imp in debug_info['imports'][:10]:  # Show first 10
                    if imp['type'] == 'import':
                        print(f"   import {imp['name']}")
                    else:
                        print(f"   from {imp['module']} import {imp['name']}")
                if len(debug_info['imports']) > 10:
                    print(f"   ... and {len(debug_info['imports']) - 10} more")

            if debug_info['functions']:
                print(f"\n🔧 Functions ({len(debug_info['functions'])}):")
                for func in debug_info['functions'][:10]:  # Show first 10
                    args_str = ', '.join(func['args'])
                    print(f"   Line {func['line']}: {func['name']}({args_str})")
                if len(debug_info['functions']) > 10:
                    print(f"   ... and {len(debug_info['functions']) - 10} more")

            if debug_info['classes']:
                print(f"\n🏗️  Classes ({len(debug_info['classes'])}):")
                for cls in debug_info['classes']:
                    bases_str = f"({', '.join(cls['bases'])})" if cls['bases'] else ""
                    print(f"   Line {cls['line']}: {cls['name']}{bases_str}")

        return 0

    except Exception as e:
        print(f"Error during debug: {e}", file=sys.stderr)
        return 1

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

def cmd_web(args) -> int:
    """Handle web interface command"""
    try:
        from .web_server import start_web_interface
        print("🌐 Starting ObfusLite Web Interface...")

        success = start_web_interface(
            host=args.host,
            port=args.port,
            debug=args.debug,
            open_browser=not args.no_browser
        )

        return 0 if success else 1

    except ImportError:
        print("❌ Web interface not available. Install Flask: pip install flask flask-cors", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error launching web interface: {e}", file=sys.stderr)
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
    elif args.command == 'combine':
        return cmd_combine(args)
    elif args.command == 'debug':
        return cmd_debug(args)
    elif args.command == 'gui':
        return cmd_gui(args)
    elif args.command == 'web':
        return cmd_web(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
