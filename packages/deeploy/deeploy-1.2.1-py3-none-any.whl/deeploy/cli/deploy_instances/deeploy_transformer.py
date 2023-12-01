# This is derived from Kserve and modified by Deeploy
# Copyright 2019 kubeflow.org.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

import kserve

from deeploy.cli.custom_instances.transformer import (
    DeeployCustomTransformer,
)
from deeploy.cli.parsers.parser_transformer import parse_args_transformer

# pylint:disable=no-name-in-module
from deeploy.cli.wrappers.transformer_wrapper import TransformerWrapper

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)


class DeeployTransformerLoader(object):
    def __init__(
        self,
    ) -> None:
        """Initialize the Deeploy Transformer Object"""
        args = parse_args_transformer(sys.argv)
        self.model_name = args.model_name
        self.predictor_host = args.predictor_host
        self.explainer_host = args.explainer_host

    def transformer_serve(
        self,
        transformer_wrapper: TransformerWrapper,
    ) -> None:
        """Deploys the transformer
        Parameters:
            transformer_wrapper (TransformerWrapper): \
                The user defined deeploy transformer wrapper
        """
        custom_transformer = DeeployCustomTransformer(
            self.model_name,
            self.predictor_host,
            self.explainer_host,
            transformer_wrapper,
        )
        kserve.ModelServer().start(models=[custom_transformer])
