from pysat.solvers import Glucose3
import time


class SudokuSatSolver():
    class EncodingMode:
        BINOMIAL = 'BINOMIAL'
        SEQUENTIAL = 'SEQUENTIAL'

    def __init__(self, blockSize: int, clues: [[]], mode: str):
        self.blockSize = blockSize
        self.clues = clues
        self.mode = mode
        self.size = blockSize * blockSize
        self.clauses = []
        self.count = 0
        self.variables = self.size ** 3
        self.customVariables = 0

    def exactOneWithSequentialEncoding(self, variables: []):
        indexFrom = self.variables + self.count * (self.size - 1)
        self.count += 1
        self.customVariables += len(variables) - 1

        self.clauses.append(variables)
        self.clauses.append([-variables[0], indexFrom + 1])
        self.clauses.append([-variables[self.size - 1], -(indexFrom + self.size - 1)])
        for i in range(2, self.size):
            self.clauses.append([-variables[i - 1], indexFrom + i])
            self.clauses.append([-(indexFrom + i - 1), indexFrom + i])
            self.clauses.append([-(indexFrom + i - 1), -variables[i - 1]])

    def exactOneWithBinomialEncoding(self, variables: []):
        self.clauses.append(variables)
        for i in range(len(variables) - 1):
            for j in range(i + 1, len(variables)):
                self.clauses.append([-variables[i], -variables[j]])

    def exactOneConstraint(self, variables: []):
        if self.mode == self.EncodingMode.SEQUENTIAL:
            self.exactOneWithSequentialEncoding(variables)
        else:
            self.exactOneWithBinomialEncoding(variables)

    def convert(self, i: int, j: int, k: int):
        return (i - 1) * self.size * self.size + (j - 1) * self.size + k

    def addClausesWithCellConstraint(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                variables = [self.convert(i, j, k) for k in range(1, self.size + 1)]
                self.exactOneConstraint(variables)

    def addClausesWithRowConstraint(self):
        for i in range(1, self.size + 1):
            for k in range(1, self.size + 1):
                variables = [self.convert(i, j, k) for j in range(1, self.size + 1)]
                self.exactOneConstraint(variables)

    def addClausesWithColumnConstraint(self):
        for j in range(1, self.size + 1):
            for k in range(1, self.size + 1):
                variables = [self.convert(i, j, k) for i in range(1, self.size + 1)]
                self.exactOneConstraint(variables)

    def addClausesWithBlockConstraint(self):
        for k in range(1, self.size + 1):
            for ii in range(1, 4):
                for jj in range(1, 4):
                    variables = [self.convert(i, j, k) for i in range(ii * 3 - 2, ii * 3 + 1) for j in
                                 range(jj * 3 - 2, jj * 3 + 1)]
                    self.exactOneConstraint(variables)

    def addClausesWithClues(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                k = self.clues[i - 1][j - 1]
                if k and k.isdigit():
                    self.clauses.append([self.convert(i, j, int(k))])

    def satSolving(self):
        g = Glucose3()
        for c in self.clauses:
            g.add_clause(c)

        satisfiable = g.solve()
        if not satisfiable:
            return None, satisfiable

        result = g.get_model()[:self.variables]
        result = [next(k + 1 for k, l in enumerate(result[i:i + self.size]) if l > 0) for i in
                  range(0, len(result), self.size)]
        result = [result[i:i + self.size] for i in range(0, len(result), self.size)]
        return result, satisfiable

    def solve(self):
        startTime = time.time()
        self.addClausesWithCellConstraint()
        self.addClausesWithRowConstraint()
        self.addClausesWithColumnConstraint()
        self.addClausesWithBlockConstraint()
        numberOfClause = len(self.clauses)

        self.addClausesWithClues()
        numberOfClauseTotal = len(self.clauses)

        result, satisfiable = self.satSolving()
        stopTime = time.time()
        return {
            'satisfiable': satisfiable,
            'result': result,
            'numberOfVariable': self.variables + self.customVariables,
            'numberOfClause': numberOfClause,
            'numberOfClauseTotal': numberOfClauseTotal,
            'timeInSecond': stopTime - startTime}
