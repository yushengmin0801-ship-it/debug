import json
import http.server
import random

class GomokuAI:
    def __init__(self, size=15):
        self.size = size

    def get_move(self, board):
        # board: 0-empty, 1-black(human), 2-white(ai)
        best_score = -float('inf')
        best_moves = []
        
        # Heuristic search
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == 0:
                    score = self.evaluate_position(board, r, c)
                    if score > best_score:
                        best_score = score
                        best_moves = [(r, c)]
                    elif score == best_score:
                        best_moves.append((r, c))
        
        return random.choice(best_moves) if best_moves else None

    def evaluate_position(self, board, r, c):
        # Simple heuristic: sum of potential in 4 directions
        score = 0
        for dr, dc in [(1,0), (0,1), (1,1), (1,-1)]:
            score += self.check_direction(board, r, c, dr, dc)
        return score

    def check_direction(self, board, r, c, dr, dc):
        score = 0
        # Check human threats (Defensive) and AI opportunities (Offensive)
        for p in [2, 1]: # 2 is AI, 1 is Human
            count = 0
            for i in range(-4, 5):
                if i == 0: continue
                nr, nc = r + dr*i, c + dc*i
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if board[nr][nc] == p:
                        count += 1
                    elif board[nr][nc] != 0:
                        count = 0 # Blocked
                        break
            weight = 10 ** count
            if p == 1: weight *= 1.1 # Prioritize defense slightly
            score += weight
        return score

class AIHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        board = data['board']
        
        ai = GomokuAI()
        move = ai.get_move(board)
        
        response = {'row': move[0], 'col': move[1]} if move else {'error': 'no moves'}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 8080), AIHandler)
    print("AI Server V3 on 8080...")
    server.serve_forever()
