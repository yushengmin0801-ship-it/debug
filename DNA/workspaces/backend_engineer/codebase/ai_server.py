import http.server
import json
import random


class AIHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        board = data["board"]

        best_score = -1
        best_moves = []

        def get_score(r, c, player):
            score = 0
            opponent = 3 - player
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
            for dr, dc in directions:
                # 己方连子
                mine = 0
                for i in range(1, 5):
                    nr, nc = r + dr * i, c + dc * i
                    if 0 <= nr < 15 and 0 <= nc < 15 and board[nr][nc] == player:
                        mine += 1
                    else:
                        break
                for i in range(1, 5):
                    nr, nc = r - dr * i, c - dc * i
                    if 0 <= nr < 15 and 0 <= nc < 15 and board[nr][nc] == player:
                        mine += 1
                    else:
                        break

                # 敌方连子 (防守核心：权重极大提升)
                his = 0
                for i in range(1, 5):
                    nr, nc = r + dr * i, c + dc * i
                    if 0 <= nr < 15 and 0 <= nc < 15 and board[nr][nc] == opponent:
                        his += 1
                    else:
                        break
                for i in range(1, 5):
                    nr, nc = r - dr * i, c - dc * i
                    if 0 <= nr < 15 and 0 <= nc < 15 and board[nr][nc] == opponent:
                        his += 1
                    else:
                        break

                # AI 的胜手
                if mine >= 4:
                    score += 100000
                # 堵截玩家
                if his >= 4:
                    score += 50000
                if his >= 3:
                    score += 10000

                score += (mine**3) + (his**3.5)
            return score

        for r in range(15):
            for c in range(15):
                if board[r][c] == 0:
                    s = get_score(r, c, 2)
                    if s > best_score:
                        best_score = s
                        best_moves = [(r, c)]
                    elif s == best_score:
                        best_moves.append((r, c))

        move = random.choice(best_moves) if best_moves else {"error": "full"}
        response = {"row": move[0], "col": move[1]} if isinstance(move, tuple) else move

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", 8080), AIHandler)
    server.serve_forever()
