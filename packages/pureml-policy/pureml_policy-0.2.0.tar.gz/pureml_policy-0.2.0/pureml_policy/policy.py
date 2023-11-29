import pureml
from pureml.components import get_org_id
import requests
from pureml.cli.auth import get_auth_headers
from pureml.schema import BackendSchema, LogSchema, ConfigKeys, ContentTypeHeader
from .schema import policy_list
from urllib.parse import urljoin
import json


def get_policy_details(policy_name='nyc144'):
    policy = policy_list[policy_name]

    task_type = policy['task_type']
    metrics = policy['metrics']
    sensitive_columns = policy['sensitive_columns']

    return task_type, metrics, sensitive_columns


def evaluate_with_policy(policy_name='nyc144', label_model=None, label_dataset=None):

    task_type, metrics, sensitive_columns = get_policy_details(policy_name)

    metric_values = pureml.eval(task_type=task_type,
                                label_model=label_model,
                                label_dataset=label_dataset,
                                metrics=metrics)

    model_name, model_version = label_model.split(":")
    dataset_name, dataset_version = label_model.split(":")
    result_policy = {
        "policy_details": {
            "name": policy_name
        },
        "model_details": {
            "name": model_name,
            "version": model_version
        },
        "dataset_details": {
            "name": dataset_name,
            "version": dataset_version
        },
        "sensitive_columns": sensitive_columns,
        "metrics": metric_values,
        "ethical_considerations": None,
        "Caveats_and_recommendations": None
    }

    post_policy_results(result_policy=result_policy,
                        model_name=model_name,
                        model_version=model_version,
                        policy_name=policy_name)

    return result_policy


def post_policy_results(result_policy, model_name, model_version, policy_name):
    org_id = get_org_id()

    backend_schema = BackendSchema().get_instance()

    url = "/reports?orgId={}&modelName={}&version={}".format(
        org_id, model_name, model_version
    )

    url = urljoin(backend_schema.BASE_URL, url)

    headers = get_auth_headers(content_type=ContentTypeHeader.ALL)

    result_policy = json.dumps(result_policy)
    data = {"data": result_policy, "policy_uuid": policy_name}

    data = json.dumps(data)

    response = requests.post(url, data=data, headers=headers)

    if response.ok:
        print(f"[bold green]Policy results have been registered!")

    else:
        print(f"[bold red]Policy results  have not been registered!")

    return response
