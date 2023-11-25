"""Contains a dummy dataset module."""

from __future__ import annotations

import logging
import sys

import numpy as np
from qualia_core.datamodel import RawDataModel
from qualia_core.datamodel.RawDataModel import RawData, RawDataSets
from qualia_core.dataset.RawDataset import RawDataset

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)

class Dummy(RawDataset):
    """Dummy preprocessing module."""

    def __init__(self) -> None:
        """Construct :class:`Dummy`.

        ``'valid'`` is removed from the sets provided by the dataset since there is no validation data.
        """
        super().__init__()
        self.sets.remove('valid')

    @override
    def __call__(self) -> RawDataModel:
        """Load dataset, dummy implementation.

        :meta public:
        :return: The loaded dataset
        :raise NotImplementedError: Always
        """
        logger.error('Not implemented.')
        data = RawData(np.zeros((1, 1, 1)), np.zeros((1, 2)))
        return RawDataModel(sets=RawDataSets(train=data, test=data), name=self.name)
