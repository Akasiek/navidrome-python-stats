<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {api} from '@/services/api'
import type {GenreStat, DecadeStat, ChartData, NeverPlayedData, LibraryStats} from '@/types'
import FormatChart from '@/components/charts/FormatChart.vue'
import GenresChart from '@/components/charts/GenresChart.vue'
import DecadesChart from '@/components/charts/DecadesChart.vue'
import MostProlificArtistsChart from '@/components/charts/MostProlificArtistsChart.vue'
import LongestAlbumsChart from '@/components/charts/LongestAlbumsChart.vue'
import MostPlayedArtistsChart from '@/components/charts/MostPlayedArtistsChart.vue'
import TopPlayedSongsChart from '@/components/charts/TopPlayedSongsChart.vue'
import NeverPlayedChart from '@/components/charts/NeverPlayedChart.vue'
import StarredBreakdownChart from '@/components/charts/StarredBreakdownChart.vue'
import ArtistDominanceChart from '@/components/charts/ArtistDominanceChart.vue'

const topGenres = ref<GenreStat[] | null>(null)
const albumsByDecade = ref<DecadeStat[] | null>(null)
const formatCounts = ref<Record<string, number> | null>(null)
const stats = ref<LibraryStats | null>(null)
const mostProlificArtists = ref<ChartData | null>(null)
const longestAlbums = ref<ChartData | null>(null)
const mostPlayedArtists = ref<ChartData | null>(null)
const topPlayedSongs = ref<ChartData | null>(null)
const neverPlayed = ref<NeverPlayedData | null>(null)
const artistDominance = ref<ChartData | null>(null)

const loadingTopGenres = ref(true)
const loadingAlbumsByDecade = ref(true)
const loadingFormatCounts = ref(true)
const loadingStats = ref(true)
const loadingProlific = ref(true)
const loadingLongest = ref(true)
const loadingMostPlayed = ref(true)
const loadingTopSongs = ref(true)
const loadingNeverPlayed = ref(true)
const loadingDominance = ref(true)

async function fetchSection<T>(
  fetcher: () => Promise<T>,
  target: { value: T | null },
  loading: { value: boolean },
) {
  try {
    target.value = await fetcher()
  } catch (err) {
    console.error('Error loading insights section:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSection(api.getTopGenres, topGenres, loadingTopGenres)
  fetchSection(api.getAlbumsByDecade, albumsByDecade, loadingAlbumsByDecade)
  fetchSection(api.getFormatCounts, formatCounts, loadingFormatCounts)
  fetchSection(api.getStats, stats, loadingStats)
  fetchSection(api.getMostProlificArtists, mostProlificArtists, loadingProlific)
  fetchSection(api.getLongestAlbums, longestAlbums, loadingLongest)
  fetchSection(api.getMostPlayedArtists, mostPlayedArtists, loadingMostPlayed)
  fetchSection(api.getTopPlayedSongs, topPlayedSongs, loadingTopSongs)
  fetchSection(api.getNeverPlayed, neverPlayed, loadingNeverPlayed)
  fetchSection(api.getArtistDominance, artistDominance, loadingDominance)
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

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-if="loadingFormatCounts" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
        <FormatChart v-else-if="formatCounts" :format-counts="formatCounts"/>

        <div v-if="loadingAlbumsByDecade" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
        <DecadesChart v-else-if="albumsByDecade" :decades="albumsByDecade"/>
      </div>

      <div v-if="loadingTopGenres" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
      <GenresChart v-else-if="topGenres" :genres="topGenres"/>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-if="loadingProlific" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
        <MostProlificArtistsChart v-else-if="mostProlificArtists" :data="mostProlificArtists"/>

        <div v-if="loadingMostPlayed" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
        <MostPlayedArtistsChart v-else-if="mostPlayedArtists" :data="mostPlayedArtists"/>
      </div>

      <div v-if="loadingTopSongs" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
      <TopPlayedSongsChart v-else-if="topPlayedSongs" :data="topPlayedSongs"/>

      <div v-if="loadingLongest" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
      <LongestAlbumsChart v-else-if="longestAlbums" :data="longestAlbums"/>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-if="loadingNeverPlayed" class="bg-zinc-800 rounded-md p-6 h-64 animate-pulse"/>
        <NeverPlayedChart v-else-if="neverPlayed" :data="neverPlayed"/>

        <div v-if="loadingStats" class="bg-zinc-800 rounded-md p-6 h-64 animate-pulse"/>
        <StarredBreakdownChart v-else-if="stats" :stats="stats"/>
      </div>

      <div v-if="loadingDominance" class="bg-zinc-800 rounded-md p-6 h-80 animate-pulse"/>
      <ArtistDominanceChart v-else-if="artistDominance" :data="artistDominance"/>
    </main>
  </div>
</template>
