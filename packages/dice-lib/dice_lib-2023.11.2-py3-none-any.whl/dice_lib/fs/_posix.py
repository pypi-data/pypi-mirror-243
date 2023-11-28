from datetime import datetime
from pathlib import Path
from typing import Callable, List, Tuple

from plumbum import local
from plumbum.commands.base import BoundCommand

from dice_lib.units import convert_to_largest_unit

from ._base import FileSystem, LsFormat


class PosixFileSystem(FileSystem):
    def __init__(self) -> None:
        # command definitions
        self._size_cmd: BoundCommand = local["nice"]["-n19", "du"]["-s"]
        self._copy_cmd: BoundCommand = local["cp"]["-p"]
        self._copy_recursive_cmd: BoundCommand = local["cp"]["-pr"]
        self._move_cmd: BoundCommand = local["mv"]
        self._ls_cmd: BoundCommand = local["ls"]["-la", "--time-style=long-iso"]
        self._mkdir_cmd: BoundCommand = local["mkdir"]["-p"]
        self._rm_cmd: BoundCommand = local["rm"]["-f"]
        self._rm_recursive_cmd: BoundCommand = local["rm"]["-fr"]
        self._dataparser: Callable[[str], datetime] = lambda x: datetime.strptime(
            x, "%Y-%m-%d %H:%M"
        )

    def get_owner(self, pathstr: str) -> str:
        path = Path(pathstr)
        return path.owner()

    def size_of_path(self, path: str) -> Tuple[str, int, float, str]:
        total, _ = self._size_cmd(path).split()
        total = int(total)
        total_scaled, unit = convert_to_largest_unit(total, "B", scale=1024)
        return str(path), total, total_scaled, unit

    def size_of_paths(self, paths: List[str]) -> List[Tuple[str, int, float, str]]:
        return [self.size_of_path(path) for path in paths]

    def copy(self, src: str, dest: str) -> None:
        self._copy_cmd(src, dest)

    def copy_recursive(self, src: str, dest: str) -> None:
        self._copy_recursive_cmd(src, dest)

    def move(self, src: str, dest: str) -> None:
        self._move_cmd(src, dest)

    def ls(self, path: str) -> LsFormat:
        cmd_output = self._ls_cmd(path)
        # skip first 3 lines (total, ., ..) and last line (empty)
        lines = cmd_output.split("\n")[3:-1]
        permissions = []
        owner = []
        group = []
        size = []
        size_scaled = []
        unit = []
        date = []
        name = []
        for line in lines:
            line = line.split()
            permissions.append(line[0])
            owner.append(line[2])
            group.append(line[3])
            raw_size = int(line[4])
            size.append(raw_size)
            tmp_size_scaled, tmp_unit = convert_to_largest_unit(
                raw_size, "B", scale=1024
            )
            size_scaled.append(tmp_size_scaled)
            unit.append(tmp_unit)
            date.append(self._dataparser(line[5] + " " + line[6]))
            name.append(line[7])
        return LsFormat(
            permissions=permissions,
            owner=owner,
            group=group,
            size=size,
            size_scaled=size_scaled,
            size_unit=unit,
            date=date,
            name=name,
        )

    def mkdir(self, path: str) -> None:
        self._mkdir_cmd(path)

    def rm(self, path: str) -> None:
        self._rm_cmd(path)

    def rm_recursive(self, path: str) -> None:
        self._rm_recursive_cmd(path)
