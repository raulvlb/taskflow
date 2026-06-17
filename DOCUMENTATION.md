# TaskFlow — Documentação do Projeto

## Visão Geral

**TaskFlow** é um gerenciador de tarefas web leve, desenvolvido com HTML5, CSS3 e JavaScript puro (sem dependências externas). A aplicação permite ao usuário criar, organizar e acompanhar tarefas do dia a dia diretamente no navegador, com persistência local via `localStorage`.

---

## Tecnologias Utilizadas

| Tecnologia   | Versão   | Finalidade                        |
|--------------|----------|-----------------------------------|
| HTML5        | —        | Estrutura semântica da interface  |
| CSS3         | —        | Estilização e responsividade      |
| JavaScript   | ES2020+  | Lógica de negócio e DOM           |
| localStorage | Web API  | Persistência de dados no cliente  |

---

## Estrutura de Arquivos

```
taskflow/
├── index.html          # Ponto de entrada da aplicação
├── css/
│   └── style.css       # Estilos globais e componentes
├── js/
│   └── app.js          # Lógica da aplicação
└── DOCUMENTATION.md    # Esta documentação
```

---

## Requisitos Funcionais

### RF001 — Adicionar Tarefa

**Descrição:** O sistema deve permitir que o usuário adicione uma nova tarefa por meio de um campo de texto e um botão de confirmação ou pressionando a tecla `Enter`.

**Critérios de aceitação:**
- O campo aceita no máximo 120 caracteres.
- Entradas em branco (somente espaços) não devem ser salvas.
- Após adição, o campo deve ser limpo e o foco retornado a ele.
- A tarefa adicionada aparece no topo da lista.

---

### RF002 — Marcar Tarefa como Concluída

**Descrição:** O sistema deve permitir que o usuário marque ou desmarque uma tarefa como concluída clicando no indicador circular ao lado do texto.

**Critérios de aceitação:**
- Tarefas concluídas exibem texto tachado e opacidade reduzida.
- O ícone do indicador muda visualmente (verde com ✓) para indicar o estado.
- A ação é reversível: clicar novamente restaura o estado pendente.

---

### RF003 — Excluir Tarefa

**Descrição:** O sistema deve permitir que o usuário remova definitivamente uma tarefa da lista.

**Critérios de aceitação:**
- O botão de exclusão (🗑️) é exibido ao passar o cursor sobre a tarefa.
- A exclusão é imediata, sem confirmação adicional.
- A tarefa removida não pode ser recuperada pela interface.

---

### RF004 — Editar Tarefa

**Descrição:** O sistema deve permitir que o usuário edite o texto de uma tarefa existente por meio de um modal de edição.

**Critérios de aceitação:**
- O botão de edição (✏️) abre um modal com o texto atual da tarefa preenchido.
- O usuário pode salvar as alterações clicando em "Salvar" ou pressionando `Enter`.
- O usuário pode cancelar a edição clicando em "Cancelar", pressionando `Esc` ou clicando fora do modal.
- Salvar com campo vazio não deve atualizar a tarefa.

---

### RF005 — Filtrar Tarefas

**Descrição:** O sistema deve oferecer filtros que permitam ao usuário visualizar subconjuntos da lista de tarefas.

**Critérios de aceitação:**
- Filtro **Todas**: exibe todas as tarefas cadastradas.
- Filtro **Pendentes**: exibe apenas tarefas não concluídas.
- Filtro **Concluídas**: exibe apenas tarefas marcadas como concluídas.
- O filtro ativo é destacado visualmente.

---

### RF006 — Persistência de Dados

**Descrição:** O sistema deve persistir as tarefas no `localStorage` do navegador, garantindo que os dados não sejam perdidos ao recarregar a página.

**Critérios de aceitação:**
- Toda alteração (adição, edição, exclusão, toggle) é salva automaticamente.
- Ao iniciar a aplicação, as tarefas armazenadas são carregadas e exibidas.
- Dados corrompidos no `localStorage` devem ser tratados graciosamente (lista vazia como fallback).

---

### RF007 — Contagem de Tarefas Pendentes

**Descrição:** O sistema deve exibir, no rodapé da lista, a quantidade de tarefas que ainda não foram concluídas.

**Critérios de aceitação:**
- O contador é atualizado em tempo real a cada alteração na lista.
- Exibe texto no singular ("1 tarefa pendente") ou plural ("3 tarefas pendentes") conforme o total.

---

### RF008 — Limpar Tarefas Concluídas

**Descrição:** O sistema deve fornecer uma ação para remover, de uma só vez, todas as tarefas marcadas como concluídas.

**Critérios de aceitação:**
- O botão "Limpar concluídas" é exibido apenas quando há ao menos uma tarefa concluída.
- A ação remove todas as tarefas concluídas permanentemente.
- Tarefas pendentes não são afetadas.

---

### RF009 — Marcar Todas as Tarefas

**Descrição:** O sistema deve permitir que o usuário marque ou desmarque todas as tarefas da lista de uma só vez.

**Critérios de aceitação:**
- O botão "Marcar todas" é exibido no rodapé da lista quando há tarefas cadastradas.
- Se todas as tarefas estiverem marcadas como concluídas, o botão exibe "Desmarcar todas" e, ao ser clicado, desmarca todas as tarefas.
- Se houver ao menos uma tarefa não concluída, o botão exibe "Marcar todas" e, ao ser clicado, marca todas as tarefas como concluídas.
- O botão não é exibido se não houver tarefas na lista.

---

### RF010 — Buscar Tarefas

**Descrição:** O sistema deve permitir que o usuário busque tarefas por texto.

**Critérios de aceitação:**
- Um campo de busca deve estar disponível acima da lista de tarefas.
- O campo de busca deve filtrar as tarefas em tempo real conforme o usuário digita.
- A busca deve ser case-insensitive (não diferencia maiúsculas e minúsculas).
- O campo de busca deve ser limpo ao recarregar a página.

---

### RF011 — Duplicar Tarefa

**Descrição:** O sistema deve permitir que o usuário duplique uma tarefa existente.

**Critérios de aceitação:**
- O botão de duplicar (⧉) é exibido ao passar o cursor sobre a tarefa.
- A tarefa duplicada deve ser adicionada logo abaixo da tarefa original.
- A tarefa duplicada deve ter um novo identificador único.
- A tarefa duplicada deve ter o mesmo texto da original, mas deve ser marcada como não concluída.

---

## Regras de Negócio

| ID    | Regra                                                                              |
|-------|------------------------------------------------------------------------------------|
| RN001 | Uma tarefa deve ter no mínimo 1 caractere (excluindo espaços) para ser salva.     |
| RN002 | O texto de uma tarefa é limitado a 120 caracteres.                                |
| RN003 | Caracteres especiais HTML são escapados para prevenir ataques XSS.                |
| RN004 | Cada tarefa possui um identificador único gerado via `Date.now()`.                |

---

## Como Executar

1. Clone ou baixe o repositório.
2. Abra o arquivo `index.html` diretamente em qualquer navegador moderno (Chrome, Firefox, Edge, Safari).
3. Nenhuma instalação ou servidor é necessário.

---

## Licença

MIT License — livre para uso, modificação e distribuição.
