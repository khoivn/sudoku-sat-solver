from pysat.solvers import Glucose3
import time
import math


class EncodingMode:
    BINOMIAL = 'BINOMIAL'
    SEQUENTIAL = 'SEQUENTIAL'
    BINARY = 'BINARY'
    COMMANDER = 'COMMANDER'
    PRODUCT = 'PRODUCT'


class SudokuSatSolver():
    def __init__(self, blockSize: int, clues: [[]], method: str):
        self.blockSize = blockSize
        self.clues = clues
        self.method = method
        self.size = blockSize * blockSize
        self.clauses = []
        self.defaultVariables = self.size ** 3
        self.customVariables = 0

    def exactOneWithBinomialEncoding(self, variables: [], append=True):
        newClauses = [variables]
        for i in range(len(variables) - 1):
            for j in range(i + 1, len(variables)):
                newClauses.append([-variables[i], -variables[j]])
        if append:
            self.clauses.extend(newClauses)
        return newClauses

    def exactOneWithSequentialEncoding(self, variables: []):
        indexFrom = self.defaultVariables + self.customVariables
        self.customVariables += len(variables) - 1

        self.clauses.append(variables)
        self.clauses.append([-variables[0], indexFrom + 1])
        self.clauses.append([-variables[self.size - 1], -(indexFrom + self.size - 1)])
        for i in range(2, self.size):
            self.clauses.append([-variables[i - 1], indexFrom + i])
            self.clauses.append([-(indexFrom + i - 1), indexFrom + i])
            self.clauses.append([-(indexFrom + i - 1), -variables[i - 1]])

    def exactOneWithBinaryEncoding(self, variables):
        self.clauses.append(variables)
        binarySize = math.ceil(math.log2(len(variables)))
        for i, variable in enumerate(variables):
            for j, sign in enumerate(self.toSignList(i, binarySize)):
                self.clauses.append([-variable, - sign * (self.defaultVariables + self.customVariables + j + 1)])
        self.customVariables += binarySize

    def exactOneWithCommanderEncoding(self, variables: []):
        p = math.ceil(math.sqrt(len(variables)))
        q = math.ceil(len(variables) / p)
        fromIndex = self.defaultVariables + self.customVariables
        self.customVariables += q

        newVariables = [fromIndex + i for i in range(1, q + 1)]
        groups = [variables[i:i + p] for i in range(0, len(variables), p)]

        self.exactOneWithBinomialEncoding(newVariables)
        for i, group in enumerate(groups):
            newVariable = fromIndex + i + 1
            self.clauses += [[-newVariable] + c for c in self.exactOneWithBinomialEncoding(group, False)]
            for x in group:
                self.clauses.append([newVariable, -x])

    def exactOneWithProductEncoding(self, variables: []):
        self.clauses.append(variables)
        p = math.ceil(math.sqrt(len(variables)))
        q = math.ceil(len(variables) / p)

        fromIndex = self.defaultVariables + self.customVariables
        self.customVariables += p + q

        for i in range(1, p):
            for j in range(i + 1, p + 1):
                self.clauses.append([-(fromIndex + i), -(fromIndex + j)])

        for i in range(1, q):
            for j in range(i + 1, q + 1):
                self.clauses.append([-(fromIndex + p + i), -(fromIndex + p + j)])

        for i, var in enumerate(variables):
            r = int(i / q) + 1
            c = i % q + 1
            self.clauses.append([-var, fromIndex + r])
            self.clauses.append([-var, fromIndex + p + c])

    def exactOneConstraint(self, variables: []):
        if self.method == EncodingMode.SEQUENTIAL:
            self.exactOneWithSequentialEncoding(variables)
        elif self.method == EncodingMode.PRODUCT:
            self.exactOneWithSequentialEncoding(variables)
        elif self.method == EncodingMode.BINARY:
            self.exactOneWithBinaryEncoding(variables)
        else:
            self.exactOneWithBinomialEncoding(variables)

    def convert(self, i: int, j: int, k: int):
        return (i - 1) * self.size * self.size + (j - 1) * self.size + k

    def toSignList(self, a: int, size: int):
        return [1 if int(i) == 1 else -1 for i in list(bin(a).replace("0b", "").zfill(size))]

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
            for ii in range(1, self.blockSize + 1):
                for jj in range(1, self.blockSize + 1):
                    variables = [self.convert(i, j, k) for i in
                                 range((ii - 1) * self.blockSize + 1, ii * self.blockSize + 1) for j in
                                 range((jj - 1) * self.blockSize + 1, jj * self.blockSize + 1)]
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

        result = g.get_model()[:self.defaultVariables]
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
        return Result(self.method, satisfiable, result, self.defaultVariables + self.customVariables, numberOfClause,
                      numberOfClauseTotal,
                      (stopTime - startTime) * 1000)


class Result:
    def __init__(self, method: str, satisfiable: bool, result: [[]], numberOfVariable: int, numberOfClause: int,
                 numberOfClauseTotal: int, timeInMilisecond: float):
        self.method = method
        self.satisfiable = satisfiable
        self.result = result
        self.numberOfVariable = numberOfVariable
        self.numberOfClause = numberOfClause
        self.numberOfClauseTotal = numberOfClauseTotal
        self.timeInMilisecond = timeInMilisecond
