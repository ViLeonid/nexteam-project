<template>
  <div v-if="isLoggedIn">
    <LoginRegister />
  </div>
  <div v-else>
    <div class="main-wrapper">
      <div class="container py-5">
        <div class="text-center mb-5">
          <h1 class="fw-bold display-5">Задачи</h1>
          <p class="text-muted">Управление задачами и дедлайнами</p>
        </div>

        <!-- ФОРМА ДОБАВЛЕНИЯ -->
        <div class="card border-0 shadow-sm mb-4 p-4 rounded-4 bg-white">
          <div class="row g-3 align-items-end">
            <div class="aitext">
              Создать свою задачу
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-bold">ЗАГОЛОВОК</label>
              <input v-model="addForm.title" class="form-control border-0 bg-light py-2" placeholder="Название...">
            </div>
            <div class="col-md-4">
              <label class="form-label small fw-bold">ОПИСАНИЕ</label>
              <input v-model="addForm.description" class="form-control border-0 bg-light py-2" placeholder="Детали задачи...">
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-bold">ДЕДЛАЙН</label>
              <input v-model="addForm.deadline" type="datetime-local" class="form-control border-0 bg-light py-2">
            </div>
            <div class="col-md-2">
              <button @click="addTodo" class="btn btn-primary w-100 fw-bold py-2 shadow-sm rounded-3">СОЗДАТЬ</button>
            </div>
          </div>
        </div>
        <!-- ФОРМА ДОБАВЛЕНИЯ С ИИ-->
        <div class="AIcard shadow-sm mb-4 p-4 rounded-4 bg-white">
          <div class="row g-3 align-items-end">
            <div class="aitext">
              Создать задачу с ИИ
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-bold">ПРЕДМЕТ</label>
              <input v-model="AIaddForm.subject" class="form-control border-0 bg-light py-2" placeholder="Название предмета...">
            </div>
            <div class="col-md-4">
              <label class="form-label small fw-bold">ТЕМА</label>
              <input v-model="AIaddForm.topic" class="form-control border-0 bg-light py-2" placeholder="Тема...">
            </div>
            <div class="col-md-3">
              <label class="form-label small fw-bold">ДЕДЛАЙН</label>
              <input v-model="AIaddForm.deadline" type="datetime-local" class="form-control border-0 bg-light py-2">
            </div>


            <div class="col-md-2">
              <button
                @click="AIaddTodo"
                :disabled="isAILoading"
                class="btn btn-purple border-0 w-100 fw-bold py-2 shadow-sm rounded-3 text-white d-flex align-items-center justify-content-center gap-2"
                style="background-color: #8b5cf6;"
              >
                <!-- Если ИИ думает, показываем спиннер загрузки Bootstrap -->
                <span v-if="isAILoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span>{{ isAILoading ? 'ГЕНЕРАЦИЯ...' : 'СОЗДАТЬ' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- ФИЛЬТРАЦИЯ -->
        <div class="d-flex justify-content-center gap-2 mb-5">
          <button
            v-for="f in ['all', 'active', 'done']"
            :key="f"
            @click="filterStatus = f"
            :class="filterStatus === f ? 'btn-dark' : 'btn-outline-secondary'"
            class="btn btn-sm px-4 rounded-pill fw-bold text-uppercase"
          >
            {{ f === 'all' ? 'Все' : f === 'active' ? 'В работе' : 'Выполнены' }}
          </button>
        </div>

        <!-- СЕТКА КАРТОЧЕК -->
        <div class="row row-cols-1 row-cols-md-3 g-4 mx-0">
          <div class="col" v-for="todo in filteredTodos" :key="todo.id">
            <div class="card h-100 border-0 shadow-sm rounded-4 task-card" :class="{'done-task': todo.is_done}">
              <div class="card-body p-4 d-flex flex-column">

                <div class="d-flex justify-content-between align-items-start mb-3">
                  <span :class="todo.is_done ? 'badge bg-success' : 'badge bg-primary'" class="px-3 py-2 rounded-pill">
                    {{ todo.is_done ? 'ВЫПОЛНЕНО' : 'В РАБОТЕ' }}
                  </span>
                  <div class="form-check form-switch mt-1">
                    <input class="form-check-input" type="checkbox" :checked="todo.is_done" @change="toggleDone(todo)">
                  </div>
                </div>

                <h4 class="fw-bold mb-2" v-html="renderMixedContent(todo.title)"></h4>
                <div class="text-muted small flex-grow-1 mb-4" v-html="renderMixedContent(todo.description)"></div>


                <div class="deadline-info py-2 mb-4 border-top border-bottom small text-secondary">
                  <i class="bi bi-calendar3 me-2"></i> {{ todo.deadline ? todo.deadline.replace('T', ' | ').replace('-','.').replace('-','.') : 'Без срока' }}
                </div>

                <div class="d-flex gap-2">
                  <button @click="openEditModal(todo)" class="btn btn-light flex-grow-1 rounded-3 fw-semibold">Изменить</button>
                  <button @click="deleteTodo(todo.id)" class="btn btn-outline-danger border-0 rounded-3">Удалить</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- МОДАЛЬНОЕ ОКНО -->
      <div v-if="showEditModal" class="custom-overlay" @click="showEditModal = false"></div>
      <div v-if="showEditModal" class="custom-modal-box shadow-lg rounded-4 bg-white p-4">
          <div class="d-flex justify-content-between align-items-center mb-4">
              <h5 class="fw-bold m-0">Редактирование задачи</h5>
              <button class="btn-close" @click="showEditModal = false"></button>
          </div>
          <div class="mb-3">
              <label class="small fw-bold mb-1">Заголовок</label>
              <input v-model="editForm.title" class="form-control border-0 bg-light">
          </div>
          <div class="mb-3">
              <label class="small fw-bold mb-1">Описание</label>
              <textarea v-model="editForm.description" class="form-control border-0 bg-light" rows="3"></textarea>
          </div>
          <div class="mb-4">
              <label class="small fw-bold mb-1">Дедлайн</label>
              <input v-model="editForm.deadline" type="datetime-local" class="form-control border-0 bg-light">
          </div>
          <div class="d-flex gap-2">
            <button @click="handleEditSubmit" class="btn btn-primary w-100 py-2 fw-bold">Сохранить</button>
            <button @click="showEditModal = false" class="btn btn-light py-2 px-4">Отмена</button>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>


