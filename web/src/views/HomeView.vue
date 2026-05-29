<script setup lang="ts">
import HeroSection from '../components/HeroSection.vue'
import ServicesSection from '../components/ServicesSection.vue'
import ProductsSection from '../components/ProductsSection.vue'
import ParallaxDivider from '../components/ParallaxDivider.vue'
import BookingSection from '../components/BookingSection.vue'
import AppointmentSection from '../components/AppointmentSection.vue'
import InstagramSection from '../components/InstagramSection.vue'
import BlogSection from '../components/BlogSection.vue'
</script>

<template>
  <div>
    <HeroSection />
    <ServicesSection />
    <ProductsSection />

    <ParallaxDivider
      image="https://images.unsplash.com/photo-1577744486770-020ab432da65?auto=format&fit=crop&w=1600&q=80"
      quote="La visión es el arte de ver lo que otros no pueden ver"
      label="Maná Óptical — Visión con Propósito"
    />

    <BookingSection />

    <ParallaxDivider
      image="https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=1600&q=80"
      quote="Tu mirada merece el mejor cuidado y el mejor estilo"
      label="Especialistas en Salud Visual"
      height="300px"
    />

    <BlogSection />
    <AppointmentSection />
    <InstagramSection />
  </div>
</template>
