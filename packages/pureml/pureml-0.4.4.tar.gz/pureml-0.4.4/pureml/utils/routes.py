BASE_URL = "https://pureml-development.up.railway.app/api"


# DataSet

DatasetCreate = BASE_URL + "/org/{orgId}/dataset/{datasetName}/create"  #  Create dataset
DatasetRegister = BASE_URL  + "/org/{orgId}/dataset/{datasetName}/register" #Register a dataset


# Model

ModelCreate = BASE_URL + "/org/{orgId}/model/{modelName}/create"   # Create Model
ModelRisk = BASE_URL + "/org/{orgId}/model/{modelName}/version/{version}/risk" # Risk Data for a Model
ModelMonitor = BASE_URL + "/org/{orgId}/model/{modelName}/version/{version}/monitor" # Monitoring data for a model
ModelRegister = BASE_URL + "/org/{orgId}/model/{modelName}/register" # Register a Model

