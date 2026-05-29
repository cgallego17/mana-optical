<script setup lang="ts">
const posts = [
  { image: 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=700&q=80', date: '30 Jul 2025', tag: 'Estilo', title: 'Gafas para Hombre de Moda', excerpt: 'Descubre las tendencias más actuales en monturas masculinas para esta temporada y cómo lucir con estilo.' },
  { image: 'https://images.unsplash.com/photo-1577744486770-020ab432da65?auto=format&fit=crop&w=700&q=80', date: '22 Jul 2025', tag: 'Visión', title: 'Monturas que te Favorecen', excerpt: 'Te ayudamos a encontrar la montura perfecta según la forma de tu rostro con nuestra guía completa.' },
  { image: 'https://images.unsplash.com/photo-1508615039623-a25605d2b022?auto=format&fit=crop&w=700&q=80', date: '15 Jul 2025', tag: 'Diseño', title: 'Personaliza tus Gafas', excerpt: 'Crea unas gafas únicas a tu medida con nuestro servicio de personalización premium.' },
]
</script>

<template>
  <section class="w-full bg-[#f8f7f5] py-24 px-8 lg:px-16">

    <!-- Header -->
    <div v-scroll-reveal class="flex flex-col items-center text-center mb-16">
      <span class="inline-block text-[11px] tracking-[0.35em] uppercase text-[#f5d984] font-medium mb-4">Blog</span>
      <h2 class="text-4xl lg:text-5xl font-black tracking-tight uppercase text-black mb-4">Últimas Novedades</h2>
      <p class="text-sm text-black/40">Mantente al día con nuestros artículos, consejos y tendencias en óptica</p>
    </div>

    <!-- Posts -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
      <article
        v-for="(post, i) in posts"
        :key="post.title"
        v-scroll-reveal="{ delay: i * 160 }"
        class="group bg-white overflow-hidden hover:shadow-xl transition-shadow duration-500 cursor-pointer flex flex-col"
      >
        <!-- Image -->
        <div class="relative overflow-hidden h-56">
          <img :src="post.image" :alt="post.title"
            class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          <span class="absolute top-4 left-4 bg-[#314037] text-white text-[10px] font-bold tracking-widest uppercase px-3 py-1">
            {{ post.tag }}
          </span>
        </div>

        <!-- Content -->
        <div class="p-7 flex flex-col flex-1">
          <p class="text-[10px] tracking-widest uppercase text-black/30 mb-3">{{ post.date }}</p>
          <h3 class="text-base font-black tracking-wide uppercase text-black mb-3 group-hover:text-[#f5d984] transition-colors duration-300 leading-snug">
            {{ post.title }}
          </h3>
          <p class="text-xs text-black/50 leading-relaxed mb-6 flex-1">{{ post.excerpt }}</p>

          <a href="#" class="inline-flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase text-black hover:text-[#f5d984] transition-colors duration-300">
            Leer Más
            <span class="block w-5 h-px bg-current group-hover:w-8 transition-all duration-300" />
          </a>
        </div>
      </article>
    </div>

  </section>
</template>
