# Project Ancient-Harmony (古典五子棋) 需求文档

## 1. 技术架构
- **Backend**: Django 4.x + Django REST Framework (DRF)。
- **Frontend**: Vue 3 (SFC) + Vite + TailwindCSS。
- **Deployment**: Codespace Port 8000 (Django) & 3000 (Vue)。

## 2. 核心逻辑
- **AI 引擎**: 迁移并优化之前的启发式搜索算法至 Python 类。
- **响应式**: 棋盘大小根据屏幕宽度动态调整 (min 320px)。

## 3. 验收标准
- 必须通过 Django 接口获取 AI 下棋坐标。
- 手机打开无错位，点击响应延迟 < 200ms。
