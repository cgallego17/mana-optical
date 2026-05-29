<script setup lang="ts">
const posts = [
  'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=500&q=80',
  'https://images.unsplash.com/photo-1617471346061-5d329ab9c574?auto=format&fit=crop&w=500&q=80',
  'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=500&q=80',
  'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=500&q=80',
  'https://images.unsplash.com/photo-1508615039623-a25605d2b022?auto=format&fit=crop&w=500&q=80',
]
</script>

<template>
  <section class="w-full bg-[#314037] pt-20 pb-0">

    <!-- Header -->
    <div v-scroll-reveal class="flex flex-col items-center text-center mb-12 px-8">
      <span class="inline-block text-[11px] tracking-[0.4em] uppercase text-[#f5d984] font-medium mb-4">Síguenos</span>
      <h2 class="text-3xl lg:text-4xl font-black tracking-tight uppercase text-white mb-3">
        @NeoOcular
      </h2>
      <p class="text-sm text-white/35 text-center">Revisa nuestras últimas publicaciones en Instagram</p>
    </div>

    <!-- Photos — no gap, edge to edge -->
    <div class="grid grid-cols-5">
      <a
        v-for="(post, i) in posts"
        :key="i"
        v-scroll-reveal="{ delay: i * 120 }"
        href="#"
        class="group relative overflow-hidden aspect-square block"
      >
        <img :src="post" :alt="`Post ${i + 1}`"
          class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-110" />
        <div class="absolute inset-0 bg-black/0 group-hover:bg-[#f5d984]/60 transition-all duration-500 flex items-center justify-center">
          <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <svg class="h-10 w-10 text-white mx-auto" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
              <circle cx="12" cy="12" r="4"/>
              <circle cx="17.5" cy="6.5" r="1.5" fill="white" stroke="none"/>
            </svg>
          </div>
        </div>
      </a>
    </div>
  </section>
</template>
