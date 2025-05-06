class VerseForm {
    constructor() {
        this.bookSelect = document.getElementById('book-select');
        this.chapterSelect = document.getElementById('chapter-select');
        this.verseNumber = document.getElementById('verse-number');
        this.aramaicText = document.getElementById('aramaic-text');
        this.portugueseText = document.getElementById('portuguese-text');
        this.form = document.getElementById('verse-form');
        
        this.initializeEventListeners();
        this.loadLastContext();
    }

    initializeEventListeners() {
        this.bookSelect.addEventListener('change', () => this.loadChapters());
        this.chapterSelect.addEventListener('change', () => this.loadNextVerse());
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Adiciona atalhos de teclado
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                this.form.dispatchEvent(new Event('submit'));
            }
        });
    }

    async loadChapters() {
        const bookId = this.bookSelect.value;
        if (!bookId) {
            this.updateChapterSelect('<option value="">Selecione um Capítulo</option>', true);
            return;
        }

        try {
            const response = await fetch(`/admin/bible_app/verse/api/chapters/?book_id=${bookId}`);
            const chapters = await response.json();
            
            let options = '<option value="">Selecione um Capítulo</option>';
            chapters.forEach(chapter => {
                options += `<option value="${chapter.id}">Capítulo ${chapter.number}</option>`;
            });
            
            this.updateChapterSelect(options, false);
        } catch (error) {
            console.error('Erro ao carregar capítulos:', error);
            this.showError('Erro ao carregar capítulos. Por favor, tente novamente.');
        }
    }

    async loadNextVerse() {
        const chapterId = this.chapterSelect.value;
        if (!chapterId) return;

        try {
            const response = await fetch(`/admin/bible_app/verse/api/next-verse/?chapter_id=${chapterId}`);
            const data = await response.json();
            this.verseNumber.value = data.next_verse;
        } catch (error) {
            console.error('Erro ao carregar próximo versículo:', error);
            this.showError('Erro ao determinar próximo número do versículo.');
        }
    }

    updateChapterSelect(html, disabled) {
        this.chapterSelect.innerHTML = html;
        this.chapterSelect.disabled = disabled;
    }

    loadLastContext() {
        const lastBook = localStorage.getItem('lastBook');
        const lastChapter = localStorage.getItem('lastChapter');
        
        if (lastBook) {
            this.bookSelect.value = lastBook;
            this.loadChapters().then(() => {
                if (lastChapter) {
                    this.chapterSelect.value = lastChapter;
                    this.loadNextVerse();
                }
            });
        }
    }

    saveContext() {
        localStorage.setItem('lastBook', this.bookSelect.value);
        localStorage.setItem('lastChapter', this.chapterSelect.value);
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            return;
        }
        
        this.saveContext();
        const formData = new FormData(this.form);
        
        try {
            const response = await fetch('/admin/bible_app/verse/add/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            if (response.ok) {
                this.showSuccess('Versículo salvo com sucesso!');
                this.clearForm();
                this.loadNextVerse();
            } else {
                const data = await response.json();
                this.showError(data.error || 'Erro ao salvar versículo.');
            }
        } catch (error) {
            console.error('Erro ao salvar versículo:', error);
            this.showError('Erro ao salvar versículo. Por favor, tente novamente.');
        }
    }

    validateForm() {
        if (!this.bookSelect.value) {
            this.showError('Por favor, selecione um livro.');
            return false;
        }
        if (!this.chapterSelect.value) {
            this.showError('Por favor, selecione um capítulo.');
            return false;
        }
        if (!this.verseNumber.value) {
            this.showError('Por favor, insira o número do versículo.');
            return false;
        }
        if (!this.aramaicText.value.trim()) {
            this.showError('Por favor, insira o texto em aramaico.');
            return false;
        }
        if (!this.portugueseText.value.trim()) {
            this.showError('Por favor, insira o texto em português.');
            return false;
        }
        return true;
    }

    clearForm() {
        this.aramaicText.value = '';
        this.portugueseText.value = '';
        this.aramaicText.focus();
    }

    showError(message) {
        const errorDiv = document.getElementById('message-container');
        errorDiv.innerHTML = `<div class="error-message">${message}</div>`;
        errorDiv.scrollIntoView({ behavior: 'smooth' });
    }

    showSuccess(message) {
        const successDiv = document.getElementById('message-container');
        successDiv.innerHTML = `<div class="success-message">${message}</div>`;
        successDiv.scrollIntoView({ behavior: 'smooth' });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VerseForm();
});