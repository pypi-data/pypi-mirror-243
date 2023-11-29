from typing import Optional

from datazone.core.dataset import Dataset


class Input:
    def __init__(self, entity, **kwargs):
        self.entity = entity
        self.kwargs = kwargs


class Output:
    def __init__(
        self,
        dataset: Optional[Dataset] = None,
        materialized: bool = True,
        partition_by: Optional[list[str]] = None,
    ):
        self.dataset = dataset
        self.materialize = materialized
        self.partition_by = partition_by
