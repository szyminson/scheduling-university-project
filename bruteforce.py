"""Brute force algorithm implementation for employee shifts scheduling"""
from common import calc_cost, check_constraints, get_shifts_with_cost, get_employee_constraints


def run(shifts: list, shifts_cost: list, employees: tuple) -> tuple:
    """Run the algorithm"""
    max_employees, employees_needed = employees
    best_cost = None
    best_solution = None
    for x0 in range(max_employees):
        for x1 in range(max_employees):
            for x2 in range(max_employees):
                for x3 in range(max_employees):
                    for x4 in range(max_employees):
                        for x5 in range(max_employees):
                            for x6 in range(max_employees):
                                solution = [x0, x1, x2, x3, x4, x5, x6]
                                cost = calc_cost(solution, shifts_cost)
                                if (not best_cost or cost < best_cost
                                    ) and check_constraints(solution, shifts, employees_needed):
                                    best_cost = cost
                                    best_solution = solution
    return best_cost, best_solution


if __name__ == '__main__':
    shifts, shifts_cost = get_shifts_with_cost()
    cost, solution = run(shifts, shifts_cost, get_employee_constraints())
    print('cost:', cost)
    print('solution:', solution)
