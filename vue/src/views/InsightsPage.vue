<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'
import type { InsightsData } from '@/types'
import FormatChart from '@/components/charts/FormatChart.vue'
import GenresChart from '@/components/charts/GenresChart.vue'
import DecadesChart from '@/components/charts/DecadesChart.vue'

const insights = ref<InsightsData | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    insights.value = await api.getInsights()
  } catch (err) {
    console.error('Error loading insights:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="bg-zinc-900 min-h-screen w-full text-white">
    <main class="container mx-auto py-12 px-4 space-y-6">
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-4xl font-bold text-white mb-2 font-serif">Insights</h1>
          <p class="text-zinc-400">A deeper look into your Navidrome library</p>
        </div>
        <RouterLink
          to="/"
          class="flex items-center gap-1 text-sm text-zinc-400 hover:text-white transition-colors mt-1 bg-zinc-800 px-4 py-2 rounded-md font-medium hover:bg-zinc-700"
        >
          <span aria-hidden="true">←</span> Library
        </RouterLink>
      </div>

      <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-for="i in 3" :key="i" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
      </div>

      <template v-else-if="insights">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <FormatChart :format-counts="insights.format_counts"/>
          <DecadesChart :decades="insights.albums_by_decade"/>
        </div>
        <GenresChart :genres="insights.top_genres"/>
      </template>
    </main>
  </div>
</template>
