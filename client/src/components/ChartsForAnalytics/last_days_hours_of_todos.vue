<template>
  <div class="analytics-card">
    <div class="header">
      <h3>Активность за 10 дней</h3>
      <span class="subtitle">Часы задач</span>
    </div>

    <div v-if="loaded" class="chart-wrapper">
      <Line :data="chartData" :options="chartOptions" />
    </div>

    <div v-else class="loading">Загрузка...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
} from 'chart.js'
import api from '@/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
)

const loaded = ref(false)
const chartData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  },
  scales: {
    x: { grid: { display: false } },
    y: { beginAtZero: true }
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get('/api/analytics/tasks-last-10-days')

    chartData.value = {
      labels: data.labels,
      datasets: [
        {
          data: data.values,
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99,102,241,0.15)',
          fill: true,
          tension: 0.4
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
  height: 340px;
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