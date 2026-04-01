<script setup lang="ts">
import { computed } from 'vue'
import type { LibraryDurationData } from '@/types'

const props = defineProps<{ data: LibraryDurationData }>()

function formatDuration(seconds: number): string {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  if (days > 0) return `${days}d ${hours}h ${minutes}m`
  if (hours > 0) return `${hours}h ${minutes}m`
  return `${minutes}m`
}

const total = computed(() => formatDuration(props.data.total_seconds))
const avg = computed(() => formatDuration(props.data.avg_album_seconds))
</script>

<template>
  <div class="bg-zinc-800 rounded-md p-6">
    <h2 class="text-white font-semibold mb-6">Library Duration</h2>
    <div class="grid grid-cols-2 gap-4">
      <div class="bg-zinc-700/50 rounded-md p-4">
        <p class="text-zinc-400 text-sm mb-1">Total Duration</p>
        <p class="text-white text-2xl font-bold font-serif">{{ total }}</p>
      </div>
      <div class="bg-zinc-700/50 rounded-md p-4">
        <p class="text-zinc-400 text-sm mb-1">Avg. Album Duration</p>
        <p class="text-white text-2xl font-bold font-serif">{{ avg }}</p>
      </div>
    </div>
  </div>
</template>