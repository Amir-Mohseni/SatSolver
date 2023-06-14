from random import randint
from copy import deepcopy


class ThreeSAT:
    def __init__(self, fname):
        self.num_vars = 0
        self.num_clauses = 0
        self.fname = fname
        self.clauses = self.proposition_read()
        self.init_solution = self.initial_solution()

    ''' Reads proposition from file '''
    def proposition_read(self):
        f = open(self.fname, 'r').readlines()
        header = f[3:4]
        clauses = f[4:]

        splt_hdr = header[0].split()
        num_vars = int(splt_hdr[2])
        num_clauses = int(splt_hdr[3])

        clauses_res = []

        ''' Maps each clause to int list; appends list to list of clauses. '''
        for i in range(0, num_clauses):
            mapped = list(map(int, clauses[i].split()[:-1]))
            clauses_res.append(mapped)

        assert(len(clauses_res) == num_clauses) # Checks for trouble ;)

        self.num_vars = num_vars
        self.num_clauses = num_clauses
        return clauses_res

    ''' Generates a random initial solution. '''
    def initial_solution(self):
        solution = {}
        for i in range(1, self.num_vars + 1):
            val = randint(-1, 1) == 0
            solution[i] = val
        return solution

    ''' Evaluates a given solution; returns num_clauses - passes. This way, as
        the number of true clauses increases, the evaluation tends to zero '''
    def eval(self, solution):
        passes = 0
        for clause in self.clauses:
            a = clause[0]
            b = clause[1]
            c = clause[2]

            sol_a = solution.get(a)
            sol_b = solution.get(b)
            sol_c = solution.get(c)

            if a < 0: sol_a = not sol_a
            if b < 0: sol_b = not sol_b
            if c < 0: sol_c = not sol_c

            if sol_a or sol_b or sol_c:
                passes += 1
                continue
        return self.num_clauses - passes

    ''' Changes a single value of a solution to its negation in order to disturb
        the solution '''
    def perturbation(self, solution):
        new_sol = deepcopy(solution)
        altered = randint(1, self.num_vars)
        val = new_sol.get(altered)
        new_sol[altered] = not val
        return new_sol
