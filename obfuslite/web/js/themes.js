// Theme Management for ObfusLite

// Theme constants
const THEMES = {
    LIGHT: 'light',
    DARK: 'dark',
    AUTO: 'auto'
};

const THEME_STORAGE_KEY = 'obfuslite-theme';

// Initialize theme system
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    setupThemeToggle();
});

// Initialize theme based on saved preference or system preference
function initializeTheme() {
    const savedTheme = getSavedTheme();
    const systemTheme = getSystemTheme();
    
    let initialTheme = savedTheme || THEMES.AUTO;
    
    // If auto theme, use system preference
    if (initialTheme === THEMES.AUTO) {
        initialTheme = systemTheme;
    }
    
    setTheme(initialTheme);
    updateThemeToggleIcons(initialTheme);
}

// Setup theme toggle functionality
function setupThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Listen for system theme changes
    if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', handleSystemThemeChange);
    }
}

// Toggle between light and dark themes
function toggleTheme() {
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === THEMES.LIGHT ? THEMES.DARK : THEMES.LIGHT;
    
    setTheme(newTheme);
    saveTheme(newTheme);
    updateThemeToggleIcons(newTheme);
    
    // Add transition effect
    addThemeTransition();
}

// Set the theme
function setTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    
    // Update meta theme-color for mobile browsers
    updateMetaThemeColor(theme);
    
    // Dispatch custom event for theme change
    const event = new CustomEvent('themeChanged', {
        detail: { theme: theme }
    });
    document.dispatchEvent(event);
}

// Get current theme
function getCurrentTheme() {
    return document.body.getAttribute('data-theme') || THEMES.LIGHT;
}

// Get saved theme from localStorage
function getSavedTheme() {
    try {
        return localStorage.getItem(THEME_STORAGE_KEY);
    } catch (e) {
        console.warn('Could not access localStorage for theme preference');
        return null;
    }
}

// Save theme to localStorage
function saveTheme(theme) {
    try {
        localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch (e) {
        console.warn('Could not save theme preference to localStorage');
    }
}

// Get system theme preference
function getSystemTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return THEMES.DARK;
    }
    return THEMES.LIGHT;
}

// Handle system theme changes
function handleSystemThemeChange(e) {
    const savedTheme = getSavedTheme();
    
    // Only update if user hasn't set a specific preference
    if (!savedTheme || savedTheme === THEMES.AUTO) {
        const newTheme = e.matches ? THEMES.DARK : THEMES.LIGHT;
        setTheme(newTheme);
        updateThemeToggleIcons(newTheme);
    }
}

// Update theme toggle icons
function updateThemeToggleIcons(theme) {
    const lightIcon = document.getElementById('light-icon');
    const darkIcon = document.getElementById('dark-icon');
    
    if (lightIcon && darkIcon) {
        if (theme === THEMES.DARK) {
            lightIcon.style.opacity = '0.4';
            darkIcon.style.opacity = '1';
        } else {
            lightIcon.style.opacity = '1';
            darkIcon.style.opacity = '0.4';
        }
    }
}

// Update meta theme-color for mobile browsers
function updateMetaThemeColor(theme) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    
    if (!metaThemeColor) {
        metaThemeColor = document.createElement('meta');
        metaThemeColor.name = 'theme-color';
        document.head.appendChild(metaThemeColor);
    }
    
    const colors = {
        [THEMES.LIGHT]: '#ffffff',
        [THEMES.DARK]: '#1a1a1a'
    };
    
    metaThemeColor.content = colors[theme] || colors[THEMES.LIGHT];
}

// Add smooth transition effect when changing themes
function addThemeTransition() {
    const transitionClass = 'theme-transition';

    // Add transition class
    document.body.classList.add(transitionClass);

    // Add a subtle animation effect
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        background: var(--background);
        opacity: 0.3;
        z-index: 9999;
        pointer-events: none;
        animation: themeTransition 0.3s ease;
    `;

    document.body.appendChild(overlay);

    // Remove transition class and overlay after animation
    setTimeout(() => {
        document.body.classList.remove(transitionClass);
        if (overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
        }
    }, 300);
}

// CSS for theme transition and animations
const themeTransitionCSS = `
.theme-transition * {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
}

@keyframes themeTransition {
    0% { opacity: 0; }
    50% { opacity: 0.3; }
    100% { opacity: 0; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.fade-in {
    animation: fadeIn 0.5s ease;
}

.slide-in {
    animation: slideIn 0.5s ease;
}

.pulse {
    animation: pulse 0.3s ease;
}

/* Enhanced theme toggle button */
#theme-toggle {
    position: relative;
    overflow: hidden;
}

#theme-toggle::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

#theme-toggle:hover::before {
    left: 100%;
}

/* Smooth icon transitions */
#theme-toggle img {
    transition: all 0.3s ease;
}

#theme-toggle:hover img {
    transform: rotate(15deg);
}

/* Loading states */
.loading {
    position: relative;
    overflow: hidden;
}

.loading::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}
`;

// Inject transition CSS
const style = document.createElement('style');
style.textContent = themeTransitionCSS;
document.head.appendChild(style);

// Theme utilities
const ThemeUtils = {
    // Get current theme
    getCurrentTheme: getCurrentTheme,
    
    // Set theme programmatically
    setTheme: setTheme,
    
    // Check if dark theme is active
    isDarkTheme: () => getCurrentTheme() === THEMES.DARK,
    
    // Check if light theme is active
    isLightTheme: () => getCurrentTheme() === THEMES.LIGHT,
    
    // Reset to system preference
    resetToSystemTheme: () => {
        const systemTheme = getSystemTheme();
        setTheme(systemTheme);
        saveTheme(THEMES.AUTO);
        updateThemeToggleIcons(systemTheme);
    },
    
    // Get available themes
    getAvailableThemes: () => Object.values(THEMES)
};

// Export for use in other scripts
window.ThemeUtils = ThemeUtils;

// Handle theme-specific functionality
document.addEventListener('themeChanged', function(e) {
    const theme = e.detail.theme;
    
    // Update any theme-specific elements
    updateCodeEditorTheme(theme);
    updateChartThemes(theme);
});

// Update code editor theme (if using a code editor library)
function updateCodeEditorTheme(theme) {
    // This would be implemented if using libraries like CodeMirror or Monaco Editor
    // Example:
    // if (window.codeEditor) {
    //     const editorTheme = theme === THEMES.DARK ? 'dark' : 'light';
    //     window.codeEditor.setTheme(editorTheme);
    // }
}

// Update chart themes (if using chart libraries)
function updateChartThemes(theme) {
    // This would be implemented if using chart libraries
    // Example:
    // if (window.charts) {
    //     window.charts.forEach(chart => {
    //         chart.updateTheme(theme);
    //     });
    // }
}

// Accessibility: Respect user's motion preferences
function respectsReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// High contrast mode detection
function isHighContrastMode() {
    return window.matchMedia('(prefers-contrast: high)').matches;
}

// Apply accessibility preferences
function applyAccessibilityPreferences() {
    if (respectsReducedMotion()) {
        document.body.classList.add('reduced-motion');
    }
    
    if (isHighContrastMode()) {
        document.body.classList.add('high-contrast');
    }
}

// Initialize accessibility preferences
document.addEventListener('DOMContentLoaded', applyAccessibilityPreferences);

// Listen for accessibility preference changes
if (window.matchMedia) {
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', applyAccessibilityPreferences);
    window.matchMedia('(prefers-contrast: high)').addEventListener('change', applyAccessibilityPreferences);
}
