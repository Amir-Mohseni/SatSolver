import math
from random import uniform
from pysat.formula import CNF
from pysat.solvers import Solver
import matplotlib.pyplot as plt

from tsat import ThreeSAT


class Annealer:
    def __init__(self,
                 sat,
                 temp=95,
                 maxcalls=500000,
                 tempmin=0.01,
                 alpha=0.05,
                 maxpert=100):
        self.sat = sat
        self.clauses = self.sat.clauses
        self.solution = sat.init_solution
        self.temp = temp
        self.tempmin = tempmin
        self.alpha = 1-alpha
        self.maxcalls = maxcalls
        self.maxpert = maxpert
        self.temp_list = []
        self.cost_list = []

    ''' Acceptance probability function. As the temperature falls, it should
        tend to zero. (Except when the proposed solution's cost is lower than
        the current solution's)'''
    def acceptance_probability(self, old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        else:
            return math.exp(-(new_cost - old_cost) / temperature)

    ''' Runs the annealer '''
    def run(self):
        solutions = []
        counter = 0
        sol_out = self.sat.init_solution
        sol_out_fo = self.sat.eval(sol_out)
        temp = self.temp
        self.temp_list.append(temp)
        self.cost_list.append(self.sat.num_clauses - sol_out_fo)
        while temp > self.tempmin and counter < self.maxcalls:
            i = 1
            success = 0
            while i <= self.maxpert:
                sol = self.sat.perturbation(sol_out)
                sol_fo = self.sat.eval(sol)
                delta = sol_out_fo - sol_fo
                ap = self.acceptance_probability(sol_out_fo, sol_fo, temp)
                if ap > uniform(0, 1):
                    sol_out = sol
                    sol_out_fo = sol_fo
                    success += 1
                i += 1
            temp = temp*self.alpha
            self.temp_list.append(temp)
            self.cost_list.append(self.sat.num_clauses - sol_out_fo)
            counter += 1
            print(sol_out_fo)
            if sol_out_fo == 0:
                if sol_out not in solutions:
                    solutions.append(sol_out)
        print("Solutions: " + str(len(solutions)))
        print(str(counter) + " iterations")
        return solutions

sat = ThreeSAT('Input.cnf')
sa = Annealer(sat, temp=100, tempmin=0.01, alpha=0.05, maxpert=100)
print("Running annealer...")
sa.run()

fig, ax = plt.subplots()
ax.set_ylabel("Clauses satisfied")
ax.set_xlabel("Temperature")
ax.plot(sa.temp_list[:], sa.cost_list[:])
plt.xlim(plt.xlim()[::-1])             # Reverses x axis
plt.show()