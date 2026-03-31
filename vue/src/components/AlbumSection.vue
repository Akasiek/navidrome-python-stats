<script setup lang="ts">
import type { Album } from '@/types'
import AlbumCarousel from "@/components/AlbumCarousel.vue";

defineProps<{
  title: string
  albums: Album[]
  loading?: boolean
}>()
</script>

<template>
  <section v-if="albums.length > 0 || loading">
    <h2 class="text-2xl font-bold mb-6 text-white">{{ title }}</h2>
    <AlbumCarousel :albums="albums" :loading="loading"/>
  </section>
</template>
