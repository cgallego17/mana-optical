<script setup lang="ts">
</script>

<template>
  <div class="pt-[108px]">
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Tu compra</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Carrito
      </h1>
      <p class="text-white/60 text-sm max-w-2xl mx-auto text-center">Revisa tus productos y procede al pago.</p>
    </section>

    <section class="bg-white py-16 px-6 lg:px-12">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <div class="lg:col-span-2 space-y-4">
          <div v-for="i in 3" :key="i" class="flex items-center gap-4 border border-black/10 p-4">
            <div class="h-16 w-16 bg-[#f8f7f5] border border-black/10" />
            <div class="flex-1">
              <p class="text-sm font-semibold text-black/80">Producto {{ i }}</p>
              <p class="text-xs text-black/50">Variante / detalle</p>
            </div>
            <div class="text-sm text-black/70">$ 100.000</div>
          </div>
        </div>
        <div class="border border-black/10 p-6 h-fit">
          <h3 class="text-sm font-black tracking-[0.3em] uppercase text-[#314037] mb-4">Resumen</h3>
          <div class="flex items-center justify-between text-sm py-2">
            <span class="text-black/60">Subtotal</span>
            <span class="text-black/80">$ 300.000</span>
          </div>
          <div class="flex items-center justify-between text-sm py-2 border-b border-black/10">
            <span class="text-black/60">Envío</span>
            <span class="text-black/80">$ 10.000</span>
          </div>
          <div class="flex items-center justify-between text-sm py-3">
            <span class="font-bold text-black">Total</span>
            <span class="font-bold text-black">$ 310.000</span>
          </div>
          <button class="w-full mt-4 btn-shine bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity">
            Proceder al pago
          </button>
        </div>
      </div>
    </section>
  </div>
</template>
