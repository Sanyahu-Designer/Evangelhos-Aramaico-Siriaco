document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchClear = document.getElementById('searchClear');
    
    if (!searchInput || !searchResults) return;

    let startY, currentY;
    let initialHeight = 60; // Altura inicial do bottom sheet em vh

    // Função para realizar a pesquisa
    async function performSearch(query) {
        if (!query.trim()) {
            searchResults.classList.remove('show');
            return;
        }

        try {
            const response = await fetch(`/search/?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Erro na pesquisa');
            
            const data = await response.json();
            const resultsGroup = searchResults.querySelector('.list-group');
            resultsGroup.innerHTML = '';
            
            if (data.results.length === 0) {
                resultsGroup.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
            } else {
                data.results.forEach(result => {
                    const item = document.createElement('a');
                    item.href = result.url;
                    item.className = 'list-group-item list-group-item-action';
                    item.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center">
                            <strong>${result.title}</strong>
                        </div>
                        <p class="mb-1 text-truncate">${result.text}</p>
                    `;
                    resultsGroup.appendChild(item);
                });
            }
            
            searchResults.classList.add('show');
        } catch (error) {
            console.error('Erro na pesquisa:', error);
        }
    }

    // Eventos do campo de pesquisa
    let debounceTimer;
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            performSearch(e.target.value);
        }, 300);
    });

    // Limpar campo
    searchClear.addEventListener('click', () => {
        searchInput.value = '';
        searchResults.classList.remove('show');
    });

    // Eventos de touch para o bottom sheet em mobile
    if (window.innerWidth <= 991.98) {
        searchResults.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
            currentY = startY;
        });

        searchResults.addEventListener('touchmove', (e) => {
            if (!startY) return;

            currentY = e.touches[0].clientY;
            const deltaY = currentY - startY;

            // Limita o movimento para baixo
            if (deltaY > 0) {
                searchResults.style.transform = `translateY(${deltaY}px)`;
                e.preventDefault();
            }
            // Permite expandir para cima até 90vh
            else if (deltaY < 0 && Math.abs(deltaY) < window.innerHeight * 0.3) {
                searchResults.style.transform = `translateY(${deltaY}px)`;
                e.preventDefault();
            }
        });

        searchResults.addEventListener('touchend', () => {
            const deltaY = currentY - startY;
            
            // Se arrastou mais que 100px para baixo, fecha
            if (deltaY > 100) {
                searchResults.classList.remove('show');
            } 
            // Se arrastou para cima, expande
            else if (deltaY < -50) {
                searchResults.style.maxHeight = '90vh';
            }
            // Volta para a posição inicial
            else {
                searchResults.style.transform = '';
            }

            startY = null;
            currentY = null;
        });
    }

    // Fechar ao clicar fora em desktop
    document.addEventListener('click', (e) => {
        if (window.innerWidth > 991.98 && 
            !searchInput.contains(e.target) && 
            !searchResults.contains(e.target)) {
            searchResults.classList.remove('show');
        }
    });

    // Limpar ao pressionar ESC
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            searchInput.value = '';
            searchResults.classList.remove('show');
        }
    });
});
