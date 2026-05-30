<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/auth'
import { apiFetch, apiFetchAuth, unwrapResults } from '../../lib/api'

const router = useRouter()
const { getAccessToken } = useAuth()

type CategoriaApi = { id: number; nombre: string; slug: string }
type PostAdminApi = {
  id: number; titulo: string; slug: string; extracto: string; contenido: string
  imagen_url: string; publicado: boolean; publicado_en: string | null
  creado_en: string; categoria: CategoriaApi | null; categoria_id: number | null
}

const cargando    = ref(false)
const errorMsg    = ref('')
const guardando   = ref(false)
const categorias  = ref<CategoriaApi[]>([])
const posts       = ref<PostAdminApi[]>([])
const seleccionadoId = ref<number | null>(null)

const form = ref({
  titulo: '', slug: '', extracto: '', contenido: '',
  imagen_url: '', publicado: false, categoria_id: null as number | null,
})

function syncForm(p: PostAdminApi) {
  form.value = {
    titulo: p.titulo || '', slug: p.slug || '', extracto: p.extracto || '',
    contenido: p.contenido || '', imagen_url: p.imagen_url || '',
    publicado: Boolean(p.publicado),
    categoria_id: p.categoria?.id ?? p.categoria_id ?? null,
  }
}

async function cargar() {
  const token = getAccessToken()
  if (!token) { router.push({ name: 'admin-login' }); return }
  cargando.value = true; errorMsg.value = ''
  try {
    const [cats, lista] = await Promise.all([
      apiFetch<CategoriaApi[] | { results: CategoriaApi[] }>('/blog/categorias/'),
      apiFetchAuth<PostAdminApi[] | { results: PostAdminApi[] }>('/blog/admin/posts/', token),
    ])
    const catsList = unwrapResults<CategoriaApi>(cats)
    const postsList = unwrapResults<PostAdminApi>(lista)
    categorias.value = catsList
    posts.value = postsList
    if (postsList.length && seleccionadoId.value == null) {
      seleccionadoId.value = postsList[0].id
      syncForm(postsList[0])
    }
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando'
  } finally { cargando.value = false }
}

function seleccionar(p: PostAdminApi) { seleccionadoId.value = p.id; syncForm(p) }

function nuevo() {
  seleccionadoId.value = null
  form.value = { titulo: '', slug: '', extracto: '', contenido: '', imagen_url: '', publicado: false, categoria_id: null }
}

async function guardar() {
  const token = getAccessToken()
  if (!token) { router.push({ name: 'admin-login' }); return }
  guardando.value = true; errorMsg.value = ''
  try {
    if (seleccionadoId.value == null) {
      const creado = await apiFetchAuth<PostAdminApi>('/blog/admin/posts/', token, { method: 'POST', body: JSON.stringify(form.value) })
      posts.value = [creado, ...posts.value]; seleccionadoId.value = creado.id; syncForm(creado)
    } else {
      const act = await apiFetchAuth<PostAdminApi>(`/blog/admin/posts/${seleccionadoId.value}/`, token, { method: 'PATCH', body: JSON.stringify(form.value) })
      posts.value = posts.value.map(p => p.id === act.id ? act : p); syncForm(act)
    }
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error guardando'
  } finally { guardando.value = false }
}

async function eliminar() {
  const token = getAccessToken()
  if (!token || seleccionadoId.value == null) return
  if (!confirm('¿Eliminar este post?')) return
  guardando.value = true; errorMsg.value = ''
  try {
    await apiFetchAuth<void>(`/blog/admin/posts/${seleccionadoId.value}/`, token, { method: 'DELETE' })
    posts.value = posts.value.filter(p => p.id !== seleccionadoId.value)
    seleccionadoId.value = posts.value.length ? posts.value[0].id : null
    if (seleccionadoId.value != null) syncForm(posts.value[0]); else nuevo()
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error eliminando'
  } finally { guardando.value = false }
}

onMounted(cargar)
</script>

