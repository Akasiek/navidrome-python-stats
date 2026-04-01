<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import type { ChartData } from '@/types'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{ data: ChartData }>()

const COLORS = [
  '#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
  '#3b82f6', '#ef4444', '#14b8a6', '#f97316', '#a855f7',
  '#52525b',
]

const chartData = computed(() => ({
  labels: props.data.labels,
  datasets: [
    {
      data: props.data.values,
      backgroundColor: COLORS.slice(0, props.data.labels.length),
      borderWidth: 0,
    },
  ],
}))

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: { color: '#a1a1aa', padding: 12, font: { size: 12 }, boxWidth: 12 },
    },
    tooltip: {
      callbacks: {
        label: (ctx: any) => ` ${ctx.label}: ${ctx.parsed.toLocaleString()} albums`,
      },
    },
  },
}
</script>

<template>
  <div class="bg-zinc-800 rounded-md p-6">
    <h2 class="text-white font-semibold mb-4">Artist Dominance</h2>
    <div class="h-72">
      <Doughnut :data="chartData" :options="options" />
    </div>
  </div>
</template>