from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
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
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="localhost", port=7777, debug=True)
