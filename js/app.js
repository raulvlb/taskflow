const STORAGE_KEY = 'taskflow_tasks';

let tasks = loadTasks();
let currentFilter = 'all';
let searchQuery = '';
let editingId = null;

const taskForm      = document.getElementById('taskForm');
const taskInput     = document.getElementById('taskInput');
const taskList      = document.getElementById('taskList');
const taskCount     = document.getElementById('taskCount');
const markAllBtn    = document.getElementById('markAllBtn');
const searchInput   = document.getElementById('searchInput');
const editModal     = document.getElementById('editModal');
const editInput     = document.getElementById('editInput');
const saveEditBtn   = document.getElementById('saveEdit');
const cancelEditBtn = document.getElementById('cancelEdit');

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    currentFilter = btn.dataset.filter;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    render();
  });
});

searchInput.addEventListener('input', () => {
  searchQuery = searchInput.value.trim().toLowerCase();
  render();
});

taskForm.addEventListener('submit', e => {
  e.preventDefault();
  const text = taskInput.value.trim();
  if (!text) return;
  addTask(text);
  taskInput.value = '';
  taskInput.focus();
});

saveEditBtn.addEventListener('click', saveEdit);
cancelEditBtn.addEventListener('click', closeModal);

editModal.addEventListener('click', e => {
  if (e.target === editModal) closeModal();
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
  if (e.key === 'Enter' && !editModal.classList.contains('hidden')) saveEdit();
});

function addTask(text) {
  const task = {
    id: Date.now(),
    text,
    completed: false,
    createdAt: new Date().toISOString(),
  };
  tasks.unshift(task);
  saveTasks();
  render();
}

function toggleTask(id) {
  const task = tasks.find(t => t.id === id);
  if (task) {
    task.completed = !task.completed;
    saveTasks();
    render();
  }
}

function deleteTask(id) {
  tasks = tasks.filter(t => t.id !== id);
  saveTasks();
  render();
}

function markAll() {
  const allDone = tasks.every(t => t.completed);
  tasks.forEach(t => { t.completed = !allDone; });
  saveTasks();
  render();
}

function duplicateTask(id) {
  const task = tasks.find(t => t.id === id);
  if (!task) return;
  const copy = { id: Date.now(), text: task.text, completed: false, createdAt: new Date().toISOString() };
  const index = tasks.findIndex(t => t.id === id);
  tasks.splice(index + 1, 0, copy);
  saveTasks();
  render();
}

function openEditModal(id) {
  const task = tasks.find(t => t.id === id);
  if (!task) return;
  editingId = id;
  editInput.value = task.text;
  editModal.classList.remove('hidden');
  editInput.focus();
  editInput.select();
}

function saveEdit() {
  const newText = editInput.value.trim();
  if (!newText || !editingId) return;
  const task = tasks.find(t => t.id === editingId);
  if (task) {
    task.text = newText;
    saveTasks();
    render();
  }
  closeModal();
}

function closeModal() {
  editModal.classList.add('hidden');
  editingId = null;
  editInput.value = '';
}

function getFilteredTasks() {
  let result = tasks;
  if (currentFilter === 'active')    result = result.filter(t => !t.completed);
  if (currentFilter === 'completed') result = result.filter(t => t.completed);
  if (searchQuery) result = result.filter(t => t.text.toLowerCase().includes(searchQuery));
  return result;
}

function render() {
  const filtered = getFilteredTasks();

  taskList.innerHTML = '';

  filtered.forEach(task => {
    const li = document.createElement('li');
    li.className = `task-item${task.completed ? ' completed' : ''}`;
    li.dataset.id = task.id;

    li.innerHTML = `
      <button class="task-checkbox${task.completed ? ' checked' : ''}" aria-label="Concluir tarefa" data-action="toggle"></button>
      <span class="task-text">${escapeHtml(task.text)}</span>
      <div class="task-actions">
        <button class="icon-btn duplicate" aria-label="Duplicar" data-action="duplicate">⧉</button>
        <button class="icon-btn edit" aria-label="Editar" data-action="edit">✏️</button>
        <button class="icon-btn delete" aria-label="Excluir" data-action="delete">🗑️</button>
      </div>
    `;

    li.addEventListener('click', e => {
      const id = Number(li.dataset.id);
      const action = e.target.closest('[data-action]')?.dataset.action;
      if (action === 'toggle')         toggleTask(id);
      else if (action === 'duplicate') duplicateTask(id);
      else if (action === 'edit')      openEditModal(id);
      else if (action === 'delete')    deleteTask(id);
    });

    taskList.appendChild(li);
  });

  updateFooter();
}

function updateFooter() {
  const pending = tasks.filter(t => !t.completed).length;
  taskCount.textContent = `${pending} tarefa${pending !== 1 ? 's' : ''} pendente${pending !== 1 ? 's' : ''}`;
  const allDone = tasks.length > 0 && tasks.every(t => t.completed);
  markAllBtn.textContent = allDone ? 'Desmarcar todas' : 'Marcar todas';
  markAllBtn.style.display = tasks.length ? 'inline-block' : 'none';
}

markAllBtn.addEventListener('click', markAll);

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function loadTasks() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveTasks() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

render();
