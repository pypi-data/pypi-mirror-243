"""Contains a dummy postprocessing module."""

from __future__ import annotations

import logging

from qualia_core.postprocessing.PostProcessing import PostProcessing
from qualia_core.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qualia_core.qualia import TrainResult  # noqa: TCH002
    from qualia_core.typing import ModelConfigDict

logger = logging.getLogger(__name__)

class Dummy(PostProcessing):
    """Dummy postprocessing module."""

    def __call__(self,
                 trainresult: TrainResult,
                 model_conf: ModelConfigDict) -> tuple[TrainResult, ModelConfigDict]:  # noqa: ARG002
        """Postprocess model, dummy implementation.

        :meta public:
        :param trainresult: TrainResult containing the model, the dataset and the training configuration
        :param model_conf: Unused
        :return: The unmodified trainresult and model configuration dict
        """
        logger.error('Not implemented.')
        return trainresult, model_conf
