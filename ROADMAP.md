# Roadmap — Maná Óptical (Django + Vue 3)

Este documento resume el plan por fases, con entregables, y marca con tachado lo que ya está hecho.

## Leyenda de estado
- [x] Completado (elemento también aparece ~~tachado~~)
- [ ] Pendiente
- [⏳] En progreso

---

## Fase 0 — Base del proyecto
- [x] ~~Pivot a Vue 3 (SPA) + Django backend~~
- [x] ~~Crear proyecto Vue en carpeta `web/`~~
- [x] ~~Configurar Tailwind v4 y estilos base (paleta dorado/negro, tipografía)~~
- [x] ~~NavBar sticky + Footer premium~~
- [x] ~~WhatsApp FAB flotante global~~
- [x] ~~Home premium con secciones (Hero, Agenda, Servicios, Catálogo, Testimonios, Galería, CTA)~~
- [x] ~~Rutas iniciales y vistas base: Servicios, Agenda, Galería, Contacto, Cuenta, Carrito, Páginas, 404~~
- [x] ~~Configurar Vite para `http://localhost:5173` y auto-open~~
- [x] ~~Fix de build producción (BlogView + TypeScript)~~
- [x] ~~Repositorio GitHub privado `cgallego17/mana-optical` y push inicial~~

## Fase 1 — UX rápidas y Finder
- [x] ~~Buscador como overlay (no página), apertura por icono y atajo Ctrl/⌘+K~~
- [x] ~~Redirigir `/buscar` al Home~~
- [x] ~~Botón flotante “Volver arriba” con smooth scroll~~

## Fase 1.1 — Responsive y correcciones (menús, navbar, FABs)
- [x] ~~Menú móvil: abrir/cerrar con scroll lock del body, z-index sobre overlays, áreas táctiles ≥44px.~~
- [x] ~~Navbar: altura y compactación al hacer scroll, wrapping correcto de enlaces, sombras/bordes sutiles.~~
- [x] ~~FABs (WhatsApp y BackToTop): posición que no se superponga, respeto de safe areas (env(safe-area-inset-*)), ocultar en modals/overlays.~~
- [x] ~~Ajustes de breakpoints: paddings/margins en hero, grids y CTAs; tamaños de tipografía para legibilidad.~~
- [x] ~~QA responsive: overflow horizontal corregido (HeroSection + Footer brands bar); menú móvil z-index y scroll-lock arreglados.~~

Aceptación:
- No hay solapamientos entre menú móvil, overlay de búsqueda y FABs.
- Interacciones accesibles (teclado/Esc/lectores) y objetivos táctiles ≥44px.
- Sin scroll “doble” del body al abrir modals/menús; z-index consistente.

## Fase 2 — Tienda moderna y Ficha de producto
- [x] ~~Rediseño `/tienda` con grid premium, filtros (categoría, orden, solo ofertas), sidebar desktop + drawer móvil, y “quick view” modal.~~
- [x] ~~Ficha de producto `/producto/:slug`: galería con miniaturas, precio con descuento, descripción, CTAs (Carrito / WhatsApp), productos relacionados, CTA de agenda.~~
- [x] ~~Estado vacío con botón “Limpiar filtros”; datos compartidos en `src/data/productos.ts`.~~
- [x] ~~Paginación o carga infinita cuando haya más de 20 productos (backend).~~

## Fase 3 — Agenda en modal (día + hora)
- [x] ~~Modal de agenda desde cualquier página: 4 pasos (servicio → fecha → hora → datos), accesible con Esc.~~
- [x] ~~Calendario mensual con días deshabilitados (domingos, pasados, >30 días) + selector de franjas horarias.~~
- [x] ~~Confirmación con WhatsApp deep link (mensaje pre-armado). Integrado en Hero, BookingSection, AgendaView y ProductoView.~~
- [ ] Validación real de disponibilidad contra backend DRF (pendiente Fase 4).

## Fase 4 — Backend Django (DRF) y modelos
- [x] ~~Configuración DRF + CORS + JWT.~~
- [⏳] Modelos y slugs SEO: Productos, Categorías, Marcas, Servicios, Clientes, Citas (timezone America/Bogota).
  - [x] ~~Catálogo: Categorías, Marcas, Productos~~
  - [x] ~~Agenda: Servicios, Reservas~~
  - [x] ~~Clientes~~
- [⏳] Endpoints REST: catálogo, búsqueda unificada, agenda (disponibilidad y reservas), blog, contenido del Home.
  - [x] ~~Health: `/api/health/`~~
  - [x] ~~Catálogo: `/api/catalogo/productos/` y `/api/catalogo/productos/<slug>/`~~
  - [x] ~~Agenda: `/api/agenda/disponibilidad/?fecha=YYYY-MM-DD` y `POST /api/agenda/reservas/`~~
  - [x] ~~Búsqueda unificada: `/api/busqueda/?q=...`~~
  - [x] ~~Blog + contenido Home~~
