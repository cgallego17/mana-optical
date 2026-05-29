<script setup lang="ts">
import { ShieldCheck, Leaf, ArrowRight } from 'lucide-vue-next'

const features = [
  { icon: ShieldCheck, title: 'Protección luz azul', description: 'Nuestras lentes filtran hasta el 95% de la luz azul dañina de pantallas y dispositivos digitales.' },
  { icon: Leaf, title: 'Materiales sostenibles', description: 'Fabricamos con materiales ecológicos certificados para cuidar tu salud y el planeta.' },
]
</script>

<template>
  <section class="w-full">
    <div class="flex flex-col lg:flex-row" style="min-height: 520px;">

      <!-- Left: photo -->
      <div class="flex-1 overflow-hidden min-h-[380px]">
        <img
          src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=900&q=80"
          alt="Hombre con gafas"
          class="w-full h-full object-cover object-top block"
        />
      </div>

      <!-- Center: product showcase -->
      <div class="w-full lg:w-52 flex-shrink-0 bg-white shadow-2xl z-10 flex flex-col divide-y divide-black/8">
        <div class="flex-1 flex items-center justify-center p-6 bg-[#f8f7f5]">
          <img
            src="https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=400&q=80"
            alt="Gafas redondas"
            class="w-full object-contain max-h-28"
          />
        </div>
        <div class="flex-1 flex items-center justify-center p-6 bg-white">
          <img
            src="https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=400&q=80"
            alt="Gafas cuadradas"
            class="w-full object-contain max-h-28"
          />
        </div>
      </div>

      <!-- Right: content -->
      <div class="flex-1 bg-[#f8f7f5] flex items-center px-10 xl:px-16 py-16">
        <div v-scroll-reveal class="w-full max-w-sm">
          <span class="inline-block text-[11px] tracking-[0.35em] uppercase text-[#f5d984] font-medium mb-4">Tecnología Óptica</span>
          <h2 class="text-3xl font-black tracking-tight text-black uppercase leading-tight mb-4">
            Lente Óptico<br />Luz Azul
          </h2>
          <p class="text-sm text-black/50 mb-10 leading-relaxed">
            Tecnología óptica de última generación diseñada para proteger tu visión en el mundo digital.
          </p>

          <div class="space-y-7 mb-10">
            <div v-for="feature in features" :key="feature.title" class="flex items-start gap-4">
              <div class="flex-shrink-0 mt-1 h-8 w-8 rounded-full bg-[#314037] flex items-center justify-center">
                <component :is="feature.icon" class="h-3.5 w-3.5 text-white" />
              </div>
              <div>
                <h4 class="text-xs font-black tracking-widest uppercase text-black mb-1.5">{{ feature.title }}</h4>
                <p class="text-xs text-black/45 leading-relaxed">{{ feature.description }}</p>
              </div>
            </div>
          </div>

          <button class="btn-shine animate-glow active:scale-95 inline-flex items-center gap-3 bg-[#314037] text-white text-[11px] font-bold tracking-[0.25em] uppercase px-8 py-4 hover:bg-[#f5d984] hover:text-[#314037] transition-colors duration-300">
            Ver Más <ArrowRight class="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

    </div>
  </section>
</template>
