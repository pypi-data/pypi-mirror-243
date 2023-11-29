from pureml_evaluate.policy.performance import Performance
from pureml_evaluate.policy.fairness import FairnessPolicy as Fairness
import numpy as np
from collections import defaultdict


class Grader:
    list_of_performance_metrics = [
    'accuracy',
    'precision',
    'recall' ,
    'f1',
    'confusionmatrix',
    'balancedaccuracyscore',
    'topkaccuracyscore' ,
    'logloss' ,
    'averageprecisionscore',
    'roc_auc' ,
    'brierscoreloss' ,
    'kolmogorovsmirnov' ,
    'wassersteindistance',
    'hellingerdistance' ,
    'linfinitydistance' ,
    'chisquaredstatistic',
    'cramersv',
    'populationstabilityindex' 
    ]
    metrics : list = []
    policy : dict   
    references : any
    predictions : any
    sensitive_features : any
    scores : dict = {}
    categories: dict = {}

    def __init__(self,references,predictions,sensitive_features,policy,metrics):
        self.references = references
        self.predictions = predictions
        self.sensitive_features  = sensitive_features
        self.policy = policy             #{'acccuracy' : 0.8}
        self.metrics = metrics       # ['accuracy']


    def compute(self):
        all_metrics = []
        
        operational_category = {} # To Store the flagged values of metrics like pass/fail
        fairness_category  = {}
        
        operational_scores = {} # To Store the values of metrics 
        fairness_scores = {}

        operational_threshold = {} # To Store Threshold values
        fairness_threshold = {}

        for metric in self.metrics:
            if metric in self.list_of_performance_metrics:
                performance = Performance()
                threshold_value = self.policy[metric]
                threshold = {metric : threshold_value}
                result = performance.compute(list_metrics = [metric],references = self.references,predictions = self.predictions,
                                             list_of_thresholds = threshold,prediction_scores = None)
                
                temp_scores  = {
                    f"{result['risk']}" : f"{result['value']}"
                }
                operational_scores.update(temp_scores)
                temp_category = {
                    f"{result['risk']}" : f"{result['severity']}"
                }
                operational_category.update(temp_category)
                temp_threshold  = {
                    f"{result['risk']}" : f"{threshold_value}"
                }
                operational_threshold.update(temp_threshold)

                

            else:
                fairness = Fairness()
                threshold_value = self.policy[metric]
                threshold = {metric : threshold_value}
                result = fairness.compute(list_metrics = [metric],references = self.references,predictions = self.predictions,
                                          list_of_thresholds = threshold,sensitive_features = self.sensitive_features,prediction_scores = None)
                
                temp_scores  = {
                    f"{result['risk']}" : f"{result['value']}"
                }
                fairness_scores.update(temp_scores)
                temp_category = {
                    f"{result['risk']}" : f"{result['severity']}"
                }
                fairness_category.update(temp_category)    
                temp_threshold  = {
                    f"{result['risk']}" : f"{threshold_value}"
                }
                fairness_threshold.update(temp_threshold)
                

        self.scores = {
                "operational" : operational_category,
                "fairness" : fairness_category,
                "operational_scores" : operational_scores,
                "fairness_scores" : fairness_scores,
                "operational_thresholds" : operational_threshold,
                "fairness_thresholds" : fairness_threshold
            }
        
        return self.scores

