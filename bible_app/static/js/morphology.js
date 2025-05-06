// Morphological Analysis Functionality
class MorphologyAnalysis {
    constructor() {
        this.initializeWordAnalysis();
        this.setupModalHandlers();
    }

    initializeWordAnalysis() {
        document.querySelectorAll('.analyzable-word').forEach(word => {
            word.addEventListener('click', (e) => {
                e.preventDefault();
                this.showWordAnalysis(word.dataset.word);
            });
        });
    }

    async showWordAnalysis(word) {
        try {
            const response = await fetch(`/api/morphology/analyze/?word=${encodeURIComponent(word)}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayAnalysisModal(data.analysis);
            } else {
                console.error('Error loading word analysis:', data.error);
            }
        } catch (error) {
            console.error('Error fetching word analysis:', error);
        }
    }

    displayAnalysisModal(analysis) {
        const modalId = `wordAnalysisModal_${analysis.word.id}`;
        const modalElement = document.getElementById(modalId);
        
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }

    setupModalHandlers() {
        document.querySelectorAll('.show-all-occurrences').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const wordId = e.target.closest('.word-analysis-modal').dataset.wordId;
                this.loadAllOccurrences(wordId);
            });
        });
    }

    async loadAllOccurrences(wordId) {
        try {
            const response = await fetch(`/api/morphology/occurrences/${wordId}/`);
            const data = await response.json();
            
            if (data.success) {
                this.updateOccurrencesList(data.occurrences);
            }
        } catch (error) {
            console.error('Error loading occurrences:', error);
        }
    }

    updateOccurrencesList(occurrences) {
        const occurrencesList = document.querySelector('.occurrences-list');
        if (occurrencesList) {
            occurrencesList.innerHTML = occurrences.map(verse => `
                <div class="occurrence-item">
                    <p class="reference">${verse.reference}</p>
                    <p class="aramaic-text">${verse.aramaic_text}</p>
                </div>
            `).join('');
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new MorphologyAnalysis();
});