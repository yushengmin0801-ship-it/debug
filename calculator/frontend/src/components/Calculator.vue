<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100 p-4">
    <div class="bg-white rounded-3xl shadow-2xl p-6 w-full max-w-xs">
      <div class="mb-6">
        <div class="text-right text-gray-500 text-sm h-6 overflow-hidden">{{ previousExpression }}</div>
        <div class="text-right text-4xl font-bold text-gray-800 break-all min-h-[3rem]">{{ display }}</div>
      </div>
      
      <div class="grid grid-cols-4 gap-3">
        <button @click="clear" class="col-span-2 bg-red-100 text-red-600 font-bold py-4 rounded-2xl hover:bg-red-200 transition">AC</button>
        <button @click="append('%')" class="bg-blue-100 text-blue-600 font-bold py-4 rounded-2xl hover:bg-blue-200 transition">%</button>
        <button @click="append('/')" class="bg-orange-100 text-orange-600 font-bold py-4 rounded-2xl hover:bg-orange-200 transition">/</button>
        
        <button @click="append('7')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">7</button>
        <button @click="append('8')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">8</button>
        <button @click="append('9')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">9</button>
        <button @click="append('*')" class="bg-orange-100 text-orange-600 font-bold py-4 rounded-2xl hover:bg-orange-200 transition">×</button>
        
        <button @click="append('4')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">4</button>
        <button @click="append('5')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">5</button>
        <button @click="append('6')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">6</button>
        <button @click="append('-')" class="bg-orange-100 text-orange-600 font-bold py-4 rounded-2xl hover:bg-orange-200 transition">-</button>
        
        <button @click="append('1')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">1</button>
        <button @click="append('2')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">2</button>
        <button @click="append('3')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">3</button>
        <button @click="append('+')" class="bg-orange-100 text-orange-600 font-bold py-4 rounded-2xl hover:bg-orange-200 transition">+</button>
        
        <button @click="append('0')" class="col-span-2 bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">0</button>
        <button @click="append('.')" class="bg-gray-100 text-gray-700 font-bold py-4 rounded-2xl hover:bg-gray-200 transition">.</button>
        <button @click="calculate" class="bg-orange-500 text-white font-bold py-4 rounded-2xl hover:bg-orange-600 shadow-lg transition" :disabled="loading">
          {{ loading ? '...' : '=' }}
        </button>
      </div>
      
      <div v-if="error" class="mt-4 text-red-500 text-xs text-center">
        {{ error }}
      </div>

      <!-- History Section -->
      <div class="mt-6 border-t border-gray-200 pt-4">
        <h3 class="font-bold text-gray-700 mb-2 text-sm uppercase tracking-wide">History</h3>
        <ul class="text-sm text-gray-600 space-y-2 max-h-40 overflow-y-auto">
          <li v-for="(item, index) in history" :key="index" class="bg-gray-50 p-2 rounded-lg border border-gray-100 flex justify-between">
             <span>{{ item }}</span>
          </li>
          <li v-if="history.length === 0" class="text-gray-400 italic text-xs">No history yet</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const display = ref('0')
const previousExpression = ref('')
const loading = ref(false)
const error = ref('')
const history = ref([])

const fetchHistory = async () => {
  try {
    const res = await fetch('http://localhost:8080/api/history')
    if (res.ok) {
      history.value = await res.json()
    }
  } catch (e) {
    console.error("Failed to fetch history", e)
  }
}

onMounted(() => {
  fetchHistory()
})

const append = (char) => {
  if (display.value === '0' && !['/', '*', '-', '+', '.', '%'].includes(char)) {
    display.value = char
  } else {
    display.value += char
  }
}

const clear = () => {
  display.value = '0'
  previousExpression.value = ''
  error.value = ''
}

const calculate = async () => {
  if (display.value === '0' || !display.value) return
  
  loading.value = true
  error.value = ''
  
  // Simple parser for num1 operator num2
  const match = display.value.match(/^(-?\d+\.?\d*)([\+\-\*\/])(-?\d+\.?\d*)$/)
  if (!match) {
    error.value = 'Please enter a simple expression like 5+3'
    loading.value = false
    return
  }

  const [_, n1, op, n2] = match
  previousExpression.value = display.value
  
  try {
    const response = await fetch('http://localhost:8080/api/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        num1: parseFloat(n1), 
        num2: parseFloat(n2), 
        operator: op 
      }),
    })
    
    if (!response.ok) {
      throw new Error('API Error')
    }
    
    const data = await response.json()
    display.value = data.result.toString()
    await fetchHistory() // Refresh history
  } catch (err) {
    error.value = 'Calculation failed: ' + err.message
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>
