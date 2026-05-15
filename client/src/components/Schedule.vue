<template>
  <div class="calendar-layout">
    <!-- Форма для быстрого добавления произвольного блока/события -->
    <div class="event-form">
      <h3>Добавить событие в календарь</h3>
      <input v-model="newEvent.title" type="text" placeholder="Название" />
      <textarea v-model="newEvent.description" placeholder="Описание"></textarea>
      
      <div class="time-inputs">
        <label>Старт: <input v-model="newEvent.start_time" type="datetime-local" /></label>
        <label>Конец: <input v-model="newEvent.end_time" type="datetime-local" /></label>
      </div>

      <label>Цвет:
        <select v-model="newEvent.color">
          <option value="blue">Синий</option>
          <option value="yellow">Желтый</option>
          <option value="purple">Фиолетовый</option>
          <option value="orange">Оранжевый</option>
        </select>
      </label>

      <button @click="submitEvent">Добавить блок</button>
    </div>

    <!-- Компонент календаря -->
    <div class="calendar-container">
      <Qalendar :events="allCalendarBlocks" :config="config" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { Qalendar } from "qalendar";
import axios from "axios";

axios.defaults.withCredentials = true;

const todos = ref([]);
const customEvents = ref([]); // Массив для чистых событий из БД

const newEvent = ref({
  title: "",
  description: "",
  start_time: "",
  end_time: "",
  color: "blue"
});

const config = ref({
  locale: "ru-RU",
  defaultMode: "month"
});

// Метод генерации эндпоинта для задач (как в прошлом ответе)

// Перевод формата бэкенда (YYYY-MM-DDTHH:mm) в формат Qalendar (YYYY-MM-DD HH:mm)
const formatTime = (dateTimeStr) => {
  if (!dateTimeStr) return "";
  return dateTimeStr.replace("T", " ");
};

// ГЛАВНОЕ: Объединение задач и кастомных событий
const allCalendarBlocks = computed(() => {
  // Форматируем задачи (Todos)
  const mappedTodos = todos.value
    .filter(todo => todo.deadline)
    .map(todo => {
      const formattedDeadline = formatTime(todo.deadline);
      
      return {
        id: `todo-${todo.id}`,
        title: `📌 [ЗАДАЧА] ${todo.title}`,
        description: todo.description,
        time: { 
          start: formattedDeadline, 
          // Ставим время окончания равным времени начала, чтобы задача стояла «на одном конкретном времени»
          end: formattedDeadline 
        },
        color: todo.is_done ? "green" : "red",
        isEditable: true
      };
    });

  // Форматируем произвольные блоки (Events)
  const mappedEvents = customEvents.value.map(ev => ({
    id: `event-${ev.id}`,
    title: ev.title,
    description: ev.description,
    time: { start: formatTime(ev.start_time), end: formatTime(ev.end_time) },
    color: ev.color,
    isEditable: true
  }));

  return [...mappedTodos, ...mappedEvents];
});


// Загрузка всех данных с бэкенда
const loadData = async () => {
  try {
    const [todosRes, eventsRes] = await Promise.all([
      axios.get('http://localhost:5000/todos'),
      axios.get('http://localhost:5000/api/events')
    ]);
    
    if (todosRes.data?.todos) todos.value = todosRes.data.todos;
    if (eventsRes.data?.events) customEvents.value = eventsRes.data.events;
  } catch (error) {
    console.error("Ошибка при обновлении данных:", error);
  }
};

// Отправка нового события на бэкенд
const submitEvent = async () => {
  if (!newEvent.value.title || !newEvent.value.start_time || !newEvent.value.end_time) {
    alert("Заполните название и время начала/окончания!");
    return;
  }
  try {
    await axios.post('http://localhost:5000/api/events', newEvent.value);
    // Сброс формы
    newEvent.value = { title: "", description: "", start_time: "", end_time: "", color: "blue" };
    // Перезагрузка данных
    await loadData();
  } catch (error) {
    console.error("Ошибка сохранения события:", error);
  }
};

onMounted(loadData);
</script>

<style>
@import "qalendar/dist/style.css";

.calendar-layout {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.event-form {
  width: 300px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: #f9f9f9;
}

.event-form input, .event-form textarea, .event-form select, .event-form button {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.time-inputs label {
  font-size: 12px;
  display: block;
  margin-top: 5px;
}

.calendar-container {
  flex-grow: 1;
  height: 85vh;
}
</style>
