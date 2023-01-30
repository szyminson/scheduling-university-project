"""Results processing utilities"""
import pickle
from pathlib import Path

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

if __name__ == '__main__':
    print(load_results())