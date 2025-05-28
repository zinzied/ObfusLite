"""
GUI interface for ObfusLite

Provides a user-friendly graphical interface for code obfuscation with multi-file support.
"""

import sys
import json
import os
import time
import shutil
import zipfile
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                                QTextEdit, QComboBox, QPushButton, QLabel, QSpinBox,
                                QCheckBox, QTabWidget, QFileDialog, QMessageBox,
                                QProgressBar, QGroupBox, QListWidget, QListWidgetItem,
                                QSplitter, QTableWidget, QTableWidgetItem, QHeaderView,
                                QTreeWidget, QTreeWidgetItem, QScrollArea, QFrame,
                                QSlider, QDoubleSpinBox, QLineEdit, QTextBrowser,
                                QInputDialog)
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QPixmap, QIcon
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

    class BatchObfuscationWorker(QThread):
        """Worker thread for batch obfuscation of multiple files"""
        file_finished = pyqtSignal(str, dict)  # filename, result
        file_error = pyqtSignal(str, str)  # filename, error
        progress = pyqtSignal(int)
        status_update = pyqtSignal(str)

        def __init__(self, file_paths, technique, layers, seed, output_dir, performance_mode='balanced'):
            super().__init__()
            self.file_paths = file_paths
            self.technique = technique
            self.layers = layers
            self.seed = seed
            self.output_dir = output_dir
            self.performance_mode = performance_mode

        def run(self):
            try:
                obfuscator = Obfuscator()
                total_files = len(self.file_paths)

                for i, file_path in enumerate(self.file_paths):
                    try:
                        self.status_update.emit(f"Processing {os.path.basename(file_path)}...")

                        # Read file
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()

                        # Obfuscate
                        result = obfuscator.obfuscate(
                            code,
                            technique=self.technique,
                            layers=self.layers,
                            seed=self.seed
                        )

                        # Generate standalone code
                        standalone_code = obfuscator.create_standalone_file(result)
                        result['standalone_code'] = standalone_code
                        result['original_file'] = file_path

                        self.file_finished.emit(file_path, result)

                    except Exception as e:
                        self.file_error.emit(file_path, str(e))

                    # Update progress
                    progress = int((i + 1) / total_files * 100)
                    self.progress.emit(progress)

                self.status_update.emit("Batch processing completed!")

            except Exception as e:
                self.status_update.emit(f"Batch processing failed: {str(e)}")

    class CodeAnalysisWorker(QThread):
        """Worker thread for code analysis"""
        analysis_finished = pyqtSignal(dict)
        error = pyqtSignal(str)

        def __init__(self, code):
            super().__init__()
            self.code = code

        def run(self):
            try:
                import ast

                # Parse the code
                tree = ast.parse(self.code)

                # Analyze the code
                analysis = {
                    'lines': len(self.code.splitlines()),
                    'characters': len(self.code),
                    'functions': 0,
                    'classes': 0,
                    'imports': 0,
                    'complexity': 0
                }

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        analysis['functions'] += 1
                    elif isinstance(node, ast.ClassDef):
                        analysis['classes'] += 1
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        analysis['imports'] += 1
                    elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                        analysis['complexity'] += 1

                self.analysis_finished.emit(analysis)

            except Exception as e:
                self.error.emit(str(e))

    class ObfuscatorGUI(QWidget):
        """Main GUI application for ObfusLite"""

        def __init__(self):
            super().__init__()
            self.obfuscation_result = None
            self.batch_results = {}
            self.current_project = None
            self.templates = {}
            self.load_templates()
            self.initUI()

        def initUI(self):
            self.setWindowTitle(f"ObfusLite v{__version__} - Advanced Python Code Obfuscation Suite")
            self.setGeometry(100, 100, 1400, 900)

            # Create main layout
            main_layout = QVBoxLayout()

            # Create tab widget
            self.tab_widget = QTabWidget()

            # Create tabs
            self.create_obfuscation_tab()
            self.create_batch_processing_tab()
            self.create_project_management_tab()
            self.create_code_analysis_tab()
            self.create_comparison_tab()
            self.create_deobfuscation_tab()
            self.create_settings_tab()

            main_layout.addWidget(self.tab_widget)
            self.setLayout(main_layout)

        def load_templates(self):
            """Load saved obfuscation templates"""
            try:
                templates_file = Path.home() / '.obfuslite_templates.json'
                if templates_file.exists():
                    with open(templates_file, 'r') as f:
                        self.templates = json.load(f)
            except Exception:
                self.templates = {}

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

        def create_batch_processing_tab(self):
            """Create the batch processing tab for multiple files"""
            batch_widget = QWidget()
            layout = QVBoxLayout()

            # File selection section
            file_group = QGroupBox("File Selection")
            file_layout = QVBoxLayout()

            # File list and controls
            file_controls = QHBoxLayout()
            self.add_files_button = QPushButton("Add Files")
            self.add_files_button.clicked.connect(self.add_batch_files)
            self.add_directory_button = QPushButton("Add Directory")
            self.add_directory_button.clicked.connect(self.add_batch_directory)
            self.clear_files_button = QPushButton("Clear All")
            self.clear_files_button.clicked.connect(self.clear_batch_files)

            file_controls.addWidget(self.add_files_button)
            file_controls.addWidget(self.add_directory_button)
            file_controls.addWidget(self.clear_files_button)
            file_controls.addStretch()
            file_layout.addLayout(file_controls)

            # File list
            self.batch_file_list = QListWidget()
            self.batch_file_list.setMinimumHeight(150)
            file_layout.addWidget(self.batch_file_list)

            file_group.setLayout(file_layout)
            layout.addWidget(file_group)

            # Configuration section
            config_group = QGroupBox("Batch Configuration")
            config_layout = QVBoxLayout()

            # Template selection
            template_layout = QHBoxLayout()
            template_layout.addWidget(QLabel("Template:"))
            self.batch_template_combo = QComboBox()
            self.update_template_list()
            template_layout.addWidget(self.batch_template_combo)

            self.save_template_button = QPushButton("Save Current as Template")
            self.save_template_button.clicked.connect(self.save_current_template)
            template_layout.addWidget(self.save_template_button)
            template_layout.addStretch()
            config_layout.addLayout(template_layout)

            # Batch-specific settings
            batch_settings = QHBoxLayout()

            # Performance mode
            batch_settings.addWidget(QLabel("Performance:"))
            self.batch_performance_combo = QComboBox()
            self.batch_performance_combo.addItems(["fast", "balanced", "full"])
            self.batch_performance_combo.setCurrentText("fast")
            batch_settings.addWidget(self.batch_performance_combo)

            # Technique
            batch_settings.addWidget(QLabel("Technique:"))
            self.batch_technique_combo = QComboBox()
            self.batch_technique_combo.addItems(get_fast_techniques())
            batch_settings.addWidget(self.batch_technique_combo)

            # Layers
            batch_settings.addWidget(QLabel("Layers:"))
            self.batch_layers_spinbox = QSpinBox()
            self.batch_layers_spinbox.setRange(1, 5)
            self.batch_layers_spinbox.setValue(2)
            batch_settings.addWidget(self.batch_layers_spinbox)

            batch_settings.addStretch()
            config_layout.addLayout(batch_settings)

            # Output settings
            output_layout = QHBoxLayout()
            output_layout.addWidget(QLabel("Output Directory:"))
            self.batch_output_line = QLineEdit()
            self.batch_output_line.setPlaceholderText("Select output directory...")
            output_layout.addWidget(self.batch_output_line)

            self.batch_output_button = QPushButton("Browse")
            self.batch_output_button.clicked.connect(self.select_batch_output)
            output_layout.addWidget(self.batch_output_button)
            config_layout.addLayout(output_layout)

            # Options
            options_layout = QHBoxLayout()
            self.create_zip_checkbox = QCheckBox("Create ZIP archive")
            self.backup_originals_checkbox = QCheckBox("Backup original files")
            self.backup_originals_checkbox.setChecked(True)
            options_layout.addWidget(self.create_zip_checkbox)
            options_layout.addWidget(self.backup_originals_checkbox)
            options_layout.addStretch()
            config_layout.addLayout(options_layout)

            config_group.setLayout(config_layout)
            layout.addWidget(config_group)

            # Process button and progress
            self.batch_process_button = QPushButton("Process All Files")
            self.batch_process_button.clicked.connect(self.start_batch_processing)
            layout.addWidget(self.batch_process_button)

            self.batch_progress_bar = QProgressBar()
            self.batch_progress_bar.setVisible(False)
            layout.addWidget(self.batch_progress_bar)

            self.batch_status_label = QLabel("")
            layout.addWidget(self.batch_status_label)

            # Results section
            results_group = QGroupBox("Processing Results")
            results_layout = QVBoxLayout()

            self.batch_results_table = QTableWidget()
            self.batch_results_table.setColumnCount(4)
            self.batch_results_table.setHorizontalHeaderLabels(["File", "Status", "Original Size", "Obfuscated Size"])
            self.batch_results_table.horizontalHeader().setStretchLastSection(True)
            results_layout.addWidget(self.batch_results_table)

            # Export buttons
            export_layout = QHBoxLayout()
            self.export_batch_button = QPushButton("Export Results")
            self.export_batch_button.clicked.connect(self.export_batch_results)
            self.view_batch_log_button = QPushButton("View Log")
            self.view_batch_log_button.clicked.connect(self.view_batch_log)
            export_layout.addWidget(self.export_batch_button)
            export_layout.addWidget(self.view_batch_log_button)
            export_layout.addStretch()
            results_layout.addLayout(export_layout)

            results_group.setLayout(results_layout)
            layout.addWidget(results_group)

            batch_widget.setLayout(layout)
            self.tab_widget.addTab(batch_widget, "Batch Processing")

        def create_project_management_tab(self):
            """Create the project management tab"""
            project_widget = QWidget()
            layout = QVBoxLayout()

            # Project controls
            project_controls = QHBoxLayout()
            self.new_project_button = QPushButton("New Project")
            self.new_project_button.clicked.connect(self.new_project)
            self.load_project_button = QPushButton("Load Project")
            self.load_project_button.clicked.connect(self.load_project)
            self.save_project_button = QPushButton("Save Project")
            self.save_project_button.clicked.connect(self.save_project)

            project_controls.addWidget(self.new_project_button)
            project_controls.addWidget(self.load_project_button)
            project_controls.addWidget(self.save_project_button)
            project_controls.addStretch()
            layout.addLayout(project_controls)

            # Project info
            info_group = QGroupBox("Project Information")
            info_layout = QVBoxLayout()

            project_info_layout = QHBoxLayout()
            project_info_layout.addWidget(QLabel("Project Name:"))
            self.project_name_line = QLineEdit()
            project_info_layout.addWidget(self.project_name_line)

            project_info_layout.addWidget(QLabel("Description:"))
            self.project_desc_line = QLineEdit()
            project_info_layout.addWidget(self.project_desc_line)
            info_layout.addLayout(project_info_layout)

            info_group.setLayout(info_layout)
            layout.addWidget(info_group)

            # Project files tree
            files_group = QGroupBox("Project Files")
            files_layout = QVBoxLayout()

            self.project_tree = QTreeWidget()
            self.project_tree.setHeaderLabels(["File", "Status", "Last Modified"])
            files_layout.addWidget(self.project_tree)

            files_group.setLayout(files_layout)
            layout.addWidget(files_group)

            project_widget.setLayout(layout)
            self.tab_widget.addTab(project_widget, "Project Management")

        def create_code_analysis_tab(self):
            """Create the code analysis tab"""
            analysis_widget = QWidget()
            layout = QVBoxLayout()

            # Input section
            input_group = QGroupBox("Code Input")
            input_layout = QVBoxLayout()

            input_controls = QHBoxLayout()
            self.analysis_load_button = QPushButton("Load File")
            self.analysis_load_button.clicked.connect(self.load_analysis_file)
            self.analyze_button = QPushButton("Analyze Code")
            self.analyze_button.clicked.connect(self.analyze_code)
            input_controls.addWidget(self.analysis_load_button)
            input_controls.addWidget(self.analyze_button)
            input_controls.addStretch()
            input_layout.addLayout(input_controls)

            self.analysis_code_input = QTextEdit()
            self.analysis_code_input.setPlaceholderText("Enter Python code to analyze...")
            self.analysis_code_input.setMaximumHeight(200)
            input_layout.addWidget(self.analysis_code_input)

            input_group.setLayout(input_layout)
            layout.addWidget(input_group)

            # Analysis results
            results_group = QGroupBox("Analysis Results")
            results_layout = QHBoxLayout()

            # Metrics table
            metrics_layout = QVBoxLayout()
            metrics_layout.addWidget(QLabel("Code Metrics:"))
            self.metrics_table = QTableWidget()
            self.metrics_table.setColumnCount(2)
            self.metrics_table.setHorizontalHeaderLabels(["Metric", "Value"])
            self.metrics_table.horizontalHeader().setStretchLastSection(True)
            metrics_layout.addWidget(self.metrics_table)

            # Complexity chart placeholder
            complexity_layout = QVBoxLayout()
            complexity_layout.addWidget(QLabel("Complexity Analysis:"))
            self.complexity_text = QTextBrowser()
            self.complexity_text.setMaximumHeight(200)
            complexity_layout.addWidget(self.complexity_text)

            results_layout.addLayout(metrics_layout)
            results_layout.addLayout(complexity_layout)
            results_group.setLayout(results_layout)
            layout.addWidget(results_group)

            # Recommendations
            recommendations_group = QGroupBox("Obfuscation Recommendations")
            recommendations_layout = QVBoxLayout()
            self.recommendations_text = QTextBrowser()
            recommendations_layout.addWidget(self.recommendations_text)
            recommendations_group.setLayout(recommendations_layout)
            layout.addWidget(recommendations_group)

            analysis_widget.setLayout(layout)
            self.tab_widget.addTab(analysis_widget, "Code Analysis")

        def create_comparison_tab(self):
            """Create the comparison tab"""
            comparison_widget = QWidget()
            layout = QVBoxLayout()

            # Controls
            controls_layout = QHBoxLayout()
            self.load_original_button = QPushButton("Load Original")
            self.load_original_button.clicked.connect(self.load_original_for_comparison)
            self.load_obfuscated_button = QPushButton("Load Obfuscated")
            self.load_obfuscated_button.clicked.connect(self.load_obfuscated_for_comparison)
            self.compare_button = QPushButton("Compare")
            self.compare_button.clicked.connect(self.compare_codes)

            controls_layout.addWidget(self.load_original_button)
            controls_layout.addWidget(self.load_obfuscated_button)
            controls_layout.addWidget(self.compare_button)
            controls_layout.addStretch()
            layout.addLayout(controls_layout)

            # Comparison view
            comparison_splitter = QSplitter(Qt.Orientation.Horizontal)

            # Original code
            original_group = QGroupBox("Original Code")
            original_layout = QVBoxLayout()
            self.original_comparison_text = QTextEdit()
            self.original_comparison_text.setReadOnly(True)
            original_layout.addWidget(self.original_comparison_text)
            original_group.setLayout(original_layout)
            comparison_splitter.addWidget(original_group)

            # Obfuscated code
            obfuscated_group = QGroupBox("Obfuscated Code")
            obfuscated_layout = QVBoxLayout()
            self.obfuscated_comparison_text = QTextEdit()
            self.obfuscated_comparison_text.setReadOnly(True)
            obfuscated_layout.addWidget(self.obfuscated_comparison_text)
            obfuscated_group.setLayout(obfuscated_layout)
            comparison_splitter.addWidget(obfuscated_group)

            layout.addWidget(comparison_splitter)

            # Comparison statistics
            stats_group = QGroupBox("Comparison Statistics")
            stats_layout = QVBoxLayout()
            self.comparison_stats_table = QTableWidget()
            self.comparison_stats_table.setColumnCount(3)
            self.comparison_stats_table.setHorizontalHeaderLabels(["Metric", "Original", "Obfuscated"])
            self.comparison_stats_table.horizontalHeader().setStretchLastSection(True)
            self.comparison_stats_table.setMaximumHeight(150)
            stats_layout.addWidget(self.comparison_stats_table)
            stats_group.setLayout(stats_layout)
            layout.addWidget(stats_group)

            comparison_widget.setLayout(layout)
            self.tab_widget.addTab(comparison_widget, "Comparison")

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

        # Batch processing methods
        def add_batch_files(self):
            """Add files to batch processing list"""
            file_paths, _ = QFileDialog.getOpenFileNames(
                self, "Select Python Files", "", "Python Files (*.py);;All Files (*)"
            )
            for file_path in file_paths:
                if file_path not in [self.batch_file_list.item(i).text() for i in range(self.batch_file_list.count())]:
                    self.batch_file_list.addItem(file_path)

        def add_batch_directory(self):
            """Add all Python files from a directory"""
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
                for root, _, files in os.walk(directory):
                    for file in files:
                        if file.endswith('.py'):
                            file_path = os.path.join(root, file)
                            if file_path not in [self.batch_file_list.item(i).text() for i in range(self.batch_file_list.count())]:
                                self.batch_file_list.addItem(file_path)

        def clear_batch_files(self):
            """Clear all files from batch list"""
            self.batch_file_list.clear()

        def select_batch_output(self):
            """Select output directory for batch processing"""
            directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
            if directory:
                self.batch_output_line.setText(directory)

        def start_batch_processing(self):
            """Start batch processing of all files"""
            if self.batch_file_list.count() == 0:
                QMessageBox.warning(self, "Warning", "No files selected for processing.")
                return

            output_dir = self.batch_output_line.text().strip()
            if not output_dir:
                QMessageBox.warning(self, "Warning", "Please select an output directory.")
                return

            # Get settings
            technique = self.batch_technique_combo.currentText()
            layers = self.batch_layers_spinbox.value()
            seed = None  # Use random seed for batch processing
            performance_mode = self.batch_performance_combo.currentText()

            # Collect file paths
            file_paths = [self.batch_file_list.item(i).text() for i in range(self.batch_file_list.count())]

            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Show progress
            self.batch_progress_bar.setVisible(True)
            self.batch_progress_bar.setValue(0)
            self.batch_process_button.setEnabled(False)

            # Clear previous results
            self.batch_results_table.setRowCount(0)
            self.batch_results = {}

            # Start batch worker
            self.batch_worker = BatchObfuscationWorker(
                file_paths, technique, layers, seed, output_dir, performance_mode
            )
            self.batch_worker.file_finished.connect(self.on_batch_file_finished)
            self.batch_worker.file_error.connect(self.on_batch_file_error)
            self.batch_worker.progress.connect(self.batch_progress_bar.setValue)
            self.batch_worker.status_update.connect(self.batch_status_label.setText)
            self.batch_worker.finished.connect(self.on_batch_processing_finished)
            self.batch_worker.start()

        def on_batch_file_finished(self, file_path, result):
            """Handle completion of a single file in batch processing"""
            self.batch_results[file_path] = result

            # Add to results table
            row = self.batch_results_table.rowCount()
            self.batch_results_table.insertRow(row)

            self.batch_results_table.setItem(row, 0, QTableWidgetItem(os.path.basename(file_path)))
            self.batch_results_table.setItem(row, 1, QTableWidgetItem("Success"))
            self.batch_results_table.setItem(row, 2, QTableWidgetItem(str(result.get('original_size', 0))))
            self.batch_results_table.setItem(row, 3, QTableWidgetItem(str(result.get('obfuscated_size', 0))))

            # Save obfuscated files
            output_dir = self.batch_output_line.text()
            base_name = os.path.splitext(os.path.basename(file_path))[0]

            # Save obfuscated data
            obfuscated_file = os.path.join(output_dir, f"{base_name}_obfuscated.json")
            with open(obfuscated_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)

            # Save standalone code
            standalone_file = os.path.join(output_dir, f"{base_name}_standalone.py")
            with open(standalone_file, 'w') as f:
                f.write(result['standalone_code'])

        def on_batch_file_error(self, file_path, error):
            """Handle error in batch processing"""
            row = self.batch_results_table.rowCount()
            self.batch_results_table.insertRow(row)

            self.batch_results_table.setItem(row, 0, QTableWidgetItem(os.path.basename(file_path)))
            self.batch_results_table.setItem(row, 1, QTableWidgetItem(f"Error: {error}"))
            self.batch_results_table.setItem(row, 2, QTableWidgetItem("N/A"))
            self.batch_results_table.setItem(row, 3, QTableWidgetItem("N/A"))

        def on_batch_processing_finished(self):
            """Handle completion of batch processing"""
            self.batch_progress_bar.setVisible(False)
            self.batch_process_button.setEnabled(True)

            # Create ZIP if requested
            if self.create_zip_checkbox.isChecked():
                self.create_batch_zip()

            QMessageBox.information(self, "Success", "Batch processing completed!")

        def create_batch_zip(self):
            """Create ZIP archive of batch results"""
            output_dir = self.batch_output_line.text()
            zip_path = os.path.join(output_dir, f"obfuscated_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, _, files in os.walk(output_dir):
                    for file in files:
                        if file.endswith(('.py', '.json')):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, output_dir)
                            zipf.write(file_path, arcname)

        def export_batch_results(self):
            """Export batch processing results"""
            if not self.batch_results:
                QMessageBox.warning(self, "Warning", "No results to export.")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Batch Results", "", "JSON Files (*.json);;CSV Files (*.csv)"
            )
            if file_path:
                try:
                    if file_path.endswith('.csv'):
                        import csv
                        with open(file_path, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['File', 'Status', 'Original Size', 'Obfuscated Size', 'Technique', 'Layers'])
                            for i in range(self.batch_results_table.rowCount()):
                                row = [self.batch_results_table.item(i, j).text() for j in range(4)]
                                writer.writerow(row)
                    else:
                        with open(file_path, 'w') as f:
                            json.dump(self.batch_results, f, indent=2, default=str)
                    QMessageBox.information(self, "Success", "Results exported successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to export results: {str(e)}")

        def view_batch_log(self):
            """View detailed batch processing log"""
            log_dialog = QMessageBox(self)
            log_dialog.setWindowTitle("Batch Processing Log")
            log_dialog.setText("Detailed processing information:")

            log_text = ""
            for file_path, result in self.batch_results.items():
                log_text += f"File: {os.path.basename(file_path)}\n"
                log_text += f"  Technique: {result.get('technique', 'N/A')}\n"
                log_text += f"  Layers: {result.get('layers', 'N/A')}\n"
                log_text += f"  Original Size: {result.get('original_size', 'N/A')} bytes\n"
                log_text += f"  Obfuscated Size: {result.get('obfuscated_size', 'N/A')} bytes\n"
                log_text += f"  Compression Ratio: {((1 - result.get('obfuscated_size', 0) / max(result.get('original_size', 1), 1)) * 100):.2f}%\n\n"

            log_dialog.setDetailedText(log_text)
            log_dialog.exec()

        # Template management methods
        def update_template_list(self):
            """Update the template combo box"""
            self.batch_template_combo.clear()
            self.batch_template_combo.addItem("Default")
            for template_name in self.templates.keys():
                self.batch_template_combo.addItem(template_name)

        def save_current_template(self):
            """Save current settings as a template"""
            template_name, ok = QInputDialog.getText(self, "Save Template", "Template name:")
            if ok and template_name:
                template = {
                    'technique': self.batch_technique_combo.currentText(),
                    'layers': self.batch_layers_spinbox.value(),
                    'performance_mode': self.batch_performance_combo.currentText()
                }
                self.templates[template_name] = template
                self.save_templates()
                self.update_template_list()
                QMessageBox.information(self, "Success", f"Template '{template_name}' saved!")

        def save_templates(self):
            """Save templates to file"""
            try:
                templates_file = Path.home() / '.obfuslite_templates.json'
                with open(templates_file, 'w') as f:
                    json.dump(self.templates, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, "Warning", f"Failed to save templates: {str(e)}")

        # Code analysis methods
        def load_analysis_file(self):
            """Load file for code analysis"""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Load Python File for Analysis", "", "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.analysis_code_input.setText(f.read())
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

        def analyze_code(self):
            """Analyze the input code"""
            code = self.analysis_code_input.toPlainText().strip()
            if not code:
                QMessageBox.warning(self, "Warning", "Please enter code to analyze.")
                return

            # Start analysis worker
            self.analysis_worker = CodeAnalysisWorker(code)
            self.analysis_worker.analysis_finished.connect(self.on_analysis_finished)
            self.analysis_worker.error.connect(self.on_analysis_error)
            self.analysis_worker.start()

        def on_analysis_finished(self, analysis):
            """Handle analysis completion"""
            # Update metrics table
            self.metrics_table.setRowCount(len(analysis))
            for i, (metric, value) in enumerate(analysis.items()):
                self.metrics_table.setItem(i, 0, QTableWidgetItem(metric.replace('_', ' ').title()))
                self.metrics_table.setItem(i, 1, QTableWidgetItem(str(value)))

            # Update complexity analysis
            complexity_text = f"""
            <h3>Complexity Analysis</h3>
            <p><b>Cyclomatic Complexity:</b> {analysis['complexity']}</p>
            <p><b>Code Structure:</b></p>
            <ul>
                <li>Functions: {analysis['functions']}</li>
                <li>Classes: {analysis['classes']}</li>
                <li>Imports: {analysis['imports']}</li>
            </ul>
            """
            self.complexity_text.setHtml(complexity_text)

            # Generate recommendations
            recommendations = self.generate_obfuscation_recommendations(analysis)
            self.recommendations_text.setHtml(recommendations)

        def on_analysis_error(self, error):
            """Handle analysis error"""
            QMessageBox.critical(self, "Error", f"Analysis failed: {error}")

        def generate_obfuscation_recommendations(self, analysis):
            """Generate obfuscation recommendations based on code analysis"""
            recommendations = "<h3>Obfuscation Recommendations</h3>"

            if analysis['lines'] < 50:
                recommendations += "<p>✓ <b>Fast techniques</b> recommended for small code</p>"
            elif analysis['lines'] < 200:
                recommendations += "<p>✓ <b>Balanced techniques</b> recommended for medium code</p>"
            else:
                recommendations += "<p>✓ <b>Advanced techniques</b> recommended for large code</p>"

            if analysis['complexity'] > 10:
                recommendations += "<p>⚠ High complexity detected - consider multiple layers</p>"

            if analysis['functions'] > 5:
                recommendations += "<p>✓ Good for function-based obfuscation</p>"

            if analysis['classes'] > 0:
                recommendations += "<p>✓ Object-oriented structure detected</p>"

            return recommendations

        # Comparison methods
        def load_original_for_comparison(self):
            """Load original file for comparison"""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Load Original File", "", "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.original_comparison_text.setText(f.read())
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

        def load_obfuscated_for_comparison(self):
            """Load obfuscated file for comparison"""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Load Obfuscated File", "", "Python Files (*.py);;JSON Files (*.json);;All Files (*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if file_path.endswith('.json'):
                            # If it's a JSON file, extract the standalone code
                            data = json.loads(content)
                            if 'standalone_code' in data:
                                content = data['standalone_code']
                        self.obfuscated_comparison_text.setText(content)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

        def compare_codes(self):
            """Compare original and obfuscated code"""
            original = self.original_comparison_text.toPlainText()
            obfuscated = self.obfuscated_comparison_text.toPlainText()

            if not original or not obfuscated:
                QMessageBox.warning(self, "Warning", "Please load both original and obfuscated code.")
                return

            # Calculate statistics
            stats = [
                ("Lines", len(original.splitlines()), len(obfuscated.splitlines())),
                ("Characters", len(original), len(obfuscated)),
                ("Size Ratio", "1.0", f"{len(obfuscated) / len(original):.2f}"),
                ("Readability", "High", "Low")
            ]

            # Update comparison table
            self.comparison_stats_table.setRowCount(len(stats))
            for i, (metric, orig_val, obf_val) in enumerate(stats):
                self.comparison_stats_table.setItem(i, 0, QTableWidgetItem(metric))
                self.comparison_stats_table.setItem(i, 1, QTableWidgetItem(str(orig_val)))
                self.comparison_stats_table.setItem(i, 2, QTableWidgetItem(str(obf_val)))

        # Project management methods
        def new_project(self):
            """Create a new project"""
            self.current_project = {
                'name': '',
                'description': '',
                'files': [],
                'settings': {},
                'created': datetime.now().isoformat()
            }
            self.project_name_line.clear()
            self.project_desc_line.clear()
            self.project_tree.clear()

        def load_project(self):
            """Load an existing project"""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Load Project", "", "Project Files (*.pyobf);;JSON Files (*.json)"
            )
            if file_path:
                try:
                    with open(file_path, 'r') as f:
                        self.current_project = json.load(f)

                    self.project_name_line.setText(self.current_project.get('name', ''))
                    self.project_desc_line.setText(self.current_project.get('description', ''))
                    self.update_project_tree()

                    QMessageBox.information(self, "Success", "Project loaded successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load project: {str(e)}")

        def save_project(self):
            """Save the current project"""
            if not self.current_project:
                self.new_project()

            self.current_project['name'] = self.project_name_line.text()
            self.current_project['description'] = self.project_desc_line.text()

            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Project", "", "Project Files (*.pyobf);;JSON Files (*.json)"
            )
            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        json.dump(self.current_project, f, indent=2)
                    QMessageBox.information(self, "Success", "Project saved successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")

        def update_project_tree(self):
            """Update the project files tree"""
            self.project_tree.clear()
            if self.current_project and 'files' in self.current_project:
                for file_info in self.current_project['files']:
                    item = QTreeWidgetItem([
                        file_info.get('path', ''),
                        file_info.get('status', 'Unknown'),
                        file_info.get('modified', '')
                    ])
                    self.project_tree.addTopLevelItem(item)

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
