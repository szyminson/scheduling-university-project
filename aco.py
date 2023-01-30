import random
from common import calc_cost, check_constraints, get_shifts_with_cost, max_employees, employees_needed

N_ANTS = 10
N_ITERATIONS = 100


def run_ant(trail: list, max_employees: int, shifts_cost: list) -> tuple:
    solution = []
    for i in range(7):
        probs = [trail[i][j]**2/sum([trail[i][j]**2 for j in range(
            max_employees)]) for j in range(max_employees)]
        selected = random.choices(
            range(max_employees), weights=probs, k=1)[0]
        solution.append(selected)
    cost = calc_cost(solution, shifts_cost)
    return cost, solution


def run_iteration(trail: list, max_employees: int, shifts_with_cost: tuple):
    shifts, shifts_cost = shifts_with_cost
    solutions = []
    costs = []
    for _ in range(N_ANTS):
        cost, solution = run_ant(trail, max_employees, shifts_cost)
        if check_constraints(solution, shifts, employees_needed):
            solutions.append(solution)
            costs.append(cost)
    return costs, solutions


def update_pheromone_trail(trail: list, iteration_solutions: list, best: tuple) -> list:
    best_ant, best_cost = best
    for i in range(7):
        for j in range(max_employees):
            trail[i][j] *= 0.95
    for i in range(7):
        for j in range(iteration_solutions[best_ant][i]):
            trail[i][j] += 1/best_cost
    return trail


def run(shifts: list, shifts_cost: list, employees_needed: list) -> tuple:
    best_cost = None
    best_solution = None
    pheromone_trail = [
        [random.uniform(0, 1) for i in range(max_employees)] for j in range(7)]

    for _ in range(N_ITERATIONS):
        iteration_costs, iteration_solutions = run_iteration(pheromone_trail, max_employees,
                                                             (shifts, shifts_cost))
        if iteration_costs:
            best_ant = iteration_costs.index(min(iteration_costs))
            if not best_cost or iteration_costs[best_ant] < best_cost:
                best_cost = iteration_costs[best_ant]
                best_solution = iteration_solutions[best_ant]
            update_pheromone_trail(pheromone_trail,
                                   iteration_solutions, (best_ant, best_cost))

    return best_cost, best_solution


if __name__ == '__main__':
    shifts, shifts_cost = get_shifts_with_cost()
    cost, solution = run(shifts, shifts_cost, employees_needed)
    print('cost:', cost)
    print('solution:', solution)
