from typing import Optional

from pydantic import BaseModel


class DockerReference(BaseModel):
    image: Optional[str]
    uri: Optional[str]
    port: Optional[int]
    credentialsId: Optional[str]


class BlobReference(BaseModel):
    url: str
    credentialsId: Optional[str]
    region: Optional[str]


class MLFlowReference(BaseModel):
    model: str
    stage: Optional[str]
    version: Optional[str]
    blob: Optional[dict]


class AzureMLReference(BaseModel):
    image: str
    uri: str
    port: int
    readinessPath: str
    livelinessPath: str
    model: Optional[str]
    version: Optional[str]


class ModelReference(BaseModel):
    docker: Optional[DockerReference]
    blob: Optional[BlobReference]
    mlflow: Optional[MLFlowReference]
    azureML: Optional[AzureMLReference]


class ModelReferenceJson(BaseModel):
    reference: ModelReference
