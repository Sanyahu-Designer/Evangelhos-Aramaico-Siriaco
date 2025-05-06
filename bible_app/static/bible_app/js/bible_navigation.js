// bible_navigation.js
document.addEventListener('DOMContentLoaded', function() {
    const bookSelect = document.getElementById('book-select');
    const chapterSelect = document.getElementById('chapter-select');
    const versesSection = document.querySelector('.verses-container');

    // Função para atualizar a URL e recarregar a página
    function navigateToChapter(bookId, chapterId) {
        if (bookId && chapterId) {
            // Construir a URL com os parâmetros
            const baseUrl = window.location.pathname;
            const queryString = `?book=${bookId}&chapter=${chapterId}`;
            
            // Redirecionar para a nova URL
            window.location.href = baseUrl + queryString;
        }
    }

    // Função para carregar capítulos
    async function loadChapters(bookId, selectedChapterId = null) {
        if (!chapterSelect) return;

        // Desabilitar select de capítulos enquanto carrega
        chapterSelect.disabled = true;
        chapterSelect.innerHTML = '<option value="">Carregando capítulos...</option>';

        try {
            const response = await fetch(`/get-chapters/?book_id=${bookId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const chapters = await response.json();
            
            // Resetar o select de capítulos
            chapterSelect.innerHTML = '<option value="">Selecione um Capítulo</option>';
            
            // Adicionar as opções de capítulos
            chapters.forEach(chapter => {
                const option = document.createElement('option');
                option.value = chapter.id;
                option.textContent = `Capítulo ${chapter.number}`;
                if (selectedChapterId && chapter.id === parseInt(selectedChapterId)) {
                    option.selected = true;
                }
                chapterSelect.appendChild(option);
            });
            
            // Habilitar o select de capítulos
            chapterSelect.disabled = false;

        } catch (error) {
            console.error('Erro ao carregar capítulos:', error);
            chapterSelect.innerHTML = '<option value="">Erro ao carregar capítulos</option>';
            chapterSelect.disabled = true;
        }
    }

    // Inicialização
    if (bookSelect) {
        const currentBookId = bookSelect.value;
        const urlParams = new URLSearchParams(window.location.search);
        const currentChapterId = urlParams.get('chapter');

        if (currentBookId) {
            loadChapters(currentBookId, currentChapterId);
        }

        // Evento de mudança do livro
        bookSelect.addEventListener('change', function(e) {
            const bookId = e.target.value;
            if (bookId) {
                loadChapters(bookId);
                if (versesSection) {
                    versesSection.innerHTML = '<div class="text-center mt-5"><h2 class="h3">Selecione um capítulo para visualizar os versículos</h2></div>';
                }
            }
        });
    }

    // Evento de mudança do capítulo
    if (chapterSelect) {
        chapterSelect.addEventListener('change', function(e) {
            const chapterId = e.target.value;
            const bookId = bookSelect ? bookSelect.value : null;
            
            if (bookId && chapterId) {
                navigateToChapter(bookId, chapterId);
            }
        });
    }

    // Adicionar debug logs
    console.log('Initial book ID:', bookSelect?.value);
    console.log('Current URL parameters:', new URLSearchParams(window.location.search).toString());
});