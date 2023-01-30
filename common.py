normal_day_cost = 150
unusual_day_costs = {
    5: 250,
    6: 270
}
employees_needed = [3, 3, 3, 3, 3, 2, 2]
max_employees = max(employees_needed)


def create_shifts() -> list:
    shifts = []
    first_day_off, second_day_off = (5, 6)
    for _ in range(7):
        shift_days = list(range(7))
        shift_days.remove(first_day_off)
        shift_days.remove(second_day_off)
        shifts.append(shift_days)

        first_day_off += 1
        if first_day_off >= 7:
            first_day_off = 0
        second_day_off += 1
        if second_day_off >= 7:
            second_day_off = 0
    return shifts


def calc_shifts_cost(shifts: list) -> list:
    shifts_cost = []
    for shift in shifts:
        days_count = len(shift)
        cost = 0
        for day in unusual_day_costs:
            if day in shift:
                days_count -= 1
                cost += unusual_day_costs[day]
        cost += normal_day_cost * days_count
        shifts_cost.append(cost)
    return shifts_cost


def get_shifts_with_cost() -> tuple:
    shifts = create_shifts()
    return shifts, calc_shifts_cost(shifts)


def calc_cost(solution: list, shifts_cost: list) -> int:
    cost = 0
    for index, x in enumerate(solution):
        cost += x * shifts_cost[index]
    return cost


def check_constraints(solution: list, shifts: list, employees_needed: list) -> bool:
    employees_per_day = [0] * len(employees_needed)
    for index, x in enumerate(solution):
        for day in shifts[index]:
            employees_per_day[day] += x
    for index, emp_count in enumerate(employees_per_day):
        if emp_count < employees_needed[index]:
            return False
    return True
