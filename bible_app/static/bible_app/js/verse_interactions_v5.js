class VerseInteractions {
    constructor() {
        this.initializeCopyButtons();
        this.initializeShareButtons();
        console.log('VerseInteractions inicializado - Versão 5.0');
    }

    initializeCopyButtons() {
        document.querySelectorAll('.copy-verse').forEach(button => {
            button.addEventListener('click', async (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const verseCard = e.target.closest('.verse-card');
                const reference = verseCard.querySelector('.verse-reference').textContent.trim();
                const aramaic = verseCard.querySelector('.aramaic-text').textContent.trim();
                const portuguese = verseCard.querySelector('.portuguese-text p') ? 
                    verseCard.querySelector('.portuguese-text p').textContent.trim() : 
                    verseCard.querySelector('[lang="pt-BR"]').textContent.trim();
                
                // Captura a fonte e o tradutor
                const metadataSection = verseCard.querySelector('.verse-metadata');
                let metadataText = 'Fonte: Não disponível';
                
                if (metadataSection) {
                    // Captura o texto completo da seção de metadados
                    metadataText = metadataSection.textContent.trim();
                }
                
                // Adiciona o domínio principal do site com HTTPS
                const domain = "https://evangelhos.netsarym.com.br";
                
                const textToCopy = `${reference}\n\nAramaico:\n${aramaic}\n\nPortuguês:\n${portuguese}\n\n${metadataText}\n\n${domain}`;
                
                try {
                    await navigator.clipboard.writeText(textToCopy);
                    this.showCopyFeedback(button);
                } catch (err) {
                    console.error('Erro ao copiar:', err);
                    alert('Não foi possível copiar o texto. Por favor, tente novamente.');
                }
            });
        });
    }

    showCopyFeedback(button, iconClass = 'bi-check-lg', tooltipText = 'Copiado!') {
        const icon = button.querySelector('i');
        const originalClass = icon.className;
        const originalTitle = button.getAttribute('title');
        
        icon.className = `bi ${iconClass}`;
        button.classList.add('btn-success');
        button.classList.remove('btn-outline-secondary');
        button.setAttribute('title', tooltipText);
        
        setTimeout(() => {
            icon.className = originalClass;
            button.classList.remove('btn-success');
            button.classList.add('btn-outline-secondary');
            button.setAttribute('title', originalTitle);
        }, 2000);
    }

    initializeShareButtons() {
        document.querySelectorAll('.share-verse').forEach(button => {
            button.addEventListener('click', async (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const verseCard = e.target.closest('.verse-card');
                const reference = verseCard.querySelector('.verse-reference').textContent.trim();
                
                // Extrair informações da referência (ex: "Mateus 1:1" -> book=1&chapter=1&highlight_start=1&highlight_end=1)
                const [bookName, chapterVerse] = reference.split(' ');
                const [chapter, verse] = chapterVerse.split(':');
                
                // Obter o ID do livro (pode ser necessário um mapeamento mais robusto em produção)
                let bookId = 1; // Padrão para Mateus
                if (bookName === 'Marcos') bookId = 2;
                if (bookName === 'Lucas') bookId = 3;
                if (bookName === 'João') bookId = 4;
                
                // Construir a URL completa para compartilhar com HTTPS
                const baseUrl = "https://evangelhos.netsarym.com.br";
                const shareUrl = `${baseUrl}/?book=${bookId}&chapter=${chapter}&highlight_start=${verse}&highlight_end=${verse}`;
                
                try {
                    // Usar a API Web Share se disponível (dispositivos móveis)
                    if (navigator.share) {
                        await navigator.share({
                            title: `Evangelhos Aramaico Siríaco - ${reference}`,
                            text: `Confira este versículo: ${reference}`,
                            url: shareUrl
                        });
                    } else {
                        // Em desktops, apenas copiar o link para a área de transferência
                        await navigator.clipboard.writeText(shareUrl);
                        this.showCopyFeedback(button, 'bi-check-lg', 'Link copiado!');
                    }
                } catch (err) {
                    console.error('Erro ao compartilhar:', err);
                }
            });
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new VerseInteractions();
});