<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuth } from '../composables/auth'

const router = useRouter()
const { login } = useAuth()

const username = ref('')
const password = ref('')
const cargando = ref(false)
const errorMsg = ref('')

async function onSubmit() {
  cargando.value = true
  errorMsg.value = ''
  try {
    await login(username.value, password.value)
    await router.push({ name: 'admin-dashboard' })
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Error de autenticación'
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#0f1612] text-white flex items-center justify-center px-6">
    <div class="w-full max-w-md bg-white/5 border border-white/10 backdrop-blur-sm p-8 shadow-2xl">
      <div class="mb-8 text-center">
        <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Admin</p>
        <h1 class="text-3xl font-black uppercase tracking-tight" style="font-family:'Playfair Display',serif;">
          Iniciar sesión
        </h1>
        <p class="text-white/50 text-sm mt-2">Panel de administración Maná Óptical</p>
      </div>

      <div v-if="errorMsg" class="mb-5 border border-red-500/30 bg-red-500/10 px-4 py-3 text-[11px] text-red-200">
        {{ errorMsg }}
      </div>

      <form class="space-y-4" @submit.prevent="onSubmit">
        <div>
          <label class="block text-[10px] tracking-widest uppercase text-white/60 mb-2">Usuario</label>
          <input
            v-model="username"
            type="text"
            autocomplete="username"
            class="w-full px-4 py-3 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984]/60 text-sm"
          />
        </div>

        <div>
          <label class="block text-[10px] tracking-widest uppercase text-white/60 mb-2">Contraseña</label>
          <input
            v-model="password"
            type="password"
            autocomplete="current-password"
            class="w-full px-4 py-3 bg-black/30 border border-white/10 outline-none focus:border-[#f5d984]/60 text-sm"
          />
        </div>

        <button
          type="submit"
          :disabled="cargando"
          class="btn-shine w-full mt-2 inline-flex items-center justify-center bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase py-3.5 disabled:opacity-60"
        >
          {{ cargando ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>
  </div>
</template>
