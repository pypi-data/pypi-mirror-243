from typing import Any, Dict, Optional

from pydantic import BaseModel


class UpdateDeployment(BaseModel):
    """Class that contains the options for updating a model"""  # noqa

    deployment_id: Optional[str]
    repository_id: Optional[str]
    status: Optional[str]
    branch_name: Optional[str]
    commit: Optional[str]
    commit_message: Optional[str]
    contract_path: Optional[str]
    deployment_backend: Optional[str]
    model_type: Optional[Any]
    model_serverless: Optional[bool] = False
    model_instance_type: Optional[str]
    model_cpu_limit: Optional[float]
    model_cpu_request: Optional[float]
    model_mem_limit: Optional[int]
    model_mem_request: Optional[int]
    model_credentials_id: Optional[str]
    explainer_type: Optional[Any]
    explainer_serverless: Optional[bool] = False
    explainer_instance_type: Optional[str]
    explainer_cpu_limit: Optional[float]
    explainer_cpu_request: Optional[float]
    explainer_mem_limit: Optional[int]
    explainer_mem_request: Optional[int]
    explainer_credentials_id: Optional[str]
    transformer_type: Optional[Any]
    transformer_serverless: Optional[bool] = False
    transformer_instance_type: Optional[str]
    transformer_cpu_limit: Optional[float]
    transformer_cpu_request: Optional[float]
    transformer_mem_limit: Optional[int]
    transformer_mem_request: Optional[int]
    transformer_credentials_id: Optional[str]

    def to_request_body(self) -> Dict:
        request_body = {
            "id": self.deployment_id,
            "repositoryId": self.repository_id,
            "status": self.status,
            "branchName": self.branch_name,
            "commit": self.commit,
            "commitMessage": self.commit_message,
            "contractPath": self.contract_path,
            "deploymentBackend": self.deployment_backend,
            "modelType": self.model_type,
            "modelServerless": self.model_serverless,
            "modelInstanceType": self.model_instance_type,
            "modelCpuLimit": self.model_cpu_limit,
            "modelCpuRequest": self.model_cpu_request,
            "modelMemLimit": self.model_mem_limit,
            "modelMemRequest": self.model_mem_request,
            "modelCredentialsId": self.model_credentials_id,
            "explainerType": self.explainer_type,
            "explainerServerless": self.explainer_serverless,
            "explainerInstanceType": self.explainer_instance_type,
            "explainerCpuLimit": self.explainer_cpu_limit,
            "explainerCpuRequest": self.explainer_cpu_request,
            "explainerMemLimit": self.explainer_mem_limit,
            "explainerMemRequest": self.explainer_mem_request,
            "explainerCredentialsId": self.explainer_credentials_id,
            "transformerType": self.transformer_type,
            "transformerServerless": self.transformer_serverless,
            "transformerInstanceType": self.transformer_instance_type,
            "transformerCpuLimit": self.transformer_cpu_limit,
            "transformerCpuRequest": self.transformer_cpu_request,
            "transformerMemLimit": self.transformer_mem_limit,
            "transformerMemRequest": self.transformer_mem_request,
            "transformerCredentialsId": self.transformer_credentials_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}


class UpdateAzureMLDeployment(BaseModel):
    """Class that contains the options for updating an Azure Machine Learning deployment"""  # noqa

    name: Optional[str]
    description: Optional[str]
    repository_id: Optional[str]
    branch_name: Optional[str]
    commit: Optional[str]
    commit_message: Optional[str]
    contract_path: Optional[str]
    input_tensor_size: Optional[str]
    output_tensor_size: Optional[str]
    model_type: Optional[Any]
    explainer_type: Optional[Any]
    transformer_type: Optional[Any]
    model_instance_type: Optional[str]
    model_instance_count: Optional[int]
    explainer_instance_type: Optional[str]
    explainer_instance_count: Optional[int]


    def to_request_body(self):
        return {
            "name": self.name,
            "description": self.description,
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "commitMessage": self.commit_message,
            "contractPath": self.contract_path,
            "modelType": self.model_type,
            "explainerType": self.explainer_type,
            "transformerType": self.transformer_type,
            "modelInstanceType": self.model_instance_type,
            "modelInstanceCount": self.model_instance_count,
            "explainerInstanceType": self.explainer_instance_type,
            "explainerInstanceCount": self.explainer_instance_count
        }



class UpdateDeploymentDescription(BaseModel):
    """Class that contains the options for updating a model that doesn't require restarting pods"""  # noqa

    deployment_id: Optional[str]
    name: Optional[str]
    description: Optional[str]

    def to_request_body(self) -> Dict:
        request_body = {
            "name": self.name,
            "description": self.description,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}
