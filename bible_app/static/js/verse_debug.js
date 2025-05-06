// Script para depurar a estrutura da página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script de depuração carregado');
    
    // Adiciona um botão de debug na página
    const debugButton = document.createElement('button');
    debugButton.textContent = 'Depurar Estrutura';
    debugButton.style.position = 'fixed';
    debugButton.style.top = '10px';
    debugButton.style.right = '10px';
    debugButton.style.zIndex = '9999';
    debugButton.style.padding = '5px 10px';
    debugButton.style.backgroundColor = '#ff5722';
    debugButton.style.color = 'white';
    debugButton.style.border = 'none';
    debugButton.style.borderRadius = '4px';
    debugButton.style.cursor = 'pointer';
    
    document.body.appendChild(debugButton);
    
    debugButton.addEventListener('click', function() {
        debugVerseStructure();
    });
    
    // Função para depurar a estrutura dos versículos
    function debugVerseStructure() {
        const verseCards = document.querySelectorAll('.verse-card');
        console.log(`Encontrados ${verseCards.length} cards de versículos`);
        
        if (verseCards.length === 0) {
            alert('Nenhum versículo encontrado na página');
            return;
        }
        
        // Analisa o primeiro versículo
        const firstCard = verseCards[0];
        console.log('HTML do primeiro versículo:', firstCard.outerHTML);
        
        // Verifica se há informações de fonte e tradutor
        const allText = firstCard.innerText;
        console.log('Texto completo do versículo:', allText);
        
        // Procura por textos específicos
        const fonteIndex = allText.indexOf('Fonte:');
        const tradutorIndex = allText.indexOf('Tradutor:');
        
        console.log('Índice de "Fonte:":', fonteIndex);
        console.log('Índice de "Tradutor:":', tradutorIndex);
        
        if (fonteIndex >= 0) {
            const fonteText = allText.substring(fonteIndex, allText.indexOf('\n', fonteIndex) > 0 ? allText.indexOf('\n', fonteIndex) : allText.length);
            console.log('Texto da fonte:', fonteText);
        } else {
            console.log('Texto "Fonte:" não encontrado');
        }
        
        if (tradutorIndex >= 0) {
            const tradutorText = allText.substring(tradutorIndex, allText.indexOf('\n', tradutorIndex) > 0 ? allText.indexOf('\n', tradutorIndex) : allText.length);
            console.log('Texto do tradutor:', tradutorText);
        } else {
            console.log('Texto "Tradutor:" não encontrado');
        }
        
        // Verifica se há elementos com classes específicas
        console.log('Elementos com classe .verse-metadata:', firstCard.querySelectorAll('.verse-metadata').length);
        
        const metadataDiv = firstCard.querySelector('.verse-metadata');
        if (metadataDiv) {
            console.log('Conteúdo da div .verse-metadata:', metadataDiv.innerHTML);
            console.log('Texto da div .verse-metadata:', metadataDiv.textContent);
        }
        
        // Adiciona temporariamente bordas coloridas para visualização
        firstCard.style.border = '2px solid red';
        
        const spans = firstCard.querySelectorAll('span');
        console.log(`Encontrados ${spans.length} elementos span`);
        
        spans.forEach((span, index) => {
            console.log(`Span ${index}:`, span.textContent);
            span.style.border = '1px solid blue';
            span.style.display = 'inline-block';
            span.style.margin = '2px';
        });
        
        // Alerta com instruções
        alert('Informações de depuração foram registradas no console do navegador. Pressione F12 para abrir as ferramentas de desenvolvedor e verificar.');
    }
});
