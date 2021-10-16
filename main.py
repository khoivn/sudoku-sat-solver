from SudokuSatSolver import SudokuSatSolver

if __name__ == '__main__':
    clues = []
    with open("sudoku.txt", "r") as f:
        for line in f.readlines():
            clues.append(line.strip().split("|"))

    solver = SudokuSatSolver(3, clues, SudokuSatSolver.EncodingMode.BINOMIAL)
    result = solver.solve()
    print(result)
