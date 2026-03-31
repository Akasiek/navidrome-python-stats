<script setup lang="ts">
import HeroStats from "@/components/HeroStats.vue"
import AlbumsHomeSection from "@/components/AlbumsHomeSection.vue";
</script>

<template>
  <div class="bg-zinc-900 min-h-screen w-full text-white">
    <main class="container mx-auto py-12 px-4 space-y-12">
      <HeroStats/>
      <AlbumsHomeSection/>
    </main>
  </div>
</template>

