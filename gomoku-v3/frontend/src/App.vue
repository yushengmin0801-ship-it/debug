<template>
  <div class="app-wrap">
    <div class="header">
      <h1>古典五子棋</h1>
      <div class="status">{{ status }}</div>
    </div>
    
    <div class="board-container">
      <div class="board" :style="{ width: boardSizePx + 'px', height: boardSizePx + 'px' }">
        <!-- Lines -->
        <div v-for="i in 15" :key="'h'+i" class="line horizontal" :style="{ top: (i-1)*cellSizePx + cellSizePx/2 + 'px' }"></div>
        <div v-for="i in 15" :key="'v'+i" class="line vertical" :style="{ left: (i-1)*cellSizePx + cellSizePx/2 + 'px' }"></div>
        
        <div v-for="(row, rIndex) in board" :key="rIndex" class="row">
          <div 
            v-for="(cell, cIndex) in row" :key="cIndex" 
            class="cell" 
            :style="{ width: cellSizePx + 'px', height: cellSizePx + 'px' }"
            @click="placeStone(rIndex, cIndex)"
          >
            <div v-if="cell === 1" class="stone black"></div>
            <div v-if="cell === 2" class="stone white"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <button @click="resetGame">重开一局</button>
    </div>

    <div v-if="winner" class="modal">
      <div class="modal-content">
        <h2>{{ winner === 1 ? '你赢了！' : 'AI赢了！' }}</h2>
        <button @click="resetGame">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const board = ref(Array(15).fill().map(() => Array(15).fill(0)))
const status = ref('请落子')
const winner = ref(null)
const lock = ref(false)

const boardSizePx = ref(300)
const cellSizePx = computed(() => boardSizePx.value / 15)

const updateSize = () => {
  boardSizePx.value = Math.min(window.innerWidth - 40, 450)
}

async function placeStone(r, c) {
  if (board.value[r][c] !== 0 || winner.value || lock.value) return
  
  board.value[r][c] = 1
  if (checkWin(r, c, 1)) {
    winner.value = 1
    status.value = '胜利！'
    return
  }

  status.value = 'AI 思考中...'
  lock.value = true
  
  try {
    const res = await axios.post('/api/move', { board: board.value })
    const { row, col } = res.data
    board.value[row][col] = 2
    if (checkWin(row, col, 2)) {
      winner.value = 2
      status.value = '惜败...'
    } else {
      status.value = '请落子'
    }
  } catch (e) {
    console.error(e)
    status.value = 'AI 接口异常'
  } finally {
    lock.value = false
  }
}

function checkWin(r, c, p) {
  const dirs = [[1,0],[0,1],[1,1],[1,-1]]
  for (const [dr, dc] of dirs) {
    let count = 1
    let nr = r + dr, nc = c + dc
    while (nr >= 0 && nr < 15 && nc >= 0 && nc < 15 && board.value[nr][nc] === p) { count++; nr += dr; nc += dc }
    nr = r - dr; nc = c - dc
    while (nr >= 0 && nr < 15 && nc >= 0 && nc < 15 && board.value[nr][nc] === p) { count++; nr -= dr; nc -= dc }
    if (count >= 5) return true
  }
  return false
}

function resetGame() {
  board.value = Array(15).fill().map(() => Array(15).fill(0))
  winner.value = null
  status.value = '请落子'
}

onMounted(() => {
  updateSize()
  window.addEventListener('resize', updateSize)
})
</script>

<style>
body { margin: 0; background: #f4ece0; font-family: "Kaiti", serif; overflow-x: hidden; }
.app-wrap { display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 20px; box-sizing: border-box; }
.header h1 { color: #3e2723; margin: 0; letter-spacing: 5px; font-size: 1.8rem; }
.status { background: #5d4037; color: #fff; padding: 5px 20px; border-radius: 20px; margin-top: 10px; font-weight: bold; }
.board-container { background: #dcb35c; padding: 10px; border: 3px solid #5d4037; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin: 20px 0; border-radius: 4px; position: relative; }
.board { display: flex; flex-direction: column; position: relative; }
.row { display: flex; flex: 1; z-index: 2; }
.cell { display: flex; justify-content: center; align-items: center; cursor: pointer; }
.line { position: absolute; background: #3e2723; opacity: 0.7; }
.horizontal { width: 100%; height: 1px; left: 0; }
.vertical { height: 100%; width: 1px; top: 0; }
.stone { width: 90%; height: 90%; border-radius: 50%; box-shadow: 2px 4px 6px rgba(0,0,0,0.3); }
.black { background: radial-gradient(circle at 30% 30%, #555, #000); }
.white { background: radial-gradient(circle at 30% 30%, #fff, #ccc); }
.footer button { background: #5d4037; color: #fff; border: none; padding: 10px 30px; font-size: 1.1rem; border-radius: 5px; cursor: pointer; }
.modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 100; }
.modal-content { background: #fff; padding: 30px; border-radius: 10px; text-align: center; border: 5px solid #dcb35c; }
</style>
