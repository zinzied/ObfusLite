"""
GUI interface for PyObfuscator

Provides a user-friendly graphical interface for code obfuscation.
"""

import sys
import json
from typing import Optional

try:
    from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                                QTextEdit, QComboBox, QPushButton, QLabel, QSpinBox,
                                QCheckBox, QTabWidget, QFileDialog, QMessageBox,
                                QProgressBar, QGroupBox)
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False

from . import Obfuscator, get_available_techniques, get_fast_techniques, __version__

if PYQT_AVAILABLE:
    class ObfuscationWorker(QThread):
        """Worker thread for obfuscation to prevent GUI freezing"""
        finished = pyqtSignal(dict)
        error = pyqtSignal(str)
        progress = pyqtSignal(int)
        
        def __init__(self, code, technique, layers, seed, performance_mode='balanced'):
            super().__init__()
            self.code = code
            self.technique = technique
            self.layers = layers
            self.seed = seed
            self.performance_mode = performance_mode
            
        def run(self):
            try:
                # Initialize obfuscator
                obfuscator = Obfuscator()
                
                self.progress.emit(25)
                
                # Perform obfuscation
                result = obfuscator.obfuscate(
                    self.code, 
                    technique=self.technique, 
                    layers=self.layers, 
                    seed=self.seed
                )
                
                self.progress.emit(80)
                
                # Generate standalone executable code
                standalone_code = obfuscator.create_standalone_file(result)
                result['standalone_code'] = standalone_code
                
                self.progress.emit(100)
                self.finished.emit(result)
                
            except Exception as e:
                self.error.emit(str(e))

    class ObfuscatorGUI(QWidget):
        """Main GUI application for PyObfuscator"""
        
        def __init__(self):
            super().__init__()
            self.obfuscation_result = None
            self.initUI()

        def initUI(self):
            self.setWindowTitle(f"PyObfuscator v{__version__} - Advanced Python Code Obfuscation")
            self.setGeometry(100, 100, 1000, 700)

            # Create main layout
            main_layout = QVBoxLayout()
            
            # Create tab widget
            self.tab_widget = QTabWidget()
            
            # Create tabs
            self.create_obfuscation_tab()
            self.create_deobfuscation_tab()
            self.create_settings_tab()
            
            main_layout.addWidget(self.tab_widget)
            self.setLayout(main_layout)

        def create_obfuscation_tab(self):
            """Create the main obfuscation tab"""
            obfuscation_widget = QWidget()
            layout = QVBoxLayout()

            # Input section
            input_group = QGroupBox("Input Code")
            input_layout = QVBoxLayout()
            
            # File operations
            file_layout = QHBoxLayout()
            self.load_file_button = QPushButton("Load from File")
            self.load_file_button.clicked.connect(self.load_file)
            self.save_input_button = QPushButton("Save Input")
            self.save_input_button.clicked.connect(self.save_input)
            file_layout.addWidget(self.load_file_button)
            file_layout.addWidget(self.save_input_button)
            file_layout.addStretch()
            input_layout.addLayout(file_layout)
            
            self.code_entry = QTextEdit()
            self.code_entry.setPlaceholderText("Enter your Python code here...")
            input_layout.addWidget(self.code_entry)
            input_group.setLayout(input_layout)
            layout.addWidget(input_group)

            # Configuration section
            config_group = QGroupBox("Obfuscation Configuration")
            config_layout = QVBoxLayout()
            
            # Performance mode selection
            perf_layout = QHBoxLayout()
            perf_layout.addWidget(QLabel("Performance Mode:"))
            self.performance_combo = QComboBox()
            self.performance_combo.addItems(["fast", "balanced", "full"])
            self.performance_combo.setCurrentText("fast")
            self.performance_combo.currentTextChanged.connect(self.update_technique_list)
            perf_layout.addWidget(self.performance_combo)
            perf_layout.addStretch()
            config_layout.addLayout(perf_layout)
            
            # Technique selection
            technique_layout = QHBoxLayout()
            technique_layout.addWidget(QLabel("Obfuscation Technique:"))
            self.technique_combo = QComboBox()
            self.update_technique_list()  # Initialize with default techniques
            technique_layout.addWidget(self.technique_combo)
            technique_layout.addStretch()
            config_layout.addLayout(technique_layout)
            
            # Layers and seed
            params_layout = QHBoxLayout()
            params_layout.addWidget(QLabel("Layers:"))
            self.layers_spinbox = QSpinBox()
            self.layers_spinbox.setRange(1, 10)
            self.layers_spinbox.setValue(2)
            params_layout.addWidget(self.layers_spinbox)
            
            params_layout.addWidget(QLabel("Seed:"))
            self.seed_spinbox = QSpinBox()
            self.seed_spinbox.setRange(0, 999999)
            self.seed_spinbox.setValue(12345)
            params_layout.addWidget(self.seed_spinbox)
            
            self.use_random_seed = QCheckBox("Use Random Seed")
            params_layout.addWidget(self.use_random_seed)
            params_layout.addStretch()
            config_layout.addLayout(params_layout)
            
            config_group.setLayout(config_layout)
            layout.addWidget(config_group)

            # Generate button and progress
            self.generate_button = QPushButton("Generate Obfuscated Code")
            self.generate_button.clicked.connect(self.generate_obfuscated_code)
            layout.addWidget(self.generate_button)
            
            self.progress_bar = QProgressBar()
            self.progress_bar.setVisible(False)
            layout.addWidget(self.progress_bar)

            # Output section
            output_group = QGroupBox("Obfuscated Output")
            output_layout = QVBoxLayout()
            
            # Output tabs
            self.output_tabs = QTabWidget()
            
            # Obfuscated data tab
            self.obfuscated_data_text = QTextEdit()
            self.obfuscated_data_text.setReadOnly(True)
            self.output_tabs.addTab(self.obfuscated_data_text, "Obfuscated Data")
            
            # Standalone code tab
            self.standalone_code_text = QTextEdit()
            self.standalone_code_text.setReadOnly(True)
            self.output_tabs.addTab(self.standalone_code_text, "Standalone Code")
            
            # Metadata tab
            self.metadata_text = QTextEdit()
            self.metadata_text.setReadOnly(True)
            self.output_tabs.addTab(self.metadata_text, "Metadata")
            
            output_layout.addWidget(self.output_tabs)
            
            # Save buttons
            save_layout = QHBoxLayout()
            self.save_obfuscated_button = QPushButton("Save Obfuscated Data")
            self.save_obfuscated_button.clicked.connect(self.save_obfuscated)
            self.save_standalone_button = QPushButton("Save Standalone Code")
            self.save_standalone_button.clicked.connect(self.save_standalone)
            save_layout.addWidget(self.save_obfuscated_button)
            save_layout.addWidget(self.save_standalone_button)
            save_layout.addStretch()
            output_layout.addLayout(save_layout)
            
            output_group.setLayout(output_layout)
            layout.addWidget(output_group)

            obfuscation_widget.setLayout(layout)
            self.tab_widget.addTab(obfuscation_widget, "Obfuscation")

        def create_deobfuscation_tab(self):
            """Create the deobfuscation tab"""
            deobfuscation_widget = QWidget()
            layout = QVBoxLayout()

            # Input section
            input_group = QGroupBox("Obfuscated Data Input")
            input_layout = QVBoxLayout()
            
            # File operations
            file_layout = QHBoxLayout()
            self.load_obfuscated_button = QPushButton("Load Obfuscated File")
            self.load_obfuscated_button.clicked.connect(self.load_obfuscated_file)
            file_layout.addWidget(self.load_obfuscated_button)
            file_layout.addStretch()
            input_layout.addLayout(file_layout)
            
            self.obfuscated_input = QTextEdit()
            self.obfuscated_input.setPlaceholderText("Paste obfuscated data here...")
            input_layout.addWidget(self.obfuscated_input)
            input_group.setLayout(input_layout)
            layout.addWidget(input_group)

            # Deobfuscate button
            self.deobfuscate_button = QPushButton("Deobfuscate Code")
            self.deobfuscate_button.clicked.connect(self.deobfuscate_code)
            layout.addWidget(self.deobfuscate_button)

            # Output section
            output_group = QGroupBox("Deobfuscated Output")
            output_layout = QVBoxLayout()
            
            self.deobfuscated_output = QTextEdit()
            self.deobfuscated_output.setReadOnly(True)
            output_layout.addWidget(self.deobfuscated_output)
            
            # Save button
            self.save_deobfuscated_button = QPushButton("Save Deobfuscated Code")
            self.save_deobfuscated_button.clicked.connect(self.save_deobfuscated)
            output_layout.addWidget(self.save_deobfuscated_button)
            
            output_group.setLayout(output_layout)
            layout.addWidget(output_group)

            deobfuscation_widget.setLayout(layout)
            self.tab_widget.addTab(deobfuscation_widget, "Deobfuscation")

        def create_settings_tab(self):
            """Create the settings tab"""
            settings_widget = QWidget()
            layout = QVBoxLayout()

            # Technique descriptions
            desc_group = QGroupBox("Available Techniques")
            desc_layout = QVBoxLayout()
            
            from .encoders import get_technique_info
            technique_info = get_technique_info()
            
            for technique, info in technique_info.items():
                desc_layout.addWidget(QLabel(
                    f"<b>{technique}:</b> {info.get('description', 'No description')}"
                ))
                
            desc_group.setLayout(desc_layout)
            layout.addWidget(desc_group)

            layout.addStretch()
            settings_widget.setLayout(layout)
            self.tab_widget.addTab(settings_widget, "Settings")

        def update_technique_list(self):
            """Update available techniques based on performance mode"""
            performance_mode = self.performance_combo.currentText()
            
            # Clear current items
            self.technique_combo.clear()
            
            if performance_mode == 'fast':
                techniques = get_fast_techniques()
            elif performance_mode == 'balanced':
                techniques = get_fast_techniques() + ['dna', 'steganographic']
            else:  # 'full'
                techniques = get_available_techniques()
            
            self.technique_combo.addItems(techniques)
            
            # Set default to a fast technique
            if 'fast_xor' in techniques:
                self.technique_combo.setCurrentText('fast_xor')

        def generate_obfuscated_code(self):
            """Generate obfuscated code using selected technique"""
            code = self.code_entry.toPlainText().strip()
            if not code:
                QMessageBox.warning(self, "Warning", "Please enter some Python code to obfuscate.")
                return

            technique = self.technique_combo.currentText()
            layers = self.layers_spinbox.value()
            seed = None if self.use_random_seed.isChecked() else self.seed_spinbox.value()
            performance_mode = self.performance_combo.currentText()

            # Limit layers for fast mode
            if performance_mode == 'fast' and layers > 3:
                layers = 3
                QMessageBox.information(self, "Info", "Layer count limited to 3 for fast mode.")

            # Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.generate_button.setEnabled(False)

            # Start obfuscation in worker thread
            self.worker = ObfuscationWorker(code, technique, layers, seed, performance_mode)
            self.worker.finished.connect(self.on_obfuscation_finished)
            self.worker.error.connect(self.on_obfuscation_error)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()

        def on_obfuscation_finished(self, result):
            """Handle obfuscation completion"""
            self.obfuscation_result = result
            
            # Display results
            self.obfuscated_data_text.setText(json.dumps(result, indent=2, default=str))
            self.standalone_code_text.setText(result.get('standalone_code', ''))
            
            # Display metadata
            metadata = {
                'technique': result.get('technique'),
                'layers': result.get('layers'),
                'obfuscation_id': result.get('obfuscation_id'),
                'original_size': result.get('original_size'),
                'obfuscated_size': result.get('obfuscated_size'),
                'compression_ratio': f"{(1 - result.get('obfuscated_size', 0) / max(result.get('original_size', 1), 1)) * 100:.2f}%"
            }
            self.metadata_text.setText(json.dumps(metadata, indent=2))
            
            # Hide progress bar and re-enable button
            self.progress_bar.setVisible(False)
            self.generate_button.setEnabled(True)
            
            QMessageBox.information(self, "Success", "Code obfuscated successfully!")

        def on_obfuscation_error(self, error_msg):
            """Handle obfuscation error"""
            self.progress_bar.setVisible(False)
            self.generate_button.setEnabled(True)
            QMessageBox.critical(self, "Error", f"Obfuscation failed: {error_msg}")

        def deobfuscate_code(self):
            """Deobfuscate the input data"""
            obfuscated_data = self.obfuscated_input.toPlainText().strip()
            if not obfuscated_data:
                QMessageBox.warning(self, "Warning", "Please enter obfuscated data to deobfuscate.")
                return

            try:
                # Parse obfuscated data
                data = json.loads(obfuscated_data)
                
                # Deobfuscate
                obfuscator = Obfuscator()
                original_code = obfuscator.deobfuscate(data)
                
                # Display result
                self.deobfuscated_output.setText(original_code)
                
                QMessageBox.information(self, "Success", "Code deobfuscated successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Deobfuscation failed: {str(e)}")

        # File operation methods (load_file, save_input, etc.) would go here
        # For brevity, I'll add them in the next part

        def load_file(self):
            """Load Python file"""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Load Python File", "", "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.code_entry.setText(f.read())
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

        def save_input(self):
            """Save input code"""
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Input Code", "", "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.code_entry.toPlainText())
                    QMessageBox.information(self, "Success", "Input code saved successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

        def save_obfuscated(self):
            """Save obfuscated data"""
            if not self.obfuscation_result:
                QMessageBox.warning(self, "Warning", "No obfuscated data to save.")
                return
                
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Obfuscated Data", "", "JSON Files (*.json);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.obfuscation_result, f, indent=2, default=str)
                    QMessageBox.information(self, "Success", "Obfuscated data saved successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

        def save_standalone(self):
            """Save standalone executable code"""
            if not self.obfuscation_result or 'standalone_code' not in self.obfuscation_result:
                QMessageBox.warning(self, "Warning", "No standalone code to save.")
                return
                
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Standalone Code", "", "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.obfuscation_result['standalone_code'])
                    QMessageBox.information(self, "Success", "Standalone code saved successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

        def load_obfuscated_file(self):
            """Load obfuscated data file"""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Load Obfuscated File", "", "JSON Files (*.json);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.obfuscated_input.setText(f.read())
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

        def save_deobfuscated(self):
            """Save deobfuscated code"""
            code = self.deobfuscated_output.toPlainText().strip()
            if not code:
                QMessageBox.warning(self, "Warning", "No deobfuscated code to save.")
                return
                
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Deobfuscated Code", "", "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(code)
                    QMessageBox.information(self, "Success", "Deobfuscated code saved successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

def main() -> int:
    """Main entry point for the GUI"""
    
    if not PYQT_AVAILABLE:
        print("Error: PyQt6 is required for the GUI interface.", file=sys.stderr)
        print("Install with: pip install PyQt6", file=sys.stderr)
        return 1
        
    app = QApplication(sys.argv)
    window = ObfuscatorGUI()
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
