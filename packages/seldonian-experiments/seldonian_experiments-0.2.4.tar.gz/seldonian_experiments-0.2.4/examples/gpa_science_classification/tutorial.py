# generate_gpa_plots.py
import os
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np 

from experiments.generate_plots import SupervisedPlotGenerator
from seldonian.utils.io_utils import load_pickle
from sklearn.metrics import log_loss,accuracy_score

from experiments.baselines.logistic_regression import BinaryLogisticRegressionBaseline
from experiments.baselines.random_classifiers import (
    UniformRandomClassifierBaseline)


def perf_eval_fn(y_pred,y,**kwargs):
    if performance_metric == 'log_loss':
        return log_loss(y,y_pred)
    elif performance_metric == 'accuracy':
        return accuracy_score(y,y_pred > 0.5)

def initial_solution_fn(m,x,y):
    return np.random.uniform(-1,1,size=10)

if __name__ == "__main__":
    # Parameter setup
    run_experiments = True
    make_plots = True
    save_plot = True
    include_legend = False
    constraint_name = 'predictive_equality'

    if constraint_name == 'disparate_impact':
        plot_title = 'Constraint:\nmin((PR | [M])/(PR | [F]),(PR | [F])/(PR | [M])) >= 0.8' 
    elif constraint_name == 'demographic_parity':
        plot_title = 'Constraint:\nabs((PR | [M]) - (PR | [F])) <= 0.2'
    elif constraint_name == 'equalized_odds':
        plot_title = 'Constraint:\nabs((FNR | [M]) - (FNR | [F])) + abs((FPR | [M]) - (FPR | [F])) <= 0.35'
    elif constraint_name == 'equal_opportunity':
        plot_title = 'Constraint:\nabs((FNR | [M]) - (FNR | [F])) <= 0.2'
    elif constraint_name == 'predictive_equality':
        plot_title = 'Constraint:\nabs((FPR | [M]) - (FPR | [F])) <= 0.2'
    fairlearn_constraint_name = constraint_name
    fairlearn_epsilon_eval = 0.8 # the epsilon used to evaluate g, needs to be same as epsilon in our definition
    fairlearn_eval_method = 'two-groups' # the epsilon used to evaluate g, needs to be same as epsilon in our definition
    fairlearn_epsilons_constraint = [0.01,0.1,1.0] # the epsilons used in the fitting constraint
    performance_metric = 'accuracy'
    n_trials = 50
    data_fracs = np.logspace(-4,0,15)
    n_workers = 7
    results_dir = f'results/gpa_{constraint_name}_{performance_metric}_2023Sep29'
    plot_savename = os.path.join(results_dir,f'gpa_{constraint_name}_{performance_metric}.png')

    verbose=True

    # Load spec
    specfile = f'../../../engine-repo-dev/examples/GPA_tutorial/{constraint_name}/spec.pkl'
    spec = load_pickle(specfile)
    spec.initial_solution_fn = initial_solution_fn
    os.makedirs(results_dir,exist_ok=True)

    # Use entire original dataset as ground truth for test set
    dataset = spec.dataset
    test_features = dataset.features
    test_labels = dataset.labels

    # Setup performance evaluation function and kwargs 
    # of the performance evaluation function

    perf_eval_kwargs = {
        'X':test_features,
        'y':test_labels,
        }

    plot_generator = SupervisedPlotGenerator(
        spec=spec,
        n_trials=n_trials,
        data_fracs=data_fracs,
        n_workers=n_workers,
        datagen_method='resample',
        perf_eval_fn=perf_eval_fn,
        constraint_eval_fns=[],
        results_dir=results_dir,
        perf_eval_kwargs=perf_eval_kwargs,
        )

    # # Baseline models
    if run_experiments:
        # Seldonian experiment
        plot_generator.run_seldonian_experiment(verbose=verbose)
        
        plot_generator.run_baseline_experiment(
            baseline_model=UniformRandomClassifierBaseline(),verbose=True)

        plot_generator.run_baseline_experiment(
            baseline_model=BinaryLogisticRegressionBaseline(),verbose=True)

        
    ######################
    # Fairlearn experiment 
    ######################

    fairlearn_sensitive_feature_names=['M']
    
    # Make dict of test set features, labels and sensitive feature vectors
    
    fairlearn_sensitive_feature_names = ['M']
    fairlearn_sensitive_col_indices = [dataset.sensitive_col_names.index(
        col) for col in fairlearn_sensitive_feature_names]
    fairlearn_sensitive_features = dataset.sensitive_attrs[:,fairlearn_sensitive_col_indices]
    # Setup ground truth test dataset for Fairlearn
    test_features_fairlearn = test_features
    fairlearn_eval_kwargs = {
        'X':test_features_fairlearn,
        'y':test_labels,
        'sensitive_features':fairlearn_sensitive_features,
        'eval_method':fairlearn_eval_method,
        'performance_metric':performance_metric,
        }

    if run_experiments:
        for fairlearn_epsilon_constraint in fairlearn_epsilons_constraint:
            plot_generator.run_fairlearn_experiment(
                verbose=verbose,
                fairlearn_sensitive_feature_names=fairlearn_sensitive_feature_names,
                fairlearn_constraint_name=fairlearn_constraint_name,
                fairlearn_epsilon_constraint=fairlearn_epsilon_constraint,
                fairlearn_epsilon_eval=fairlearn_epsilon_eval,
                fairlearn_eval_kwargs=fairlearn_eval_kwargs,
                )

    if make_plots:
        plot_generator.make_plots(fontsize=12,legend_fontsize=12,
            performance_label=performance_metric,
            performance_yscale='linear',
            custom_title=plot_title,
            include_legend=include_legend,
            savename=plot_savename if save_plot else None,
            save_format="png")