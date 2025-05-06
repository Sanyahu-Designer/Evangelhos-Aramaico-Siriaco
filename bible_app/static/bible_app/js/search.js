document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchClear = document.getElementById('searchClear');
    const resultsContainer = searchResults.querySelector('.list-group');
    
    // Função para mostrar resultados
    function showResults(results) {
        if (!results || results.length === 0) {
            searchResults.style.display = 'none';
            return;
        }

        resultsContainer.innerHTML = results
            .map(result => `
                <a href="#" class="list-group-item list-group-item-action">
                    ${result}
                </a>
            `)
            .join('');

        searchResults.style.display = 'block';
    }

    // Limpar pesquisa
    searchClear.addEventListener('click', function() {
        searchInput.value = '';
        searchResults.style.display = 'none';
        searchInput.focus();
    });

    // Pesquisar ao digitar
    let timeoutId;
    searchInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        
        const query = this.value.trim();
        if (!query) {
            searchResults.style.display = 'none';
            return;
        }

        // Simular delay de pesquisa
        timeoutId = setTimeout(() => {
            // Aqui você deve implementar sua lógica real de pesquisa
            // Por enquanto, usando resultados de exemplo
            const mockResults = [
                'Mateus 1:1 - Livro da genealogia de Jesus Cristo...',
                'Mateus 1:2 - Abraão gerou a Isaque...',
                'Mateus 1:3 - Isaque gerou a Jacó...'
            ];
            showResults(mockResults);
        }, 300);
    });

    // Fechar resultados ao clicar fora
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && 
            !searchResults.contains(e.target) && 
            !searchClear.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });

    // Prevenir que o formulário seja submetido
    searchInput.closest('form')?.addEventListener('submit', function(e) {
        e.preventDefault();
    });
});
