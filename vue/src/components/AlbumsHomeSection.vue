<script setup lang="ts">
import type { Album, AlbumsResponse } from '@/types'
import { onMounted, ref } from "vue";
import { api } from "@/services/api.ts";
import AlbumSection from "@/components/AlbumSection.vue";

const newestAlbums = ref<Album[]>([])
const frequentAlbums = ref<Album[]>([])
const starredAlbums = ref<Album[]>([])
const recentAlbums = ref<Album[]>([])
const topRatedAlbums = ref<Album[]>([])
const loading = ref(true)

interface AlbumSectionConfig {
  title: string
  data: { value: Album[] }
  fetch: (size?: number, offset?: number) => Promise<AlbumsResponse>
}

const sections: AlbumSectionConfig[] = [
  { title: 'Newly added', data: newestAlbums, fetch: api.getNewestAlbums },
  { title: 'Recently played', data: frequentAlbums, fetch: api.getFrequentAlbums },
  { title: 'Favourite', data: starredAlbums, fetch: api.getStarredAlbums },
  { title: 'Recently Played', data: recentAlbums, fetch: api.getRecentAlbums },
  { title: 'Top Rated', data: topRatedAlbums, fetch: api.getTopRatedAlbums },
]

const loadAllAlbums = async () => {
  loading.value = true
  try {
    const results = await Promise.all(sections.map(s => s.fetch(20)))
    results.forEach((res, index) => {
      const section = sections[index]
      if (section && section.data) {
        section.data.value = res.albums
      }
    })
  } catch (err) {
    console.error('Error loading albums:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAllAlbums()
})
</script>

<template>
  <AlbumSection
    v-for="section in sections"
    :key="section.title"
    :title="section.title"
    :albums="section.data.value"
    :loading="loading"
  />
</template>
