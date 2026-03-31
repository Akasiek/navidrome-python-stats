<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { Album } from '@/types'
import AlbumCard from '@/components/AlbumCard.vue'
import AlbumCardSkeleton from '@/components/AlbumCardSkeleton.vue'
import CarouselButton from '@/components/CarouselButton.vue'

interface Props {
  albums: Album[]
  loading?: boolean
}

defineProps<Props>()

const scrollContainer = ref<HTMLElement | null>(null)
const isAtStart = ref(true)
const isAtEnd = ref(false)

function updateScrollState() {
  const container = scrollContainer.value
  if (!container) {
    return
  }
  const { scrollLeft, scrollWidth, clientWidth } = container
  isAtStart.value = scrollLeft <= 1
  isAtEnd.value = scrollLeft + clientWidth >= scrollWidth - 1
}

function scroll(direction: 'left' | 'right') {
  const container = scrollContainer.value
  if (!container) {
    return
  }

  const scrollAmount = container.clientWidth * 0.8
  const targetScroll = container.scrollLeft + (direction === 'right' ? scrollAmount : -scrollAmount)

  container.scrollTo({
    left: targetScroll,
    behavior: 'smooth',
  })
}

onMounted(() => {
  scrollContainer.value?.addEventListener('scroll', updateScrollState, { passive: true })
  window.addEventListener('resize', updateScrollState)
  // Initial check
  setTimeout(updateScrollState, 100)
})

onUnmounted(() => {
  scrollContainer.value?.removeEventListener('scroll', updateScrollState)
  window.removeEventListener('resize', updateScrollState)
})
</script>

<template>
  <div class="relative group/carousel">
    <CarouselButton direction="left" :hidden="isAtStart" @click="scroll('left')" />

    <div
      ref="scrollContainer"
      class="flex gap-4 overflow-x-auto scrollbar-hide scroll-smooth snap-x snap-mandatory py-2 -my-2"
      style="scrollbar-width: none; -ms-overflow-style: none"
    >
      <template v-if="loading">
        <AlbumCardSkeleton v-for="i in 6" :key="`loading-${i}`" width-class="w-56" />
      </template>
      <template v-else>
        <AlbumCard
          v-for="album in albums"
          :key="album.name + album.artist"
          :album="album"
          class="flex-none w-56 snap-start"
        />
      </template>

      <div v-if="!loading && albums.length === 0" class="w-full py-8 text-center text-zinc-500">
        No albums found
      </div>
    </div>

    <CarouselButton direction="right" :hidden="isAtEnd" @click="scroll('right')" />
  </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
