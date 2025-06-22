// ObfusLite Web Interface JavaScript

// Global variables
let currentConfig = {};
let isProcessing = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeInterface();
    setupEventListeners();
    updateCurrentCommand();
});

// Initialize interface
function initializeInterface() {
    // Expand all sections by default
    const sections = ['script-location', 'obfuscation-settings', 'output-settings'];
    sections.forEach(section => {
        const content = document.getElementById(section + '-content');
        const chevron = document.getElementById(section + '-chevron');
        if (content && chevron) {
            content.classList.remove('hidden');
            chevron.style.transform = 'rotate(180deg)';
        }
    });

    // Collapse advanced section by default
    const advancedContent = document.getElementById('advanced-content');
    const advancedChevron = document.getElementById('advanced-chevron');
    if (advancedContent && advancedChevron) {
        advancedContent.classList.add('hidden');
        advancedChevron.style.transform = 'rotate(0deg)';
    }

    // Load saved preferences
    loadPreferences();
}

// Setup event listeners
function setupEventListeners() {
    // File browser
    document.getElementById('file-browser').addEventListener('change', handleFileSelect);
    document.getElementById('directory-browser').addEventListener('change', handleDirectorySelect);

    // Form inputs
    const inputs = ['script-location', 'code-input', 'technique-select', 'layers-input', 
                   'seed-input', 'random-seed', 'performance-mode', 'output-directory',
                   'create-standalone', 'backup-original', 'custom-options', 'debug-mode'];
    
    inputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('change', updateCurrentCommand);
            element.addEventListener('input', updateCurrentCommand);
        }
    });

    // Performance mode change
    document.getElementById('performance-mode').addEventListener('change', updateTechniqueOptions);

    // Random seed checkbox
    document.getElementById('random-seed').addEventListener('change', toggleSeedInput);

    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

// Toggle section visibility
function toggleSection(sectionName) {
    const content = document.getElementById(sectionName + '-content');
    const chevron = document.getElementById(sectionName + '-chevron');
    const header = chevron.parentElement;
    
    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        chevron.style.transform = 'rotate(180deg)';
        header.classList.remove('collapsed');
    } else {
        content.classList.add('hidden');
        chevron.style.transform = 'rotate(0deg)';
        header.classList.add('collapsed');
    }
}

// Browse for file
function browseFile(targetId) {
    const fileBrowser = document.getElementById('file-browser');
    fileBrowser.onchange = function(e) {
        if (e.target.files.length > 0) {
            document.getElementById(targetId).value = e.target.files[0].path || e.target.files[0].name;
            updateCurrentCommand();
        }
    };
    fileBrowser.click();
}

// Browse for directory
function browseDirectory(targetId) {
    const dirBrowser = document.getElementById('directory-browser');
    dirBrowser.onchange = function(e) {
        if (e.target.files.length > 0) {
            const path = e.target.files[0].webkitRelativePath.split('/')[0];
            document.getElementById(targetId).value = path;
            updateCurrentCommand();
        }
    };
    dirBrowser.click();
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.py')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('code-input').value = e.target.result;
            updateCurrentCommand();
        };
        reader.readAsText(file);
    }
}

// Handle directory selection
function handleDirectorySelect(event) {
    // Implementation for directory handling
    console.log('Directory selected:', event.target.files);
}

// Update technique options based on performance mode
function updateTechniqueOptions() {
    const performanceMode = document.getElementById('performance-mode').value;
    const techniqueSelect = document.getElementById('technique-select');
    
    // Clear current options
    techniqueSelect.innerHTML = '';
    
    let techniques = [];
    switch (performanceMode) {
        case 'fast':
            techniques = [
                { value: 'fast_xor', text: 'Fast XOR' },
                { value: 'base64', text: 'Base64' },
                { value: 'hex', text: 'Hex Encoding' }
            ];
            break;
        case 'balanced':
            techniques = [
                { value: 'fast_xor', text: 'Fast XOR' },
                { value: 'base64', text: 'Base64' },
                { value: 'hex', text: 'Hex Encoding' },
                { value: 'zlib', text: 'Zlib Compression' },
                { value: 'dna', text: 'DNA Encoding' }
            ];
            break;
        case 'full':
            techniques = [
                { value: 'fast_xor', text: 'Fast XOR' },
                { value: 'base64', text: 'Base64' },
                { value: 'hex', text: 'Hex Encoding' },
                { value: 'zlib', text: 'Zlib Compression' },
                { value: 'dna', text: 'DNA Encoding' },
                { value: 'steganographic', text: 'Steganographic' }
            ];
            break;
    }
    
    techniques.forEach(technique => {
        const option = document.createElement('option');
        option.value = technique.value;
        option.textContent = technique.text;
        techniqueSelect.appendChild(option);
    });
    
    updateCurrentCommand();
}

