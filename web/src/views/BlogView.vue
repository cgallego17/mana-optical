<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
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

const categoriasApi = ref<CategoriaApi[]>([])
const categoriaActiva = ref('Todos')
const postsApi = ref<PostApi[]>([])
const cargando = ref(false)
const errorMsg = ref('')

function formatFecha(iso: string | null, fallbackIso: string): string {
  const raw = iso || fallbackIso
  try {
    const d = new Date(raw)
    return d.toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: '2-digit' })
  } catch {
    return raw
  }
}

async function cargarBlog() {
  cargando.value = true
  errorMsg.value = ''
  try {
    const [cats, posts] = await Promise.all([
      apiFetch<CategoriaApi[] | { results: CategoriaApi[] }>('/blog/categorias/'),
      apiFetch<PostApi[] | { results: PostApi[] }>('/blog/posts/'),
    ])
    categoriasApi.value = unwrapResults<CategoriaApi>(cats)
    postsApi.value = unwrapResults<PostApi>(posts)
  } catch (e) {
    categoriasApi.value = []
    postsApi.value = []
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando blog'
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  cargarBlog()
})

const categorias = computed(() => {
  return ['Todos', ...categoriasApi.value.map(c => c.nombre)]
})

const posts = computed(() => {
  return postsApi.value.map(p => ({
    id: p.id,
    imagen: p.imagen_url || 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=700&q=80',
    fecha: formatFecha(p.publicado_en, p.creado_en),
    categoria: p.categoria?.nombre ?? 'General',
    categoriaSlug: p.categoria?.slug ?? '',
    titulo: p.titulo,
    resumen: p.extracto || '',
    slug: p.slug,
  }))
})

const filtrados = computed(() => {
  if (categoriaActiva.value === 'Todos') return posts.value
  return posts.value.filter((p) => p.categoria === categoriaActiva.value)
})

const destacado = computed(() => posts.value[0])
</script>

<template>
  <div class="pt-[108px]">

    <!-- Hero -->
    <div class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Nuestro Blog</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Artículos & Consejos
      </h1>
      <div class="flex justify-center px-4">
        <p class="text-white/50 text-sm text-center max-w-sm">Salud visual, estilo y tendencias en óptica</p>
      </div>
    </div>

    <div class="bg-[#f8f7f5] py-20 px-8 lg:px-16">
      <div class="max-w-6xl mx-auto">

        <!-- Post destacado -->
        <div v-if="errorMsg" class="mb-6 border border-red-200 bg-red-50 px-4 py-3 text-[11px] text-red-700">
          {{ errorMsg }}
        </div>

        <div v-if="cargando" class="py-16 text-center text-[11px] text-black/40">
          Cargando blog...
        </div>

        <div v-else-if="destacado" class="grid grid-cols-1 lg:grid-cols-2 gap-0 mb-16 group cursor-pointer overflow-hidden bg-white shadow-lg">
          <div class="relative overflow-hidden h-72 lg:h-auto">
            <img :src="destacado.imagen" :alt="destacado.titulo" loading="lazy"
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
            <RouterLink
              :to="{ name: 'blog-post', params: { slug: destacado.slug } }"
              class="inline-flex items-center gap-3 text-[11px] font-bold tracking-widest uppercase text-[#314037] hover:text-[#f5d984] transition-colors duration-300"
            >
              Leer Artículo <ArrowRight class="h-4 w-4" />
            </RouterLink>
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
          <RouterLink
            v-for="post in filtrados"
            :key="post.id"
            :to="{ name: 'blog-post', params: { slug: post.slug } }"
            class="group bg-white overflow-hidden hover:shadow-xl transition-shadow duration-500 cursor-pointer flex flex-col"
          >
            <div class="relative overflow-hidden h-52">
              <img :src="post.imagen" :alt="post.titulo" loading="lazy"
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
              <span class="inline-flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase text-black hover:text-[#314037] transition-colors duration-300">
                Leer Más <span class="block w-5 h-px bg-current group-hover:w-8 transition-all duration-300" />
              </span>
            </div>
          </RouterLink>
        </div>

      </div>
    </div>
  </div>
</template>
