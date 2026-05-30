<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import { apiFetch } from '../lib/api'
import { useSeo, removeJsonLd } from '../composables/seo'

const { setPage, setBlogPost, setBreadcrumb } = useSeo()

type CategoriaApi = { id: number; nombre: string; slug: string }

type PostDetailApi = {
  id: number
  titulo: string
  slug: string
  extracto: string
  contenido: string
  imagen_url: string
  publicado_en: string | null
  creado_en: string
  categoria: CategoriaApi | null
}

const route = useRoute()
const router = useRouter()

const post = ref<{
  titulo: string
  categoria: string
  fecha: string
  extracto: string
  contenido: string
  imagen: string
} | null>(null)

const cargando = ref(false)
const errorMsg = ref('')

function formatFecha(iso: string | null, fallbackIso: string): string {
  const raw = iso || fallbackIso
  try {
    const d = new Date(raw)
    return d.toLocaleDateString('es-CO', { year: 'numeric', month: 'long', day: '2-digit' })
  } catch {
    return raw
  }
}

async function cargar() {
  const slug = String(route.params.slug || '')
  if (!slug) return

  cargando.value = true
  errorMsg.value = ''
  try {
    const data = await apiFetch<PostDetailApi>(`/blog/posts/${encodeURIComponent(slug)}/`)
    post.value = {
      titulo: data.titulo,
      categoria: data.categoria?.nombre ?? 'General',
      fecha: formatFecha(data.publicado_en, data.creado_en),
      extracto: data.extracto || '',
      contenido: data.contenido || '',
      imagen: data.imagen_url || 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=1200&q=80',
    }
    // SEO
    setPage({
      title: `${data.titulo} | Blog Maná Óptical`,
      description: (data.extracto || data.titulo).slice(0, 160),
      image: post.value.imagen,
      type: 'article',
    })
    setBlogPost({
      titulo: data.titulo,
      extracto: data.extracto || '',
      imagen: post.value.imagen,
      slug: data.slug,
      fecha: data.publicado_en || data.creado_en,
    })
    setBreadcrumb([
      { name: 'Inicio', url: `${window.location.origin}/` },
      { name: 'Blog',   url: `${window.location.origin}/blog` },
      { name: data.titulo, url: window.location.href },
    ])
  } catch (e) {
    post.value = null
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando el post'
  } finally {
    cargando.value = false
  }
}

onMounted(() => { cargar() })
onUnmounted(() => { removeJsonLd('ld-blogpost'); removeJsonLd('ld-breadcrumb') })
</script>

<template>
  <div class="pt-[108px]">
    <div class="bg-[#314037] py-10 px-8">
      <div class="max-w-4xl mx-auto">
        <button
          type="button"
          class="inline-flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase text-[#f5d984] hover:text-white transition-colors duration-300"
          @click="router.push({ name: 'blog' })"
        >
          <ArrowLeft class="h-4 w-4" /> Volver al Blog
        </button>
      </div>
    </div>

    <div class="bg-[#f8f7f5] py-14 px-8 lg:px-16">
      <div class="max-w-4xl mx-auto">
        <div v-if="errorMsg" class="mb-6 border border-red-200 bg-red-50 px-4 py-3 text-[11px] text-red-700">
          {{ errorMsg }}
        </div>

        <div v-if="cargando" class="py-16 text-center text-[11px] text-black/40">
          Cargando artículo...
        </div>

        <article v-else-if="post" class="bg-white shadow-lg overflow-hidden">
          <div class="relative overflow-hidden">
            <img :src="post.imagen" :alt="post.titulo" class="w-full h-72 object-cover" loading="lazy" />
          </div>

          <div class="p-8 lg:p-10">
            <p class="text-[10px] tracking-widest uppercase text-black/40 mb-3">
              {{ post.fecha }} · {{ post.categoria }}
            </p>

            <h1
              class="text-3xl lg:text-4xl font-black tracking-tight text-black uppercase leading-tight mb-5"
              style="font-family:'Playfair Display',serif;"
            >
              {{ post.titulo }}
            </h1>

            <p class="text-sm text-black/55 leading-relaxed mb-8">
              {{ post.extracto }}
            </p>

            <div
              class="prose prose-neutral max-w-none"
              v-html="post.contenido"
            />
          </div>
        </article>

        <div v-else class="py-10 text-center text-[11px] text-black/40">
          No se encontró el artículo.
        </div>
      </div>
    </div>
  </div>
</template>
