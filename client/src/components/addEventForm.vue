<template>
    <div class="custom-event-form" ref="formRef">
      <h3>Добавить событие</h3>
      
      <!-- Убрали props. везде -->
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
          <option value="red">Красный</option>
          <option value="green">Зелёный</option>
        </select>
      </label>
      <div style="display:flex; gap: 10px; margin-top: 10px;">
        <button @click="submitEvent" class="submit-button">Добавить</button>
        <button @click="cancelEvent" class="cancel-button">Отмена</button>
      </div>
    </div>
</template>


<script setup>
import { ref, inject, nextTick } from "vue";
import api from '@/api';

// Инжектируем всё необходимое из родителя (Schedule.vue)
const loadData = inject('loadData');
const restoreSavedScroll = inject('restoreSavedScroll');
const saveCurrentScroll = inject('saveCurrentScroll');
const newEvent = inject('newEvent'); // Теперь меняем форму напрямую без props!
const draftEventId = inject('draftEventId');
const customEvents = inject('customEvents');
const isFormActive = inject('isFormActive');

api.defaults.withCredentials = true;

// Начальное состояние для сброса
const initialEventState = {
  title: "Новое событие",
  description: "",
  start_time: "",
  end_time: "",
  color: "blue"
};
const getScrollElement = () => {
  return document.querySelector('.calendar-week__wrapper')
      || document.querySelector('.calendar-body__time-grid')
      || document.querySelector('[class*="__wrapper"].ps');
};
const submitEvent = async () => {
  if (
    !newEvent.value.title ||
    !newEvent.value.start_time ||
    !newEvent.value.end_time
  ) {
    alert("Заполните название и время начала/окончания!");
    return;
  }

  try {
    const payload = {
      title: newEvent.value.title,
      description: newEvent.value.description,
      start_time: newEvent.value.start_time,
      end_time: newEvent.value.end_time,
      color: newEvent.value.color
    };

    const { data } = await api.post("/api/events", payload);

    // удаляем черновик
    customEvents.value = customEvents.value.filter(
      ev => ev.id !== draftEventId
    );

    // сразу добавляем настоящее событие
    saveCurrentScroll();

    customEvents.value.push({
        id: data.id,
        title: payload.title,
        description: payload.description,
        start_time: payload.start_time,
        end_time: payload.end_time,
        color: payload.color
    });

    await nextTick();

    restoreSavedScroll();
    console.log(getScrollElement().scrollTop);
      await nextTick();
      console.log(getScrollElement().scrollTop);
      setTimeout(() => {
          console.log(getScrollElement().scrollTop);
      }, 0);
      setTimeout(() => {
          console.log(getScrollElement().scrollTop);
      }, 100);

    // очищаем форму
    newEvent.value = { ...initialEventState };

    isFormActive.value = false;
  }
  catch (error) {
    console.error(error);
  }
};


const cancelEvent = () => {
  saveCurrentScroll();

  // Удаляем черновик из календаря при отмене
  customEvents.value = customEvents.value.filter(ev => ev.id !== draftEventId);
  
  // Обнуляем поля формы
  newEvent.value = { ...initialEventState };
  
  restoreSavedScroll();
  isFormActive.value = false;

};
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
  width: 330px;
  height: 540px;
  position: absolute;
  padding: 24px;
  border: 1px solid #334155;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background-color: #1e293b; /* Цвет панели */
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  box-sizing: border-box;
  z-index: 1;
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
