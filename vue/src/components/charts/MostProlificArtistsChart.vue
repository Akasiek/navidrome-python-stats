<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip } from 'chart.js'
import type { ChartData } from '@/types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip)

const props = defineProps<{ data: ChartData }>()

const chartData = computed(() => ({
  labels: props.data.labels,
  datasets: [
    {
      label: 'Albums',
      data: props.data.values,
      backgroundColor: '#10b981',
      borderRadius: 4,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y' as const,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx: any) => ` ${ctx.parsed.x} albums`,
      },
    },
  },
  scales: {
    x: {
      ticks: { color: '#a1a1aa' },
      grid: { color: '#3f3f46' },
    },
    y: {
      ticks: { color: '#a1a1aa' },
      grid: { display: false },
    },
  },
}
</script>

<template>
  <div class="bg-zinc-800 rounded-md p-6">
    <h2 class="text-white font-semibold mb-4">Most Prolific Artists</h2>
    <div class="h-96">
      <Bar :data="chartData" :options="options" />
    </div>
  </div>
</template>