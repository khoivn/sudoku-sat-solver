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
    # result = {"numberOfClause": 11988,
    #           "result": [[6, 9, 3, 7, 8, 4, 5, 1, 2], [4, 8, 7, 5, 1, 2, 9, 3, 6], [1, 2, 5, 9, 6, 3, 8, 7, 4],
    #                      [9, 3, 2, 6, 5, 1, 4, 8, 7], [5, 6, 8, 2, 4, 7, 3, 9, 1], [7, 4, 1, 3, 9, 8, 6, 2, 5],
    #                      [3, 1, 9, 4, 7, 5, 2, 6, 8], [8, 5, 6, 1, 2, 9, 7, 4, 3], [2, 7, 4, 8, 3, 6, 1, 5, 9]],
    #           "timeInSecond": 0.060225486755371094}
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="localhost", port=7777, debug=True)
