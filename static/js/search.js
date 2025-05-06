// Namespace para o aplicativo de busca - Versão 2.0
const SearchApp = {
    init: function() {
        console.log('Inicializando aplicativo de busca - Versão 2.0');
        
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        const searchClear = document.getElementById('searchClear');
        const bookSelect = document.getElementById('book-select');
        const chapterSelect = document.getElementById('chapter-select');
        const categorySelect = document.getElementById('category-select');
        const bibleForm = document.getElementById('bible-form');
        let resultsList;
        let searchTimeout;

        // Garantir que temos a lista de resultados
        if (!searchResults.querySelector('.list-group')) {
            resultsList = document.createElement('div');
            resultsList.className = 'list-group';
            searchResults.appendChild(resultsList);
        } else {
            resultsList = searchResults.querySelector('.list-group');
        }

        // Função para realizar a busca
        function performSearch(query) {
            if (!query) {
                searchResults.style.display = 'none';
                return;
            }

            console.log('Realizando busca para:', query);
            
            // Verificar se é uma busca por intervalo de versículos
            const rangePattern = /^(\d*\s*[A-Za-zÀ-ÖØ-öø-ÿ]+)\s+(\d+):(\d+)-(\d+)$/;
            const isRange = rangePattern.test(query.trim());
            
            if (isRange) {
                console.log('Detectada busca por intervalo de versículos');
                // Para buscas de intervalo, usar uma abordagem diferente
                // Criar um formulário e submeter diretamente para evitar problemas de redirecionamento
                const form = document.createElement('form');
                form.method = 'GET';
                form.action = '/search/';
                form.style.display = 'none';
                
                const input = document.createElement('input');
                input.type = 'text';
                input.name = 'q';
                input.value = query;
                
                form.appendChild(input);
                document.body.appendChild(form);
                
                form.submit();
                return;
            }
            
            // Mostrar indicador de carregamento
            resultsList.innerHTML = '<div class="list-group-item">Buscando...</div>';
            searchResults.style.display = 'block';

            // Para buscas normais, usar fetch
            fetch(`/search/?q=${encodeURIComponent(query)}`)
                .then(response => {
                    console.log('Resposta recebida:', response.status, response.redirected ? 'redirecionado' : 'não redirecionado');
                    
                    // Se for redirecionado, seguir o redirecionamento
                    if (response.redirected) {
                        console.log('Redirecionando para:', response.url);
                        window.location.href = response.url;
                        return null;
                    }
                    
                    if (!response.ok) {
                        throw new Error(`Erro na requisição: ${response.status}`);
                    }
                    
                    return response.json();
                })
                .then(data => {
                    if (data === null) return;
                    
                    console.log('Dados recebidos:', data);
                    resultsList.innerHTML = '';
                    
                    if (data.results && data.results.length > 0) {
                        data.results.forEach(result => {
                            const item = document.createElement('a');
                            item.href = result.url;
                            item.className = 'list-group-item list-group-item-action';
                            item.innerHTML = `
                                <div class="d-flex justify-content-between">
                                    <h6 class="mb-1">${result.title}</h6>
                                </div>
                                <p class="mb-1">${result.text}</p>
                            `;
                            resultsList.appendChild(item);
                        });
                        searchResults.style.display = 'block';
                    } else {
                        resultsList.innerHTML = '<div class="list-group-item">Nenhum resultado encontrado</div>';
                        searchResults.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Erro na busca:', error);
                    resultsList.innerHTML = `<div class="list-group-item text-danger">Erro ao realizar a busca: ${error.message}</div>`;
                    searchResults.style.display = 'block';
                });
        }

        // Event listener para input de busca com debounce
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const query = this.value.trim();
                
                if (query) {
                    searchTimeout = setTimeout(() => performSearch(query), 300);
                } else {
                    searchResults.style.display = 'none';
                }
            });
            
            // Adicionar listener para tecla Enter
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const query = this.value.trim();
                    if (query) {
                        performSearch(query);
                    }
                }
            });
        }

        // Event listener para botão limpar
        if (searchClear) {
            searchClear.addEventListener('click', function() {
                searchInput.value = '';
                searchResults.style.display = 'none';
            });
        }

        // Atualizar o formulário quando o usuário selecionar um capítulo
        if (chapterSelect) {
            chapterSelect.addEventListener('change', function() {
                if (bookSelect.value && chapterSelect.value) {
                    bibleForm.submit();
                }
            });
        }
        
        // Atualizar o formulário quando o usuário selecionar uma categoria
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                if (bookSelect.value && chapterSelect.value) {
                    bibleForm.submit();
                }
            });
        }

        // Fechar resultados ao clicar fora
        document.addEventListener('click', function(e) {
            if (searchResults && !searchResults.contains(e.target) && e.target !== searchInput) {
                searchResults.style.display = 'none';
            }
        });
    }
};

// Inicializar o aplicativo quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    SearchApp.init();
});
