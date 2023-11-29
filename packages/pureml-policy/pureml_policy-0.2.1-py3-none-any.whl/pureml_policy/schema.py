

policy_list = {

    'nyc144': {
        'sensitive_columns': ['sex', 'race'],
        'task_type': ['classification', 'fairness'],
        'metrics':
            {
                'classification':
                [
                    {'name': 'accuracy', 'threshold': 0.6}
                ],
                'fairness':
                [
                    {'name': 'demographic_parity_difference', 'threshold': 0.1}
                ]
        }
    }
}
