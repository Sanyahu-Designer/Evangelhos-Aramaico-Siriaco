class VerseInteractions {
    constructor() {
        this.initializeCopyButtons();
        this.initializePrintButtons();
    }

    initializeCopyButtons() {
        document.querySelectorAll('.copy-verse').forEach(button => {
            button.addEventListener('click', async (e) => {
                // Previne que o evento se propague para elementos pai
                e.preventDefault();
                e.stopPropagation();
                
                // Encontra o elemento clicado (pode ser o ícone ou o botão)
                const clickedElement = e.target.closest('.copy-verse');
                if (!clickedElement) return;
                
                const verseCard = clickedElement.closest('.verse-card');
                const aramaic = verseCard.querySelector('.aramaic-text p').textContent.trim();
                const portuguese = verseCard.querySelector('.portuguese-text p').textContent.trim();
                const reference = verseCard.querySelector('.verse-reference').textContent.trim();
                const fonte = verseCard.querySelector('.verse-metadata span:first-child').textContent.trim();
                const tradutor = verseCard.querySelector('.verse-metadata span:last-child').textContent.trim();
                
                const textToCopy = `${reference}

Aramaico:
${aramaic}

Português:
${portuguese}

${fonte}
${tradutor}`;
                
                try {
                    await navigator.clipboard.writeText(textToCopy);
                    const icon = clickedElement.querySelector('i');
                    const originalClass = icon.className;
                    
                    // Atualiza o ícone e texto
                    icon.className = 'bi bi-check-lg';
                    clickedElement.setAttribute('title', 'Copiado!');
                    
                    // Restaura o ícone original após 2 segundos
                    setTimeout(() => {
                        icon.className = originalClass;
                        clickedElement.setAttribute('title', 'Copiar versículo');
                    }, 2000);
                } catch (err) {
                    console.error('Erro ao copiar:', err);
                    alert('Não foi possível copiar o texto. Por favor, tente novamente.');
                }
            });
        });
    }

    initializePrintButtons() {
        document.querySelectorAll('.print-verse').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const clickedElement = e.target.closest('.print-verse');
                if (!clickedElement) return;
                
                const verseCard = clickedElement.closest('.verse-card');
                const reference = verseCard.querySelector('.verse-reference').textContent.trim();
                const aramaic = verseCard.querySelector('.aramaic-text p').textContent.trim();
                const portuguese = verseCard.querySelector('.portuguese-text p').textContent.trim();
                const fonte = verseCard.querySelector('.verse-metadata span:first-child').textContent.trim();
                const tradutor = verseCard.querySelector('.verse-metadata span:last-child').textContent.trim();
                
                const printWindow = window.open('', '_blank');
                printWindow.document.write(`
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>${reference}</title>
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
                        <style>
                            @media print {
                                body { padding: 20px; }
                                .hebrew-font {
                                    font-family: 'SBL Hebrew', serif;
                                    direction: rtl;
                                    text-align: right;
                                    font-size: 18px;
                                }
                                .verse-content { margin: 20px 0; }
                                .text-section { margin: 15px 0; }
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2 class="mb-4">${reference}</h2>
                            <div class="verse-content">
                                <div class="text-section">
                                    <h5>Texto em Aramaico:</h5>
                                    <p class="hebrew-font">${aramaic}</p>
                                </div>
                                <div class="text-section">
                                    <h5>Tradução em Português:</h5>
                                    <p>${portuguese}</p>
                                </div>
                                <div class="text-section mt-4">
                                    <p class="text-muted">${fonte}</p>
                                    <p class="text-muted">${tradutor}</p>
                                </div>
                            </div>
                        </div>
                        <script>
                            window.onload = () => {
                                setTimeout(() => {
                                    window.print();
                                    window.close();
                                }, 500);
                            };
                        </script>
                    </body>
                    </html>
                `);
                printWindow.document.close();
            });
        });
    }
}

// Inicializa as interações quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new VerseInteractions();
});