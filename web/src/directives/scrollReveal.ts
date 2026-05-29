import type { Directive } from 'vue'

export const vScrollReveal: Directive = {
  mounted(el: HTMLElement, binding) {
    const delay = binding.value?.delay ?? 0
    const direction = binding.value?.direction ?? 'up'

    const transforms: Record<string, string> = {
      up: 'translateY(60px)',
      left: 'translateX(60px)',
      right: 'translateX(-60px)',
    }

    el.classList.add('sr-init')
    el.style.setProperty('--sr-transform', transforms[direction] ?? transforms.up)
    el.style.setProperty('--sr-delay', `${delay}ms`)

    const show = () => {
      el.classList.add('sr-visible')
      el.classList.remove('sr-init')
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(show, delay)
          observer.disconnect()
        }
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    )

    // Fallback: reveal after 1.5s regardless
    const fallback = setTimeout(show, 1500 + delay)

    observer.observe(el)

    // Store cleanup
    ;(el as any).__srCleanup = () => {
      clearTimeout(fallback)
      observer.disconnect()
    }
  },
  unmounted(el: HTMLElement) {
    ;(el as any).__srCleanup?.()
  },
}
