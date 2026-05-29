<script setup lang="ts">
import { ref } from 'vue'
import { ArrowRight } from 'lucide-vue-next'

const categorias = ['Todos', 'Salud Visual', 'Estilo', 'Consejos', 'Noticias']
const categoriaActiva = ref('Todos')

const posts = [
  { id: 1, imagen: 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=700&q=80', fecha: '30 Jul 2025', categoria: 'Estilo', titulo: 'Gafas para Hombre de Moda', resumen: 'Descubre las tendencias más actuales en monturas masculinas para esta temporada y cómo lucir con estilo.' },
  { id: 2, imagen: 'https://images.unsplash.com/photo-1577744486770-020ab432da65?auto=format&fit=crop&w=700&q=80', fecha: '22 Jul 2025', categoria: 'Estilo', titulo: 'Monturas que te Favorecen', resumen: 'Te ayudamos a encontrar la montura perfecta según la forma de tu rostro con nuestra guía completa.' },
  { id: 3, imagen: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=700&q=80', fecha: '15 Jul 2025', categoria: 'Salud Visual', titulo: 'Realízate Chequeos Visuales', resumen: 'Un examen visual a tiempo puede detectar problemas oculares antes de que afecten tu calidad de vida.' },
  { id: 4, imagen: 'https://images.unsplash.com/photo-1617471346061-5d329ab9c574?auto=format&fit=crop&w=700&q=80', fecha: '10 Jul 2025', categoria: 'Consejos', titulo: 'Cómo Cuidar tus Lentes', resumen: 'Aprende las mejores prácticas para mantener tus gafas en perfecto estado y prolongar su vida útil.' },
  { id: 5, imagen: 'https://images.unsplash.com/photo-1508615039623-a25605d2b022?auto=format&fit=crop&w=700&q=80', fecha: '05 Jul 2025', categoria: 'Salud Visual', titulo: 'Protección contra Luz Azul', resumen: 'Conoce cómo los lentes con filtro de luz azul protegen tus ojos en la era digital.' },
  { id: 6, imagen: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=700&q=80', fecha: '01 Jul 2025', categoria: 'Noticias', titulo: 'Nueva Colección 2025', resumen: 'Presentamos nuestra nueva colección de monturas con diseños exclusivos para cada personalidad.' },
]

const postsFiltrados = computed => {
  if (categoriaActiva.value === 'Todos') return posts
  return posts.filter(p => p.categoria === categoriaActiva.value)
}

import { computed } from 'vue'
const filtrados = computed(() => {
  if (categoriaActiva.value === 'Todos') return posts
  return posts.filter(p => p.categoria === categoriaActiva.value)
})

const destacado = posts[0]
</script>

<template>
  <div class="pt-[108px]">

    <!-- Hero -->
    <div class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Nuestro Blog</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Artículos & Consejos
      </h1>
      <p class="text-white/50 text-sm">Salud visual, estilo y tendencias en óptica</p>
    </div>

    <div class="bg-[#f8f7f5] py-20 px-8 lg:px-16">
      <div class="max-w-6xl mx-auto">

        <!-- Post destacado -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-0 mb-16 group cursor-pointer overflow-hidden bg-white shadow-lg">
          <div class="relative overflow-hidden h-72 lg:h-auto">
            <img :src="destacado.imagen" :alt="destacado.titulo"
              class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
            <span class="absolute top-5 left-5 bg-[#314037] text-[#f5d984] text-[10px] font-bold tracking-widest uppercase px-4 py-1.5">
              Destacado
            </span>
          </div>
          <div class="p-10 flex flex-col justify-center">
            <p class="text-[10px] tracking-widest uppercase text-[#314037] font-bold mb-3">{{ destacado.fecha }} · {{ destacado.categoria }}</p>
            <h2 class="text-2xl font-black tracking-wide uppercase text-black mb-4 leading-snug" style="font-family:'Playfair Display',serif;">
              {{ destacado.titulo }}
            </h2>
            <p class="text-sm text-black/50 leading-relaxed mb-8">{{ destacado.resumen }}</p>
            <a href="#" class="inline-flex items-center gap-3 text-[11px] font-bold tracking-widest uppercase text-[#314037] hover:text-[#f5d984] transition-colors duration-300">
              Leer Artículo <ArrowRight class="h-4 w-4" />
            </a>
          </div>
        </div>

        <!-- Filtros categoría -->
        <div class="flex gap-2 flex-wrap mb-10">
          <button
            v-for="cat in categorias"
            :key="cat"
            @click="categoriaActiva = cat"
            class="px-5 py-2.5 text-[11px] font-bold tracking-widest uppercase transition-all duration-300"
            :class="categoriaActiva === cat
              ? 'bg-[#314037] text-[#f5d984]'
              : 'border border-black/15 text-black/60 hover:border-[#314037] hover:text-[#314037]'"
          >
            {{ cat }}
          </button>
        </div>

        <!-- Grid posts -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <article
            v-for="post in filtrados"
            :key="post.id"
            class="group bg-white overflow-hidden hover:shadow-xl transition-shadow duration-500 cursor-pointer flex flex-col"
          >
            <div class="relative overflow-hidden h-52">
              <img :src="post.imagen" :alt="post.titulo"
                class="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" />
              <span class="absolute top-4 left-4 bg-[#314037] text-[#f5d984] text-[10px] font-bold tracking-widest uppercase px-3 py-1">
                {{ post.categoria }}
              </span>
            </div>
            <div class="p-6 flex flex-col flex-1">
              <p class="text-[10px] tracking-widest uppercase text-black/30 mb-2">{{ post.fecha }}</p>
              <h3 class="text-sm font-black tracking-wide uppercase text-black mb-3 group-hover:text-[#314037] transition-colors duration-300 leading-snug flex-1">
                {{ post.titulo }}
              </h3>
              <p class="text-xs text-black/50 leading-relaxed mb-5">{{ post.resumen }}</p>
              <a href="#" class="inline-flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase text-black hover:text-[#314037] transition-colors duration-300">
                Leer Más <span class="block w-5 h-px bg-current group-hover:w-8 transition-all duration-300" />
              </a>
            </div>
          </article>
        </div>

      </div>
    </div>
  </div>
</template>
