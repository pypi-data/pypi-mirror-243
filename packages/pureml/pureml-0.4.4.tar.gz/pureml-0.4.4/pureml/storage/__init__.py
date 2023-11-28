from pathlib import Path
from urllib.parse import urljoin
from uuid import uuid4

import requests
from pureml.cli.helpers import get_auth_headers
from pureml.components import get_org_id

from pureml.schema.backend import BackendSchema
from pureml.schema.request import AcceptHeader
from .providers.aws import S3StorageProvider
from .providers.cloudflare import R2StorageProvider
from .providers.local import LocalStorageProvider

from pureml.cli.puremlconfig import PureMLConfigYML


project_path = Path.cwd()
if Path.exists(project_path / "puremlconfig.yaml"):
    puremlconfig = PureMLConfigYML(project_path / "puremlconfig.yaml")
else:
    puremlconfig = None

backend_schema = BackendSchema().get_instance()


def upload_and_get_provider_and_path(file_path: str, storage_provider: str = None, opt_base_dir: str = "") -> str or None:
    """
    Gets the storage provider from config repository and uploads the file to the storage provider

    Config file should have the following format -
    repository: <storage_provider>://<repository_argument>

    repository_argument is the argument required for the storage provider
    for file : repository_argument is the path of the directory where the file is to be stored
    for s3 : repository_argument is the name of the secret made in pureml secrets for s3
    for r2 : repository_argument is the name of the secret made in pureml secrets for r2


    Parameters
    ----------
    file_path: str
        Path of the file to be uploaded

    storage_provider: str (default: None)
        Storage provider to be used for uploading the file

    Returns
    -------
    str, str or None
        Provider used and Path of the uploaded file or None if the file is not uploaded successfully
    """
    repository_argument = ""
    if storage_provider is None:
        if puremlconfig is not None:
            storage_provider = puremlconfig.data["repository"].split("://")[0]
            repository_argument = puremlconfig.data["repository"].split(
                "://")[1]
        else:
            raise KeyError("No storage provider found in config file")

    if storage_provider not in ["s3", "r2", "file"]:
        raise ValueError("Invalid storage provider")

    if storage_provider == "file":
        return storage_provider, file_path

    # windows paths support and appending base dir
    file_path = file_path.replace(r'\\', "/").lstrip("/")

    # Get secrets from backend API
    org_id = get_org_id()
    url = f"org/{org_id}/secret/{str(repository_argument)}"
    url = urljoin(backend_schema.BASE_URL, url)
    # print(url)

    headers = get_auth_headers(content_type=None, accept=AcceptHeader.APP_JSON)

    response = requests.get(url, headers=headers)

    if response.ok:
        secrets = response.json()["data"]
        if secrets and len(secrets) != 0:
            secrets = secrets[0]
    else:
        # print(response.json())
        raise ValueError("Invalid repository argument")

    # Get storage provider client
    del secrets["source_type"]
    storage_provider_client = get_storage_provider(storage_provider, **secrets)

    key = file_path.split("/")[-1]
    ext = key.split(".")[-1]
    name = ".".join(key.split(".")[:-1])
    random_string = str(uuid4())[:8]
    key = f"{opt_base_dir}/{name}_{random_string}.{ext}"

    upload_path = storage_provider_client.upload_file(file_path, key)
    print("upload_path", upload_path)

    if upload_path is None:
        raise ValueError("File not uploaded successfully")

    return storage_provider, upload_path


def get_storage_provider(provider, **kwargs):
    """
    Function to dynamically create a client for a storage provider
    NOTE: all keyword arguments are passed from backend secrets hence are defined in the providers although not used
    Currently supported storage providers -

    ---

    1. S3
    ...

    Required kwargs -

    access_key_id: str
        AWS access key

    access_key_secret: str
        AWS secret key

    bucket_name: str
        AWS bucket name

    bucket_location: str
        AWS region

    public_url: str (default: None)
        Public URL of the bucket

    2. R2
    ...

    Required kwargs -

    access_key_id: str
        Cloudflare access key

    access_key_secret: str
        Cloudflare secret key

    bucket_name: str
        Cloudflare bucket name

    account_id: str
        Cloudflare account ID

    public_url: str
        Public URL of the bucket
    """
    if provider == "s3":
        return S3StorageProvider(**kwargs)
    elif provider == "r2":
        return R2StorageProvider(**kwargs)
    # elif provider == "local":
    #     return LocalStorageProvider(**kwargs)
    else:
        raise ValueError("Invalid storage provider")
