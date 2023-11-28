import os
import numpy as np 
import tracemalloc,linecache

from experiments.generate_plots import SupervisedPlotGenerator
from experiments.baselines.logistic_regression import BinaryLogisticRegressionBaseline
from experiments.baselines.random_classifiers import (
    UniformRandomClassifierBaseline,WeightedRandomClassifierBaseline)
from experiments.baselines.random_forest import RandomForestClassifierBaseline
from seldonian.utils.io_utils import load_pickle
from seldonian.dataset import SupervisedDataSet
from sklearn.metrics import log_loss,accuracy_score
from sklearn.model_selection import train_test_split

def perf_eval_fn(y_pred,y,**kwargs):
    # Deterministic accuracy. Should really be using probabilistic accuracy, 
    # but use deterministic it to match Thomas et al. (2019)
    performance_metric = kwargs['performance_metric']
    if performance_metric == 'Accuracy':
        return accuracy_score(y,y_pred > 0.5)
        
def main():
    # Parameter setup
    run_experiments = False
    make_plots = True
    save_plot = True
    include_legend = True

    model_label_dict = {
        'qsa':'This work',
        'logistic_regression': 'Standard ML model 1',
        'random_forest': 'Standard ML model 2',
        'fairlearn_eps0.10': 'MSFT Fairlearn (model 1)',
        'fairlearn_eps1.00': 'MSFT Fairlearn (model 2)',
        }

    ignore_models = ['fairlearn_eps0.01']
    hoz_axis_label = "# of training samples"

    constraint_name = 'disparate_impact'
    fairlearn_constraint_name = constraint_name
    fairlearn_epsilon_eval = 0.8 # the epsilon used to evaluate g, needs to be same as epsilon in our definition
    fairlearn_eval_method = 'two-groups' # two-groups is the Seldonian definition, 'native' is the fairlearn definition
    # fairlearn_epsilons_constraint = [0.01,0.1,1.0] # the epsilons used in the fitting constraint
    fairlearn_epsilons_constraint = [0.1,1.0] # the epsilons used in the fitting constraint
    performance_metric = 'Accuracy'
    n_trials = 50
    data_fracs = np.logspace(-4,0,15)
    n_workers = 6
    # results_dir = f'../../results/gpa_{constraint_name}_{performance_metric}'
    # results_dir = f'results/gpa_test_newbaselines'
    results_dir = f'results/for_pitch_deck'
    plot_savename = os.path.join(results_dir,f'gpa_{constraint_name}_{performance_metric}.png')
    # plot_savename = os.path.join(results_dir,f'gpa_{constraint_name}_{performance_metric}_fa.png')

    verbose=False

    # Load spec
    specfile = f'../../../engine-repo-dev/examples/GPA_tutorial/{constraint_name}/spec.pkl'
    spec = load_pickle(specfile)

    os.makedirs(results_dir,exist_ok=True)

    # Reset spec dataset to only use 2/3 of the original data, 
    # use remaining 1/3 for ground truth set for the experiment
    # Use entire original dataset as ground truth for test set
    orig_features = spec.dataset.features
    orig_labels = spec.dataset.labels
    orig_sensitive_attrs = spec.dataset.sensitive_attrs
    # First, shuffle features
    (train_features,test_features,train_labels,
    test_labels,train_sensitive_attrs,
    test_sensitive_attrs
        ) = train_test_split(
            orig_features,
            orig_labels,
            orig_sensitive_attrs,
            shuffle=True,
            test_size=0.33,
            random_state=42)
    new_dataset = SupervisedDataSet(
        features=train_features, 
        labels=train_labels,
        sensitive_attrs=train_sensitive_attrs, 
        num_datapoints=len(train_features),
        meta=spec.dataset.meta)
    # Set spec dataset to this new dataset
    spec.dataset = new_dataset
    # Setup performance evaluation function and kwargs 

    perf_eval_kwargs = {
        'X':test_features,
        'y':test_labels,
        'performance_metric':performance_metric
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
        lr_baseline = BinaryLogisticRegressionBaseline()
        plot_generator.run_baseline_experiment(
            baseline_model=lr_baseline,verbose=True)

        rf_classifier = RandomForestClassifierBaseline()
        plot_generator.run_baseline_experiment(
            baseline_model=rf_classifier,verbose=True)

        # Seldonian experiment
        plot_generator.run_seldonian_experiment(verbose=verbose)


    ######################
    # Fairlearn experiment 
    ######################

    fairlearn_sensitive_feature_names = ['M']
    fairlearn_sensitive_col_indices = [new_dataset.sensitive_col_names.index(
        col) for col in fairlearn_sensitive_feature_names]

    fairlearn_sensitive_features = new_dataset.sensitive_attrs[:,fairlearn_sensitive_col_indices]

    # Setup ground truth test dataset for Fairlearn
    test_features_fairlearn = test_features
    test_labels_fairlearn = test_labels
    test_sensitive_attrs_fairlearn = test_sensitive_attrs[:,fairlearn_sensitive_col_indices]

    fairlearn_eval_kwargs = {
        'X':test_features_fairlearn,
        'y':test_labels,
        'sensitive_features':test_sensitive_attrs_fairlearn,
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
        plot_generator.make_plots(
            fontsize=15,
            legend_fontsize=12,
            ncols_legend=5,
            performance_label=performance_metric,
            sr_label="Solution rate",
            fr_label="Noncompliance rate",
            include_legend=include_legend,
            model_label_dict=model_label_dict,
            ignore_models=ignore_models,
            hoz_axis_label=hoz_axis_label,
            show_confidence_level=False,
            save_format="png",
            show_title=False,
            savename=plot_savename if save_plot else None)



if __name__ == "__main__":

    main()