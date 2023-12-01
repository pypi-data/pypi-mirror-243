# This is derived from Kserve and modified by Deeploy
# Copyright 2021 The KServe Authors.
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
from typing import List

import kserve


class TransformerWrapper:
    logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)

    def __init__(self):
        """Initializes the Transformer Wrapper Class"""

    def _preprocess(self, inputs: List) -> List:
        """Preprocess transformation before model prediction
        Parameters:
            inputs (List): \
                Receive one input that needs to be transformed before model prediction \
                  eg. [0, 0, 1]

        Returns
            transformed input as List
                Note: For no transformation return inputs
        """
        raise NotImplementedError

    def _postprocess(self, inputs: List) -> List:
        """Postprocess transformation on model prediction output
        Parameters:
            inputs (List): \
                Receive one input that needs to be transformed after model prediction \
                  eg. [0, 0, 1]

        Returns
            transformed input as List
                Note: For no transformation return inputs
        """
        raise NotImplementedError
