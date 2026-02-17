# API 接口设计文档 - 历史记录

## 1. 接口: 获取历史记录
- **Method**: `GET /api/history`
- **Request**: 无参数
- **Response**: `List<String>`
- **Sample**: `["5 + 3 = 8", "10 * 2 = 20"]`

## 2. 接口: 计算
- **Method**: `POST /api/calculate` (无需修改，但计算成功后需自动存入历史记录)
