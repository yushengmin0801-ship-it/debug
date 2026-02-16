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
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const display = ref('0')
const previousExpression = ref('')
const loading = ref(false)
const error = ref('')

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
    const response = await fetch('https://curly-space-spoon-wr6v5654jwj5h57x9-8080.app.github.dev/api/calculate', {
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
  } catch (err) {
    error.value = 'Calculation failed: ' + err.message
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>
