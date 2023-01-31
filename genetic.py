"""Genetic algorithm implementation for employee shifts scheduling"""
import random
from common import calc_cost, check_constraints, get_shifts_with_cost, get_employee_constraints
population_size = 100
generations = 100
mutation_rate = 0.01
crossover_rate = 0.7


def run(shifts: list, shifts_cost: list, employees: tuple) -> tuple:
    """Run the algorithm"""
    max_employees, employees_needed = employees

    population = [generate_random_solution(
        max_employees) for _ in range(population_size)]
    best_cost = None
    best_solution = None

    for _ in range(generations):
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2, crossover_rate)
            child = mutate(child, mutation_rate, max_employees)
            cost = calc_cost(child, shifts_cost)
            if check_constraints(child, shifts, employees_needed) and (not best_cost or cost < best_cost):
                best_cost = cost
                best_solution = child
            offspring.append(child)
        population = offspring

    return best_cost, best_solution


def generate_random_solution(max_employees: int) -> list:
    """Generate a random solution"""
    return [random.randint(0, max_employees) for _ in range(7)]


def crossover(parent1: list, parent2: list, rate: float) -> list:
    """Crossover two parents to create a child"""
    child = []
    for p1, p2 in zip(parent1, parent2):
        if random.random() < rate:
            child.append(p1)
        else:
            child.append(p2)
    return child


def mutate(solution: list, rate: float, max_employees: int) -> list:
    """Mutate a solution"""
    for i in range(len(solution)):
        if random.random() < rate:
            solution[i] = random.randint(0, max_employees)
    return solution


if __name__ == '__main__':
    try:
        shifts, shifts_cost = get_shifts_with_cost()
        cost, solution = run(shifts, shifts_cost, get_employee_constraints(1))
        print('cost:', cost)
        print('solution:', solution)
    except KeyboardInterrupt:
        exit
