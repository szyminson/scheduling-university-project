"""Experiment utilities"""
from time import time
from collections.abc import Callable
from func_timeout import func_timeout, FunctionTimedOut
from alive_progress import alive_bar
import bruteforce
import aco
import genetic
from common import get_shifts_with_cost, get_employee_constraints
from result_processing import save_results, process_results

repeats = 5
timeout_sec = 10
problem_sizes = [1, 4, 6, 8, 12]

algorithms = {
    'aco': aco,
    'bruteforce': bruteforce,
    'genetic': genetic,
}


def calc_avg(times: list, costs: list) -> tuple:
    """Calculate averages of 2 given lists"""
    return (sum(times)/len(times)), (sum(costs)/len(costs))


def run_algorithm(algorithm: Callable[[list, list, tuple], tuple], params: tuple) -> tuple:
    """Run given algorithm callable with timeout restriction"""
    timeout_sec, repeats, sizes = params
    shifts, shifts_cost = get_shifts_with_cost()
    results = {}
    for size in sizes:
        args = shifts, shifts_cost, get_employee_constraints(size)
        times = []
        costs = []
        with alive_bar(repeats) as bar:
            bar.title('Instance size: ' + str(size).rjust(3))
            for _ in range(repeats):
                start_time = time()
                try:
                    cost, _ = func_timeout(timeout_sec, algorithm, args)
                    times.append(time() - start_time)
                    costs.append(cost)
                    bar()
                except FunctionTimedOut:
                    results[size] = float('inf'), float('inf')
                    return results
        results[size] = calc_avg(times, costs)
    return results


def run(algorithms: dict, timeout_sec: int, repeats: int, sizes: list):
    """Run experiment"""
    results = {}
    for algorithm in algorithms:
        print('\nRunning: ' + algorithm)
        results[algorithm] = run_algorithm(algorithms[algorithm].run,
                                           (timeout_sec, repeats, sizes))
    return results


if __name__ == '__main__':
    try:
        results = run(algorithms, timeout_sec, repeats, problem_sizes)
        save_results(results)
        process_results(results)
    except KeyboardInterrupt:
        exit
