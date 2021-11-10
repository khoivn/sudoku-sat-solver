from SudokuSatSolver import SudokuSatSolver, EncodingMode

if __name__ == '__main__':
    BLOCK_SIZE = 4
    FILE_NAME = "sudoku_16x16.txt"

    clues = []
    with open(FILE_NAME, "r") as f:
        for line in f.readlines():
            clue = line.strip().split("|")
            assert len(clue) == BLOCK_SIZE * BLOCK_SIZE
            clues.append(clue)

    solver = SudokuSatSolver(BLOCK_SIZE, clues, EncodingMode.SEQUENTIAL)
    result = solver.solve()
    for row in result.result:
        print(row)
