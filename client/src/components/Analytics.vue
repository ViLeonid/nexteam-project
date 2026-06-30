<script setup>
// Импортируем ваши сохраненные компоненты
import ChartsForAnalytics from '@/components/ChartsForAnalytics/todays_time_donut.vue'
import Last_days_hours_of_todos from './ChartsForAnalytics/last_days_hours_of_todos.vue';
import Bar_charts from './ChartsForAnalytics/bar_charts.vue';
</script>

<template>
  <h1>Аналитика</h1>
  <div class="analytics-wrapper">
    <!-- Первые два графика сохраняют свои исходные размеры -->
    <div class="chart-first"><ChartsForAnalytics /></div>
    <div class="chart-second"><Last_days_hours_of_todos /></div>
    
    <!-- Третий график принудительно переносится вниз -->
    <div class="chart-third"><Bar_charts /></div>
  </div>
</template>

<style scoped> /* Исправлено: scoped */
h1 {
  margin: 1vw;
  text-align: center;
}

/* Главный контейнер */
.analytics-wrapper {
  display: flex;
  flex-wrap: wrap; /* Разрешаем перенос на вторую строку */
  margin: 50px;
  gap: 24px;
}

/* Первый график (Пончик): сохраняет фиксированную ширину 400px из своего файла */
.chart-first {
  flex: 0 0 auto; 
}

/* Второй график (Линейный): занимает всё оставшееся свободное место справа */
.chart-second {
  flex: 1 1 0; 
  min-width: 300px; /* Защита от сминания на мелких экранах */
}

/* Третий график (Столбцы): принудительно переносится на вторую строку */
.chart-third {
  flex: 1 1 100%; /* Занимает 100% ширины, поэтому падает вниз */
}
</style>
