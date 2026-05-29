<script setup lang="ts">
import { ref } from 'vue'
import { ChevronDown } from 'lucide-vue-next'

const faqActivo = ref<number | null>(null)

const faqs = [
  { pregunta: '¿Cada cuánto debo hacerme un examen visual?', respuesta: 'Se recomienda realizarse un chequeo visual cada 6 a 12 meses. Un examen a tiempo puede detectar problemas oculares antes de que afecten tu calidad de vida.' },
  { pregunta: '¿Qué incluye el examen visual?', respuesta: 'Nuestro examen incluye evaluación de agudeza visual, refracción, revisión de presión intraocular y salud general del ojo.' },
  { pregunta: '¿Hacen domicilios?', respuesta: 'Por el momento atendemos en nuestro local ubicado en Calle 19 #19-06, Betania, Antioquia. Puedes escribirnos por WhatsApp para agendar tu cita.' },
  { pregunta: '¿Cuáles son los métodos de pago?', respuesta: 'Aceptamos efectivo, transferencias bancarias y pagos por QR. Contáctanos para más información.' },
  { pregunta: '¿Tienen garantía en los productos?', respuesta: 'Sí, todos nuestros productos tienen garantía. Los detalles varían según el producto. Pregunta en tienda o por WhatsApp.' },
  { pregunta: '¿Trabajan con seguros médicos?', respuesta: 'Contáctanos directamente por WhatsApp para verificar si trabajamos con tu plan de salud.' },
]

const politicas = [
  { titulo: 'Política de Devoluciones', contenido: 'Los productos pueden devolverse dentro de los primeros 8 días de compra, siempre que estén en perfectas condiciones y con su empaque original. Productos personalizados como lentes con fórmula no aplican para devolución.' },
  { titulo: 'Política de Garantía', contenido: 'Ofrecemos garantía en monturas y lentes. Las monturas tienen garantía de 6 meses por defectos de fabricación. Los lentes oftálmicos tienen garantía de 3 meses. La garantía no cubre daños por mal uso.' },
  { titulo: 'Política de Privacidad', contenido: 'En Maná Óptical respetamos tu privacidad. La información que compartes con nosotros (nombre, contacto, datos de salud visual) es usada exclusivamente para brindarte nuestros servicios y nunca será compartida con terceros.' },
]
</script>

<template>
  <div class="pt-[108px]">

    <!-- Hero -->
    <div class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Información</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Páginas & Políticas
      </h1>
      <p class="text-white/50 text-sm">Preguntas frecuentes y políticas de nuestra óptica</p>
    </div>

    <!-- FAQ -->
    <section class="bg-white py-24 px-8 lg:px-16">
      <div class="max-w-3xl mx-auto">
        <div v-scroll-reveal class="flex flex-col items-center text-center mb-14">
          <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] font-medium mb-3">Dudas Frecuentes</p>
          <h2 class="text-3xl font-black tracking-tight text-black uppercase" style="font-family:'Playfair Display',serif;">
            Preguntas Frecuentes
          </h2>
        </div>

        <div class="space-y-2">
          <div
            v-for="(faq, i) in faqs"
            :key="i"
            v-scroll-reveal="{ delay: i * 60 }"
            class="border border-black/10 overflow-hidden"
          >
            <button
              @click="faqActivo = faqActivo === i ? null : i"
              class="w-full flex items-center justify-between px-6 py-5 text-left hover:bg-[#f8f7f5] transition-colors duration-300"
            >
              <span class="text-sm font-bold tracking-wide text-black">{{ faq.pregunta }}</span>
              <ChevronDown
                class="h-4 w-4 text-[#314037] flex-shrink-0 ml-4 transition-transform duration-300"
                :class="{ 'rotate-180': faqActivo === i }"
              />
            </button>
            <div
              v-show="faqActivo === i"
              class="px-6 pb-5 text-sm text-black/55 leading-relaxed border-t border-black/8 pt-4"
            >
              {{ faq.respuesta }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Políticas -->
    <section class="bg-[#f8f7f5] py-24 px-8 lg:px-16">
      <div class="max-w-4xl mx-auto">
        <div v-scroll-reveal class="flex flex-col items-center text-center mb-14">
          <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] font-medium mb-3">Información Legal</p>
          <h2 class="text-3xl font-black tracking-tight text-black uppercase" style="font-family:'Playfair Display',serif;">
            Nuestras Políticas
          </h2>
        </div>

        <div class="space-y-6">
          <div
            v-for="(pol, i) in politicas"
            :key="pol.titulo"
            v-scroll-reveal="{ delay: i * 100 }"
            class="bg-white p-8 border-l-4 border-[#314037]"
          >
            <h3 class="text-sm font-black tracking-widest uppercase text-[#314037] mb-4">{{ pol.titulo }}</h3>
            <p class="text-sm text-black/55 leading-relaxed">{{ pol.contenido }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA contacto -->
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-white/50 text-sm mb-4">¿Tienes más preguntas?</p>
      <a
        href="https://wa.me/573005262309"
        target="_blank"
        class="btn-shine inline-flex items-center gap-3 bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity"
      >
        Escríbenos por WhatsApp
      </a>
    </section>

  </div>
</template>
