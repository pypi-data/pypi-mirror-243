# experiment_with_random_forest_baseline.py
import os
import numpy as np 

from seldonian.utils.io_utils import load_pickle
from experiments.generate_plots import SupervisedPlotGenerator
from experiments.perf_eval_funcs import binary_logistic_loss
from experiments.baselines.logistic_regression import BinaryLogisticRegressionBaseline
from experiments.baselines.random_forest import RandomForestClassifierBaseline

if __name__ == "__main__":
	run_experiments = False
	make_plots = True
	model_label_dict = {
		'qsa':'Seldonian model',
		'random_forest': 'Random forest (no constraints)',
		}
	n_trials = 10
	data_fracs = np.logspace(-3,0,10)
	n_workers = 6
	verbose=False
	results_dir = f'results/loans_random_forest_50estimators'
	os.makedirs(results_dir,exist_ok=True)

	plot_savename = os.path.join(results_dir,"loans_random_forest.png")

	# Load spec
	specfile = f'./data/spec/loans_disparate_impact_0.9_spec.pkl'
	spec = load_pickle(specfile)

	# Use entire original dataset as ground truth for test set
	dataset = spec.dataset
	test_features = dataset.features
	test_labels = dataset.labels

	# Setup performance evaluation function and kwargs 
	# of the performance evaluation function
	perf_eval_fn = binary_logistic_loss
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

	if run_experiments:
		# Baseline model
		rf_baseline = RandomForestClassifierBaseline(n_estimators=50)
		plot_generator.run_baseline_experiment(
			baseline_model=rf_baseline,verbose=verbose)

		# Seldonian experiment
		plot_generator.run_seldonian_experiment(verbose=verbose)

	if make_plots:
			plot_generator.make_plots(fontsize=12,legend_fontsize=8,
				performance_label="Log loss",
				performance_yscale='log',
				model_label_dict=model_label_dict,
				savename=plot_savename,
				save_format="png"
			)
