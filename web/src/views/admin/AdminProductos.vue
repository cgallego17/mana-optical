<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Pencil, Trash2, X } from 'lucide-vue-next'
import { apiFetch, apiFetchAuth, unwrapResults } from '../../lib/api'
import { useAuth } from '../../composables/auth'

const router = useRouter()
const { getAccessToken } = useAuth()

type CatApi   = { id: number; nombre: string; slug: string }
type MarcaApi = { id: number; nombre: string; slug: string }
type ProdApi  = {
  id: number; nombre: string; slug: string; descripcion: string
  precio: string; precio_antes: string | null; imagen_url: string
  categoria: CatApi | null; marca: MarcaApi | null
  disponible?: boolean
}

type Prod = {
  id: number; nombre: string; slug: string; descripcion: string
  precio: number; precioAnterior: number | null; oferta: boolean
  imagen: string; categoria: string; categoriaId: number | null
  marca: string; marcaId: number | null; disponible: boolean
}

function mapProd(p: ProdApi): Prod {
  const precio = Number(p.precio)
  const pa = p.precio_antes ? Number(p.precio_antes) : null
  return {
    id: p.id, nombre: p.nombre, slug: p.slug, descripcion: p.descripcion,
    precio, precioAnterior: pa, oferta: Boolean(pa && pa > precio),
    imagen: p.imagen_url, categoria: p.categoria?.nombre ?? '—',
    categoriaId: p.categoria?.id ?? null, marca: p.marca?.nombre ?? '—',
    marcaId: p.marca?.id ?? null, disponible: p.disponible ?? true,
  }
}

const cargando  = ref(false)
const guardando = ref(false)
const errorMsg  = ref('')
const productos = ref<Prod[]>([])
const categorias = ref<CatApi[]>([])
const marcas     = ref<MarcaApi[]>([])

const panelAbierto  = ref(false)
const editandoId    = ref<number | null>(null)
const busqueda      = ref('')
const filtrarCat    = ref('')

const form = ref({
  nombre: '', slug: '', descripcion: '', precio: '',
  precio_antes: '', imagen_url: '', categoria_id: null as number | null,
  marca_id: null as number | null, disponible: true,
})

const prodsFiltrados = computed(() =>
  productos.value.filter(p => {
    const busOk = p.nombre.toLowerCase().includes(busqueda.value.toLowerCase()) ||
                  p.slug.toLowerCase().includes(busqueda.value.toLowerCase())
    const catOk = !filtrarCat.value || p.categoriaId === Number(filtrarCat.value)
    return busOk && catOk
  })
)

function abrirNuevo() {
  editandoId.value = null
  form.value = { nombre: '', slug: '', descripcion: '', precio: '', precio_antes: '', imagen_url: '', categoria_id: null, marca_id: null, disponible: true }
  panelAbierto.value = true
}

function abrirEditar(p: Prod) {
  editandoId.value = p.id
  form.value = {
    nombre: p.nombre, slug: p.slug, descripcion: p.descripcion,
    precio: String(p.precio), precio_antes: p.precioAnterior ? String(p.precioAnterior) : '',
    imagen_url: p.imagen, categoria_id: p.categoriaId, marca_id: p.marcaId, disponible: p.disponible,
  }
  panelAbierto.value = true
}

async function cargar() {
  const token = getAccessToken()
  if (!token) { router.push({ name: 'admin-login' }); return }
  cargando.value = true; errorMsg.value = ''
  try {
    const [prods, cats, mrcs] = await Promise.all([
      apiFetchAuth<ProdApi[] | { results: ProdApi[] }>('/catalogo/admin/productos/', token),
      apiFetch<CatApi[]>('/catalogo/categorias/'),
      apiFetch<MarcaApi[]>('/catalogo/marcas/'),
    ])
    const lista = unwrapResults<ProdApi>(prods)
    productos.value = lista.map(mapProd)
    categorias.value = cats
    marcas.value = mrcs
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Error cargando productos'
  } finally { cargando.value = false }
}

async function guardar() {
  const token = getAccessToken()
  if (!token) return
  guardando.value = true; errorMsg.value = ''
  try {
    const body = {
      nombre: form.value.nombre, slug: form.value.slug,
      descripcion: form.value.descripcion, precio: form.value.precio,
      precio_antes: form.value.precio_antes || null,
      imagen_url: form.value.imagen_url,
      categoria_id: form.value.categoria_id,
      marca_id: form.value.marca_id,
      disponible: form.value.disponible,
    }
    if (editandoId.value == null) {
      const c = await apiFetchAuth<ProdApi>('/catalogo/admin/productos/', token, { method: 'POST', body: JSON.stringify(body) })
      productos.value = [mapProd(c), ...productos.value]
    } else {
      const u = await apiFetchAuth<ProdApi>(`/catalogo/admin/productos/${editandoId.value}/`, token, { method: 'PATCH', body: JSON.stringify(body) })
      productos.value = productos.value.map(p => p.id === u.id ? mapProd(u) : p)
    }
    panelAbierto.value = false
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error guardando'
  } finally { guardando.value = false }
}

