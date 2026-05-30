<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

import { apiFetch, unwrapResults } from '../lib/api'

type CategoriaApi = { id: number; nombre: string; slug: string }
type PostApi = {
  id: number
  titulo: string
  slug: string
  extracto: string
  imagen_url: string
  publicado_en: string | null
  creado_en: string
  categoria: CategoriaApi | null
}

const posts = ref<Array<{ image: string; date: string; tag: string; title: string; excerpt: string; slug: string }>>([])
const cargando = ref(false)

function formatFecha(iso: string | null, fallbackIso: string): string {
  const raw = iso || fallbackIso
  try {
    const d = new Date(raw)
    return d.toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: '2-digit' })
  } catch {
    return raw
  }
}

async function cargar() {
  cargando.value = true
  try {
    const data = await apiFetch<PostApi[] | { results: PostApi[] }>('/blog/posts/')
    const lista = unwrapResults<PostApi>(data)
    posts.value = lista.slice(0, 3).map(p => ({
      image: p.imagen_url || 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=700&q=80',
      date: formatFecha(p.publicado_en, p.creado_en),
      tag: p.categoria?.nombre ?? 'General',
      title: p.titulo,
      excerpt: p.extracto || '',
      slug: p.slug,
    }))
  } catch {
    posts.value = []
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  cargar()
})
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
    <div v-if="cargando" class="py-10 text-center text-[11px] text-black/40">
      Cargando...
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
      <RouterLink
        v-for="(post, i) in posts"
        :key="post.title"
        :to="{ name: 'blog-post', params: { slug: post.slug } }"
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

          <span class="inline-flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase text-black hover:text-[#f5d984] transition-colors duration-300">
            Leer Más
            <span class="block w-5 h-px bg-current group-hover:w-8 transition-all duration-300" />
          </span>
        </div>
      </RouterLink>
    </div>

  </section>
</template>
