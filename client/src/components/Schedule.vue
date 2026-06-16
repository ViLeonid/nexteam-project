<template>

<div class="calendar-layout-fixed">
    <div class="qalendar-holder">

        <addEventForm 
            v-model:newEvent="newEvent"
            v-show="isFormActive"
            class="calendar-form-overlay"
         />

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
import addEventForm from "./addEventForm.vue";
import { ref, onMounted, computed, nextTick, provide } from "vue";
import { Qalendar } from "qalendar";
import api from '@/api';

api.defaults.withCredentials = true;

const todos = ref([]);
const customEvents = ref([]);
const isFormActive = ref(false);

// Чистый объект для сброса формы
const initialEventState = {
  title: "Новое событие",
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
      blue: { color: '#ffffff', backgroundColor: 'rgba(59, 130, 246, 0.5)', border: '4px solid #3b82f6' },
      yellow: { color: '#ffffff', backgroundColor: 'rgba(234, 179, 8, 0.5)', border: '4px solid #eab308' },
      purple: { color: '#ffffff', backgroundColor: 'rgba(168, 85, 247, 0.5)', border: '4px solid #a855f7' },
      orange: { color: '#ffffff', backgroundColor: 'rgba(249, 115, 22, 0.5)', border: '4px solid #f97316' },
      red: { color: '#ffffff', backgroundColor: 'rgba(239, 68, 68, 0.5)', border: '4px solid #ef4444' },
      green: { color: '#ffffff', backgroundColor: 'rgba(34, 197, 94, 0.5)', border: '4px solid #22c55e' }
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


// Переменные для контроля положения скролла
const savedScrollPosition = ref(0);

// Ищет контейнер скролла внутри Qalendar
const getScrollElement = () => {
  return document.querySelector('.calendar-week__wrapper')
      || document.querySelector('.calendar-body__time-grid')
      || document.querySelector('[class*="__wrapper"].ps');
};

// ФУНКЦИЯ 1: Запоминает, где сейчас находится скролл (вызывается ДО обновления данных)
const saveCurrentScroll = () => {
  const scrollElement = getScrollElement();
  if (scrollElement) {
    savedScrollPosition.value = scrollElement.scrollTop;
  }
};

// ФУНКЦИЯ 2: Возвращает скролл на сохраненное место БЕЗ дёргания
const restoreSavedScroll = async () => {
  await nextTick();
  
  // requestAnimationFrame срабатывает ДО того, как браузер отрисует кадр на экране.
  // Это убирает эффект визуального прыжка скролла.
  requestAnimationFrame(() => {
    const scrollElement = getScrollElement();
    if (scrollElement && savedScrollPosition.value > 0) {
      
      // Мгновенно выставляем сохраненную позицию
      scrollElement.scrollTop = savedScrollPosition.value;
      
      // Дополнительно дублируем через scrollTo, чтобы плагин Perfect Scrollbar подхватил позицию
      scrollElement.scrollTo({
        top: savedScrollPosition.value,
        behavior: 'instant' // Используем мгновенный скролл вместо 'auto' или 'smooth'
      });
      
    }
  });
};

// Функция обновления текста о прокрутке при обычном скролле мышкой


// Клик по пустой ячейке: создаем черновик прямо в массиве событий
const handleCalendarClick = (timeString) => {
  // Запоминаем скролл перед изменением реактивного массива
  saveCurrentScroll();
  isFormActive.value = true;
  console.log(isFormActive.value);
  
  const isoString = timeString.replace(" ", "T");
  const firstDate = new Date(isoString);
  const startDate = new Date(firstDate.setMinutes(Math.round(firstDate.getMinutes()/15)*15));
  const endDate = new Date(startDate.getTime() + 60 * 60 * 1000); 

  // Заполняем форму слева
  newEvent.value.title = newEvent.value.title || "Новое событие";
  newEvent.value.start_time = formatToInputDateTime(startDate);
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
  // Восстанавливаем скролл, чтобы сетка времени не прыгала вверх
  restoreSavedScroll();
};

// Функция синхронизации: когда подергали или растянули блок на календаре
const syncUpdatedEvent = async (updatedEvent) => {
  // 1. Мгновенно запоминаем скролл, прежде чем Vue начнет мутировать массив
  saveCurrentScroll();

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

  // 2. Возвращаем скролл на место в следующем кадре анимации
  await restoreSavedScroll();
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

  return mappedEvents;
});

