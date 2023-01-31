"""Ant colony optimization algorithm implementation for employee shifts scheduling"""
import random
from common import calc_cost, check_constraints, get_shifts_with_cost, get_employee_constraints

ant_number = 10
iteration_number = 100
evaporation_rate = .95


def run_ant(trail: list, max_employees: int, shifts_cost: list) -> tuple:
    """Run single ant"""
    solution = []
    for i in range(7):
        probs = [trail[i][j]**2/sum([trail[i][j]**2 for j in range(
            max_employees)]) for j in range(max_employees)]
        selected = random.choices(
            range(max_employees), weights=probs, k=1)[0]
        solution.append(selected)
    cost = calc_cost(solution, shifts_cost)
    return cost, solution


def run_iteration(trail: list, employees: tuple, shifts_with_cost: tuple):
    """Run single iteration of ants"""
    max_employees, employees_needed = employees
    shifts, shifts_cost = shifts_with_cost
    solutions = []
    costs = []
    for _ in range(ant_number):
        cost, solution = run_ant(trail, max_employees, shifts_cost)
        if check_constraints(solution, shifts, employees_needed):
            solutions.append(solution)
            costs.append(cost)
    return costs, solutions


def update_pheromone_trail(trail: list, iteration_solutions: list, best: tuple, max_employees: int) -> list:
    """Update pheromone trail based on best solution and evaporation rate"""
    best_ant, best_cost = best
    for i in range(7):
        for j in range(max_employees):
            trail[i][j] *= evaporation_rate
    for i in range(7):
        for j in range(iteration_solutions[best_ant][i]):
            trail[i][j] += 1/best_cost
    return trail


def run(shifts: list, shifts_cost: list, employees: tuple) -> tuple:
    """Run the algorithm"""
    max_employees, _ = employees
    best_cost = None
    best_solution = None
    pheromone_trail = [
        [random.uniform(0, 1) for _ in range(max_employees)] for _ in range(7)]

    for _ in range(iteration_number):
        iteration_costs, iteration_solutions = run_iteration(pheromone_trail, employees,
                                                             (shifts, shifts_cost))
        if iteration_costs:
            best_ant = iteration_costs.index(min(iteration_costs))
            if not best_cost or iteration_costs[best_ant] < best_cost:
                best_cost = iteration_costs[best_ant]
                best_solution = iteration_solutions[best_ant]
            update_pheromone_trail(pheromone_trail,
                                   iteration_solutions, (best_ant, best_cost),
                                   max_employees)

    return best_cost, best_solution


if __name__ == '__main__':
    try:
        shifts, shifts_cost = get_shifts_with_cost()
        cost, solution = run(shifts, shifts_cost, get_employee_constraints(1))
        print('cost:', cost)
        print('solution:', solution)
    except KeyboardInterrupt:
        exit
