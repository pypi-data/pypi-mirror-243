from typing import Dict

from kserve import Model

from deeploy.cli.wrappers.transformer_wrapper import TransformerWrapper


class DeeployCustomTransformer(Model):
    def __init__(
        self,
        name: str,
        predictor_host: str,
        explainer_host: str,
        transformer_wrapper: TransformerWrapper,
    ):
        """Initializes the Deeploy Model Class
        Parameters:
            name (str): Name of the transformer
            predictor_host (str): Interface to model deployment,
            explainer_host (str): Interface to explainer deployment
            transformer_wrapper (TransformerWrapper): User defined transformer wrapper
        """
        super().__init__(name)
        self.predictor_host = predictor_host
        self.explainer_host = explainer_host
        self.transformer = transformer_wrapper()
        self.ready = True

    def preprocess(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        """
        Parameters:
            payload (Dict): To be predicted input values for model.
            headers (Dict): Request headers.

        Returns:
            Dict: Return the pre model prediction transformed inputs.
        """
        return {
            "instances": [
                self.transformer._preprocess(inputs=instance)
                for instance in payload["instances"]
            ]
        }

    def postprocess(self, response: Dict, headers: Dict[str, str] = None) -> Dict:
        """
        Parameters:
            payload (Dict): Predicted values from model.
            headers (Dict): Request headers.

        Returns:
            Dict: Return the post model prediction transformed result.
        """
        return {
            "predictions": [
                self.transformer._postprocess(inputs=prediction)
                for prediction in response["predictions"]
            ]
        }