// Удаление события
// Удаление события
const handleDeleteEvent = async (event) => {
  // Запоминаем скролл перед удалением

  saveCurrentScroll();
  // Очищаем ID от префикса библиотеки Qalendar
  
  const id = event.replace("event-", "");
  
  if (id === draftEventId.replace("event-", "")) {
    
    customEvents.value = customEvents.value.filter(ev => ev.id !== draftEventId);
    newEvent.value = { ...initialEventState };
    await restoreSavedScroll();
    return; 
  }

  try {
    await api.delete(`/api/events/${id}`);
    await loadData();
  } catch (error) {
    console.error("Ошибка при удалении события с сервера:", error);
  }
};



// Загрузка данных с бэкенда
const loadData = async () => {
  try {
    // Перед запросом запоминаем, где стоял скролл у пользователя
    saveCurrentScroll();

    const [todosRes, eventsRes] = await Promise.all([
      api.get('/api/todos'),
      api.get('/api/events')
    ]);
    if (todosRes.data?.todos) todos.value = todosRes.data.todos;
    if (eventsRes.data?.events) customEvents.value = eventsRes.data.events;

    // После обновления данных возвращаем скролл на то же самое место
    await restoreSavedScroll();
  } catch (error) {
    console.error("Ошибка при обновлении данных:", error);
  }
};
provide('loadData', loadData);
provide('restoreSavedScroll', restoreSavedScroll);
provide('saveCurrentScroll', saveCurrentScroll);
provide('newEvent', newEvent);
provide('draftEventId', draftEventId);
provide('customEvents', customEvents);
provide('isFormActive', isFormActive)
onMounted(async () => {
  // Первичная загрузка данных
  await loadData();
});
</script>

<style>
@import "qalendar/dist/style.css";

/* Главный контейнер на весь экран */
.calendar-layout-fixed {
  display: flex;
  gap: 24px;
  padding: 24px;
  background-color: #0f172a; /* Глубокий темный фон всего экрана */
  height: 100vh;             /* Строго высота экрана */
  max-height: 100vh;
  box-sizing: border-box;
  overflow: hidden;          /* Запрещаем скролл самого экрана */
}

/* Обертка для левой панели */
.sidebar-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 320px;
  min-width: 320px;
  z-index: 10;
}

/* Кнопки управления скроллом */
.controls {
  display: flex;
  gap: 12px;
}
.scroll-btn {
  flex: 1;
  padding: 10px;
  background-color: #1e293b;
  border: 1px solid #334155;
  color: #ffffff;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  transition: all 0.2s;
}
.scroll-btn:hover {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

/* Правая часть: Календарь забирает ВСЁ оставшееся место */
.calendar-layout-fixed {
    width: 100%;
    height: 100vh;
    padding: 0;
    margin: 0;
    overflow: hidden;
}

.qalendar-holder {
    width: 100%;
    height: 100vh;
    position: relative;
}

.calendar-form-overlay {
    position: absolute;
    top: 80px;
    right: 20px;

    width: 320px;
    z-index: 9999;

    background: #1e293b;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,.35);
}
/* Красивая темная левая форма (оставляем ваши стили, убирая лишнее) */


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

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.scroll-info {
  margin-top: 8px;
  padding: 10px;
  background-color: #1e293b;
  border: 1px dashed #475569;
  border-radius: 10px;
  color: #94a3b8;
  font-size: 13px;
  text-align: center;
}

.scroll-info span {
  color: #3b82f6; /* Подсветим пиксели синим цветом */
  font-weight: bold;
}

</style>
