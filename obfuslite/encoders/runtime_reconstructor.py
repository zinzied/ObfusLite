"""
Runtime Reconstruction for Python Code Obfuscation
Creates self-modifying code that reconstructs itself at runtime
"""

import ast
import base64
import json
import random
import string
import hashlib
from typing import Dict, Any, List, Tuple
from obfuscator_core import BaseEncoder

class RuntimeReconstructor(BaseEncoder):
    """
    Runtime reconstructor that creates self-modifying code
    which rebuilds the original program during execution
    """
    
    def __init__(self):
        self.reconstruction_methods = {
            'bytecode_assembly': self._bytecode_assembly_method,
            'ast_reconstruction': self._ast_reconstruction_method,
            'string_concatenation': self._string_concatenation_method,
            'function_composition': self._function_composition_method,
            'dynamic_import': self._dynamic_import_method
        }
        
    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode code for runtime reconstruction
        """
        # Parse the code to understand its structure
        try:
            tree = ast.parse(data)
            code_structure = self._analyze_code_structure(tree)
        except SyntaxError:
            # Fallback for non-parseable code
            code_structure = {'type': 'raw_string', 'content': data}
            
        # Choose reconstruction method
        method = random.choice(list(self.reconstruction_methods.keys()))
        
        # Create reconstruction components
        reconstruction_data = self.reconstruction_methods[method](data, code_structure)
        
        # Generate runtime loader
        runtime_loader = self._generate_runtime_loader(reconstruction_data, method)
        
        # Create execution environment
        execution_env = self._create_execution_environment()
        
        # Encode everything
        encoded_data = base64.b64encode(json.dumps({
            'reconstruction_data': reconstruction_data,
            'runtime_loader': runtime_loader,
            'execution_env': execution_env
        }).encode()).decode()
        
        return {
            'encoded': encoded_data,
            'metadata': {
                'method': method,
                'original_length': len(data),
                'code_structure': code_structure,
                'reconstruction_complexity': len(reconstruction_data)
            }
        }
        
    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode and reconstruct the original code
        """
        # Decode the data
        runtime_data = json.loads(base64.b64decode(encoded_data.encode()).decode())
        
        # Extract components
        reconstruction_data = runtime_data['reconstruction_data']
        method = metadata['method']
        
        # Reconstruct the original code
        original_code = self._reconstruct_code(reconstruction_data, method)
        
        return original_code
        
    def _analyze_code_structure(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze the structure of the Python code"""
        structure = {
            'imports': [],
            'functions': [],
            'classes': [],
            'variables': [],
            'statements': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    structure['imports'].append({
                        'type': 'import',
                        'name': alias.name,
                        'asname': alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    structure['imports'].append({
                        'type': 'from_import',
                        'module': node.module,
                        'name': alias.name,
                        'asname': alias.asname
                    })
            elif isinstance(node, ast.FunctionDef):
                structure['functions'].append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'lineno': node.lineno
                })
            elif isinstance(node, ast.ClassDef):
                structure['classes'].append({
                    'name': node.name,
                    'bases': [base.id if isinstance(base, ast.Name) else str(base) 
                             for base in node.bases],
                    'lineno': node.lineno
                })
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        structure['variables'].append({
                            'name': target.id,
                            'lineno': node.lineno
                        })
                        
        return structure
        
    def _bytecode_assembly_method(self, code: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Create bytecode assembly reconstruction"""
        # Compile code to bytecode
        compiled_code = compile(code, '<string>', 'exec')
        
        # Extract bytecode information
        bytecode_data = {
            'code_object': {
                'co_code': list(compiled_code.co_code),
                'co_names': compiled_code.co_names,
                'co_varnames': compiled_code.co_varnames,
                'co_consts': [self._serialize_const(const) for const in compiled_code.co_consts],
                'co_filename': compiled_code.co_filename,
                'co_name': compiled_code.co_name,
                'co_firstlineno': compiled_code.co_firstlineno,
                'co_lnotab': list(compiled_code.co_lnotab),
                'co_flags': compiled_code.co_flags,
                'co_argcount': compiled_code.co_argcount,
                'co_nlocals': compiled_code.co_nlocals,
                'co_stacksize': compiled_code.co_stacksize
            }
        }
        
        # Create reconstruction instructions
        reconstruction_steps = [
            'import types',
            'import marshal',
            f'_code_data = {bytecode_data}',
            '_co = _code_data["code_object"]',
            '_code_obj = types.CodeType(',
            '    _co["co_argcount"],',
            '    _co["co_nlocals"],', 
            '    _co["co_stacksize"],',
            '    _co["co_flags"],',
            '    bytes(_co["co_code"]),',
            '    tuple(_co["co_consts"]),',
            '    _co["co_names"],',
            '    _co["co_varnames"],',
            '    _co["co_filename"],',
            '    _co["co_name"],',
            '    _co["co_firstlineno"],',
            '    bytes(_co["co_lnotab"])',
            ')',
            'exec(_code_obj)'
        ]
        
        return {
            'method': 'bytecode_assembly',
            'data': bytecode_data,
            'reconstruction_steps': reconstruction_steps
        }
        
    def _ast_reconstruction_method(self, code: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Create AST-based reconstruction"""
        # Parse code into AST
        tree = ast.parse(code)
        
        # Serialize AST nodes
        ast_data = self._serialize_ast(tree)
        
        # Create reconstruction steps
        reconstruction_steps = [
            'import ast',
            f'_ast_data = {ast_data}',
            '_tree = _deserialize_ast(_ast_data)',
            '_code = compile(_tree, "<reconstructed>", "exec")',
            'exec(_code)'
        ]
        
        # Add deserializer function
        deserializer_code = '''
def _deserialize_ast(data):
    if isinstance(data, dict):
        node_type = getattr(ast, data['_type'])
        node = node_type()
        for key, value in data.items():
            if key != '_type':
                if isinstance(value, list):
                    setattr(node, key, [_deserialize_ast(item) for item in value])
                elif isinstance(value, dict) and '_type' in value:
                    setattr(node, key, _deserialize_ast(value))
                else:
                    setattr(node, key, value)
        return node
    return data
'''
        
        return {
            'method': 'ast_reconstruction',
            'data': ast_data,
            'reconstruction_steps': reconstruction_steps,
            'deserializer': deserializer_code
        }
        
    def _string_concatenation_method(self, code: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Create string concatenation reconstruction"""
        # Split code into chunks
        chunk_size = random.randint(10, 50)
        chunks = [code[i:i+chunk_size] for i in range(0, len(code), chunk_size)]
        
        # Encode chunks with different methods
        encoded_chunks = []
        for i, chunk in enumerate(chunks):
            if i % 3 == 0:
                # Base64 encoding
                encoded_chunks.append({
                    'type': 'base64',
                    'data': base64.b64encode(chunk.encode()).decode()
                })
            elif i % 3 == 1:
                # Character code encoding
                encoded_chunks.append({
                    'type': 'charcode',
                    'data': [ord(c) for c in chunk]
                })
            else:
                # XOR encoding
                key = random.randint(1, 255)
                encoded_chunks.append({
                    'type': 'xor',
                    'data': [ord(c) ^ key for c in chunk],
                    'key': key
                })
                
        # Create reconstruction steps
        reconstruction_steps = [
            'import base64',
            f'_chunks = {encoded_chunks}',
            '_code_parts = []',
            'for chunk in _chunks:',
            '    if chunk["type"] == "base64":',
            '        _code_parts.append(base64.b64decode(chunk["data"]).decode())',
            '    elif chunk["type"] == "charcode":',
            '        _code_parts.append("".join(chr(c) for c in chunk["data"]))',
            '    elif chunk["type"] == "xor":',
            '        _code_parts.append("".join(chr(c ^ chunk["key"]) for c in chunk["data"]))',
            '_reconstructed_code = "".join(_code_parts)',
            'exec(_reconstructed_code)'
        ]
        
        return {
            'method': 'string_concatenation',
            'data': encoded_chunks,
            'reconstruction_steps': reconstruction_steps
        }
        
    def _function_composition_method(self, code: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Create function composition reconstruction"""
        # Break code into logical components
        components = self._break_into_components(code, structure)
        
        # Create function generators
        function_generators = []
        for i, component in enumerate(components):
            func_name = f'_gen_{i}'
            encoded_component = base64.b64encode(component.encode()).decode()
            
            function_generators.append({
                'name': func_name,
                'encoded_data': encoded_component,
                'dependencies': []  # Could add dependency analysis
            })
            
        # Create reconstruction steps
        reconstruction_steps = [
            'import base64',
            f'_generators = {function_generators}',
            '_components = []',
            'for gen in _generators:',
            '    _components.append(base64.b64decode(gen["encoded_data"]).decode())',
            '_final_code = "\\n".join(_components)',
            'exec(_final_code)'
        ]
        
        return {
            'method': 'function_composition',
            'data': function_generators,
            'reconstruction_steps': reconstruction_steps
        }
        
    def _dynamic_import_method(self, code: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Create dynamic import reconstruction"""
        # Create a fake module structure
        module_data = {
            'module_name': f'_temp_module_{random.randint(1000, 9999)}',
            'code_content': base64.b64encode(code.encode()).decode(),
            'imports': structure.get('imports', [])
        }
        
        # Create reconstruction steps
        reconstruction_steps = [
            'import base64',
            'import types',
            'import sys',
            f'_module_data = {module_data}',
            '_module_name = _module_data["module_name"]',
            '_code_content = base64.b64decode(_module_data["code_content"]).decode()',
            '_module = types.ModuleType(_module_name)',
            'exec(_code_content, _module.__dict__)',
            'sys.modules[_module_name] = _module',
            'exec(_code_content)'
        ]
        
        return {
            'method': 'dynamic_import',
            'data': module_data,
            'reconstruction_steps': reconstruction_steps
        }
        
    def _generate_runtime_loader(self, reconstruction_data: Dict[str, Any], method: str) -> str:
        """Generate the runtime loader code"""
        loader_template = f'''
# Runtime Loader - Method: {method}
def _load_and_execute():
    {chr(10).join("    " + step for step in reconstruction_data['reconstruction_steps'])}

# Additional helper functions
{reconstruction_data.get('deserializer', '')}

# Execute the loader
_load_and_execute()
'''
        return loader_template
        
    def _create_execution_environment(self) -> Dict[str, Any]:
        """Create execution environment metadata"""
        return {
            'python_version': '3.8+',
            'required_modules': ['base64', 'ast', 'types', 'sys'],
            'execution_order': 'sequential',
            'cleanup_required': True
        }
        
    def _serialize_const(self, const):
        """Serialize constants for bytecode reconstruction"""
        if const is None:
            return None
        elif isinstance(const, (int, float, str, bool)):
            return const
        elif isinstance(const, (list, tuple)):
            return [self._serialize_const(item) for item in const]
        else:
            return str(const)
            
    def _serialize_ast(self, node):
        """Serialize AST node to dictionary"""
        if isinstance(node, ast.AST):
            result = {'_type': node.__class__.__name__}
            for field, value in ast.iter_fields(node):
                if isinstance(value, list):
                    result[field] = [self._serialize_ast(item) for item in value]
                elif isinstance(value, ast.AST):
                    result[field] = self._serialize_ast(value)
                else:
                    result[field] = value
            return result
        return node
        
    def _break_into_components(self, code: str, structure: Dict[str, Any]) -> List[str]:
        """Break code into logical components"""
        lines = code.split('\n')
        components = []
        current_component = []
        
        for line in lines:
            current_component.append(line)
            
            # Break on function/class definitions or after certain statements
            if (line.strip().startswith(('def ', 'class ')) or 
                line.strip().endswith(':') or
                len(current_component) > 10):
                
                if current_component:
                    components.append('\n'.join(current_component))
                    current_component = []
                    
        # Add remaining lines
        if current_component:
            components.append('\n'.join(current_component))
            
        return components
        
    def _reconstruct_code(self, reconstruction_data: Dict[str, Any], method: str) -> str:
        """Reconstruct the original code from reconstruction data"""
        if method == 'string_concatenation':
            chunks = reconstruction_data['data']
            code_parts = []
            
            for chunk in chunks:
                if chunk['type'] == 'base64':
                    code_parts.append(base64.b64decode(chunk['data']).decode())
                elif chunk['type'] == 'charcode':
                    code_parts.append(''.join(chr(c) for c in chunk['data']))
                elif chunk['type'] == 'xor':
                    code_parts.append(''.join(chr(c ^ chunk['key']) for c in chunk['data']))
                    
            return ''.join(code_parts)
            
        elif method == 'function_composition':
            generators = reconstruction_data['data']
            components = []
            
            for gen in generators:
                components.append(base64.b64decode(gen['encoded_data']).decode())
                
            return '\n'.join(components)
            
        elif method == 'dynamic_import':
            module_data = reconstruction_data['data']
            return base64.b64decode(module_data['code_content']).decode()
            
        # For other methods, return a placeholder
        return "# Reconstruction method not implemented for decode"
