#!/usr/bin/env python3
"""
Smart Batch Obfuscator for ObfusLite
Handles module dependencies correctly when obfuscating multiple files
"""

import os
import ast
import json
import shutil
from pathlib import Path
from typing import List, Dict, Set

def analyze_project_structure(project_dir: str) -> Dict:
    """
    Analyze Python project structure and dependencies
    
    Args:
        project_dir: Path to the project directory
        
    Returns:
        Dictionary with project analysis
    """
    project_path = Path(project_dir)
    python_files = list(project_path.rglob("*.py"))
    
    analysis = {
        'files': [],
        'dependencies': {},
        'main_candidates': [],
        'modules': {}
    }
    
    for py_file in python_files:
        if py_file.name == "__init__.py":
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Analyze imports
            imports = []
            local_imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        if node.level > 0 or any(node.module.startswith(p) for p in ['.', 'src', 'lib']):
                            local_imports.append(node.module)
                        else:
                            imports.append(node.module)
            
            # Check if it's a main file
            has_main = any(isinstance(node, ast.If) and 
                          isinstance(node.test, ast.Compare) and
                          isinstance(node.test.left, ast.Name) and
                          node.test.left.id == '__name__'
                          for node in tree.body)
            
            file_info = {
                'path': str(py_file),
                'relative_path': str(py_file.relative_to(project_path)),
                'imports': imports,
                'local_imports': local_imports,
                'has_main': has_main,
                'size': len(content)
            }
            
            analysis['files'].append(file_info)
            analysis['dependencies'][str(py_file)] = local_imports
            
            if has_main:
                analysis['main_candidates'].append(str(py_file))
                
        except Exception as e:
            print(f"Warning: Could not analyze {py_file}: {e}")
    
    return analysis

def create_obfuscation_strategy(analysis: Dict) -> Dict:
    """
    Create an obfuscation strategy based on project analysis
    
    Args:
        analysis: Project analysis from analyze_project_structure
        
    Returns:
        Obfuscation strategy
    """
    strategy = {
        'approach': 'single_file',  # Default to single file
        'main_file': None,
        'files_to_combine': [],
        'standalone_files': []
    }
    
    # Determine strategy
    if len(analysis['files']) == 1:
        strategy['approach'] = 'single_file'
        strategy['main_file'] = analysis['files'][0]['path']
    elif analysis['main_candidates']:
        # Multi-file project with main file
        strategy['approach'] = 'combine_and_obfuscate'
        strategy['main_file'] = analysis['main_candidates'][0]  # Use first main candidate
        strategy['files_to_combine'] = [f['path'] for f in analysis['files']]
    else:
        # Multiple standalone files
        strategy['approach'] = 'individual_files'
        strategy['standalone_files'] = [f['path'] for f in analysis['files']]
    
    return strategy

