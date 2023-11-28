from .get_dataset import get_dataset_helper
from .get_model import get_model_helper
from .get_predictor import get_predictor_helper
import requests
from .routes import *
from pydantic import BaseModel
from rich import print
from typing import Any
from pureml_evaluate.evaluators.evaluator import eval as eval_fn
from pureml.cli.auth import get_auth_headers
from pureml.components import get_org_id
from pureml.predictor.predictor import BasePredictor
import json
import httpx


class EvalHelper(BaseModel):
    label_model: str
    label_dataset: str
    dataset: Any = None
    task_type: None = None
    model: Any
    predictor: Any

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    def load_dataset(self):
        self.dataset = get_dataset_helper(self.label_dataset)

    def load_model(self):
        self.predictor.load_models()
        # self.model = get_model_helper(self.label_model)
        # print(f"self.model : {self.predictor.load_models()}")

    def load_predictor(self):
        predictor_class = get_predictor_helper()
        self.predictor = predictor_class.load_predictor()
        # print(f"From Evaluator File: {self.predictor}")

    def load(self):
        self.load_dataset()
        self.load_predictor()
        self.load_model()

    def get_y_pred(self):
        return self.predictor.predict(self.dataset["x_test"]) if ('x_test' in self.dataset.keys() and self.predictor != None) else None

    def get_y_true(self):
        return self.dataset["y_test"] if 'y_test' in self.dataset.keys() else None

    def get_sensitive_features(self):
        return self.dataset['sensitive_features'] if 'sensitive_features' in self.dataset.keys() else None


def evalfunction(label_model: str, label_dataset: str, task_type: list[str], metrics=None, path_to_config=None, pdf_file_name='metrics_graph.pdf'):
    evaluator = EvalHelper(
        task_type=None, label_dataset=label_dataset, label_model=label_model
    )

    evaluator.load()

    y_pred = evaluator.get_y_pred()
    y_true = evaluator.get_y_true()
    sensitive_features = evaluator.get_sensitive_features()

    values = eval_fn(y_true=y_true, y_pred=y_pred, sensitive_features=sensitive_features,
                     evaluators=task_type, y_pred_scores=None, metrics=metrics,
                     path_to_config=path_to_config, as_pdf=True, pdf_file_name=pdf_file_name)

    # send_data_to_backend(values, label_model)
    return values


def send_data_to_backend(values, label_model):
    keys_in_values = values.keys()
    orgID = get_org_id()
    model_name, branch_name, version = label_model.split(":")
    risk_url = ModelRisk.format(
        orgId=orgID, modelName=model_name, branchName=branch_name, version=version)
    print(f"risk_url : {risk_url}")
    for i in keys_in_values:            # i = complete / subsets
        categories = values[i].keys()
        for j in categories:             # j = performance / fairness
            metrics = values[i][j].keys()
            for k in metrics:              # k  = accuracy / precision
                payload = create_payload(values, i, j, k)
                print(payload)
                try:
                    response = httpx.post(
                        risk_url, data=payload, headers=get_auth_headers())
                    # response = requests.post(risk_url, data=payload,headers = get_auth_headers())
                    print(f"Status Code: {response.status_code}")
                except Exception as e:
                    print(e)

                if response.status_code == 200:
                    print(
                        "[bold green] Succesfully sent the evaluation results to PureML server")
                else:
                    print(response.status_code)
                    print(response.json())


def create_payload(values, i, j, k):
    try:
        value = format(values[i][j][k]['value'], '.2f')
        payload = {
            "category": f"{j}",
            "risk": f"{k}",
                    "severity": f"{values[i][j][k]['severity']}",
                    "value": str(value),
                    "threshold": str(values[i][j][k]['threshold']),
                    "policy": "test-sr-11-7"
        }
        return json.dumps(payload, indent=4)
    except Exception as e:
        print(e)
        return None
