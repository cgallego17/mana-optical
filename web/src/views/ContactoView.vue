<script setup lang="ts">
import { Mail, Phone, MapPin, Clock, Send, Instagram, Facebook, Twitter } from 'lucide-vue-next'
</script>

<template>
  <div class="pt-[108px]">
    <!-- Hero -->
    <section class="bg-[#314037] py-16 px-8 text-center relative overflow-hidden">
      <div class="absolute inset-0 opacity-[0.06] pointer-events-none" style="background-image: radial-gradient(#f5d984 1px, transparent 1px); background-size: 18px 18px;" />
      <p class="relative text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Estamos para ayudarte</p>
      <h1 class="relative text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Contacto
      </h1>
      <p class="relative text-white/70 text-sm max-w-2xl mx-auto text-center">Escríbenos, llámanos o visítanos. Respuesta rápida y atención cercana.</p>
    </section>

    <!-- Content -->
    <section class="bg-white py-20 px-6 lg:px-12">
      <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10">
        <!-- Info card -->
        <div class="relative overflow-hidden border border-black/10 bg-[#f8f7f5]">
          <div class="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-[#f5d984]/30 blur-2xl" />
          <div class="p-8 lg:p-10 space-y-6 relative">
            <h3 class="text-sm font-black tracking-[0.3em] uppercase text-[#314037]">Datos de contacto</h3>

            <div class="space-y-3">
              <a href="mailto:manaoptical2@gmail.com" class="group flex items-center gap-3 text-sm text-black/70 hover:text-[#314037] transition-colors">
                <Mail class="h-4 w-4 text-[#314037]" />
                <span>manaoptical2@gmail.com</span>
              </a>
              <a href="https://wa.me/573005262309" target="_blank" class="group flex items-center gap-3 text-sm text-black/70 hover:text-[#314037] transition-colors">
                <Phone class="h-4 w-4 text-[#314037]" />
                <span>300 526 2309</span>
              </a>
              <div class="flex items-start gap-3 text-sm text-black/70">
                <MapPin class="h-4 w-4 text-[#314037] mt-0.5" />
                <span>Calle 19 #19-06<br/>Betania, Antioquia</span>
              </div>
              <div class="flex items-center gap-3 text-sm text-black/70">
                <Clock class="h-4 w-4 text-[#314037]" />
                <span>Lun–Sáb: 9:00 AM – 9:00 PM</span>
              </div>
            </div>

            <div class="pt-2">
              <div class="text-[11px] font-bold tracking-[0.25em] uppercase text-black/40 mb-3">Redes</div>
              <div class="flex items-center gap-4">
                <a href="#" class="text-[#314037] hover:opacity-70 transition"><Instagram class="h-4 w-4" /></a>
                <a href="#" class="text-[#314037] hover:opacity-70 transition"><Facebook class="h-4 w-4" /></a>
                <a href="#" class="text-[#314037] hover:opacity-70 transition"><Twitter class="h-4 w-4" /></a>
              </div>
            </div>

            <div class="h-56 bg-white border border-black/10 flex items-center justify-center text-black/40 text-xs">
              Mapa próximamente
            </div>
          </div>
        </div>

        <!-- Form card -->
        <form class="border border-black/10 bg-white p-6 md:p-8 lg:p-10 shadow-sm">
          <div class="text-center md:text-left mb-6">
            <p class="text-[11px] tracking-[0.35em] uppercase text-black/40 font-semibold">Escríbenos</p>
            <h3 class="text-xl font-black tracking-tight text-black uppercase" style="font-family:'Playfair Display',serif;">Formulario de contacto</h3>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label class="block">
              <span class="sr-only">Nombre</span>
              <input required type="text" placeholder="Nombre*" class="w-full border border-black/10 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#f5d984] placeholder:text-black/40" />
            </label>
            <label class="block">
              <span class="sr-only">Correo</span>
              <input required type="email" placeholder="Correo*" class="w-full border border-black/10 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#f5d984] placeholder:text-black/40" />
            </label>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <label class="block">
              <span class="sr-only">Teléfono</span>
              <input type="tel" placeholder="Teléfono" class="w-full border border-black/10 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#f5d984] placeholder:text-black/40" />
            </label>
            <label class="block">
              <span class="sr-only">Asunto</span>
              <select class="w-full border border-black/10 px-4 py-3 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#f5d984] text-black/70">
                <option>Consulta general</option>
                <option>Agendar cita</option>
                <option>Productos y precios</option>
                <option>Otros</option>
              </select>
            </label>
          </div>
          <label class="block mt-4">
            <span class="sr-only">Mensaje</span>
            <textarea rows="6" required placeholder="Mensaje*" class="w-full border border-black/10 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#f5d984] placeholder:text-black/40"></textarea>
          </label>
          <div class="flex items-start gap-3 mt-4">
            <input id="consent" type="checkbox" class="mt-1 h-4 w-4 border-black/20" />
            <label for="consent" class="text-xs text-black/60">Acepto la política de privacidad. <RouterLink to="/paginas" class="underline hover:text-black">Ver políticas</RouterLink></label>
          </div>
          <div class="pt-6">
            <button type="button" class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity">
              <Send class="h-4 w-4" /> Enviar mensaje
            </button>
          </div>
        </form>
      </div>
    </section>

    <!-- CTA WhatsApp -->
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-white/70 text-sm mb-4 text-center">¿Prefieres hablar ahora mismo?</p>
      <a
        href="https://wa.me/573005262309" target="_blank"
        class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity"
      >
        Escríbenos por WhatsApp
      </a>
    </section>
  </div>
</template>
