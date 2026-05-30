export interface Producto {
  id: number
  slug: string
  nombre: string
  categoria: string
  marca: string
  precio: number
  precioAnterior: number | null
  oferta: boolean
  imagen: string
  imagenes: string[]
  descripcion: string
  disponible: boolean
}

export const categorias = ['Todos', 'Monturas', 'Gafas de Sol', 'Lentes de Contacto', 'Accesorios'] as const

export const productos: Producto[] = [
  {
    id: 1, slug: 'lennons-metalicos',
    nombre: 'Lennons Metálicos', categoria: 'Monturas', marca: 'Maná Studio',
    precio: 175000, precioAnterior: 199000, oferta: true,
    imagen: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Montura redonda estilo Lennon en metal dorado mate. Ligera, resistente y elegante para uso diario. Compatible con lentes fotocromáticos y antirreflejo.',
    disponible: true,
  },
  {
    id: 2, slug: 'gafas-cat-eye',
    nombre: 'Gafas Cat Eye', categoria: 'Monturas', marca: 'Vision Pro',
    precio: 199000, precioAnterior: null, oferta: false,
    imagen: 'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Diseño cat-eye clásico en acetato negro brillante. Un ícono del estilo contemporáneo con ajuste preciso y gran durabilidad.',
    disponible: true,
  },
  {
    id: 3, slug: 'aviador-clasico',
    nombre: 'Aviador Clásico', categoria: 'Gafas de Sol', marca: 'Eye–Blue',
    precio: 211000, precioAnterior: null, oferta: false,
    imagen: 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Gafas de sol tipo aviador con lentes polarizadas y montura en acero inoxidable dorado. Protección UV400. Ideales para conducir y actividades al aire libre.',
    disponible: true,
  },
  {
    id: 4, slug: 'ovaladas-carey',
    nombre: 'Ovaladas Carey', categoria: 'Gafas de Sol', marca: 'Optical',
    precio: 189000, precioAnterior: 220000, oferta: true,
    imagen: 'https://images.unsplash.com/photo-1582142306909-195724d33ffc?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1582142306909-195724d33ffc?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Estilo retro con acabado carey de alta calidad. Lentes ahumados con filtro UV. Diseño unisex perfecto para playa y ciudad.',
    disponible: true,
  },
  {
    id: 5, slug: 'montura-delgada',
    nombre: 'Montura Delgada', categoria: 'Monturas', marca: 'Bionic',
    precio: 165000, precioAnterior: null, oferta: false,
    imagen: 'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1509695507497-903c140c43b0?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Montura ultra delgada de titanio flexible. Minimalismo y confort para todo el día. Disponible en negro, plata y dorado.',
    disponible: true,
  },
  {
    id: 6, slug: 'redondas-clip-on',
    nombre: 'Redondas Clip-On', categoria: 'Monturas', marca: 'Maná Studio',
    precio: 225000, precioAnterior: null, oferta: false,
    imagen: 'https://images.unsplash.com/photo-1473496169904-658ba7574b0d?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1473496169904-658ba7574b0d?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Montura redonda con clip-on magnético incluido para convertirlas en gafas de sol al instante. Versatilidad y estilo en un solo accesorio.',
    disponible: true,
  },
  {
    id: 7, slug: 'sol-cuadradas',
    nombre: 'Sol Cuadradas', categoria: 'Gafas de Sol', marca: 'Wear',
    precio: 195000, precioAnterior: null, oferta: false,
    imagen: 'https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1577803645773-f96470509666?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Gafas de sol cuadradas con lentes degradados y marco en acetato de alta calidad. Unisex. Protección UV400 certificada.',
    disponible: true,
  },
  {
    id: 8, slug: 'estuche-premium',
    nombre: 'Estuche Premium', categoria: 'Accesorios', marca: 'Maná Studio',
    precio: 35000, precioAnterior: null, oferta: false,
    imagen: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Estuche rígido en piel sintética con cierre magnético. Protección total para tus monturas. Incluye paño de limpieza de microfibra.',
    disponible: true,
  },
  {
    id: 9, slug: 'pano-microfibra',
    nombre: 'Paño Microfibra', categoria: 'Accesorios', marca: 'Maná Studio',
    precio: 15000, precioAnterior: null, oferta: false,
    imagen: 'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=900&q=80',
    imagenes: [
      'https://images.unsplash.com/photo-1508296695146-257a814070b4?auto=format&fit=crop&w=900&q=80',
    ],
    descripcion: 'Paño de microfibra ultra suave 30×30 cm. Limpieza eficaz sin rayar tus lentes. Lavable y reutilizable. Disponible en varios colores.',
    disponible: true,
  },
]

export function getProductoPorSlug(slug: string): Producto | undefined {
  return productos.find(p => p.slug === slug)
}

export function formatPrecio(n: number): string {
  return `$${n.toLocaleString('es-CO')}`
}
