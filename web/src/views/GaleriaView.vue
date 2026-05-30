<script setup lang="ts">
const fotos = [
  'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1582142306909-195724d33ffc?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1473496169904-658ba7574b0d?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1617471346061-5d329ab9c574?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1551190822-a9333d879b1f?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1587614382346-4ec70e388b28?auto=format&fit=crop&w=800&q=80',
]
</script>

<template>
  <div style="padding-top: var(--header-h, 4rem)">

    <!-- Hero -->
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Inspírate</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3"
          style="font-family:'Playfair Display',serif;">
        Galería
      </h1>
      <div class="flex justify-center px-4">
        <p class="text-white/60 text-sm text-center max-w-sm">
          Looks, monturas y momentos en Maná Óptical.
        </p>
      </div>
    </section>

    <!-- Grid masonry -->
    <section class="bg-white py-16 px-5 lg:px-12">
      <div class="columns-2 sm:columns-3 lg:columns-4 gap-4">
        <div v-for="(foto, i) in fotos" :key="i" class="break-inside-avoid mb-4">
          <img
            :src="foto"
            :alt="`Maná Óptical — imagen ${i + 1}`"
            loading="lazy"
            class="w-full object-cover rounded-sm border border-black/[0.06] hover:scale-[1.02] transition-transform duration-500"
          />
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="bg-[#f8f7f5] py-16 px-8 text-center">
      <RouterLink
        to="/tienda"
        class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity"
      >
        Ver colección en tienda
      </RouterLink>
    </section>

  </div>
</template>
