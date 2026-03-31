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
  badgeKey?: keyof LibraryStats
  badgeLabel?: string
}

const primaryCards: StatCard[] = [
  { label: 'Songs', key: 'song_count', badgeKey: 'starred_song_count', badgeLabel: 'starred' },
  { label: 'Albums', key: 'album_count', badgeKey: 'starred_album_count', badgeLabel: 'starred' },
  {
    label: 'Artists',
    key: 'artist_count',
    badgeKey: 'starred_artist_count',
    badgeLabel: 'starred',
  },
]

const secondaryCards: StatCard[] = [
  { label: 'Genres', key: 'genre_count' },
  { label: 'Playlists', key: 'playlist_count' },
  { label: 'Radio Stations', key: 'radio_station_count' },
]
</script>

<template>
  <section>
    <div class="flex items-start justify-between mb-8">
      <div>
        <h1 class="text-4xl font-bold text-white mb-2 font-serif">Navidrome Python Stats</h1>
        <p class="text-zinc-400 font-sans">An overview of your Navidrome collection</p>
      </div>
      <RouterLink
        to="/insights"
        class="flex items-center gap-1 text-sm text-zinc-400 hover:text-white transition-colors mt-1 bg-zinc-800 px-4 py-2 rounded-md font-medium hover:bg-zinc-700"
      >
        Insights <span aria-hidden="true">→</span>
      </RouterLink>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
      <div
        v-for="card in primaryCards"
        :key="card.key"
        class="bg-zinc-800 rounded-md p-7 flex flex-col gap-1"
      >
        <p class="text-zinc-400 text-sm font-medium">{{ card.label }}</p>
        <p v-if="loading" class="h-10 w-24 bg-zinc-700 rounded animate-pulse mt-1"/>
        <p v-else class="text-5xl font-bold text-white font-serif">
          {{ stats ? stats[card.key].toLocaleString() : '—' }}
        </p>

        <div class="flex gap-2 mt-2 flex-wrap -mb-2">
          <template v-if="loading">
            <span class="h-5 w-20 bg-zinc-700 rounded-full animate-pulse"/>
          </template>
          <template v-else-if="stats">
            <span
              v-if="card.badgeKey"
              class="text-xs font-medium bg-zinc-700 text-zinc-300 rounded-full px-2 py-0.5"
            >
              ★ {{ (stats[card.badgeKey] as number).toLocaleString() }} {{ card.badgeLabel }}
            </span>
            <template v-if="card.key === 'song_count'">
              <span
                v-for="(count, format) in stats.format_counts"
                :key="format"
                class="text-xs font-medium bg-zinc-700 text-zinc-300 rounded-full px-2 py-0.5"
              >
                {{ String(format).toUpperCase() }} {{ count.toLocaleString() }}
              </span>
            </template>
          </template>
        </div>
      </div>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div
        v-for="card in secondaryCards"
        :key="card.key"
        class="bg-zinc-800 rounded-md p-5 flex flex-col gap-1"
      >
        <span class="text-zinc-400 text-sm font-medium">{{ card.label }}</span>
        <span v-if="loading" class="h-8 w-20 bg-zinc-700 rounded animate-pulse mt-1"/>
        <span v-else class="text-3xl font-bold text-white font-serif">
          {{ stats ? stats[card.key].toLocaleString() : '—' }}
        </span>
      </div>
    </div>
  </section>
</template>
