<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{
  formatCounts: Record<string, number>
}>()

const COLORS = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe', '#f5f3ff']

const chartData = computed(() => {
  const entries = Object.entries(props.formatCounts)
  return {
    labels: entries.map(([fmt]) => fmt.toUpperCase()),
    datasets: [
      {
        data: entries.map(([, count]) => count),
        backgroundColor: COLORS.slice(0, entries.length),
        borderWidth: 0,
      },
    ],
  }
})

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
    <h2 class="text-white font-semibold mb-4">Format Distribution</h2>
    <div class="h-64">
      <Doughnut :data="chartData" :options="options" />
    </div>
  </div>
</template>
