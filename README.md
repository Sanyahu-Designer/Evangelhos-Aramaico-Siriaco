# Evangelhos Aramaico Siríaco
<p align="center">
  <a href="https://evangelhos.netsarym.com.br">
    <img src="https://placehold.co/400x200/3498db/ffffff?text=Evangelhos+Aramaico+Siriaco" alt="Evangelhos Aramaico Siriaco" width="400"/>
  </a>
</p>

Este projeto apresenta uma tradução dos Evangelhos do Aramaico Siríaco para o Português do Brasil, com o objetivo de fornecer uma versão acessível e fiel aos textos originais. Desenvolvido com Django, este projeto busca oferecer uma experiência de leitura moderna e intuitiva.

## ✨ Site Oficial (Demonstração)

<a href="https://evangelhos.netsarym.com.br" target="_blank">Evangelhos Aramaico Siríaco</a>
> **Nota:** Clique no link ou na imagem acima. Para abrir em uma nova aba, pressione `Ctrl + Clique` (ou `Cmd + Clique` no Mac).

## ✨ Funcionalidades Principais

- **Tradução Direta:** Textos traduzidos diretamente do Aramaico Siríaco para o Português do Brasil, garantindo a maior fidelidade possível aos manuscritos originais.
- **Manuscritos Antigos:** Baseado em manuscritos como os Evangelhos Curetonianos Siríacos, o Palimpsesto Sinaítico Siríaco Antigo e a Peshitta.
- **Navegação Intuitiva:** Interface simples e amigável para navegar entre livros, capítulos e versículos, facilitando a leitura e o estudo.
- **Notas do Tradutor:** Informações adicionais e notas explicativas fornecidas pelos tradutores para auxiliar na compreensão do contexto e nuances dos textos.
- **Design Responsivo:** Compatível com diversos dispositivos, como desktops, tablets e smartphones, proporcionando uma experiência de leitura consistente em qualquer tela.
- **Tooltips:** Informações adicionais sobre palavras específicas ao passar o mouse, enriquecendo a compreensão do texto.
- **Temas Dark/Light:** Alternância entre temas claro e escuro para uma leitura mais confortável em diferentes ambientes e preferências.
- **Autenticação:** Sistema de autenticação para usuários que desejam contribuir com notas e marcações.
- **Painel Administrativo:** Interface administrativa para gerenciar livros, capítulos, versículos e traduções específicas.
- **Monitoramento de Cache:** Dashboard para monitorar o desempenho do cache e otimizar a performance da aplicação.

## 🔧 Tecnologias Utilizadas

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Banco de Dados:** MariaDB
- **Cache:** Redis
- **Servidor:** WhiteNoise

## ⚙️ Como Executar o Projeto

1. Abra o Visual Studio Code.

2. Clone o repositório diretamente no VS Code:
   - Vá até o menu `Fonte de Controle` (ícone de ramificação no lado esquerdo).
   - Clique em `Clonar Repositório`.
   - Insira a URL do repositório:
     ```plaintext
     https://github.com/Sanyahu-Designer/Biblia-Aramaico-Portugues.git
     ```
   - Escolha uma pasta local para salvar o projeto.

3. Abra o terminal integrado no VS Code (atalho `Ctrl + '` ou `Cmd + '` no Mac).

4. Navegue até o diretório do projeto:
   ```bash
   cd Biblia-Aramaico-Portugues
   ```

5. Copie o arquivo de exemplo do ambiente e configure as variáveis de ambiente:
   - Renomeie o arquivo `.env.example` para `.env`:
     ```bash
     mv .env.example .env
     ```
   - Abra o arquivo `.env` e insira os dados do banco de dados e outras configurações necessárias.

6. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

7. Configure o banco de dados MariaDB:
   - Certifique-se de que o MariaDB está instalado e em execução.
   - Crie um banco de dados para o projeto e configure as credenciais no arquivo `.env`.

8. Crie as migrações:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

9. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

10. Acesse a aplicação no seu navegador: `http://localhost:8000`

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções.

## 📜 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

## ✉️ Contato

Para dúvidas ou sugestões, entre em contato através do email: [arte@sanyahudesigner.com.br](mailto:arte@sanyahudesigner.com.br)

---
<p align="center">
    Criado por <a href="https://sanyahudesigner.com.br">Sanyahu Designer</a>
</p>