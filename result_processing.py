"""Results processing utilities"""
import pickle
from pathlib import Path
import json
from matplotlib import pyplot as plt

filename='results.pickle'
directory='results'
directory=Path(directory)

def save_results(results: dict):
    """Save results dict to serialized binary file"""
    directory.mkdir(parents=True, exist_ok=True)
    with open(directory.joinpath(filename), 'wb') as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_results()->dict:
    """Load results dict from serialized binary file"""
    with open(directory.joinpath(filename), 'rb') as handle:
        return pickle.load(handle)

def draw_plot(results: dict, algorithms: list = [], prefix: str = ''):
    times_fig, times_ax = plt.subplots()
    times_ax.set_ylabel('Times [s]')
    times_ax.set_xlabel('Sizes')
    costs_fig, costs_ax = plt.subplots()
    costs_ax.set_ylabel('Costs [pln]')
    costs_ax.set_xlabel('Sizes')
    for algorithm in results:
        if algorithms and algorithm not in algorithms:
            continue
        sizes = list(results[algorithm].keys())
        times = []
        costs = []
        for size in results[algorithm]:
            time, cost = results[algorithm][size]
            times.append(time)
            costs.append(cost)
        times_ax.plot(sizes, times, 'o--', label=algorithm)
        costs_ax.plot(sizes, costs, 'o--', label=algorithm)
    times_ax.legend()
    costs_ax.legend()
    times_fig.savefig(directory.joinpath(prefix + 'times_plot'))
    costs_fig.savefig(directory.joinpath(prefix + 'costs_plot'))

def process_results(results: dict):
    draw_plot(results)

if __name__ == '__main__':
    results = load_results()
    draw_plot(results)
    draw_plot(results, ['genetic', 'aco'], 'ga_')

    print(json.dumps(results, sort_keys=True, indent=4))