// Toggle seed input based on random seed checkbox
function toggleSeedInput() {
    const randomSeed = document.getElementById('random-seed').checked;
    const seedInput = document.getElementById('seed-input');
    seedInput.disabled = randomSeed;
    if (randomSeed) {
        seedInput.value = Math.floor(Math.random() * 999999);
    }
    updateCurrentCommand();
}

// Update current command display
function updateCurrentCommand() {
    const config = getCurrentConfig();
    const command = buildCommand(config);
    document.getElementById('current-command').value = command;
    currentConfig = config;
}

// Get current configuration
function getCurrentConfig() {
    return {
        scriptLocation: document.getElementById('script-location').value,
        codeInput: document.getElementById('code-input').value,
        technique: document.getElementById('technique-select').value,
        layers: parseInt(document.getElementById('layers-input').value),
        seed: document.getElementById('random-seed').checked ? null : parseInt(document.getElementById('seed-input').value),
        performanceMode: document.getElementById('performance-mode').value,
        outputDirectory: document.getElementById('output-directory').value,
        createStandalone: document.getElementById('create-standalone').checked,
        backupOriginal: document.getElementById('backup-original').checked,
        customOptions: document.getElementById('custom-options').value,
        debugMode: document.getElementById('debug-mode').checked
    };
}

// Build command string
function buildCommand(config) {
    let command = 'obfuslite';
    
    if (config.scriptLocation) {
        command += ` "${config.scriptLocation}"`;
    }
    
    command += ` --technique ${config.technique}`;
    command += ` --layers ${config.layers}`;
    
    if (config.seed !== null) {
        command += ` --seed ${config.seed}`;
    }
    
    command += ` --performance ${config.performanceMode}`;
    
    if (config.outputDirectory) {
        command += ` --output "${config.outputDirectory}"`;
    }
    
    if (config.createStandalone) {
        command += ' --standalone';
    }
    
    if (config.backupOriginal) {
        command += ' --backup';
    }
    
    if (config.debugMode) {
        command += ' --debug';
    }
    
    if (config.customOptions) {
        command += ` ${config.customOptions}`;
    }
    
    return command;
}

// Start obfuscation process
async function startObfuscation() {
    if (isProcessing) return;
    
    const config = getCurrentConfig();
    
    // Validate input
    if (!config.scriptLocation && !config.codeInput) {
        showError('Please provide either a script file or paste code to obfuscate.');
        return;
    }
    
    isProcessing = true;
    showLoadingSpinner(true);
    document.getElementById('obfuscate-button').disabled = true;
    
    try {
        const response = await fetch('/api/obfuscate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess(result);
        } else {
            showError(result.error || 'Obfuscation failed');
        }
        
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        isProcessing = false;
        showLoadingSpinner(false);
        document.getElementById('obfuscate-button').disabled = false;
    }
}

// Show loading spinner
function showLoadingSpinner(show) {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = show ? 'flex' : 'none';
}

// Show success result
function showSuccess(result) {
    const outputText = document.getElementById('output-text');
    outputText.classList.remove('error');
    outputText.value = `Obfuscation completed successfully!\n\n${result.message || ''}`;
    
    if (result.outputPath) {
        document.getElementById('open-output-button').style.display = 'block';
        document.getElementById('open-output-button').onclick = () => openOutputFolder(result.outputPath);
    }
    
    document.getElementById('common-issue-link').style.display = 'none';
}

// Show error
function showError(message) {
    const outputText = document.getElementById('output-text');
    outputText.classList.add('error');
    outputText.value = `Error: ${message}`;
    document.getElementById('common-issue-link').style.display = 'block';
}

// Open output folder
function openOutputFolder(path) {
    if (path) {
        // Send request to backend to open folder
        fetch('/api/open-folder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ path: path })
        });
    }
}

// Handle keyboard shortcuts
function handleKeyboardShortcuts(event) {
    if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
            case 'Enter':
                event.preventDefault();
                if (!isProcessing) {
                    startObfuscation();
                }
                break;
            case 'o':
                event.preventDefault();
                browseFile('script-location');
                break;
        }
    }
}

// Load preferences from localStorage
function loadPreferences() {
    const saved = localStorage.getItem('obfuslite-preferences');
    if (saved) {
        try {
            const preferences = JSON.parse(saved);
            Object.keys(preferences).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    if (element.type === 'checkbox') {
                        element.checked = preferences[key];
                    } else {
                        element.value = preferences[key];
                    }
                }
            });
            updateCurrentCommand();
        } catch (e) {
            console.error('Error loading preferences:', e);
        }
    }
}

// Save preferences to localStorage
function savePreferences() {
    const preferences = getCurrentConfig();
    localStorage.setItem('obfuslite-preferences', JSON.stringify(preferences));
}

