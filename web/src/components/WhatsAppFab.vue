<script setup lang="ts">
const phone = '573005262309'
const text = encodeURIComponent('Hola Mana Óptical, quiero agendar una cita. ¿Me ayudas, por favor?')
</script>

<template>
  <a
    class="fixed bottom-5 right-5 z-50"
    :href="`https://wa.me/${phone}?text=${text}`"
    target="_blank"
    rel="noopener noreferrer"
    aria-label="WhatsApp Mana Óptical"
  >
    <span class="group relative inline-flex">
      <span class="absolute -inset-3 rounded-full bg-[radial-gradient(circle_at_center,rgba(212,175,55,0.35),transparent_60%)] opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-100" />
      <span class="flex h-14 w-14 items-center justify-center rounded-full border border-[#D4AF37]/20 bg-[#0b1a10]/95 text-[#D4AF37] shadow-[0_22px_60px_rgba(0,0,0,0.35)] backdrop-blur-md transition-transform duration-300 group-hover:-translate-y-0.5">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-6 w-6">
          <path d="M20.52 3.48A11.94 11.94 0 0 0 12.06 0C5.49.03.19 5.33.22 11.91a11.86 11.86 0 0 0 1.62 6.06L0 24l6.2-1.62a11.92 11.92 0 0 0 5.86 1.58h.05c6.57-.03 11.87-5.33 11.9-11.9a11.86 11.86 0 0 0-3.49-8.58ZM12.1 21.53h-.05a9.62 9.62 0 0 1-4.9-1.34l-.35-.2-3.68.96.98-3.59-.23-.37a9.66 9.66 0 0 1-1.34-4.86c-.03-5.33 4.3-9.68 9.63-9.71h.04c2.57 0 4.99 1 6.81 2.83a9.57 9.57 0 0 1 2.84 6.84c-.02 5.32-4.35 9.64-9.75 9.64Zm5.55-7.05c-.3-.15-1.78-.88-2.06-.98-.28-.1-.48-.15-.68.15-.2.3-.78.98-.95 1.18-.18.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.78-1.68-2.08-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.53.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.53-.07-.15-.68-1.63-.94-2.23-.25-.6-.5-.52-.68-.53-.17-.01-.37-.01-.57-.01-.2 0-.53.08-.8.38-.28.3-1.07 1.05-1.07 2.56s1.1 2.97 1.25 3.18c.15.2 2.16 3.3 5.24 4.63.73.32 1.3.5 1.74.64.73.23 1.4.2 1.93.12.59-.09 1.78-.73 2.03-1.47.25-.74.25-1.38.17-1.52-.07-.14-.27-.22-.57-.37Z"/>
        </svg>
      </span>
    </span>
  </a>
</template>
