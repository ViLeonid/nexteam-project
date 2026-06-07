<template>
  <div class="analytics-wrapper">
    <!-- Карточка 1: Сегодняшняя занятость -->
    <div class="chart-box light-minimal">
      <h3>Занятость за сегодня</h3>
      <div v-if="loaded" class="chart-wrapper">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>
      <div v-else class="loading">Загрузка данных...</div>
    </div>

    <!-- Пример Карточки 2 (для проверки сетки слева направо) -->
    <div class="chart-box light-minimal dummy-card">
      <h3>Общий баланс сил</h3>
      <div class="chart-wrapper dummy-content">
        <span>Здесь будет следующий график</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const loaded = ref(false)
const chartData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%', // Аккуратное тонкое кольцо
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        boxWidth: 8,
        usePointStyle: true, // Аккуратные точки вместо квадратов
        padding: 15,
        color: '#4b5563', // Спокойный серый текст подписей (Tailwind gray-600)
        font: { family: 'Inter, sans-serif', size: 12, weight: '500' }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.95)', // Элегантный темный тултип
      padding: 12,
      borderRadius: 8,
      titleFont: { size: 13, weight: 'bold' },
      bodyFont: { size: 12 },
      callbacks: {
        label: (context) => {
          if (context.label === "Свободный день") return " Отдых 24 ч.";
          return ` ${context.label}: ${context.raw} ч.`;
        }
      }
    }
  }
}

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:5000/api/analytics/today', {
      credentials: 'include'
    })
    const result = await response.json()

    chartData.value = {
      labels: result.labels,
      datasets: [
        {
          data: result.values,
          backgroundColor: result.colors, // Пастельные цвета вернутся из вашего Flask
          borderWidth: 4, // Красивый белый разделитель секторов
          borderColor: '#ffffff'
        }
      ]
    }
    
    loaded.value = true
  } catch (error) {
    console.error("Ошибка загрузки аналитики:", error)
  }
})
</script>

<style scoped>
/* Главный контейнер-сетка: карточки идут слева направо и переносятся вниз */
.analytics-wrapper {
  margin: 0;
  display: flex;
  flex-direction: row;     /* Направление: слева направо */
  flex-wrap: wrap;         /* Перенос на новую строку сверху вниз */
  gap: 24px;               /* Расстояние между карточками */
  width: 100%;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc;
  box-sizing: border-box;
  padding: 40px;
  align-content: flex-start; /* Прижимает строки к верху страницы */
}

/* Светлая минималистичная карточка */
.light-minimal {
  background: #ffffff;
  border: 1px solid #e2e8f0; /* Едва заметная серая граница */
  padding: 24px;
  border-radius: 16px;
  width: 100%;
  max-width: 340px; /* Фиксированная базовая ширина карточки */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03); /* Очень мягкая тень */
  box-sizing: border-box;
}

h3 {
  margin: 0 0 16px 0;
  color: #1e293b; /* Глубокий slate-цвет для текста */
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.3px;
}

.chart-wrapper {
  position: relative;
  height: 220px;
  width: 100%;
}

.loading {
  text-align: center;
  color: #94a3b8;
  padding: 50px 0;
  font-size: 14px;
}

/* Стили для временной второй карточки (можно удалить) */
.dummy-card {
  display: flex;
  flex-direction: column;
}
.dummy-content {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
  color: #94a3b8;
  font-size: 14px;
}
</style>
