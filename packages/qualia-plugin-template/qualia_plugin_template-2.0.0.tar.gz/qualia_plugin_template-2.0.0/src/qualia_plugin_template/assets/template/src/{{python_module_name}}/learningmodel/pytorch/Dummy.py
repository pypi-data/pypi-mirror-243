"""Contains a dummy model for demonstration purposes."""

from __future__ import annotations

import logging
import sys

from qualia_core.learningmodel.pytorch.LearningModel import LearningModel
from qualia_core.typing import TYPE_CHECKING

if TYPE_CHECKING:
    import torch  # noqa: TCH002

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)

class Dummy(LearningModel):
    """Dummy model template."""

    def __init__(self,
                 input_shape: tuple[int, ...],
                 output_shape: tuple[int, ...]) -> None:
        """Construct :class:`DummyModel`.

        :param input_shape: Input shape
        :param output_shape: Output shape
        """
        super().__init__(input_shape=input_shape,
                         output_shape=output_shape)

    @override
    def forward(self, input: torch.Tensor) -> torch.Tensor:  # noqa: A002
        """Forward for the model, dummy implementation.

        :param input: Input tensor
        :return: Output tensor
        """
        logger.error('Not implemented.')
        return input.new_zeros((input.size(0), 2))