- [x] ~~Seeds/datos ejemplo y admin de Django como respaldo técnico.~~

## Fase 5 — Panel de administración SPA
- [x] ~~Login (JWT) y protección de rutas admin con guard en router (beforeEach con matched.some).~~
- [x] ~~Dashboard con KPIs: total productos, posts publicados, reservas totales y pendientes.~~
- [x] ~~CRUD Catálogo: productos (tabla + panel lateral), categorías y marcas (edición inline).~~
- [x] ~~CRUD Blog: lista de posts + editor (título, slug, categoría, extracto, contenido HTML, publicado).~~
- [x] ~~Agenda: tabla de reservas con filtro por estado y cambio de estado (confirmar/cancelar); CRUD de servicios.~~
- [x] ~~Sidebar de navegación con sub-rutas (/admin/dashboard, /admin/productos, /admin/blog, etc.), responsive (hamburger móvil).~~

## Fase 6 — SEO avanzado, URLs y PWA
- [x] ~~Metadatos dinámicos por ruta: `<title>`, `<meta description>`, canonical, OG/Twitter en `router.afterEach`. Composable `useSeo` reutilizable.~~
- [x] ~~URLs con slugs legibles: `/producto/:slug` ✅, `/categoria/:slug` ✅ (vista filtrada por categoría), `/blog/:slug` ✅.~~
- [x] ~~JSON-LD: `Organization/LocalBusiness` (global en App), `Product` + `BreadcrumbList` (ProductoView), `BlogPosting` + `BreadcrumbList` (BlogPostView).~~
- [x] ~~`sitemap.xml` con 8 rutas y prioridades, `robots.txt` con Disallow para `/admin/` y `/api/`.~~
- [x] ~~Lazy loading (`loading="lazy"`) en imágenes de TiendaView, ProductoView, CategoriaView, BlogView, BlogPostView, BookingSection.~~
- [x] ~~PWA: `manifest.webmanifest` con shortcuts (Tienda, Agenda, Blog), Service Worker con cache-first para assets y network-first para navegación.~~
- [ ] Lighthouse SEO/Perf > 90 (requiere deploy en producción con HTTPS para medir con precisión).

---

## Hitos y entregables
- PR1 (F1): Overlay de búsqueda + FAB “Top” + redirección `/buscar`.
- PR2 (F2): Tienda moderna + Quick View + Ficha de producto + slugs.
- PR3 (F3+F4): Agenda modal + endpoints de disponibilidad/reserva (DRF + JWT + CORS).
- PR4 (F5): Panel admin SPA (auth, dashboard, CRUDs completos).
- PR5 (F6): SEO/URLs + sitemaps + JSON-LD + PWA + optimización de performance.

## Estado actual (resumen)
- ✅ Frontend SPA con Home premium y páginas base.
- ✅ UX rápidas: overlay de búsqueda, botón “Volver arriba”, WhatsApp FAB.
- ✅ Responsive corregido: navbar, hero, footer, overflow.
- ✅ Tienda premium: sidebar filtros, quick view modal, grid responsivo.
- ✅ Ficha de producto `/producto/:slug` con galería, precios, relacionados.
- ✅ Agenda modal: 4 pasos, calendario, horarios, WhatsApp deep link.
- ✅ Admin SPA completo: sidebar, dashboard KPIs, CRUDs de catálogo, blog y agenda.
- ✅ SEO completo: OG/Twitter, JSON-LD, canonical, sitemap, robots.txt, lazy loading, PWA.
- ✅ Ruta `/categoria/:slug` con vista filtrada y breadcrumb.
- 🕒 Pendiente: deploy en producción + Lighthouse audit real.

## Próximo paso sugerido
1) Implementar `Clientes` (modelo + endpoints) si aplica.
2) Blog + contenido Home (endpoints + admin).
3) Panel admin SPA (JWT + CRUDs).

---

## Anexos (rutas y archivos clave)
- Frontend: `web/` (Vite + Vue 3 + Tailwind v4)
- Router: `web/src/router/index.ts`
- Overlay búsqueda: `web/src/components/SearchOverlay.vue` + `web/src/composables/searchOverlay.ts`
- FAB Top: `web/src/components/BackToTop.vue`
- WhatsApp FAB: `web/src/components/WhatsAppFab.vue`
- Home y layout: `web/src/App.vue`, `web/src/components/NavBar.vue`, `web/src/components/Footer.vue`
- Contacto mejorado: `web/src/views/ContactoView.vue`
- GitHub: https://github.com/cgallego17/mana-optical
