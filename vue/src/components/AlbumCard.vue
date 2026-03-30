<script setup lang="ts">
import type { Album } from "@/types";
import IconHeart from "@/components/icons/IconHeart.vue";
import IconStar from "@/components/icons/IconStar.vue";
import IconPlay from "@/components/icons/IconPlay.vue";

const props = defineProps<{
  album: Album
}>();
console.log(props.album)
const formatDuration = (seconds?: number) => {
  if (!seconds) return "";
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  if (hours > 0) {
    return `${hours}h ${minutes % 60}m`;
  }
  return `${minutes}m`;
};
</script>

<template>
  <a
    class="block hover:-translate-y-1 transition-all duration-300 group no-underline"
    :href="album.url" target="_blank" rel="noopener noreferrer"
  >
    <div class="aspect-square rounded-md overflow-hidden relative shadow-lg group-hover:shadow-2xl group-hover:shadow-blue-500/10 transition-shadow">
      <img v-if="album.cover_art_url" :src="album.cover_art_url" alt="Album Cover"
           class="w-full h-full object-cover">
      <div v-if="album.year" class="absolute top-2 right-2 bg-black/60 backdrop-blur-sm px-2 py-0.5 rounded text-xs font-medium text-zinc-100">
        {{ album.year }}
      </div>
      <div v-if="album.starred" class="absolute top-2 left-2 bg-black/60 backdrop-blur-sm p-1 rounded-full text-zinc-50 shadow-sm">
        <IconHeart class="w-4 h-4" />
      </div>
      <div v-if="album.rating" class="absolute bottom-2 left-2 bg-black/60 backdrop-blur-sm px-1.5 py-0.5 rounded flex items-center gap-0.5 shadow-sm">
        <IconStar class="w-3 h-3 mb-0.5 text-yellow-500" />
        <span class="text-[10px] font-bold text-zinc-100 mr-0.5">{{ album.rating }}</span>
      </div>
    </div>

    <div class="p-4 mt-4 bg-zinc-800 rounded-md group-hover:bg-zinc-700 transition-colors">
      <h3 class="text-base font-bold text-zinc-50 truncate" :title="album.name">{{ album.name }}</h3>
      <div class="flex flex-col gap-1 mt-1">
        <a :href="album.artist_url" target="_blank" rel="noopener noreferrer"
           class="text-sm text-zinc-400 hover:text-zinc-200 transition-colors truncate no-underline" @click.stop>
          {{ album.artist }}
        </a>
        <div class="flex items-center justify-between mt-1">
          <div class="flex items-center gap-2 text-xs text-zinc-500">
            <span v-if="album.duration">{{ formatDuration(album.duration) }}</span>
          </div>
          <div v-if="album.play_count" class="flex items-center gap-1 text-[10px] font-medium text-zinc-500">
            <IconPlay class="w-3 h-3" />
            <span>{{ album.play_count }}</span>
          </div>
        </div>
      </div>
    </div>
  </a>
</template>
