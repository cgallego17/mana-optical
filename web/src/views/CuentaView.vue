<script setup lang="ts">
</script>

<template>
  <div class="pt-[108px]">
    <section class="bg-[#314037] py-16 px-8 text-center">
      <p class="text-[11px] tracking-[0.4em] uppercase text-[#f5d984] mb-3">Tu perfil</p>
      <h1 class="text-4xl lg:text-5xl font-black text-white uppercase tracking-tight mb-3" style="font-family:'Playfair Display',serif;">
        Mi Cuenta
      </h1>
      <p class="text-white/60 text-sm max-w-2xl mx-auto text-center">Inicia sesión para gestionar tus datos y reservas.</p>
    </section>

    <section class="bg-white py-16 px-6 lg:px-12">
      <div class="max-w-md mx-auto space-y-4">
        <input type="email" placeholder="Correo" class="w-full border border-black/10 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#f5d984]" />
        <input type="password" placeholder="Contraseña" class="w-full border border-black/10 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#f5d984]" />
        <button class="btn-shine w-full bg-[#f5d984] text-[#314037] text-[11px] font-bold tracking-[0.25em] uppercase px-10 py-4 hover:opacity-90 transition-opacity">
          Iniciar sesión
        </button>
        <p class="text-center text-sm text-black/50">¿No tienes cuenta?
          <RouterLink to="/agenda" class="underline hover:text-black">Reserva tu cita</RouterLink>
        </p>
      </div>
    </section>
  </div>
</template>
