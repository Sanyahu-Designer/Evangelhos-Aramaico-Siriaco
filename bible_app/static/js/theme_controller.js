class ThemeController {
    constructor() {
        this.theme = localStorage.getItem('theme') || this.getPreferredTheme();
        this.init();
    }

    init() {
        this.applyTheme();
        this.setupListeners();
    }

    getPreferredTheme() {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        document.body.classList.toggle('dark-mode', this.theme === 'dark');
        this.updateToggleButton();
        this.dispatchThemeEvent();
    }

    updateToggleButton() {
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            const sunIcon = toggleButton.querySelector('.bi-sun-fill');
            const moonIcon = toggleButton.querySelector('.bi-moon-fill');
            
            if (this.theme === 'dark') {
                sunIcon.style.display = 'inline-block';
                moonIcon.style.display = 'none';
            } else {
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'inline-block';
            }
        }
    }

    dispatchThemeEvent() {
        window.dispatchEvent(new CustomEvent('themechange', {
            detail: { theme: this.theme }
        }));
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
    }

    setupListeners() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                if (!localStorage.getItem('theme')) {
                    this.theme = e.matches ? 'dark' : 'light';
                    this.applyTheme();
                }
            });
        }

        document.addEventListener('DOMContentLoaded', () => {
            this.applyTheme();
        });
    }
}

// Initialize theme controller immediately
const themeController = new ThemeController();