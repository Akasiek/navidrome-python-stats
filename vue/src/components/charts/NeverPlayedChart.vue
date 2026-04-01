<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import type { NeverPlayedData } from '@/types'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{ data: NeverPlayedData }>()

const albumsChartData = computed(() => ({
  labels: ['Played', 'Never Played'],
  datasets: [
    {
      data: [props.data.albums_played, props.data.albums_never_played],
      backgroundColor: ['#10b981', '#3f3f46'],
      borderWidth: 0,
    },
  ],
}))

const songsChartData = computed(() => ({
  labels: ['Played', 'Never Played'],
  datasets: [
    {
      data: [props.data.songs_played, props.data.songs_never_played],
      backgroundColor: ['#6366f1', '#3f3f46'],
      borderWidth: 0,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { color: '#a1a1aa', padding: 16, font: { size: 12 } },
    },
    tooltip: {
      callbacks: {
        label: (ctx: any) => ` ${ctx.label}: ${ctx.parsed.toLocaleString()}`,
      },
    },
  },
}
</script>

<template>
  <div class="bg-zinc-800 rounded-md p-6">
    <h2 class="text-white font-semibold mb-4">Never Played</h2>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <p class="text-zinc-400 text-sm text-center mb-2">Albums</p>
        <div class="h-48">
          <Doughnut :data="albumsChartData" :options="options" />
        </div>
      </div>
      <div>
        <p class="text-zinc-400 text-sm text-center mb-2">Songs</p>
        <div class="h-48">
          <Doughnut :data="songsChartData" :options="options" />
        </div>
      </div>
    </div>
  </div>
</template>