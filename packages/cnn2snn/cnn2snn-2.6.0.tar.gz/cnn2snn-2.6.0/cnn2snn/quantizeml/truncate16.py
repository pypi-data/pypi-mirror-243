#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
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
# ******************************************************************************
"""Functions to convert quantizeml Truncate16 to Akida Truncate16 layer.
"""

from quantizeml import layers
from akida import Truncate16

from ..akida_versions import AkidaVersion
from .block_converter import BlockConverter, register_conversion_patterns


__all__ = ["Truncate16BlockConverter"]

_PATTERNS = [(layers.Truncate16,)]


def convert_truncate16_block(model_ak, block):
    """Converts a truncate16 block into an akida Truncate16 layer.

    Args:
        model_ak (:obj:`akida.Model`): the target Akida model.
        block (list(:obj:`tf.keras.Layer`)): the block layers.

    Returns:
        bool: Returns True for a successful conversion.
    """
    truncate16 = block[0]
    # initialize input_shape with ones.
    input_shape = [1] * 3
    # Iterate over the layer input shape dimensions.
    for i, dim in enumerate(reversed(truncate16.input_shape[1:])):
        input_shape[-1 - i] = dim
    # Evaluate the layer params
    layer_params = dict(
        input_shape=tuple(int(x) for x in input_shape),
        name=truncate16.name
    )

    truncate16_ak = Truncate16(**layer_params)

    # Add layer to the model to build its internal variables
    model_ak.add(truncate16_ak)

    return True


class Truncate16BlockConverter(BlockConverter):
    """Main class that should be used to check if the truncate16 block is compatible to an Akida v2
    conversion and provides a method to convert it in an equivalent Akida Truncate16 layer.

    Args:
        block (list): list of quantizeml quantized layers.
    """

    def convert(self, model_ak):
        assert len(model_ak.layers) == 0, "Truncate16 should be the first model layer."
        return convert_truncate16_block(model_ak, self._block)


# Register the valid truncate16 block pattern for Akida v1 and v2
register_conversion_patterns(AkidaVersion.v2, _PATTERNS, Truncate16BlockConverter, True)
