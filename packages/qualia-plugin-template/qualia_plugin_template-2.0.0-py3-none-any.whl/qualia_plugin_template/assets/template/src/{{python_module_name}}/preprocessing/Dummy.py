"""Contains a dummy preprocessing module."""

from __future__ import annotations

import logging
import sys

from qualia_core.datamodel import RawDataModel
from qualia_core.preprocessing.Preprocessing import Preprocessing

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)

class Dummy(Preprocessing[RawDataModel, RawDataModel]):
    """Dummy preprocessing module."""

    @override
    def __call__(self, datamodel: RawDataModel) -> RawDataModel:
        """Preprocess dataset, dummy implementation.

        :meta public:
        :param datamodel: The input dataset
        :return: The unchanged dataset
        """
        logger.error('Not implemented.')
        return datamodel
