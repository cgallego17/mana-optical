<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar />
    <RouterView />
    <Footer />
  </div>
</template>
