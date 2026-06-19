<script setup>
// Импортируем ваш сохраненный компонент
import ChartsForAnalytics from '@/components/ChartsForAnalytics/todays_time_donut.vue'
import Last_days_hours_of_todos from './ChartsForAnalytics/last_days_hours_of_todos.vue';
</script>

<template>
  
  <h1>Аналитика</h1>
  <div class="analytics-wrapper">
    <ChartsForAnalytics />
    <Last_days_hours_of_todos />
  </div>
</template>
<style scooped>
/* Главный контейнер-сетка: карточки идут слева направо и переносятся вниз */
.analytics-wrapper {
  display: flex;
  margin: 50px;
  gap: 24px;
}
h1 {
  margin: 1vw;
  text-align: center;
}
</style>