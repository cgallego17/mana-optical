<script setup lang="ts">
defineProps<{
  image: string
  quote?: string
  label?: string
  height?: string
}>()
</script>

<template>
  <div
    class="relative w-full flex items-center justify-center"
    :style="{
      height: height ?? '360px',
      backgroundImage: `url('${image}')`,
      backgroundAttachment: 'fixed',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }"
  >
    <div class="absolute inset-0 bg-black/70" />

    <div class="relative z-10 text-center px-6 max-w-2xl mx-auto">
      <span v-if="label" class="inline-block text-[10px] tracking-[0.5em] uppercase text-[#f5d984] font-medium mb-6">
        — {{ label }} —
      </span>
      <p
        v-if="quote"
        class="text-3xl md:text-4xl text-white leading-snug"
        style="font-family: 'Playfair Display', serif; font-style: italic; font-weight: 400;"
      >
        "{{ quote }}"
      </p>
    </div>
  </div>
</template>
