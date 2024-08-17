from pysat.solvers import Glucose3

class PropositionalLogic:
    def __init__(self):
        self.clauses = set()

    def adding_clause(self, clause):
        normalized_clause = tuple(sorted(clause))
        self.clauses.add(normalized_clause)

    def removing_clause(self, clause):
        normalized_clause = tuple(sorted(clause))
        self.clauses.discard(normalized_clause)

    def is_inferable(self, hypothesis):
        solver = Glucose3()
        for clause in self.clauses:
            solver.add_clause(list(clause))
        for clause in hypothesis:
            solver.add_clause(clause)
        return not solver.solve()