// Auto-save preferences on change
document.addEventListener('change', savePreferences);

// Additional functionality for enhanced user experience

// Real-time validation
function validateInput() {
    const scriptLocation = document.getElementById('script-location').value.trim();
    const codeInput = document.getElementById('code-input').value.trim();
    const obfuscateButton = document.getElementById('obfuscate-button');

    // Enable/disable obfuscate button based on input
    if (scriptLocation || codeInput) {
        obfuscateButton.disabled = false;
        obfuscateButton.textContent = 'Obfuscate Code';
    } else {
        obfuscateButton.disabled = true;
        obfuscateButton.textContent = 'Enter Code to Obfuscate';
    }

    // Validate file extension
    if (scriptLocation && !scriptLocation.endsWith('.py')) {
        showWarning('Selected file should be a Python (.py) file');
    } else {
        hideWarning();
    }
}

// Show warning message
function showWarning(message) {
    const warningsDiv = document.getElementById('warnings');
    warningsDiv.innerHTML = `
        <div>
            <p>⚠️ ${message}</p>
        </div>
    `;
}

// Hide warning message
function hideWarning() {
    const warningsDiv = document.getElementById('warnings');
    warningsDiv.innerHTML = '';
}

// Drag and drop functionality
function setupDragAndDrop() {
    const codeInput = document.getElementById('code-input');
    const scriptLocation = document.getElementById('script-location');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        codeInput.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        codeInput.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        codeInput.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    codeInput.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        codeInput.classList.add('drag-over');
    }

    function unhighlight(e) {
        codeInput.classList.remove('drag-over');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            const file = files[0];
            if (file.name.endsWith('.py')) {
                scriptLocation.value = file.name;

                const reader = new FileReader();
                reader.onload = function(e) {
                    codeInput.value = e.target.result;
                    updateCurrentCommand();
                    validateInput();
                };
                reader.readAsText(file);
            } else {
                showWarning('Please drop a Python (.py) file');
            }
        }
    }
}

// Code syntax highlighting (basic)
function addSyntaxHighlighting() {
    const codeInput = document.getElementById('code-input');

    codeInput.addEventListener('input', function() {
        // Basic syntax validation
        const code = this.value;
        try {
            // Simple check for common Python syntax errors
            if (code.includes('def ') && !code.includes(':')) {
                showWarning('Function definition missing colon (:)');
            } else if (code.includes('if ') && !code.includes(':')) {
                showWarning('If statement missing colon (:)');
            } else {
                hideWarning();
            }
        } catch (e) {
            // Ignore syntax checking errors
        }
    });
}

// Auto-resize textarea
function setupAutoResize() {
    const textareas = document.querySelectorAll('textarea');

    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showTemporaryMessage('Copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy: ', err);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showTemporaryMessage('Copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
        document.body.removeChild(textArea);
    }
}

// Show temporary message
function showTemporaryMessage(message, duration = 3000) {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--primary);
        color: white;
        padding: 12px 20px;
        border-radius: var(--border-radius);
        z-index: 1001;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 300);
    }, duration);
}

// Add copy buttons to output areas
function addCopyButtons() {
    const outputAreas = ['current-command', 'output-text'];

    outputAreas.forEach(id => {
        const textarea = document.getElementById(id);
        if (textarea) {
            const container = textarea.parentElement;
            const copyButton = document.createElement('button');
            copyButton.textContent = 'Copy';
            copyButton.className = 'copy-button';
            copyButton.onclick = () => copyToClipboard(textarea.value);

            // Style the copy button
            copyButton.style.cssText = `
                position: absolute;
                top: 8px;
                right: 8px;
                padding: 4px 8px;
                font-size: 12px;
                background: var(--primary);
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                opacity: 0.7;
                transition: opacity 0.3s;
            `;

            copyButton.addEventListener('mouseenter', () => {
                copyButton.style.opacity = '1';
            });

            copyButton.addEventListener('mouseleave', () => {
                copyButton.style.opacity = '0.7';
            });

            container.style.position = 'relative';
            container.appendChild(copyButton);
        }
    });
}

// Initialize enhanced functionality
document.addEventListener('DOMContentLoaded', function() {
    setupDragAndDrop();
    addSyntaxHighlighting();
    setupAutoResize();
    addCopyButtons();

    // Add input validation
    const inputs = ['script-location', 'code-input'];
    inputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', validateInput);
        }
    });

    // Initial validation
    validateInput();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }

    .drag-over {
        border-color: var(--primary) !important;
        background-color: var(--primary-shadow) !important;
    }

    .copy-button:hover {
        background-color: var(--primary-darker) !important;
    }
`;
document.head.appendChild(style);
