<template>
  <div class="analytics-card">
    <div class="header">
      <h3>Отдых за 10 дней</h3>
      <span class="subtitle">Часы</span>
    </div>

    <div v-if="loaded" class="chart-wrapper">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
    <div v-else class="loading">Загрузка...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import api from '@/api'
// Обязательно регистрируем модули Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const loaded = ref(false)
const chartData = ref(null)

// 2. Настройки (Опции) диаграммы
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },

  // Все настройки шкал объединяются в один единственный объект scales
  scales: {
    x: {
      ticks: {
        color: '#e2e8f0'         // Цвет оцифровки оси X
      },
      grid: {
        drawOnChartArea: false,  // Отключаем фоновую сетку
        drawTicks: true,         // ВКЛЮЧАЕМ ШТРИХИ
        tickColor: '#e2e8f0',    // Цвет штрихов
        tickLength: 6,           // Длина штрихов в пикселях
        tickWidth: 1             // Толщина штрихов
      },
      border: {
        display: true,           // Включаем саму линию оси X
        color: '#e2e8f0',        // Цвет оси
        width: 1                 // Толщина оси
      }
    },
    y: {
      beginAtZero: true,         // Ось Y начинается с нуля
      ticks: {
        color: '#e2e8f0'         // Цвет оцифровки оси Y
      },
      grid: {
        drawOnChartArea: false,  // Отключаем фоновую сетку
        drawTicks: true,         // ВКЛЮЧАЕМ ШТРИХИ
        tickColor: '#e2e8f0',    // Цвет штрихов
        tickLength: 6,           // Длина штрихов в пикселях
        tickWidth: 1             // Толщина штрихов
      },
      border: {
        display: true,           // Включаем саму линию оси Y
        color: '#e2e8f0',        // Цвет оси
        width: 1                 // Толщина оси
      }
    }
  }
}



onMounted(async () => {
  try {
    const { data } = await api.get('/api/analytics/hours-of-subject')

    chartData.value = {
      labels: data.labels,
      datasets: [
        {
            label: 'Часы отдыха', // Название столбцов в легенде
            data: data.values,
            backgroundColor: '#3b82f6',
            borderRadius: 12,         // Скругляет все углы столбца
            borderSkipped: false,  // Раскомментируйте, если нужно скруглить и нижние углы тоже

            hoverBackgroundColor: '#3b82f6', // Цвет столбца при наведении

        }
      ]
    }

    loaded.value = true
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.analytics-card {

  display: flex;
  flex-direction: column;
  height: 400px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 16px;
}

.header {
  flex: 0 0 auto;
}

h3 {
  margin: 0;
  font-size: 14px;
}

.subtitle {
  font-size: 12px;
  color: #64748b;
}

.chart-wrapper {
  flex: 1;
  min-height: 0;
  position: relative;
}

.chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
}

.loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>