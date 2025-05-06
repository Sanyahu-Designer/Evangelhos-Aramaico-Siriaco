// Font size controller
class FontController {
    constructor() {
        this.baseSize = parseInt(localStorage.getItem('fontSize')) || 16;
        this.init();
    }

    init() {
        this.applyFontSize();
        this.setupControls();
    }

    applyFontSize() {
        document.documentElement.style.fontSize = `${this.baseSize}px`;
    }

    adjustSize(delta) {
        this.baseSize = Math.max(12, Math.min(24, this.baseSize + delta));
        localStorage.setItem('fontSize', this.baseSize);
        this.applyFontSize();
    }

    setupControls() {
        const increase = document.getElementById('increase-font');
        const decrease = document.getElementById('decrease-font');
        const reset = document.getElementById('reset-font');

        if (increase) increase.addEventListener('click', () => this.adjustSize(1));
        if (decrease) decrease.addEventListener('click', () => this.adjustSize(-1));
        if (reset) reset.addEventListener('click', () => {
            this.baseSize = 16;
            localStorage.removeItem('fontSize');
            this.applyFontSize();
        });
    }
}

// Initialize font controller
document.addEventListener('DOMContentLoaded', () => {
    window.fontController = new FontController();
});