from SudokuSatSolver import SudokuSatSolver, EncodingMode

if __name__ == '__main__':
    BLOCK_SIZE = 7
    FILE_NAME = "sudoku_49x49.txt"
    METHOD = EncodingMode.PRODUCT

    clues = []
    with open(FILE_NAME, "r") as f:
        for line in f.readlines():
            if not line.strip():
                continue
            clue = line.strip().split("|")
            assert len(clue) == BLOCK_SIZE * BLOCK_SIZE
            clues.append(clue)

    solver = SudokuSatSolver(BLOCK_SIZE, clues, METHOD)
    result = solver.solve()
    print(f"Method: {result.method}")
    print(f"Satisfiable: {result.satisfiable}")
    print(f"Variables: {result.numberOfVariable}")
    print(f"Clauses: {result.numberOfClause}")
    print(f"Clauses with input: {result.numberOfClauseTotal}")
    print(f"Execution time (ms): {result.timeInMilisecond}")
    if result.satisfiable:
        print()
        for row in result.result:
            print(row)
