import { ref } from 'vue'

const isOpen = ref(false)
const query = ref('')

function open(q?: string) {
  if (q) query.value = q
  isOpen.value = true
}
function close() {
  isOpen.value = false
  query.value = ''
}

export function useSearchOverlay() {
  return { isOpen, query, open, close }
}