<template>
  <div class="p-6 lg:p-10">
    <div class="flex items-center justify-between mb-8">
      <div>
        <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Contenido</p>
        <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Blog — Posts</h2>
      </div>
      <button @click="nuevo" class="text-[11px] font-bold tracking-widest uppercase border border-white/20 px-4 py-2 hover:border-[#f5d984] hover:text-[#f5d984] transition">
        + Nuevo
      </button>
    </div>

    <div v-if="errorMsg" class="mb-5 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorMsg }}</div>
    <div v-if="cargando" class="py-16 text-center text-[11px] text-white/40">Cargando...</div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Lista -->
      <section class="lg:col-span-4 bg-white/5 border border-white/[0.07] rounded overflow-hidden">
        <div class="px-5 py-4 border-b border-white/[0.07]">
          <p class="text-[10px] tracking-widest uppercase text-white/40">{{ posts.length }} posts</p>
        </div>
        <div class="divide-y divide-white/[0.07] max-h-[60vh] overflow-y-auto">
          <button
            v-for="p in posts" :key="p.id"
            type="button"
            class="w-full text-left px-5 py-4 hover:bg-white/5 transition"
            :class="seleccionadoId === p.id ? 'bg-white/5 border-l-2 border-[#f5d984]' : 'border-l-2 border-transparent'"
            @click="seleccionar(p)"
          >
            <p class="text-[10px] tracking-widest uppercase mb-1" :class="p.publicado ? 'text-[#f5d984]' : 'text-white/30'">
              {{ p.publicado ? 'Publicado' : 'Borrador' }}
            </p>
            <p class="text-sm font-bold text-white leading-tight">{{ p.titulo }}</p>
            <p class="text-[10px] text-white/30 mt-1">/{{ p.slug }}</p>
          </button>
          <div v-if="!posts.length" class="px-5 py-10 text-[11px] text-white/30">No hay posts.</div>
        </div>
      </section>

      <!-- Editor -->
      <section class="lg:col-span-8 bg-white/5 border border-white/[0.07] rounded overflow-hidden flex flex-col">
        <div class="px-5 py-4 border-b border-white/[0.07] flex items-center justify-between shrink-0">
          <h3 class="text-sm font-black uppercase tracking-widest">{{ seleccionadoId == null ? 'Nuevo post' : 'Editar post' }}</h3>
          <div class="flex items-center gap-2">
            <button v-if="seleccionadoId != null" type="button" :disabled="guardando" @click="eliminar"
              class="text-[10px] font-bold tracking-widest uppercase border border-red-500/40 text-red-300 px-3 py-2 hover:border-red-400 transition disabled:opacity-40">
              Eliminar
            </button>
            <button type="button" :disabled="guardando" @click="guardar"
              class="bg-[#f5d984] text-[#314037] text-[10px] font-bold tracking-widest uppercase px-4 py-2 hover:opacity-90 transition disabled:opacity-40">
              {{ guardando ? 'Guardando…' : 'Guardar' }}
            </button>
          </div>
        </div>

        <div class="p-5 space-y-4 overflow-y-auto flex-1">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="admin-label">Título</label>
              <input v-model="form.titulo" type="text" class="admin-input" />
            </div>
            <div>
              <label class="admin-label">Slug</label>
              <input v-model="form.slug" type="text" class="admin-input" />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="admin-label">Categoría</label>
              <select v-model="form.categoria_id" class="admin-input">
                <option :value="null">(Sin categoría)</option>
                <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
            <div class="flex items-end">
              <label class="flex items-center gap-3 cursor-pointer">
                <input v-model="form.publicado" type="checkbox" class="h-4 w-4 accent-[#f5d984]" />
                <span class="text-[11px] font-bold tracking-widest uppercase text-white/60">Publicado</span>
              </label>
            </div>
          </div>
          <div>
            <label class="admin-label">Imagen URL</label>
            <input v-model="form.imagen_url" type="text" class="admin-input" />
          </div>
          <div>
            <label class="admin-label">Extracto</label>
            <textarea v-model="form.extracto" rows="2" class="admin-input" />
          </div>
          <div>
            <label class="admin-label">Contenido (HTML)</label>
            <textarea v-model="form.contenido" rows="8" class="admin-input" />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
@reference "../../style.css";
.admin-label { @apply block text-[10px] tracking-widest uppercase text-white/50 mb-1.5 }
.admin-input { @apply w-full px-3 py-2.5 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
</style>