import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import katex from 'katex';

function renderMixedContent(str) {
  if (!str) return ''
  const escapeHtml = (text) =>
    text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;')

  const regex = /(\$\$[\s\S]*?\$\$|\$[\s\S]*?\$)/g

  let lastIndex = 0
  let result = ''
  let match

  while ((match = regex.exec(str)) !== null) {
    // Текст до формулы
    const textBefore = str.slice(lastIndex, match.index)
    result += escapeHtml(textBefore)

    // Сама формула (снимаем крайние $$ или $)
    let formula = match[0]
    let displayMode = false
    if (formula.startsWith('$$') && formula.endsWith('$$')) {
      displayMode = true
      formula = formula.slice(2, -2).trim()
    } else if (formula.startsWith('$') && formula.endsWith('$')) {
      formula = formula.slice(1, -1).trim()
    }

    try {
      result += katex.renderToString(formula, {
        throwOnError: false,
        displayMode
      })
    } catch (e) {
      // На случай совсем кривой формулы – выводим как текст
      result += escapeHtml(match[0])
    }

    lastIndex = regex.lastIndex
  }

  // Оставшийся текст после последней формулы
  result += escapeHtml(str.slice(lastIndex))
  return result
}



const todos = ref([])
const filterStatus = ref('all') // Текущий фильтр
const showEditModal = ref(false)
const addForm = ref({ title: '', description: '', deadline: '' })
const AIaddForm = ref({subject: '', topic: '', deadline: ''})
const editForm = ref({ id: '', title: '', description: '', deadline: '', is_done: false })

const getTodos = () => {
  api.get('/api/todos').then(res => { todos.value = res.data.todos })
}

// Вычисляемое свойство для фильтрации списка
const filteredTodos = computed(() => {
  if (filterStatus.value === 'active') return todos.value.filter(t => !t.is_done)
  if (filterStatus.value === 'done') return todos.value.filter(t => t.is_done)
  return todos.value
})


const isAILoading = ref(false)

const AIaddTodo = async () => {
  if (!AIaddForm.value.subject || isAILoading.value) return;
  isAILoading.value = true;
  try {
    await api.post('/api/todos', AIaddForm.value);
    getTodos();
    AIaddForm.value = { subject: '', topic: '', deadline: '' };
  } catch (e) {
    alert('Ошибка генерации задачи');
  } finally {
    isAILoading.value = false;
  }
}

const addTodo = () => {
  if (!addForm.value.title) return;
  api.post('/api/todos', addForm.value).then(() => {
    getTodos();
    addForm.value = { title: '', description: '', deadline: '' };
  });
}

const toggleDone = (todo) => {
  todo.is_done = !todo.is_done;
  api.put(`/api/todos/${todo.id}`, todo).then(() => getTodos());
}

const deleteTodo = (id) => {
  api.delete(`/api/todos/${id}`).then(() => getTodos());
}

const openEditModal = (todo) => {
  editForm.value = { ...todo };
  showEditModal.value = true;
}

const handleEditSubmit = () => {
  api.put(`/api/todos/${editForm.value.id}`, editForm.value).then(() => {
    getTodos();
    showEditModal.value = false;
  });
}

onMounted(getTodos)
</script>
<style scoped>
.main-wrapper{
    min-height:100vh;
    background:#080808;
    color:#f5f5f5;
    padding:40px;
}

/* ---------------- Заголовок ---------------- */

.text-center h1{
    color:#fff;
    font-weight:800;
    font-size:56px;
    letter-spacing:-2px;
}

.text-center p{
    color:#8b8b8b !important;
    font-size:18px;
}

/* ---------------- Карточки ---------------- */

