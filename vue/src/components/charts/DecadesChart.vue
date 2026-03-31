<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip } from 'chart.js'
import type { DecadeStat } from '@/types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip)

const props = defineProps<{
  decades: DecadeStat[]
}>()

const chartData = computed(() => ({
  labels: props.decades.map((d) => d.decade),
  datasets: [
    {
      label: 'Albums',
      data: props.decades.map((d) => d.album_count),
      backgroundColor: '#8b5cf6',
      borderRadius: 4,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx: any) => ` ${ctx.parsed.y.toLocaleString()} albums`,
      },
    },
  },
  scales: {
    x: {
      ticks: { color: '#a1a1aa' },
      grid: { display: false },
    },
    y: {
      ticks: { color: '#a1a1aa' },
      grid: { color: '#3f3f46' },
    },
  },
}
</script>

<template>
  <div class="bg-zinc-800 rounded-md p-6">
    <h2 class="text-white font-semibold mb-4">Albums by Decade</h2>
    <div class="h-64">
      <Bar :data="chartData" :options="options" />
    </div>
  </div>
</template>
