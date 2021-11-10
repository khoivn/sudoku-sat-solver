from flask import Flask, jsonify
from waitress import serve
from flask import render_template
from flask import request
from SudokuSatSolver import SudokuSatSolver

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/solve", methods=['POST'])
def solve():
    body = request.get_json()
    solver = SudokuSatSolver(int(body['blockSize']), body['data'], body['mode'])
    result = solver.solve()
    return jsonify(result.__dict__)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=7777)
