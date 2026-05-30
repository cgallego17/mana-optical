<script setup lang="ts">
</script>

<template>
  <div class="pt-[108px]">
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Inspírate</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Galería
      </h1>
      <p class="text-white/60 text-sm max-w-2xl mx-auto text-center">Looks, monturas y momentos en Maná Óptical.</p>
    </section>

    <section class="bg-white py-20 px-6 lg:px-12">
      <div class="columns-1 sm:columns-2 lg:columns-3 gap-5 [column-fill:_balance]">
        <img v-for="i in 12" :key="i" :src="`https://images.unsplash.com/photo-1527698575443-644bf8dceb37?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=MnwyMDkyMnwwfDF8c2VhcmNofDJ8fGdsYXNzZXMlMjBleWVzfGVufDB8fHx8MTY5` + i"
             class="mb-5 w-full rounded-sm border border-black/10 object-cover" alt="Galería"/>
      </div>
    </section>

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
