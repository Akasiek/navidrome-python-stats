<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip } from 'chart.js'
import type { GenreStat } from '@/types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip)

const props = defineProps<{
  genres: GenreStat[]
}>()

const chartData = computed(() => ({
  labels: props.genres.map((g) => g.name),
  datasets: [
    {
      label: 'Songs',
      data: props.genres.map((g) => g.song_count),
      backgroundColor: '#6366f1',
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
        label: (ctx: any) => ` ${ctx.parsed.x.toLocaleString()} songs`,
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
    <h2 class="text-white font-semibold mb-4">Top Genres</h2>
    <div class="h-96">
      <Bar :data="chartData" :options="options" />
    </div>
  </div>
</template>
