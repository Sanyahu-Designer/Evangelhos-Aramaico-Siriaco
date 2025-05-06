// Script para depurar a estrutura do DOM
document.addEventListener('DOMContentLoaded', () => {
    // Função para inspecionar a estrutura do DOM
    function inspectDOM() {
        const verseCards = document.querySelectorAll('.verse-card');
        
        if (verseCards.length === 0) {
            console.log('Nenhum card de versículo encontrado na página');
            return;
        }
        
        console.log(`Encontrados ${verseCards.length} cards de versículos`);
        
        // Inspeciona o primeiro card para entender sua estrutura
        const firstCard = verseCards[0];
        console.log('Estrutura do primeiro card de versículo:');
        
        // Referência
        const reference = firstCard.querySelector('.verse-reference');
        console.log('Referência:', reference ? reference.textContent : 'Não encontrada');
        
        // Texto Aramaico
        console.log('Elementos com texto aramaico:');
        ['p.aramaic-text', '.aramaic-text p', '.hebrew-font', '[lang="arc"]', '.text-section.aramaic-text p'].forEach(selector => {
            const element = firstCard.querySelector(selector);
            console.log(`  Seletor "${selector}":`, element ? element.textContent.trim() : 'Não encontrado');
        });
        
        // Texto Português
        console.log('Elementos com texto português:');
        ['p.portuguese-text', '.portuguese-text p', '.text-section.portuguese-text p'].forEach(selector => {
            const element = firstCard.querySelector(selector);
            console.log(`  Seletor "${selector}":`, element ? element.textContent.trim() : 'Não encontrado');
        });
        
        // Fonte e Tradutor
        console.log('Elementos com informações de fonte e tradutor:');
        const metadataDiv = firstCard.querySelector('.verse-metadata');
        if (metadataDiv) {
            console.log('  Conteúdo da div .verse-metadata:', metadataDiv.textContent.trim());
            
            const spans = metadataDiv.querySelectorAll('span');
            spans.forEach((span, index) => {
                console.log(`  Span ${index + 1}:`, span.textContent.trim());
            });
        } else {
            console.log('  Div .verse-metadata não encontrada');
            
            // Procura por texto que contenha "Fonte:" ou "Tradutor:"
            const allText = firstCard.textContent;
            const fonteMatch = allText.match(/Fonte:\s*([^\n\r]+)/);
            const tradutorMatch = allText.match(/Tradutor:\s*([^\n\r]+)/);
            
            console.log('  Fonte (via regex):', fonteMatch ? fonteMatch[0] : 'Não encontrada');
            console.log('  Tradutor (via regex):', tradutorMatch ? tradutorMatch[0] : 'Não encontrado');
        }
        
        // Exibe a estrutura HTML completa para análise
        console.log('HTML completo do primeiro card:');
        console.log(firstCard.outerHTML);
    }
    
    // Executa a inspeção após um pequeno delay para garantir que a página esteja carregada
    setTimeout(inspectDOM, 1000);
});
