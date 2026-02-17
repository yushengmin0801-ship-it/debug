import random
class GomokuAI:
    def get_best_move(self, board):
        size = 15
        best_score = -1
        best_moves = []
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    s = self._eval(board, r, c)
                    if s > best_score:
                        best_score = s
                        best_moves = [(r, c)]
                    elif s == best_score:
                        best_moves.append((r, c))
        return random.choice(best_moves) if best_moves else None
    def _eval(self, board, r, c):
        score = 0
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            score += self._line(board, r, c, dr, dc, 2) * 1.5 # AI
            score += self._line(board, r, c, dr, dc, 1) * 1.0 # Player
        return score
    def _line(self, board, r, c, dr, dc, p):
        count = 0
        for i in range(1, 5):
            nr, nc = r+dr*i, c+dc*i
            if 0<=nr<15 and 0<=nc<15 and board[nr][nc] == p: count += 1
            else: break
        for i in range(1, 5):
            nr, nc = r-dr*i, c-dc*i
            if 0<=nr<15 and 0<=nc<15 and board[nr][nc] == p: count += 1
            else: break
        return count ** 3
