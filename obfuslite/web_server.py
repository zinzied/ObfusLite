"""
Web Server for ObfusLite GUI

Provides a Flask-based web interface for ObfusLite obfuscation functionality.
"""

import os
import json
import tempfile
import subprocess
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from . import Obfuscator, get_available_techniques, get_fast_techniques, __version__


class ObfusLiteWebServer:
    """Web server for ObfusLite GUI"""
    
    def __init__(self, host='127.0.0.1', port=5000, debug=False):
        if not FLASK_AVAILABLE:
            raise ImportError("Flask is required for the web interface. Install with: pip install flask flask-cors")
        
        self.host = host
        self.port = port
        self.debug = debug
        # Get the directory where this module is located
        module_dir = os.path.dirname(os.path.abspath(__file__))
        self.web_dir = os.path.join(module_dir, 'web')

        self.app = Flask(__name__,
                        static_folder=self.web_dir,
                        static_url_path='')

        # Enable CORS for development
        CORS(self.app)

        # Configure Flask
        self.app.config['SECRET_KEY'] = 'obfuslite-web-interface'
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        def index():
            """Serve the main interface"""
            try:
                return send_from_directory(self.web_dir, 'index.html')
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Could not serve index.html: {str(e)}'
                }), 500

        @self.app.route('/<path:filename>')
        def static_files(filename):
            """Serve static files"""
            try:
                return send_from_directory(self.web_dir, filename)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'File not found: {filename}'
                }), 404
        
        @self.app.route('/api/techniques')
        def get_techniques():
            """Get available obfuscation techniques"""
            try:
                return jsonify({
                    'success': True,
                    'techniques': {
                        'fast': get_fast_techniques(),
                        'all': get_available_techniques()
                    }
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/obfuscate', methods=['POST'])
        def obfuscate_code():
            """Handle obfuscation requests"""
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({
                        'success': False,
                        'error': 'No data provided'
                    }), 400
                
                # Extract configuration
                config = self.extract_config(data)
                
                # Validate input
                validation_error = self.validate_config(config)
                if validation_error:
                    return jsonify({
                        'success': False,
                        'error': validation_error
                    }), 400
                
                # Perform obfuscation
                result = self.perform_obfuscation(config)
                
                return jsonify(result)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Obfuscation failed: {str(e)}'
                }), 500
        
        @self.app.route('/api/open-folder', methods=['POST'])
        def open_folder():
            """Open output folder in file explorer"""
            try:
                data = request.get_json()
                folder_path = data.get('path')
                
                if not folder_path or not os.path.exists(folder_path):
                    return jsonify({
                        'success': False,
                        'error': 'Invalid folder path'
                    }), 400
                
                # Open folder in file explorer
                self.open_file_explorer(folder_path)
                
                return jsonify({
                    'success': True,
                    'message': 'Folder opened successfully'
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/version')
        def get_version():
            """Get ObfusLite version information"""
            return jsonify({
                'success': True,
                'version': __version__,
                'techniques_count': len(get_available_techniques())
            })
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors"""
            return jsonify({
                'success': False,
                'error': 'Endpoint not found'
            }), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 errors"""
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
    
    def extract_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and normalize configuration from request data"""
        return {
            'script_location': data.get('scriptLocation', '').strip(),
            'code_input': data.get('codeInput', '').strip(),
            'technique': data.get('technique', 'fast_xor'),
            'layers': max(1, min(10, int(data.get('layers', 2)))),
            'seed': data.get('seed') if not data.get('randomSeed', False) else None,
            'performance_mode': data.get('performanceMode', 'fast'),
            'output_directory': data.get('outputDirectory', '').strip(),
            'create_standalone': data.get('createStandalone', True),
            'backup_original': data.get('backupOriginal', True),
            'debug_mode': data.get('debugMode', False),
            'custom_options': data.get('customOptions', '').strip()
        }
    
    def validate_config(self, config: Dict[str, Any]) -> Optional[str]:
        """Validate configuration and return error message if invalid"""
        
        # Check if we have input
        if not config['script_location'] and not config['code_input']:
            return 'Please provide either a script file or paste code to obfuscate'
        
        # Check if script file exists
        if config['script_location'] and not os.path.exists(config['script_location']):
            return f'Script file not found: {config["script_location"]}'
        
        # Check technique
        available_techniques = get_available_techniques()
        if config['technique'] not in available_techniques:
            return f'Invalid technique: {config["technique"]}'
        
        # Check performance mode limits
        if config['performance_mode'] == 'fast' and config['layers'] > 3:
            config['layers'] = 3  # Auto-correct for fast mode
        
        return None
    
    def perform_obfuscation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the actual obfuscation"""
        try:
            # Initialize obfuscator
            obfuscator = Obfuscator()
            
            # Get code to obfuscate
            if config['script_location']:
                with open(config['script_location'], 'r', encoding='utf-8') as f:
                    code = f.read()
            else:
                code = config['code_input']
            
            # Perform obfuscation
            result = obfuscator.obfuscate(
                code,
                technique=config['technique'],
                layers=config['layers'],
                seed=config['seed']
            )
            
            # Generate standalone code if requested
            standalone_code = None
            if config['create_standalone']:
                standalone_code = obfuscator.create_standalone_file(result)
            
            # Save output files
            output_info = self.save_output_files(result, standalone_code, config)
            
            return {
                'success': True,
                'message': 'Obfuscation completed successfully!',
                'result': {
                    'technique': result.get('technique'),
                    'layers': result.get('layers'),
                    'original_size': result.get('original_size'),
                    'obfuscated_size': result.get('obfuscated_size'),
                    'compression_ratio': self.calculate_compression_ratio(
                        result.get('original_size', 0),
                        result.get('obfuscated_size', 0)
                    ),
                    'obfuscation_id': result.get('obfuscation_id')
                },
                'output_path': output_info['output_directory'],
                'files_created': output_info['files_created']
            }
            
        except Exception as e:
            raise Exception(f'Obfuscation process failed: {str(e)}')
    
    def save_output_files(self, result: Dict[str, Any], standalone_code: Optional[str], 
                         config: Dict[str, Any]) -> Dict[str, Any]:
        """Save obfuscation output files"""
        
        # Determine output directory
        if config['output_directory']:
            output_dir = config['output_directory']
        else:
            output_dir = os.path.join(os.getcwd(), 'obfuscated_output')
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate base filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"obfuscated_{timestamp}"
        
        files_created = []
        
        # Save obfuscated data (JSON)
        obfuscated_file = os.path.join(output_dir, f"{base_name}.json")
        with open(obfuscated_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        files_created.append(obfuscated_file)
        
        # Save standalone code if requested
        if standalone_code and config['create_standalone']:
            standalone_file = os.path.join(output_dir, f"{base_name}_standalone.py")
            with open(standalone_file, 'w', encoding='utf-8') as f:
                f.write(standalone_code)
            files_created.append(standalone_file)
        
        # Backup original file if requested and we have a script location
        if config['backup_original'] and config['script_location']:
            backup_file = os.path.join(output_dir, f"{base_name}_original.py")
            with open(config['script_location'], 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            files_created.append(backup_file)
        
        return {
            'output_directory': output_dir,
            'files_created': files_created
        }
    
    def calculate_compression_ratio(self, original_size: int, obfuscated_size: int) -> str:
        """Calculate compression ratio as percentage"""
        if original_size == 0:
            return "0.00%"
        
        ratio = (1 - obfuscated_size / original_size) * 100
        return f"{ratio:.2f}%"
    
    def open_file_explorer(self, path: str):
        """Open file explorer at the given path"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif os.name == 'posix':  # macOS and Linux
                if os.uname().sysname == 'Darwin':  # macOS
                    subprocess.run(['open', path])
                else:  # Linux
                    subprocess.run(['xdg-open', path])
        except Exception as e:
            print(f"Could not open file explorer: {e}")
    
    def run(self, open_browser=True):
        """Run the web server"""
        url = f"http://{self.host}:{self.port}"
        
        print(f"Starting ObfusLite Web Interface...")
        print(f"Server running at: {url}")
        print(f"Press Ctrl+C to stop the server")
        
        if open_browser:
            # Open browser after a short delay
            import threading
            import time
            
            def open_browser_delayed():
                time.sleep(1.5)  # Wait for server to start
                try:
                    webbrowser.open(url)
                except Exception as e:
                    print(f"Could not open browser automatically: {e}")
                    print(f"Please open {url} manually in your browser")
            
            threading.Thread(target=open_browser_delayed, daemon=True).start()
        
        try:
            self.app.run(host=self.host, port=self.port, debug=self.debug, threaded=True)
        except KeyboardInterrupt:
            print("\nShutting down ObfusLite Web Interface...")
        except Exception as e:
            print(f"Server error: {e}")


def start_web_interface(host='127.0.0.1', port=5000, debug=False, open_browser=True):
    """Start the ObfusLite web interface"""
    if not FLASK_AVAILABLE:
        print("Error: Flask is required for the web interface.")
        print("Install with: pip install flask flask-cors")
        return False
    
    try:
        server = ObfusLiteWebServer(host=host, port=port, debug=debug)
        server.run(open_browser=open_browser)
        return True
    except Exception as e:
        print(f"Failed to start web interface: {e}")
        return False


if __name__ == '__main__':
    start_web_interface()
