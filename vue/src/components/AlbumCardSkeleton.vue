<script setup lang="ts">
defineProps<{
  widthClass: string
}>();
</script>

<template>
  <div :class="`flex-none snap-start ${widthClass}`">
    <div class="aspect-square bg-zinc-800 animate-pulse rounded-md"></div>
    <div class="mt-4 p-4 bg-zinc-800/50 rounded-md">
      <div class="h-4 bg-zinc-700 animate-pulse rounded w-3/4"></div>
      <div class="mt-3 h-3 bg-zinc-700 animate-pulse rounded w-1/2"></div>
    </div>
  </div>
</template>
