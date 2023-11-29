from pydantic import BaseModel
from pureml.predictor.predictor import BasePredictor
from pureml.components import dataset
from typing import Any
from importlib import import_module
from rich import print
import requests
from pureml_evaluate.evaluators.evaluator import eval as eval_fn
from pureml.cli.auth import get_auth_headers
from pureml.components import get_org_id
from .grade import Grader
from collections import defaultdict
import numpy as np
from typing import Union
import matplotlib.pyplot as plt



class EvalHelper(BaseModel):  # To pass the requirements to eval in pureml_evaluate
    label_model: str
    label_dataset: str
    policy: dict
    predictor: BasePredictor = None
    predictor_path: str = "predict.py"
    dataset: Any = None
    sensitive_features: Union[None, Any]
    y_true: Any
    y_pred: Any
    y_pred_scores: Any = None
    


    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    def load_dataset(self):
        self.dataset = dataset.fetch(self.label_dataset)
        print("[bold green] Succesfully fetched the dataset")

    def load_predictor(self):
        module_path = self.predictor_path.replace(".py", "")
        module_import = import_module(module_path)

        predictor_class = getattr(module_import, "Predictor")

        self.predictor = predictor_class()
        print("[bold green] Succesfully fetched the predictor")

    def load_model(self):
        self.predictor.load_models()
        print("[bold green] Succesfully fetched the model")

    def load_policy(self):
        return list(self.policy.keys())
    
    def load_sensitive_features(self):
        if 'sensitive_features' in self.dataset.keys():
            self.sensitive_features = self.dataset['sensitive_features']
            return self.dataset['sensitive_features']
        else:
            return None

    def load_y_true(self):
        self.y_true = self.dataset["y_test"]
        return self.dataset["y_test"]
    
    def load_y_pred(self):
        self.y_pred = self.predictor.predict(self.dataset["x_test"])
        return self.predictor.predict(self.dataset["x_test"])
    
    def load(self):
        self.load_dataset()
        self.load_predictor()
        self.load_model()
        self.load_policy()
        self.load_sensitive_features()
        self.load_y_true()
        self.load_y_pred()

    def get_y_pred(self):
        return self.predictor.predict(self.dataset["x_test"])

    def get_y_true(self):
        return self.dataset["y_test"]

    def get_sensitive_features(self):
        print(f"Dataset Keys: {self.dataset.keys()}")
        if 'sensitive_features' in self.dataset.keys():
            print(
                f"Data in sensitive_features: {self.dataset['sensitive_features']}")
            return self.dataset['sensitive_features']
        else:
            return None

    def evaluate(self):
        y_pred = self.get_y_pred()
        y_true = self.get_y_true()
        sensitive_features = self.get_sensitive_features()
        metrics = self.load_policy()
        grader = Grader(references=y_true, predictions=y_pred,
                        sensitive_features=sensitive_features, policy=self.policy, metrics=metrics)

        result  = grader.compute()
        # labelmodel = self.label_model.split(':')
        # version = labelmodel[2]
        # model_branch = f"{labelmodel[0]}:{labelmodel[1]}"
        # #print(f"version: {version}")
        # #print(f"model_branch: {model_branch}")
        # formatted_result = {
        #     "model" : f"{model_branch}",
        #     "version" : f"{version}",
        #     "result" : [result]
        # }
        # return formatted_result
        return {'complete' : result}

    def evaluate_subsets(self):
        if self.sensitive_features is None:  # If No Sensitive Features are given
            return 
    
        if self.sensitive_features is not None: 
            subsets = self.give_subsets()

            values_subsets_all = {}

            for subset in subsets:
                values_all = defaultdict(dict)

                key = subset['key']
                y_true = subset['y_true']
                y_pred = subset['y_pred']
                sensitive_features = subset['sensitive_features']
                y_pred_scores = subset['y_pred_scores']

                sensitive_features = self.get_sensitive_features()
                metrics = self.load_policy()
                grader = Grader(references = y_true, predictions = y_pred, sensitive_features = sensitive_features, policy = self.policy, metrics = metrics)
                result = grader.compute()
                values_subsets_all[key] = result

            return values_subsets_all

    def give_subsets(self):
        subsets = []
        unique_values = np.unique(self.sensitive_features)

        for value in unique_values:
            ind = np.where(self.sensitive_features == value)
            sub_dict = {
                "key": value,
                "y_true": self.y_true[ind],
                "y_pred": self.y_pred[ind],
                "sensitive_features": self.sensitive_features[ind],
            }
            if self.y_pred_scores is not None:
                sub_dict.update({"y_pred_scores": self.y_pred_scores[ind]})
            else:
                sub_dict.update({"y_pred_scores": self.y_pred_scores})

            subsets.append(sub_dict)

        return subsets


def eval(label_model: str, label_dataset: str, policy: dict):
    evaluator = EvalHelper(label_model=label_model,
                           label_dataset=label_dataset, policy=policy)

    evaluator.load()
    complete = evaluator.evaluate()
    subsets = evaluator.evaluate_subsets()
    labelmodel = label_model.split(':')
    version = labelmodel[1]
    model = labelmodel[0]
    result = {'complete' : complete, 'subsets' : subsets}
    formatted_result = {
            "model" : f"{model}",
            "version" : f"{version}",
            "result" : [result]
    }
    plot_balanced_accuracy(formatted_result)
    return formatted_result

def plot_balanced_accuracy(results_json, orientation='horizontal'):
    """
    Plots the balanced accuracy for Complete, Male, and Female categories
    against a specified threshold.
    
    Parameters:
    - results_json: Dictionary containing the results data
    - orientation: 'horizontal' or 'vertical' to determine the bar graph orientation
    """
    # Extracting data
    results = results_json['result'][0]
    complete_data = float(results['complete']['complete']['fairness_scores']['balanced_accuracy'])
    male_data = float(results['subsets'][1]['fairness_scores']['balanced_accuracy'])
    female_data = float(results['subsets'][2]['fairness_scores']['balanced_accuracy'])
    threshold = float(results['complete']['complete']['fairness_thresholds']['balanced_accuracy'])
    
    # Categories
    categories = ['Complete', 'Male', 'Female']
    
    # Values
    values = [complete_data, male_data, female_data]
    
    # Colors
    colors = ['#1f77b4', '#60a3d9', '#c2e0f9']
    
    # Creating the bar graph
    fig, ax = plt.subplots()
    if orientation == 'horizontal':
        bars = ax.barh(categories, values, color=colors)
        ax.axvline(x=threshold, color='gray', linestyle='--', label=f'Threshold ({threshold})')
        ax.set_xlabel('Balanced Accuracy')
        ax.set_ylabel('Categories')
    else:
        bars = ax.bar(categories, values, color=colors)
        ax.axhline(y=threshold, color='gray', linestyle='--', label=f'Threshold ({threshold})')
        ax.set_ylabel('Balanced Accuracy')
        ax.set_xlabel('Categories')
    
    # Adding labels and title
    ax.set_title('Balanced Accuracy Comparison')
    ax.legend()
    
    # Displaying the bar graph
    plt.show()