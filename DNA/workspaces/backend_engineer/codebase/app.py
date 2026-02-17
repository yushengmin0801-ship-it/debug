from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)


@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]
    empty_cells = [(r, c) for r in range(15) for c in range(15) if board[r][c] == 0]
    if not empty_cells:
        return jsonify({"error": "full"})
    row, col = random.choice(empty_cells)
    return jsonify({"row": row, "col": col})


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
