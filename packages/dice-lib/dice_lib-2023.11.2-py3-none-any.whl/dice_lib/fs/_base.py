from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Tuple

import pandas as pd


@dataclass
class LsFormat:
    permissions: List[str]
    owner: List[str]
    group: List[str]
    size: List[int]
    size_scaled: List[float]
    size_unit: List[str]
    date: List[datetime]
    name: List[str]

    def to_pandas(self) -> pd.DataFrame:
        import pandas as pd

        return pd.DataFrame(
            {
                "permissions": self.permissions,
                "owner": self.owner,
                "group": self.group,
                "size": self.size,
                "size_scaled": self.size_scaled,
                "size_unit": self.size_unit,
                "date": self.date,
                "name": self.name,
            }
        )

    def __repr__(self) -> str:
        return str(self.to_pandas().__repr__())

    def to_list(self) -> Any:
        return self.to_pandas().values.tolist()


class FileSystem(ABC):
    _protocol: str = "file://"

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def size_of_path(self, path: str) -> Tuple[str, int, float, str]:
        """
        Returns a tuple of (path, size_in_bytes, size_in_largest_unit, largest_unit) for a given path.
        Largest unit is the largest unit where size is smaller than the scale of the next one.
        Scale for sizes is 1024.
        """

    @abstractmethod
    def size_of_paths(self, paths: List[str]) -> List[Tuple[str, int, float, str]]:
        ...

    @abstractmethod
    def get_owner(self, pathstr: str) -> str:
        ...

    @abstractmethod
    def ls(self, path: str) -> LsFormat:
        ...

    @abstractmethod
    def mkdir(self, path: str) -> None:
        ...

    @abstractmethod
    def rm(self, path: str) -> None:
        ...

    @abstractmethod
    def rm_recursive(self, path: str) -> None:
        ...

    @abstractmethod
    def copy(self, src: str, dest: str) -> None:
        ...

    @abstractmethod
    def copy_recursive(self, src: str, dest: str) -> None:
        ...

    @abstractmethod
    def move(self, src: str, dest: str) -> None:
        ...
