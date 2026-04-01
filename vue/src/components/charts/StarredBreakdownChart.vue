<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import type { LibraryStats } from '@/types'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{ stats: LibraryStats }>()

function makeChart(starred: number, total: number, color: string) {
  return {
    labels: ['Starred', 'Unstarred'],
    datasets: [
      {
        data: [starred, total - starred],
        backgroundColor: [color, '#3f3f46'],
        borderWidth: 0,
      },
    ],
  }
}

const albumsChart = computed(() =>
  makeChart(props.stats.starred_album_count, props.stats.album_count, '#f59e0b'),
)
const songsChart = computed(() =>
  makeChart(props.stats.starred_song_count, props.stats.song_count, '#ec4899'),
)
const artistsChart = computed(() =>
  makeChart(props.stats.starred_artist_count, props.stats.artist_count, '#10b981'),
)

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { color: '#a1a1aa', padding: 12, font: { size: 11 } },
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
    <h2 class="text-white font-semibold mb-4">Starred Breakdown</h2>
    <div class="grid grid-cols-3 gap-4">
      <div>
        <p class="text-zinc-400 text-sm text-center mb-2">Albums</p>
        <div class="h-40">
          <Doughnut :data="albumsChart" :options="options" />
        </div>
      </div>
      <div>
        <p class="text-zinc-400 text-sm text-center mb-2">Songs</p>
        <div class="h-40">
          <Doughnut :data="songsChart" :options="options" />
        </div>
      </div>
      <div>
        <p class="text-zinc-400 text-sm text-center mb-2">Artists</p>
        <div class="h-40">
          <Doughnut :data="artistsChart" :options="options" />
        </div>
      </div>
    </div>
  </div>
</template>