def smart_obfuscate_project(project_dir: str, output_dir: str = None) -> bool:
    """
    Smart obfuscation of a Python project
    
    Args:
        project_dir: Path to the project directory
        output_dir: Output directory (default: project_dir + "_obfuscated")
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from obfuslite import Obfuscator, quick_obfuscate
    except ImportError:
        print("❌ ObfusLite not found. Install with: pip install obfuslite")
        return False
    
    if output_dir is None:
        output_dir = f"{project_dir}_obfuscated"
    
    print(f"🔍 Analyzing project: {project_dir}")
    analysis = analyze_project_structure(project_dir)
    
    print(f"📊 Found {len(analysis['files'])} Python files")
    print(f"🎯 Main candidates: {len(analysis['main_candidates'])}")
    
    strategy = create_obfuscation_strategy(analysis)
    print(f"📋 Strategy: {strategy['approach']}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    if strategy['approach'] == 'single_file':
        # Single file obfuscation
        file_path = strategy['main_file']
        print(f"🔒 Obfuscating single file: {Path(file_path).name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        obfuscated_code = quick_obfuscate(code, technique='fast_xor', layers=2)
        
        output_file = os.path.join(output_dir, f"{Path(file_path).stem}_obfuscated.py")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        
        print(f"✅ Obfuscated file: {output_file}")
        
    elif strategy['approach'] == 'combine_and_obfuscate':
        # Combine files and obfuscate
        print(f"🔗 Combining {len(strategy['files_to_combine'])} files...")
        
        combined_code = combine_files(strategy['files_to_combine'], strategy['main_file'])
        
        print(f"🔒 Obfuscating combined code...")
        obfuscated_code = quick_obfuscate(combined_code, technique='fast_xor', layers=2)
        
        main_name = Path(strategy['main_file']).stem
        output_file = os.path.join(output_dir, f"{main_name}_combined_obfuscated.py")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(obfuscated_code)
        
        print(f"✅ Combined obfuscated file: {output_file}")
        
    elif strategy['approach'] == 'individual_files':
        # Obfuscate each file individually
        print(f"🔒 Obfuscating {len(strategy['standalone_files'])} files individually...")
        
        obfuscator = Obfuscator()
        
        for file_path in strategy['standalone_files']:
            print(f"   Processing: {Path(file_path).name}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            result = obfuscator.obfuscate(code, technique='fast_xor', layers=2)
            standalone_code = obfuscator.create_standalone_file(result)
            
            file_name = Path(file_path).stem
            output_file = os.path.join(output_dir, f"{file_name}_obfuscated.py")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(standalone_code)
        
        print(f"✅ Obfuscated {len(strategy['standalone_files'])} files")
    
    # Copy non-Python files
    copy_non_python_files(project_dir, output_dir)
    
    # Create run instructions
    create_run_instructions(output_dir, strategy)
    
    return True

def combine_files(file_paths: List[str], main_file: str) -> str:
    """Combine multiple Python files into one"""
    all_imports = set()
    all_code = []
    
    # Process non-main files first
    for file_path in file_paths:
        if file_path == main_file:
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
            
            # Extract imports and code
            imports = []
            code_nodes = []
            
            for node in tree.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    # Skip local imports
                    if isinstance(node, ast.ImportFrom) and node.module:
                        if node.level > 0 or any(node.module.startswith(p) for p in ['.', 'src', 'lib']):
                            continue
                    imports.append(ast.unparse(node))
                else:
                    code_nodes.append(node)
            
            all_imports.update(imports)
            
            if code_nodes:
                all_code.append(f"\n# === Code from {Path(file_path).name} ===")
                for node in code_nodes:
                    all_code.append(ast.unparse(node))
                    
        except Exception as e:
            print(f"Warning: Could not process {file_path}: {e}")
    
    # Process main file last
    with open(main_file, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    try:
        tree = ast.parse(main_content)
        
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    if node.level > 0 or any(node.module.startswith(p) for p in ['.', 'src', 'lib']):
                        continue
                all_imports.add(ast.unparse(node))
            else:
                all_code.append(ast.unparse(node))
                
    except Exception as e:
        print(f"Warning: Could not process main file {main_file}: {e}")
        all_code.append(main_content)
    
    # Combine everything
    combined = []
    combined.append('#!/usr/bin/env python3')
    combined.append('"""Combined and Obfuscated Application"""')
    combined.append('')
    
    if all_imports:
        combined.extend(sorted(all_imports))
        combined.append('')
    
    combined.extend(all_code)
    
    return '\n'.join(combined)

def copy_non_python_files(source_dir: str, dest_dir: str):
    """Copy non-Python files to output directory"""
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    for item in source_path.rglob("*"):
        if item.is_file() and not item.suffix == '.py':
            relative_path = item.relative_to(source_path)
            dest_file = dest_path / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_file)

def create_run_instructions(output_dir: str, strategy: Dict):
    """Create instructions for running the obfuscated application"""
    instructions = f"""
# ObfusLite Obfuscated Application

## Strategy Used: {strategy['approach']}

## How to Run:
"""
    
    if strategy['approach'] == 'single_file':
        main_file = Path(strategy['main_file']).stem + "_obfuscated.py"
        instructions += f"""
1. Run the obfuscated file:
   python {main_file}

2. Create executable:
   pyinstaller --onefile {main_file}
"""
    elif strategy['approach'] == 'combine_and_obfuscate':
        main_name = Path(strategy['main_file']).stem
        combined_file = f"{main_name}_combined_obfuscated.py"
        instructions += f"""
1. Run the combined obfuscated file:
   python {combined_file}

2. Create executable:
   pyinstaller --onefile {combined_file}
"""
    else:
        instructions += """
1. Run individual obfuscated files:
   python <filename>_obfuscated.py

2. Create executables:
   pyinstaller --onefile <filename>_obfuscated.py
"""
    
    with open(os.path.join(output_dir, "README.txt"), 'w') as f:
        f.write(instructions)

def main():
    """Main function for command line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python smart_batch_obfuscator.py <project_directory> [output_directory]")
        print("Example: python smart_batch_obfuscator.py my_app my_app_obfuscated")
        return
    
    project_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("🛡️ ObfusLite Smart Batch Obfuscator")
    print("=" * 50)
    
    if smart_obfuscate_project(project_dir, output_dir):
        print("\n🎉 Obfuscation completed successfully!")
    else:
        print("\n❌ Obfuscation failed!")

if __name__ == "__main__":
    main()
