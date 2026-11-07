# Desafio: O Arquiteto de Software

## Objetivos

1. Desenvolver um Gerenciador de Tarefs Inteligente 
2. Tornar-se um orquestrador de agentes de IA, dominando a estrutura formal de prompts, leitura crítica de erros e refinamento iterativo

## As 5 Regras do "Prompt-Master"

1. Papel/Persona: DEfinir a persona e o nível de conhecimento e atuação da IA
2. Objetivos: Especificação Detalhada e Funcional, dividida em passos lógicos
3. Contexto: Tecnologias permitidas, público-alvo, localidade e padrão de arquitetura de desenvolvimento.
4. Limitações/Restrições: O que a IA Não Pode fazer, (restrições tecnológicas, legais ou de localização)
5. Output(Formato de Saída): Exemplos de Formatos de saídas, planos de implementação

## Tecnologias Utilizadas

- IDE: Vscode
- IA: Antigravity
- Plano de Desenvolvimento com IA (Master-Prompt)

## Master-Prompt

[Persona]
Atue com um Engenehrio de software FullStack sênior e especialista em UI/UX

[Objetivos]
O aplicativo de fazer:
1. Criar, listar, editar e deletar tarefa (CRUD Completo)
2. Organizar as Tarefas por Categorias(Trabalho, Estudo, Pessoais) e utilizar cores diferentes
3. Classificar as tarefas por nível de prioridade (Baixa, Média, Alta)
4. A persistência de Dados deve acontecer em um arquivo db.json, utilizando a biblioteca json-server
5. Filtar as tarefas por status utilizando colunas de separação (Em aberto, Pendentes, Concluídas), além de um filtro por título da tarefa


[Contexto]
Estamos Desenvolvendo um aplicativo web chamado "TarefasMaster" (Gerenciador de Tarefas Moderno). O Projeto deve rodar localmente direto no navegador. organize os arquivos utilizando o React para o FrontEnd e crie uma pasta para armazenar o BackEnd (db.json)


[Restrições]
- Não utilize Tailwind CSS 
- Não utilize as cores amarelo, roxo e marrom

[Output]
Gere primeiro um plano de implementação detalhado em tópicos, descrevendo a estrutura de pastas e arquivos. Crie tambem o modelo de dados de cada tarefa (JSON schema) e a ordem de construção recomendada da aplicação.