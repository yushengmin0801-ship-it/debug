<template>
  <div class="game-container">
    <h1>古典五子棋</h1>
    <div class="status">{{ status }}</div>
    <div class="board-wrapper">
      <div class="board" ref="boardRef">
        <div v-for="r in 15" :key="r" class="row">
          <div v-for="c in 15" :key="c" class="cell" @click="handleClick(r-1, c-1)">
            <div v-if="grid[r-1][c-1] === 1" class="stone black"></div>
            <div v-if="grid[r-1][c-1] === 2" class="stone white"></div>
          </div>
        </div>
      </div>
    </div>
    <button @click="reset">重新开始</button>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const grid = ref(Array(15).fill().map(() => Array(15).fill(0)))
const status = ref('玩家执黑，请落子')
const gameOver = ref(false)

const handleClick = async (r, c) => {
  if (grid.value[r][c] !== 0 || gameOver.value) return
  grid.value[r][c] = 1
  status.value = 'AI 思考中...'
  
  try {
    const res = await axios.post('/api/move', { board: grid.value })
    if (res.data) {
      grid.value[res.data.row][res.data.col] = 2
      status.value = '玩家执黑，请落子'
    }
  } catch (e) {
    status.value = '连接服务器失败'
  }
}

const reset = () => {
  grid.value = Array(15).fill().map(() => Array(15).fill(0))
  gameOver.value = false
  status.value = '玩家执黑，请落子'
}
</script>

<style scoped>
.game-container { display: flex; flex-direction: column; align-items: center; background: #fdf5e6; height: 100vh; padding: 20px; font-family: serif; }
.board-wrapper { background: #deb887; padding: 10px; border: 2px solid #8b4513; border-radius: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
.board { display: flex; flex-direction: column; width: 90vw; max-width: 450px; height: 90vw; max-height: 450px; }
.row { display: flex; flex: 1; }
.cell { flex: 1; border: 0.5px solid #8b4513; display: flex; justify-content: center; align-items: center; position: relative; cursor: pointer; }
.stone { width: 80%; height: 80%; border-radius: 50%; box-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
.black { background: radial-gradient(circle at 30% 30%, #444, #000); }
.white { background: radial-gradient(circle at 30% 30%, #fff, #ccc); }
.status { margin-bottom: 20px; font-size: 20px; font-weight: bold; color: #5d4037; }
button { margin-top: 20px; padding: 10px 20px; background: #8b4513; color: white; border: none; border-radius: 4px; cursor: pointer; }
</style>
