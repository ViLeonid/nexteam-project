<template>
  <div class="analytics-card">
    <h3>Занятость за сегодня</h3>

    <div v-if="loaded" class="chart-wrapper">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>

    <div v-else class="loading">Загрузка данных...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import api from '@/api'

ChartJS.register(ArcElement, Tooltip, Legend)

const loaded = ref(false)
const chartData = ref(null)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',

  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        boxWidth: 8,
        usePointStyle: true,
        padding: 12,
        color: '#e2e8f0',
        font: { size: 12, weight: '500' }
      },
      onClick: function(e, legendItem, legend) {
        // Отменяем стандартное поведение (зачеркивание и скрытие)
        e.native.stopPropagation();
      }
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      padding: 10,
      borderRadius: 8,
      callbacks: {
        label: (ctx) => ` ${ctx.label}: ${ctx.raw} ч.`
      }
    }
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get('/api/analytics/today')

    chartData.value = {
      labels: data.labels,
      datasets: [
        {
          data: data.values,
          backgroundColor: data.colors,
          borderWidth: 0,
          borderColor: '#fff'
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
  width: 400px;
  height: 340px;

  display: flex;
  flex-direction: column;

  background: #000000;
  border-radius: 16px;
  padding: 16px;

}

h3 {
  flex: 0 0 auto;
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
}

.chart-wrapper {
  flex: 1;
  min-height: 0;
  width: 100%;
  position: relative;
}



.loading {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}
</style>