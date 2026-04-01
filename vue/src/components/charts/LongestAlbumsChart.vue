<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip } from 'chart.js'
import type { ChartData } from '@/types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip)

const props = defineProps<{ data: ChartData }>()

function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  return h > 0 ? `${h}h ${m}m` : `${m}m`
}

const chartData = computed(() => ({
  labels: props.data.labels,
  datasets: [
    {
      label: 'Duration',
      data: props.data.values.map((s) => Math.round(s / 60)),
      backgroundColor: '#f59e0b',
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
        label: (ctx: any) => ` ${formatDuration(props.data.values[ctx.dataIndex])}`,
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#a1a1aa',
        callback: (value: any) => `${value}m`,
      },
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
    <h2 class="text-white font-semibold mb-4">Longest Albums</h2>
    <div class="h-96">
      <Bar :data="chartData" :options="options" />
    </div>
  </div>
</template>