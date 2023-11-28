from pydantic import BaseModel
from pureml.components import model
from rich import print


def get_model_helper(label_model):
        model_load = model.fetch(label = label_model)
        if model_load is None:
            print("[bold red] Unable to  fetched the model")
            return None
        else:
            print("[bold green] Succesfully fetched the model")
            return model_load
