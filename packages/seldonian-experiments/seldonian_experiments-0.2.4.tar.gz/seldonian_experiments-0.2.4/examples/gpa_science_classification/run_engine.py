import os
os.environ["OMP_NUM_THREADS"] = "1"
import autograd.numpy as np 
from seldonian.utils.io_utils import load_pickle
from seldonian.seldonian_algorithm import SeldonianAlgorithm

def initial_solution_fn(model,X,Y):
    return model.fit(X,Y)

def main():
    constraint_name = "disparate_impact"
    specfile = f'gpa_{constraint_name}/spec.pkl'
    spec = load_pickle(specfile)
    SA = SeldonianAlgorithm(spec)
    passed_safety,solution = SA.run(debug=True)
    print(passed_safety,solution)
    
if __name__ == "__main__":

    main()