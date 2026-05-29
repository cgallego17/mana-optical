<script setup lang="ts">
const products = [
  { id: 1, name: 'Lennons Metálicos', category: 'Ojo de Gato / Lujo', price: 175.00, originalPrice: 199.00, sale: true, image: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=700&q=80' },
  { id: 2, name: 'Gafas Cat Eye', category: 'Ojo de Gato / Lujo', price: 199.00, originalPrice: null, sale: false, image: 'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=700&q=80' },
  { id: 3, name: 'Gafas Diseñadas', category: 'Aviador / Lujo', price: 211.00, originalPrice: null, sale: false, image: 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=700&q=80' },
  { id: 4, name: 'Ovaladas Carey', category: 'Oval / Vintage', price: 189.00, originalPrice: null, sale: false, image: 'https://images.unsplash.com/photo-1582142306909-195724d33ffc?auto=format&fit=crop&w=700&q=80' },
  { id: 5, name: 'Montura Delgada', category: 'Sin Aro / Minimal', price: 165.00, originalPrice: null, sale: false, image: 'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=700&q=80' },
  { id: 6, name: 'Redondas Clip-On', category: 'Redondas / Clásico', price: 225.00, originalPrice: null, sale: false, image: 'https://images.unsplash.com/photo-1473496169904-658ba7574b0d?auto=format&fit=crop&w=700&q=80' },
]
</script>

<template>
  <section class="w-full bg-white py-24 px-8 lg:px-16">

    <!-- Header -->
    <div v-scroll-reveal class="flex flex-col items-center text-center mb-20">
      <span class="inline-block text-[11px] tracking-[0.35em] uppercase text-[#f5d984] mb-4 font-medium">Colección 2025</span>
      <h2 class="text-4xl lg:text-5xl font-black tracking-tight text-black uppercase mb-5">Nuestros Productos</h2>
      <p class="text-sm text-black/40 leading-relaxed">Explora nuestra selección de monturas de diseño exclusivo para cada estilo</p>
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-14 max-w-6xl mx-auto">
      <div
        v-for="(product, i) in products"
        :key="product.id"
        v-scroll-reveal="{ delay: (i % 3) * 150 }"
        class="group cursor-pointer"
      >
        <!-- Image area -->
        <div class="relative bg-[#f8f7f5] overflow-hidden mb-5">
          <div class="h-60 flex items-center justify-center p-6">
            <img
              :src="product.image"
              :alt="product.name"
              class="h-full w-full object-contain transition-transform duration-700 group-hover:scale-108"
            />
          </div>

          <!-- Sale badge -->
          <span v-if="product.sale"
            class="absolute top-4 left-4 bg-[#314037] text-white text-[10px] font-bold tracking-[0.2em] uppercase px-3 py-1.5">
            Oferta
          </span>

          <!-- Add to cart — slide up on hover -->
          <div class="absolute inset-x-0 bottom-0 translate-y-full group-hover:translate-y-0 transition-transform duration-400 ease-out">
            <button class="btn-shine active:scale-95 w-full bg-[#314037] text-white text-[11px] font-bold tracking-[0.25em] uppercase py-4
              hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300">
              + Añadir al carrito
            </button>
          </div>
        </div>

        <!-- Info -->
        <div class="text-center px-2">
          <p class="text-[10px] tracking-[0.3em] uppercase text-black/35 mb-2">{{ product.category }}</p>
          <h3 class="text-sm font-bold tracking-wide uppercase text-black mb-3">{{ product.name }}</h3>
          <div class="flex items-center justify-center gap-3">
            <span v-if="product.originalPrice" class="text-sm line-through text-black/25">
              ${{ product.originalPrice.toFixed(2) }}
            </span>
            <span class="text-base font-black text-black">${{ product.price.toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>

  </section>
</template>
