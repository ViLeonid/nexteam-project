<template>
  <div class="calendar-layout-fixed">
    <!-- Форма для быстрого добавления произвольного блока/события -->
    <div class="custom-event-form">
      <h3>Добавить событие</h3>
      
      <input v-model="newEvent.title" type="text" placeholder="Название" class="custom-input" />
      <textarea v-model="newEvent.description" placeholder="Описание" class="custom-textarea"></textarea>
      
      <div class="time-inputs-grid">
        <label>Старт: <input v-model="newEvent.start_time" type="datetime-local" class="custom-input-date" /></label>
        <label>Конец: <input v-model="newEvent.end_time" type="datetime-local" class="custom-input-date" /></label>
      </div>

      <label class="color-label">Цвет блока:
        <select v-model="newEvent.color" class="custom-select">
          <option value="blue">Синий</option>
          <option value="yellow">Желтый</option>
          <option value="purple">Фиолетовый</option>
          <option value="orange">Оранжевый</option>
        </select>
      </label>

      <button @click="submitEvent" class="custom-button">Добавить блок</button>
    </div>

    <!-- Компонент календаря -->
    <div class="calendar-container-fixed">
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
const customEvents = ref([]);

const newEvent = ref({
  title: "",
  description: "",
  start_time: "",
  end_time: "",
  color: "blue"
});

const config = ref({
  locale: "ru-RU",
  defaultMode: "week", // Оставляем режим недели
  showCurrentTime: true,
  style: {
    colorSchemes: {
      blue: { color: '#ffffff', backgroundColor: 'rgba(59, 130, 246, 0.15)', border: '4px solid #3b82f6' },
      yellow: { color: '#ffffff', backgroundColor: 'rgba(234, 179, 8, 0.15)', border: '4px solid #eab308' },
      purple: { color: '#ffffff', backgroundColor: 'rgba(168, 85, 247, 0.15)', border: '4px solid #a855f7' },
      orange: { color: '#ffffff', backgroundColor: 'rgba(249, 115, 22, 0.15)', border: '4px solid #f97316' },
      red: { color: '#ffffff', backgroundColor: 'rgba(239, 68, 68, 0.15)', border: '4px solid #ef4444' },
      green: { color: '#ffffff', backgroundColor: 'rgba(34, 197, 94, 0.15)', border: '4px solid #22c55e' }
    }
  }
});

const formatTime = (dateTimeStr) => {
  if (!dateTimeStr) return "";
  return dateTimeStr.replace("T", " ");
};

const allCalendarBlocks = computed(() => {
  const mappedTodos = todos.value
    .filter(todo => todo.deadline)
    .map(todo => {
      const formattedDeadline = formatTime(todo.deadline);
      return {
        id: `todo-${todo.id}`,
        title: `📌 ${todo.title}`,
        description: todo.description,
        time: { start: formattedDeadline, end: formattedDeadline },
        color: todo.is_done ? "green" : "red",
        isEditable: true
      };
    });

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

const submitEvent = async () => {
  if (!newEvent.value.title || !newEvent.value.start_time || !newEvent.value.end_time) {
    alert("Заполните название и время начала/окончания!");
    return;
  }
  try {
    await axios.post('http://localhost:5000/api/events', newEvent.value);
    newEvent.value = { title: "", description: "", start_time: "", end_time: "", color: "blue" };
    await loadData();
  } catch (error) {
    console.error("Ошибка сохранения события:", error);
  }
};

onMounted(loadData);
</script>

<style>
@import "qalendar/dist/style.css";

/* Базовая раскладка на чистом CSS */
.calendar-layout-fixed {
  display: flex;
  gap: 24px;
  padding: 24px;
  background-color: #0f172a; /* Глубокий темный фон всего экрана */
  min-height: 95vh;
  box-sizing: border-box;
}

/* Красивая темная левая панель */
.custom-event-form {
  width: 320px;
  min-width: 320px;
  padding: 24px;
  border: 1px solid #334155;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: #1e293b; /* Цвет панели */
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  box-sizing: border-box;
  height: fit-content;
}

.custom-event-form h3 {
  margin: 0 0 4px 0;
  color: #ffffff;
  font-size: 18px;
  font-weight: 700;
}

/* Кастомизация полей ввода */
.custom-input, .custom-textarea, .custom-select, .custom-input-date {
  width: 100%;
  padding: 10px 14px;
  background-color: #0f172a;
  border: 1px solid #475569;
  border-radius: 10px;
  color: #ffffff;
  font-family: inherit;
  font-size: 14px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}

.custom-input:focus, .custom-textarea:focus, .custom-select:focus, .custom-input-date:focus {
  border-color: #3b82f6;
}

.custom-textarea {
  resize: none;
  height: 80px;
}

.time-inputs-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.time-inputs-grid label, .color-label {
  color: #94a3b8;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* Красивая кнопка */
.custom-button {
  width: 100%;
  padding: 12px;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}

.custom-button:hover {
  background-color: #1d4ed8;
}

.custom-button:active {
  transform: scale(0.98);
}

/* Контейнер календаря */
.calendar-container-fixed {
  flex-grow: 1;
  height: 85vh;
}

/* Стили самого календаря Qalendar */
.calendar-container-fixed .calendar-root {
  --qalendar-bg-color: #0f172a !important;
  --qalendar-border-color: #334155 !important;
  --qalendar-text-color: #f1f5f9 !important;
  --qalendar-grid-line-color: #1e293b !important;
}

.calendar-root {
  border-radius: 16px !important;
  border: 1px solid #334155 !important;
  overflow: hidden;
}
</style>