.card{
    background:#070707 !important;

    border:3px solid rgba(208,208,208,.9) !important;
    border-radius:28px !important;

    box-shadow:
        0 0 20px rgba(136,136,136,.65),
        inset 0 0 20px rgba(136,136,136,.22);

    color:white;

    transition:.3s;
}

.task-card:hover{
    transform:translateY(-6px);

    box-shadow:
        0 0 28px rgba(255,255,255,.18),
        inset 0 0 20px rgba(255,255,255,.08);
}

/* ---------------- AI карточка ---------------- */

.AIcard{
    position:relative;
    overflow:hidden;

    background:#070707 !important;

    border:3px solid transparent !important;

    background-image:
        linear-gradient(#070707,#070707),
        linear-gradient(90deg,#7b3ff2,#ff4d4d,#ffbf47);

    background-origin:border-box;
    background-clip:padding-box,border-box;

    box-shadow:
        0 0 30px rgba(140,92,246,.35);
}

.aitext{
    display:flex;
    justify-content:center;
    align-items:center;

    margin-bottom:12px;

    font-size:30px;
    font-weight:700;

    color:white;
}

/* ---------------- Поля ---------------- */

.form-label{
    color:#8b8b8b;
    font-size:13px;
    font-weight:600;
}

.form-control{

    background:#0b0b0b !important;

    color:white !important;

    border:2px solid rgba(105,105,105,.8) !important;

    border-radius:14px !important;

    transition:.25s;
}

.form-control:focus{

    border-color:white !important;

    box-shadow:
        0 0 12px rgba(255,255,255,.15);

    background:#0b0b0b;
}

.form-control::placeholder{
    color:#666;
}

/* ---------------- Кнопки ---------------- */

.btn{

    border-radius:14px !important;

    transition:.25s;
}

.btn:hover{
    transform:translateY(-2px);
}

.btn-primary{

    background:white !important;
    color:#111 !important;
    border:none !important;
}

.btn-light{

    background:#141414 !important;

    color:white !important;

    border:2px solid rgba(105,105,105,.8) !important;
}

.btn-light:hover{

    border-color:white !important;
}

.btn-outline-danger{

    background:transparent !important;

    color:#ff5d5d !important;

    border:2px solid rgba(255,90,90,.5) !important;
}

.btn-outline-danger:hover{

    background:#ff4d4d !important;

    color:white !important;
}

.btn-purple{

    background:linear-gradient(
        90deg,#ffd86b,#7d5d07
    ) !important;

    border:none !important;
}

/* ---------------- Фильтр ---------------- */

.btn-dark{

    background:white !important;

    color:black !important;

    border:none !important;
}

.btn-outline-secondary{

    background:transparent !important;

    color:#999 !important;

    border:2px solid rgba(105,105,105,.8) !important;
}

.btn-outline-secondary:hover{

    color:white !important;

    border-color:white !important;
}

/* ---------------- Задача ---------------- */

.task-card h4{

    color:white;

    font-size:24px;

    font-weight:700;
}

.task-card .text-muted{

    color:#b0b0b0 !important;

    line-height:1.7;
}

.deadline-info{

    color:#8b8b8b;

    border-color:#232323 !important;
}

/* ---------------- Badge ---------------- */

.badge{

    border-radius:999px;

    padding:10px 18px;

    font-size:12px;

    font-weight:700;
}

.bg-primary{

    background:white !important;

    color:#111 !important;
}

.bg-success{

    background:#23c55e !important;
}

/* ---------------- Switch ---------------- */

.form-check-input{

    width:48px;

    height:24px;

    cursor:pointer;

    background-color:#333;

    border:none;
}

.form-check-input:checked{

    background-color:#d4d4d4;

    border:none;
}

/* ---------------- Выполненная ---------------- */

.done-task{

    opacity:.55;

    transform:none !important;
}

.done-task h4,
.done-task .text-muted,
.done-task .deadline-info{

    text-decoration:line-through;

    color:#777 !important;
}

/* ---------------- Модальное окно ---------------- */

.custom-overlay{

    position:fixed;

    inset:0;

    background:rgba(0,0,0,.7);

    backdrop-filter:blur(10px);

    z-index:9998;
}

.custom-modal-box{

    position:fixed;

    top:50%;
    left:50%;

    transform:translate(-50%,-50%);

    width:520px;
    max-width:90%;

    background:#070707 !important;

    color:white;

    border:3px solid rgba(208,208,208,.9);

    border-radius:28px;

    box-shadow:
        0 0 30px rgba(255,255,255,.15),
        inset 0 0 20px rgba(255,255,255,.06);

    z-index:9999;
}

.custom-modal-box textarea{

    resize:none;
}

.btn-close{

    filter:invert(1);
}

/* ---------------- Scroll ---------------- */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#444;
    border-radius:10px;
}

/* ---------------- Responsive ---------------- */

@media(max-width:900px){

    .main-wrapper{
        padding:22px;
    }

    .text-center h1{
        font-size:42px;
    }
}
</style>
