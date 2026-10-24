// Chave utilizada para persistencia no LocalStorage
const STORAGE_KEY = "minhas_tarefas_meu_dia";

// Elementos da interface
const formTarefa = document.getElementById("form-tarefa");
const inputTarefa = document.getElementById("input-tarefa");
const listaTarefas = document.getElementById("lista-tarefas");

// Responsabilidade: Ler os dados gravados no LocalStorage
function obterTarefas() {
  const dados = localStorage.getItem(STORAGE_KEY);
  return dados ? JSON.parse(dados) : [];
}

// Responsabilidade: Gravar o array atualizado no LocalStorage
function salvarTarefas(tarefas) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tarefas));
}

// Responsabilidade: Criar o botao de exclusao da tarefa
function criarBotaoExcluir(indice) {
  const botao = document.createElement("button");
  botao.textContent = "Excluir";
  botao.className = "btn-excluir";
  botao.addEventListener("click", () => removerTarefa(indice));
  return botao;
}

// Responsabilidade: Construir o elemento visual (li) de uma tarefa
function criarElementoTarefa(texto, indice) {
  const item = document.createElement("li");
  item.className = "item-tarefa";

  const span = document.createElement("span");
  span.className = "texto-tarefa";
  span.textContent = texto;

  const botaoExcluir = criarBotaoExcluir(indice);

  item.appendChild(span);
  item.appendChild(botaoExcluir);
  return item;
}

// Responsabilidade: Atualizar a exibicao da lista na tela
function renderizarTarefas() {
  const tarefas = obterTarefas();
  listaTarefas.innerHTML = "";

  tarefas.forEach((tarefa, indice) => {
    const elemento = criarElementoTarefa(tarefa, indice);
    listaTarefas.appendChild(elemento);
  });
}

// Responsabilidade: Lidar com a adicao de uma nova tarefa
function adicionarTarefa(evento) {
  evento.preventDefault();
  const texto = inputTarefa.value.trim();

  if (!texto) {
    alert("Por favor, digite uma tarefa antes de adicionar!");
    return;
  }

  const tarefas = obterTarefas();
  tarefas.push(texto);
  salvarTarefas(tarefas);

  inputTarefa.value = "";
  inputTarefa.focus();
  renderizarTarefas();
}

// Responsabilidade: Lidar com a remocao de uma tarefa existente
function removerTarefa(indice) {
  const tarefas = obterTarefas();
  tarefas.splice(indice, 1);
  salvarTarefas(tarefas);
  renderizarTarefas();
}

// Responsabilidade: Configurar os ouvintes de eventos da aplicacao
function inicializarApp() {
  formTarefa.addEventListener("submit", adicionarTarefa);
  renderizarTarefas();
}

// Inicia a aplicacao apos o carregamento do script
inicializarApp();

