Atue como um Desenvolvedor Full-Stack Sênior. Crie uma aplicação web completa e interativa para uma "Biblioteca Digital" com catálogo de livros, detalhes interativos e sistema de reserva persistido via json-server.

### 1. Tecnologias Requeridas
- Frontend: HTML5 semântico, CSS3 moderno (Flexbox/Grid, responsivo, tema limpo/moderno), JavaScript Vanilla (ES6+, Fetch API, async/await).
- Backend / Persistência: json-server para simular uma API REST real.

---

### 2. Estrutura de Arquivos do Projeto
Organize o projeto na seguinte estrutura:
├── db.json               # Banco de dados simulado do json-server
├── package.json          # Configuração das dependências e scripts npm
├── index.html            # Estrutura da página
├── styles.css            # Estilização completa e responsiva
└── app.js                # Lógica de consumo da API, renderização e eventos

---

### 3. Modelagem de Dados (`db.json`)
O arquivo `db.json` deve conter dois endpoints:

1. `books`:
   - id (número ou string)
   - title (string)
   - author (string)
   - year (número)
   - genre (string)
   - coverUrl (URL pública de imagem válida de capa de livro)
   - synopsis (string com resumo da obra)
   - availableCopies (número de cópias disponíveis)
   - totalCopies (número total de cópias)
   (Preencha com pelo menos 6 livros de gêneros variados)

2. `reservations`:
   - Começar como um array vazio `[]` pronto para receber:
     - id (automático)
     - bookId (id do livro)
     - bookTitle (título do livro)
     - userName (nome do leitor)
     - userEmail (email do leitor)
     - reservationDate (data/hora da solicitação no formato ISO)
     - status (padrão: "Pendente")

---

### 4. Funcionalidades da Aplicação

1. **Catálogo de Livros (GET /books):**
   - Grid de cards responsivos com: capa, título, autor, gênero e badge visual indicando "Disponível" (verde) ou "Esgotado" (vermelho).
   - Barra de busca em tempo real (filtro por título e autor).
   - Filtro por gênero via `<select>`.

2. **Modal de Detalhes:**
   - Ao clicar em um card, abrir um modal com a sinopse completa, ano de publicação, quantidade de cópias disponíveis e o botão "Solicitar Reserva".
   - Se `availableCopies <= 0`, o botão de reserva deve ficar desabilitado com o texto "Indisponível".

3. **Fluxo de Solicitação de Reserva (POST /reservations + PATCH /books/:id):**
   - Modal ou formulário solicitando Nome e E-mail do usuário.
   - Validação básica dos campos antes de enviar.
   - Enviar a reserva via `POST` para `http://localhost:3000/reservations`.
   - Atualizar a quantidade de cópias do livro subtraindo 1 via `PATCH` para `http://localhost:3000/books/{id}` (`availableCopies: current - 1`).
   - Exibir mensagem de feedback (sucesso ou erro) em tela sem recarregar a página (Toast/Alert visual).
   - Atualizar a UI imediatamente refletindo a nova quantidade de cópias.

4. **Aba/Seção de Minhas Reservas (GET /reservations):**
   - Um botão ou aba no topo para alternar entre "Catálogo" e "Reservas Realizadas".
   - Na lista de reservas, exibir: título do livro, nome do solicitante, data da reserva formatada e badge com o status ("Pendente").

---

### 5. Requisitos de Código e Estilo
- **Design:** Moderno, limpo (estilo card design, sombras suaves, tipografia legível, feedback visual em hover).
- **Tratamento de Erros e Loading:** Adicionar feedback visual enquanto as requisições acontecem (ex: "Carregando catálogo...").
- **Modularidade:** JavaScript bem documentado, funções com responsabilidade única (ex: `fetchBooks()`, `renderBooks()`, `handleReserveSubmit()`, etc.).
- **Instruções de execução:** Ao final, forneça o passo a passo exato no terminal para instalar as dependências, iniciar o `json-server` e abrir o app no navegador.