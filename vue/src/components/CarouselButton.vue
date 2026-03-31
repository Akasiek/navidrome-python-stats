<script setup lang="ts">
import IconChevronRight from '@/components/icons/IconChevronRight.vue'

defineProps<{
  direction: 'left' | 'right'
  hidden: boolean
}>()

defineEmits<{
  (e: 'click'): void
}>()
</script>

<template>
  <button
    @click="$emit('click')"
    class="absolute top-1/2 -translate-y-1/2 z-10 bg-zinc-800/80 hover:bg-zinc-700 shadow-lg rounded-full p-2 transition-all border border-zinc-700 disabled:opacity-0 cursor-pointer"
    :class="[
      direction === 'left' ? 'left-0 -ml-6' : 'right-0 -mr-6',
      {
        'opacity-0 group-hover/carousel:opacity-100': !hidden,
        'opacity-0 pointer-events-none': hidden,
      },
    ]"
    :disabled="hidden"
    :aria-label="`Scroll ${direction}`"
  >
    <IconChevronRight class="w-6 h-6 text-white" :class="{ 'rotate-180': direction === 'left' }" />
  </button>
</template>
