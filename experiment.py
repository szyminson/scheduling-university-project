"""Experiment utilities"""
from time import time
from func_timeout import func_timeout, FunctionTimedOut
import bruteforce
import aco
from common import get_shifts_with_cost, get_employee_constraints
from result_processing import save_results

repeats = 10
timeout_sec = 10
problem_sizes = [1, 4]

algorithms = {
    'aco': aco,
    'bruteforce': bruteforce
}


def calc_avg(times: list, costs: list) -> tuple:
    """Calculate averages of 2 given lists"""
    return (sum(times)/len(times)), (sum(costs)/len(costs))


def run_algorithm(algorithm: callable, params: tuple) -> tuple:
    """Run given algorithm callable with timeout restriction"""
    timeout_sec, repeats, sizes = params
    shifts, shifts_cost = get_shifts_with_cost()
    results = {}
    for size in sizes:
        args = shifts, shifts_cost, get_employee_constraints(size)
        times = []
        costs = []
        for _ in range(repeats):
            start_time = time()
            try:
                cost, _ = func_timeout(timeout_sec, algorithm, args)
                times.append(time() - start_time)
                costs.append(cost)
            except FunctionTimedOut:
                results[size] = float('inf'), float('inf')
                return results
        results[size] = calc_avg(times, costs)
    return results

def run(algorithms: dict, timeout_sec: int, repeats: int, sizes: list):
    """Run experiment"""
    
    results = {}
    for algorithm in algorithms:
        results[algorithm] = run_algorithm(algorithms[algorithm].run,
                                                    (timeout_sec, repeats, sizes))
    return results


if __name__ == '__main__':
    results = run(algorithms, timeout_sec, repeats, problem_sizes)
    save_results(results)
    print(results)
