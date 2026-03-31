<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'
import type { LibraryStats } from '@/types'

const stats = ref<LibraryStats | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    stats.value = await api.getStats()
  } catch (err) {
    console.error('Error loading stats:', err)
  } finally {
    loading.value = false
  }
})

interface StatCard {
  label: string
  key: keyof LibraryStats
}

const primaryCards: StatCard[] = [
  { label: 'Artists', key: 'artist_count' },
  { label: 'Albums', key: 'album_count' },
  { label: 'Songs', key: 'song_count' },
]

const secondaryCards: StatCard[] = [
  { label: 'Starred Artists', key: 'starred_artist_count' },
  { label: 'Starred Albums', key: 'starred_album_count' },
  { label: 'Starred Songs', key: 'starred_song_count' },
  { label: 'Playlists', key: 'playlist_count' },
]
</script>

<template>
  <section>
    <h1 class="text-4xl font-bold text-white mb-2">Navidrome Python Stats</h1>
    <p class="text-zinc-400 mb-8">An overview of your Navidrome collection</p>
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
      <div
        v-for="card in primaryCards"
        :key="card.key"
        class="bg-zinc-800 rounded-md p-7 flex flex-col gap-1"
      >
        <span class="text-zinc-400 text-sm font-medium">{{ card.label }}</span>
        <span v-if="loading" class="h-10 w-24 bg-zinc-700 rounded animate-pulse mt-1"/>
        <span v-else class="text-5xl font-bold text-white">
          {{ stats ? stats[card.key].toLocaleString() : '—' }}
        </span>
      </div>
    </div>
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="card in secondaryCards"
        :key="card.key"
        class="bg-zinc-800 rounded-md p-5 flex flex-col gap-1"
      >
        <span class="text-zinc-400 text-sm font-medium">{{ card.label }}</span>
        <span v-if="loading" class="h-8 w-20 bg-zinc-700 rounded animate-pulse mt-1"/>
        <span v-else class="text-3xl font-bold text-white">
          {{ stats ? stats[card.key].toLocaleString() : '—' }}
        </span>
      </div>
    </div>
  </section>
</template>