async function eliminar(p: Prod) {
  const token = getAccessToken()
  if (!token) return
  if (!confirm(`¿Eliminar "${p.nombre}"?`)) return
  errorMsg.value = ''
  try {
    await apiFetchAuth<void>(`/catalogo/admin/productos/${p.id}/`, token, { method: 'DELETE' })
    productos.value = productos.value.filter(pr => pr.id !== p.id)
  } catch (e) { errorMsg.value = e instanceof Error ? e.message : 'Error eliminando' }
}

function formatPrecio(n: number) { return `$${n.toLocaleString('es-CO')}` }

onMounted(cargar)
</script>

<template>
  <div class="p-6 lg:p-10">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8 flex-wrap gap-4">
      <div>
        <p class="text-[10px] tracking-[0.35em] uppercase text-[#f5d984]/70 mb-1">Catálogo</p>
        <h2 class="text-2xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">Productos</h2>
      </div>
      <button @click="abrirNuevo"
        class="flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-4 py-2.5 hover:opacity-90 transition">
        <Plus class="h-4 w-4" /> Nuevo producto
      </button>
    </div>

    <!-- Filtros -->
    <div class="flex flex-wrap gap-3 mb-6">
      <input v-model="busqueda" type="text" placeholder="Buscar por nombre o slug…"
        class="admin-input flex-1 min-w-[200px]" />
      <select v-model="filtrarCat" class="admin-input min-w-[160px]">
        <option value="">Todas las categorías</option>
        <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
      </select>
    </div>

    <div v-if="errorMsg" class="mb-5 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">{{ errorMsg }}</div>
    <div v-if="cargando" class="py-16 text-center text-[11px] text-white/40">Cargando productos…</div>

    <!-- Tabla -->
    <div v-else class="bg-white/5 border border-white/[0.07] rounded overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/[0.07] text-left">
              <th class="px-4 py-3 text-[10px] font-black tracking-widest uppercase text-white/30 w-14">Img</th>
              <th class="px-4 py-3 text-[10px] font-black tracking-widest uppercase text-white/30">Nombre</th>
              <th class="px-4 py-3 text-[10px] font-black tracking-widest uppercase text-white/30 hidden md:table-cell">Categoría</th>
              <th class="px-4 py-3 text-[10px] font-black tracking-widest uppercase text-white/30 hidden lg:table-cell">Marca</th>
              <th class="px-4 py-3 text-[10px] font-black tracking-widest uppercase text-white/30">Precio</th>
              <th class="px-4 py-3 text-[10px] font-black tracking-widest uppercase text-white/30 hidden sm:table-cell">Estado</th>
              <th class="px-4 py-3 w-20"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/[0.05]">
            <tr
              v-for="p in prodsFiltrados" :key="p.id"
              class="hover:bg-white/[0.03] transition-colors"
            >
              <td class="px-4 py-3">
                <img :src="p.imagen" :alt="p.nombre" class="h-10 w-10 object-cover bg-white/5 rounded" />
              </td>
              <td class="px-4 py-3">
                <p class="font-semibold text-white leading-tight">{{ p.nombre }}</p>
                <p class="text-[10px] text-white/30">/{{ p.slug }}</p>
              </td>
              <td class="px-4 py-3 hidden md:table-cell text-white/50 text-[12px]">{{ p.categoria }}</td>
              <td class="px-4 py-3 hidden lg:table-cell text-white/50 text-[12px]">{{ p.marca }}</td>
              <td class="px-4 py-3">
                <p class="font-bold text-[#f5d984]">{{ formatPrecio(p.precio) }}</p>
                <p v-if="p.precioAnterior" class="text-[10px] text-white/30 line-through">{{ formatPrecio(p.precioAnterior) }}</p>
              </td>
              <td class="px-4 py-3 hidden sm:table-cell">
                <span class="inline-block text-[9px] font-bold tracking-widest uppercase px-2 py-0.5"
                  :class="p.disponible ? 'bg-emerald-500/20 text-emerald-300' : 'bg-white/10 text-white/30'">
                  {{ p.disponible ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center gap-1">
                  <button @click="abrirEditar(p)" class="p-1.5 text-white/40 hover:text-[#f5d984] transition" title="Editar">
                    <Pencil class="h-3.5 w-3.5" />
                  </button>
                  <button @click="eliminar(p)" class="p-1.5 text-white/40 hover:text-red-300 transition" title="Eliminar">
                    <Trash2 class="h-3.5 w-3.5" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!prodsFiltrados.length">
              <td colspan="7" class="px-4 py-12 text-center text-[11px] text-white/30">No hay productos.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Panel lateral de edición -->
  <transition name="slide-panel">
    <div v-if="panelAbierto" class="fixed inset-0 z-[60] flex justify-end">
      <div class="absolute inset-0 bg-black/50" @click="panelAbierto = false" />
      <div class="relative w-full max-w-md bg-[#0f1612] border-l border-white/[0.07] h-full flex flex-col shadow-2xl">
        <!-- Header panel -->
        <div class="flex items-center justify-between border-b border-white/[0.07] px-6 py-5 shrink-0">
          <h3 class="text-sm font-black uppercase tracking-widest">{{ editandoId == null ? 'Nuevo producto' : 'Editar producto' }}</h3>
          <button @click="panelAbierto = false" class="p-1.5 text-white/40 hover:text-white hover:bg-white/10 rounded transition">
            <X class="h-4 w-4" />
          </button>
        </div>

        <!-- Form -->
        <div class="flex-1 overflow-y-auto p-6 space-y-4">
          <div v-if="errorMsg" class="border border-red-500/30 bg-red-500/10 px-3 py-2 text-[11px] text-red-200">{{ errorMsg }}</div>

          <div class="grid grid-cols-2 gap-4">
            <div class="col-span-2">
              <label class="admin-label">Nombre *</label>
              <input v-model="form.nombre" type="text" class="admin-input" />
            </div>
            <div class="col-span-2">
              <label class="admin-label">Slug *</label>
              <input v-model="form.slug" type="text" class="admin-input" />
            </div>
            <div>
              <label class="admin-label">Precio (COP) *</label>
              <input v-model="form.precio" type="number" class="admin-input" />
            </div>
            <div>
              <label class="admin-label">Precio anterior</label>
              <input v-model="form.precio_antes" type="number" class="admin-input" />
            </div>
            <div>
              <label class="admin-label">Categoría</label>
              <select v-model="form.categoria_id" class="admin-input">
                <option :value="null">—</option>
                <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
            <div>
              <label class="admin-label">Marca</label>
              <select v-model="form.marca_id" class="admin-input">
                <option :value="null">—</option>
                <option v-for="m in marcas" :key="m.id" :value="m.id">{{ m.nombre }}</option>
              </select>
            </div>
            <div class="col-span-2">
              <label class="admin-label">Imagen URL</label>
              <input v-model="form.imagen_url" type="text" class="admin-input" />
            </div>
            <div class="col-span-2">
              <label class="admin-label">Descripción</label>
              <textarea v-model="form.descripcion" rows="3" class="admin-input" />
            </div>
            <div class="col-span-2 flex items-center gap-3">
              <input v-model="form.disponible" type="checkbox" class="h-4 w-4 accent-[#f5d984]" />
              <label class="text-[11px] font-bold tracking-widest uppercase text-white/60 cursor-pointer">Disponible / Activo</label>
            </div>
          </div>
        </div>

        <!-- Footer panel -->
        <div class="border-t border-white/[0.07] px-6 py-4 flex justify-end gap-3 shrink-0">
          <button @click="panelAbierto = false" class="text-[11px] font-bold tracking-widest uppercase border border-white/15 px-5 py-2.5 hover:border-white/40 transition">
            Cancelar
          </button>
          <button @click="guardar" :disabled="guardando"
            class="text-[11px] font-bold tracking-widest uppercase bg-[#f5d984] text-[#314037] px-5 py-2.5 hover:opacity-90 transition disabled:opacity-40">
            {{ guardando ? 'Guardando…' : 'Guardar' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
@reference "../../style.css";
.admin-label { @apply block text-[10px] tracking-widest uppercase text-white/50 mb-1.5 }
.admin-input { @apply w-full px-3 py-2.5 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984] text-sm text-white rounded }
.slide-panel-enter-active, .slide-panel-leave-active { transition: opacity .2s ease }
.slide-panel-enter-active .relative, .slide-panel-leave-active .relative { transition: transform .25s ease }
.slide-panel-enter-from, .slide-panel-leave-to { opacity: 0 }
.slide-panel-enter-from .relative, .slide-panel-leave-to .relative { transform: translateX(100%) }
</style>
