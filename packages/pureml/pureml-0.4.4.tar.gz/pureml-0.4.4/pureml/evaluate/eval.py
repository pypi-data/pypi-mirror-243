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


class EvalHelper(BaseModel):  # To pass the requirements to eval in pureml_evaluate
    task_type: None = None
    label_model: str
    label_dataset: str
    predictor: BasePredictor = None
    predictor_path: str = "predict.py"
    dataset: Any = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

    def load_dataset(self):
        # print(self.label_dataset)
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

    def load(self):
        self.load_dataset()
        self.load_predictor()
        self.load_model()

    def get_y_pred(self):
        return self.predictor.predict(self.dataset["x_test"])

    def get_y_true(self):
        return self.dataset["y_test"]

    def get_sensitive_features(self):
        # print(f"Dataset Keys: {self.dataset.keys()}")
        if 'sensitive_features' in self.dataset.keys():
            # print(f"Data in sensitive_features: {self.dataset['sensitive_features']}")
            return self.dataset['sensitive_features']
        # else:
        #    return None

    # This Function is to Format Risk Name. Eg - balanced_acc_score to Balanced Acc Score
    def format_riskname(self, metric_name):
        metricname = metric_name.split('_')
        return (
            metricname[0].capitalize()
            if len(metricname) == 1
            else ' '.join(word.capitalize() for word in metricname))

    def post(self, values):
        base_url = "https://pureml-development.up.railway.app/api"
        risk_url = "/org/{orgId}/model/{modelName}/version/{version}/risk"
        orgID = get_org_id()
        model_details = self.label_model.split(":")
        model_name = model_details[0]
        version = model_details[1]
        complete_url = base_url + \
            risk_url.format(orgId=orgID, modelName=model_name, version=version)
        # print(complete_url)
        response_status = 200
        if 'performance' in values['complete']:
            category = "performance"
            metric_name = values['complete']['performance']
            for i in metric_name:
                risk = self.format_riskname(i)
                severity = values['complete']['performance'][i]['severity']
                value = values['complete']['performance'][i]['value']
                value = format(value, '.2f')
                description = values['complete']['performance'][i]['description']
                matters = values['complete']['performance'][i]['matters']
                summary = values['complete']['performance'][i]['summary']
                threshold = values['complete']['performance'][i]['threshold']
                payload = {
                    "category": f"{category}",
                    "description": f"{description}",
                    "matters": f"{matters}",
                    "risk": f"{risk}",
                    "severity": f"{severity}",
                    "summary": f"{summary}",
                    "threshold": str(threshold),
                    "value": str(value)
                }
                # print(payload)
                try:
                    response = requests.post(
                        complete_url, json=payload, headers=get_auth_headers())
                    print(f"Response Status Code: {response.status_code}")
                    response_status = response.status_code
                except Exception as e:
                    print(e)

        if 'fairness' in values['complete']:
            category = "fairness"
            metric_name = values['complete']['fairness']
            for i in metric_name:
                risk = self.format_riskname(i)
                severity = values['complete']['fairness'][i]['severity']
                value = values['complete']['fairness'][i]['value']
                value = format(value, '.2f')
                description = values['complete']['fairness'][i]['description']
                matters = values['complete']['fairness'][i]['matters']
                summary = values['complete']['fairness'][i]['summary']
                threshold = values['complete']['fairness'][i]['threshold']
                payload = {
                    "category": f"{category}",
                    "description": f"{description}",
                    "matters": f"{matters}",
                    "risk": f"{risk}",
                    "severity": f"{severity}",
                    "summary": f"{summary}",
                    "threshold": str(threshold),
                    "value": str(value)
                }
                # print(payload)
                try:
                    response = requests.post(
                        complete_url, json=payload, headers=get_auth_headers())
                    print(f"Status Code: {response.status_code}")
                    response_status = response.status_code
                except Exception as e:
                    print(e)

        response = requests.get(complete_url, headers=get_auth_headers())
        print(response.json())
        if response_status == 200:
            print(
                "[bold green] Succesfully sent the evaluation results to PureML server")


def eval(label_model: str, label_dataset: str, task_type: list[str], metrics=None, path_to_config=None, pdf_file_name='metrics_graph.pdf'):
    evaluator = EvalHelper(
        task_type=None, label_dataset=label_dataset, label_model=label_model
    )

    evaluator.load()

    y_pred = evaluator.get_y_pred()
    y_true = evaluator.get_y_true()
    sensitive_features = evaluator.get_sensitive_features()
    # sensitive_features=None

    values = eval_fn(y_true=y_true, y_pred=y_pred, sensitive_features=sensitive_features,
                     evaluators=task_type, y_pred_scores=None, metrics=metrics,
                     path_to_config=path_to_config, as_pdf=True, pdf_file_name=pdf_file_name)

    # print()
    # evaluator.post(values)

    # print(data)
    # print(values)
    # result_split_json(values=values, label_model=label_model)
    # return values


def result_split_json(values, label_model):
    performance = values['complete']['performance']
    fairness = values['complete']['fairness']

    # severity_json = {}
    # for i in performance:
    #     severity_json[i] = performance[i]['severity']

    # values_json = {}
    # for i in performance:
    #     values_json[i] = performance[i]['value']

    for i in performance:
        payload = {
            "category": "performance",
            "risk": i,
            "severity": performance[i]['severity'],
            "value": str(performance[i]['value']),
            "threshold": str(performance[i]['threshold']),
            "policy": "nyc144"
        }
    base_url = "https://pureml-development.up.railway.app/api"
    risk_url = "/org/{orgId}/model/{modelName}/version/{version}/risk"
    orgID = get_org_id()
    model_details = label_model.split(":")
    model_name = model_details[0]
    version = model_details[1]
    complete_url = base_url + \
        risk_url.format(orgId=orgID, modelName=model_name, version=version)
    # print(complete_url)
    response_status = 200
    # print(payload)
    try:
        response = requests.post(
            complete_url, json=payload, headers=get_auth_headers())
        print(f"Status Code: {response.status_code}")
        # print(f"Reason: {response.reason}")
        # print(response.json())
        response_status = response.status_code
    except Exception as e:
        print(e)

    response = requests.get(complete_url, headers=get_auth_headers())
    print(response.json())
    if response_status == 200:
        print("[bold green] Succesfully sent the evaluation results to PureML server")

    for i in fairness:
        payload = {
            "category": "fairness",
            "risk": i,
            "severity": fairness[i]['severity'],
            "value": str(fairness[i]['value']),
            "threshold": str(fairness[i]['threshold']),
            "policy": "nyc144"

        }
    base_url = "https://pureml-development.up.railway.app/api"
    risk_url = "/org/{orgId}/model/{modelName}/version/{version}/risk"
    orgID = get_org_id()
    model_details = label_model.split(":")
    model_name = model_details[0]
    version = model_details[1]
    complete_url = base_url + \
        risk_url.format(orgId=orgID, modelName=model_name, version=version)
    # print(complete_url)
    response_status = 200
    # print(payload)
    try:
        response = requests.post(
            complete_url, json=payload, headers=get_auth_headers())
        print(f"Status Code: {response.status_code}")
        # print(f"Reason: {response.reason}")
        # print(response.json())
        response_status = response.status_code
    except Exception as e:
        print(e)

    response = requests.get(complete_url, headers=get_auth_headers())
    print(response.json())
    if response_status == 200:
        print("[bold green] Succesfully sent the evaluation results to PureML server")
