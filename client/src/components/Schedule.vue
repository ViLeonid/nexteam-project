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
          <option value="orange">Оранжевый</option>=
          <option value="red">Красный</option>
          <option value="green">Зелёный</option>
        </select>
      </label>
      <div style="display:flex">
        <button @click="submitEvent" class="submit-button">Добавить</button>
        <button @click="cancelEvent" class="cancel-button">Отмена</button>
      </div>
    </div>

    <!-- Компонент календаря с обработчиком клика по времени -->
    <!-- Компонент календаря с обработчиками -->
    <div class="calendar-container-fixed">
      <Qalendar 
        :events="allCalendarBlocks" 
        :config="config" 
        @datetime-was-clicked="handleCalendarClick"
        @event-was-resized="syncUpdatedEvent"
        @event-was-dragged="syncUpdatedEvent"
        @delete-event="handleDeleteEvent"
      />
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

// Чистый объект для сброса формы
const initialEventState = {
  title: "",
  description: "",
  start_time: "",
  end_time: "",
  color: "blue"
};

const newEvent = ref({ ...initialEventState });
const draftEventId = "draft-event-id"; // Фиксированный ID для черновика

const config = ref({
  locale: "ru-RU",
  defaultMode: "week",
  showCurrentTime: true,
  isInteractive: true, // Включает возможность перетаскивания и растягивания блоков
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

const formatToInputDateTime = (date) => {
  const tzOffset = date.getTimezoneOffset() * 60000;
  return new Date(date - tzOffset).toISOString().slice(0, 16);
};

// Клик по пустой ячейке: создаем черновик прямо в массиве событий
const handleCalendarClick = (timeString) => {
  const isoString = timeString.replace(" ", "T");
  const startDate = new Date(isoString);
  const endDate = new Date(startDate.getTime() + 60 * 60 * 1000); // +1 час по умолчанию

  // Заполняем форму слева
  newEvent.value.title = newEvent.value.title || "Новое событие";
  newEvent.value.start_time = isoString;
  newEvent.value.end_time = formatToInputDateTime(endDate);

  // Удаляем старый черновик, если он был, чтобы не плодить копии
  customEvents.value = customEvents.value.filter(ev => ev.id !== draftEventId);

  // Пушим черновик в основной массив для интерактива
  customEvents.value.push({
    id: draftEventId,
    title: newEvent.value.title,
    description: newEvent.value.description,
    start_time: newEvent.value.start_time,
    end_time: newEvent.value.end_time,
    color: newEvent.value.color
  });
};

// Функция синхронизации: когда подергали блок на календаре, обновляем форму и массив
const syncUpdatedEvent = (updatedEvent) => {
  const startISO = updatedEvent.time.start.replace(" ", "T");
  const endISO = updatedEvent.time.end.replace(" ", "T");

  // Если это наш черновик — обновляем форму слева
  if (updatedEvent.id === draftEventId) {
    newEvent.value.start_time = startISO;
    newEvent.value.end_time = endISO;
  }

  // Обновляем объект внутри массива customEvents
  const target = customEvents.value.find(ev => ev.id === updatedEvent.id || `event-${ev.id}` === updatedEvent.id);
  if (target) {
    target.start_time = startISO;
    target.end_time = endISO;
  }
};

// Сюда транслируется массив для отображения
const allCalendarBlocks = computed(() => {
  const mappedEvents = customEvents.value.map(ev => ({
    id: ev.id === draftEventId ? draftEventId : `event-${ev.id}`,
    title: ev.id === draftEventId ? newEvent.value.title : ev.title, // Синхроним ввод текста на лету
    description: ev.id === draftEventId ? newEvent.value.description : ev.description,
    time: { start: formatTime(ev.start_time), end: formatTime(ev.end_time) },
    colorScheme: ev.id === draftEventId ? newEvent.value.color : ev.color,
    isEditable: true // Разрешаем редактирование и растягивание
  }));
  console.log('events',mappedEvents);

  return mappedEvents;
});
const handleDeleteEvent = async (event) => {
  const id = event.replace("event-","")
  console.log(id);
  await axios.delete(
    `http://localhost:5000/api/events/${id}`
  );

  await loadData();
};

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
    // Отправляем чистый объект без временного id
    const payload = {
      title: newEvent.value.title,
      description: newEvent.value.description,
      start_time: newEvent.value.start_time,
      end_time: newEvent.value.end_time,
      color: newEvent.value.color
    };
    
    await axios.post('http://localhost:5000/api/events', payload);
    newEvent.value = { ...initialEventState };
    await loadData(); // Перезагрузит данные, затерев временный черновик
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
.submit-button {
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

.submit-button:hover {
  background-color: #1d4ed8;
}

.submit-button:active {
  transform: scale(0.98);
}

.cancel-button{
  width: 100%;
  padding: 12px;
  background-color: #585858;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  box-shadow: 0 4px 6px -1px rgba(85, 85, 85, 0.2);
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
