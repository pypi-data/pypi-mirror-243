from __future__ import annotations
from collections import deque
from .aoc_ocr import convert_array_6
from .coordinate import Coordinate, DistanceAlgorithm, Shape
from enum import Enum
from heapq import heappop, heappush
from math import inf
from typing import Any, Dict, List

OFF = False
ON = True


class GridTransformation(Enum):
    # Rotations always take the axis to rotate around as if it were the z-axis and then rotate clockwise
    # Counter-Rotations likewise, just anti-clockwise
    # 3D-only OPs have a number > 10
    ROTATE_Z = 3
    ROTATE_X = 11
    ROTATE_Y = 12
    COUNTER_ROTATE_X = 14
    COUNTER_ROTATE_Y = 15
    COUNTER_ROTATE_Z = 7
    FLIP_X = 4
    FLIP_Y = 5
    FLIP_Z = 13

    # Handy aliases
    FLIP_HORIZONTALLY = 5
    FLIP_VERTICALLY = 4
    ROTATE_RIGHT = 3
    ROTATE_LEFT = 7


class Grid:
    def __init__(self, default=False):
        self.__default = default
        self.__grid = {}
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        self.minZ = None
        self.maxZ = None
        self.mode3D = False

    def __trackBoundaries(self, pos: Coordinate):
        if self.minX is None:
            self.minX, self.maxX, self.minY, self.maxY = pos.x, pos.x, pos.y, pos.y
        else:
            self.minX = pos.x if pos.x < self.minX else self.minX
            self.minY = pos.y if pos.y < self.minY else self.minY
            self.maxX = pos.x if pos.x > self.maxX else self.maxX
            self.maxY = pos.y if pos.y > self.maxY else self.maxY

        if self.mode3D:
            if self.minZ is None:
                self.minZ = self.maxZ = pos.z
            else:
                self.minZ = pos.z if pos.z < self.minZ else self.minZ
                self.maxZ = pos.z if pos.z > self.maxZ else self.maxZ

    def recalcBoundaries(self) -> None:
        self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ = (
            None,
            None,
            None,
            None,
            None,
            None,
        )
        for c in self.__grid:
            self.__trackBoundaries(c)

    def getBoundaries(self) -> (int, int, int, int, int, int):
        if self.mode3D:
            return self.minX, self.minY, self.maxX, self.maxY, self.minZ, self.maxZ
        else:
            return self.minX, self.minY, self.maxX, self.maxY, -inf, inf

    def rangeX(self, pad: int = 0, reverse=False):
        if reverse:
            return range(self.maxX + pad, self.minX - pad - 1, -1)
        else:
            return range(self.minX - pad, self.maxX + pad + 1)

    def rangeY(self, pad: int = 0, reverse=False):
        if reverse:
            return range(self.maxY + pad, self.minY - pad - 1, -1)
        else:
            return range(self.minY - pad, self.maxY + pad + 1)

    def rangeZ(self, pad: int = 0, reverse=False):
        if not self.mode3D:
            raise ValueError("rangeZ not available in 2D space")
        if reverse:
            return range(self.maxZ + pad, self.minZ - pad - 1, -1)
        else:
            return range(self.minZ - pad, self.maxZ + pad + 1)

    def toggle(self, pos: Coordinate):
        if pos in self.__grid:
            del self.__grid[pos]
        else:
            self.__trackBoundaries(pos)
            self.__grid[pos] = not self.__default

    def toggleGrid(self):
        for x in self.rangeX():
            for y in self.rangeY():
                if not self.mode3D:
                    self.toggle(Coordinate(x, y))
                else:
                    for z in self.rangeZ():
                        self.toggle(Coordinate(x, y, z))

    def set(self, pos: Coordinate, value: Any = True) -> Any:
        if pos.z is not None:
            self.mode3D = True

        if (value == self.__default) and pos in self.__grid:
            del self.__grid[pos]
        elif value != self.__default:
            self.__trackBoundaries(pos)
            self.__grid[pos] = value

        return value

    def move(
        self,
        pos: Coordinate,
        vec: Coordinate,
    ):
        target = pos + vec
        self.set(target, self.get(pos))
        if pos in self.__grid:
            del self.__grid[pos]

    def add(self, pos: Coordinate, value: int | float = 1) -> int | float:
        return self.set(pos, self.get(pos) + value)

    def sub(self, pos: Coordinate, value: int | float = 1) -> int | float:
        return self.set(pos, self.get(pos) - value)

    def mul(self, pos: Coordinate, value: int | float = 1) -> int | float:
        return self.set(pos, self.get(pos) * value)

    def div(self, pos: Coordinate, value: int | float = 1) -> int | float:
        return self.set(pos, self.get(pos) / value)

    def add_shape(self, shape: Shape, value: int | float = 1) -> None:
        for x in range(shape.top_left.x, shape.bottom_right.x + 1):
            for y in range(shape.top_left.y, shape.bottom_right.y + 1):
                if not shape.mode_3d:
                    pos = Coordinate(x, y)
                    self.set(pos, self.get(pos) + value)
                else:
                    for z in range(shape.top_left.z, shape.bottom_right.z + 1):
                        pos = Coordinate(x, y, z)
                        self.set(pos, self.get(pos) + value)

    def get(self, pos: Coordinate) -> Any:
        return self.__grid.get(pos, self.__default)

    def getOnCount(self) -> int:
        return len(self.__grid)

    def count(self, value: Any) -> int:
        return list(self.__grid.values()).count(value)

    def isSet(self, pos: Coordinate) -> bool:
        return pos in self.__grid

    def getCorners(self) -> List[Coordinate]:
        if not self.mode3D:
            return [
                Coordinate(self.minX, self.minY),
                Coordinate(self.minX, self.maxY),
                Coordinate(self.maxX, self.minY),
                Coordinate(self.maxX, self.maxY),
            ]
        else:
            return [
                Coordinate(self.minX, self.minY, self.minZ),
                Coordinate(self.minX, self.minY, self.maxZ),
                Coordinate(self.minX, self.maxY, self.minZ),
                Coordinate(self.minX, self.maxY, self.maxZ),
                Coordinate(self.maxX, self.minY, self.minZ),
                Coordinate(self.maxX, self.minY, self.maxZ),
                Coordinate(self.maxX, self.maxY, self.minZ),
                Coordinate(self.maxX, self.maxY, self.maxZ),
            ]

    def isCorner(self, pos: Coordinate) -> bool:
        return pos in self.getCorners()

    def isWithinBoundaries(self, pos: Coordinate) -> bool:
        if self.mode3D:
            return (
                self.minX <= pos.x <= self.maxX
                and self.minY <= pos.y <= self.maxY
                and self.minZ <= pos.z <= self.maxZ
            )
        else:
            return self.minX <= pos.x <= self.maxX and self.minY <= pos.y <= self.maxY

    def getActiveCells(
        self, x: int = None, y: int = None, z: int = None
    ) -> List[Coordinate]:
        if x is not None or y is not None or z is not None:
            return [
                c
                for c in self.__grid.keys()
                if (c.x == x if x is not None else True)
                and (c.y == y if y is not None else True)
                and (c.z == z if z is not None else True)
            ]
        else:
            return list(self.__grid.keys())

    def getActiveRegion(
        self,
        start: Coordinate,
        includeDiagonal: bool = False,
        ignore: List[Coordinate] = None,
    ) -> List[Coordinate]:
        if not self.get(start):
            return []
        if ignore is None:
            ignore = []
        ignore.append(start)
        for c in self.getNeighboursOf(start, includeDiagonal=includeDiagonal):
            if c not in ignore:
                ignore = self.getActiveRegion(c, includeDiagonal, ignore)

        return ignore

    def values(self):
        return self.__grid.values()

    def getSum(self, includeNegative: bool = True) -> int | float:
        if not self.mode3D:
            return sum(
                self.get(Coordinate(x, y))
                for x in self.rangeX()
                for y in self.rangeY()
                if includeNegative or self.get(Coordinate(x, y)) >= 0
            )
        else:
            return sum(
                self.get(Coordinate(x, y, z))
                for x in self.rangeX()
                for y in self.rangeY()
                for z in self.rangeZ()
                if includeNegative or self.get(Coordinate(x, y)) >= 0
            )

    def getNeighboursOf(
        self,
        pos: Coordinate,
        includeDefault: bool = False,
        includeDiagonal: bool = True,
    ) -> List[Coordinate]:
        neighbours = pos.getNeighbours(
            includeDiagonal=includeDiagonal,
            minX=self.minX,
            minY=self.minY,
            minZ=self.minZ,
            maxX=self.maxX,
            maxY=self.maxY,
            maxZ=self.maxZ,
        )
        for x in neighbours:
            if includeDefault or x in self.__grid:
                yield x

    def getNeighbourSum(
        self,
        pos: Coordinate,
        includeNegative: bool = True,
        includeDiagonal: bool = True,
    ) -> int | float:
        neighbour_sum = 0
        for neighbour in self.getNeighboursOf(pos, includeDefault=includeDiagonal):
            if includeNegative or self.get(neighbour) > 0:
                neighbour_sum += self.get(neighbour)

        return neighbour_sum

    def flip(self, c1: Coordinate, c2: Coordinate):
        buf = self.get(c1)
        self.set(c1, self.get(c2))
        self.set(c2, buf)

    def transform(self, mode: GridTransformation):
        if mode.value > 10 and not self.mode3D:
            raise ValueError("Operation not possible in 2D space", mode)

        coords = self.__grid
        self.__grid = {}
        if mode == GridTransformation.ROTATE_X:
            shift_z = self.maxY
            for c, v in coords.items():
                self.set(Coordinate(c.x, c.z, -c.y), v)
            self.shift(shift_z=shift_z)
        elif mode == GridTransformation.ROTATE_Y:
            shift_x = self.maxX
            for c, v in coords.items():
                self.set(Coordinate(-c.z, c.y, c.x), v)
            self.shift(shift_x=shift_x)
        elif mode == GridTransformation.ROTATE_Z:
            shift_x = self.maxX
            for c, v in coords.items():
                self.set(Coordinate(-c.y, c.x, c.z), v)
            self.shift(shift_x=shift_x)
        elif mode == GridTransformation.COUNTER_ROTATE_X:
            shift_y = self.maxY
            for c, v in coords.items():
                self.set(Coordinate(c.x, -c.z, c.y), v)
            self.shift(shift_y=shift_y)
        elif mode == GridTransformation.COUNTER_ROTATE_Y:
            shift_z = self.maxZ
            for c, v in coords.items():
                self.set(Coordinate(c.z, c.y, -c.x), v)
            self.shift(shift_z=shift_z)
        elif mode == GridTransformation.COUNTER_ROTATE_Z:
            shift_y = self.maxY
            for c, v in coords.items():
                self.set(Coordinate(c.y, -c.x, c.z), v)
            self.shift(shift_y=shift_y)
        elif mode == GridTransformation.FLIP_X:
            shift_x = self.maxX
            for c, v in coords.items():
                self.set(Coordinate(-c.x, c.y, c.z), v)
            self.shift(shift_x=shift_x)
        elif mode == GridTransformation.FLIP_Y:
            shift_y = self.maxY
            for c, v in coords.items():
                self.set(Coordinate(c.x, -c.y, c.z), v)
            self.shift(shift_y=shift_y)
        elif mode == GridTransformation.FLIP_Z:
            shift_z = self.maxZ
            for c, v in coords.items():
                self.set(Coordinate(c.x, c.y, -c.z), v)
            self.shift(shift_z=shift_z)
        else:
            raise NotImplementedError(mode)

        self.recalcBoundaries()

    def shift(self, shift_x: int = 0, shift_y: int = 0, shift_z: int = 0):
        self.minX, self.minY = self.minX + shift_x, self.minY + shift_y
        self.maxX, self.maxY = self.maxX + shift_x, self.maxY + shift_y
        if self.mode3D:
            self.minZ, self.maxZ = self.minZ + shift_z, self.maxZ + shift_z
        coords = self.__grid
        self.__grid = {}
        for c, v in coords.items():
            if self.mode3D:
                nc = Coordinate(c.x + shift_x, c.y + shift_y, c.z + shift_z)
            else:
                nc = Coordinate(c.x + shift_x, c.y + shift_y)
            self.set(nc, v)

    def shift_zero(self, recalc: bool = True):
        # self.shift() to (0, 0, 0) being top, left, front
        if recalc:
            self.recalcBoundaries()
        if self.mode3D:
            self.shift(0 - self.minX, 0 - self.minY, 0 - self.minZ)
        else:
            self.shift(0 - self.minX, 0 - self.minY)

    def getPath_BFS(
        self,
        pos_from: Coordinate,
        pos_to: Coordinate,
        includeDiagonal: bool,
        walls: List[Any] = None,
        stop_at_first: Any = None,
    ) -> List[Coordinate] | None:
        queue = deque()
        came_from = {pos_from: None}
        queue.append(pos_from)
        if walls is None:
            walls = [self.__default]

        while queue:
            current = queue.popleft()
            found_end = False
            for c in self.getNeighboursOf(
                current,
                includeDiagonal=includeDiagonal,
                includeDefault=self.__default not in walls,
            ):
                if c in came_from and self.get(c) in walls:
                    continue
                came_from[c] = current
                if c == pos_to or (
                    stop_at_first is not None and self.get(c) == stop_at_first
                ):
                    pos_to = c
                    found_end = True
                    break
                queue.append(c)
            if found_end:
                break

        if pos_to not in came_from:
            return None

        ret = []
        while pos_to in came_from:
            ret.insert(0, pos_to)
            pos_to = came_from[pos_to]

        return ret

    def getPath(
        self,
        pos_from: Coordinate,
        pos_to: Coordinate,
        includeDiagonal: bool,
        walls: List[Any] = None,
        weighted: bool = False,
    ) -> List[Coordinate] | None:
        f_costs = []
        if walls is None:
            walls = [self.__default]

        openNodes: Dict[Coordinate, tuple] = {}
        closedNodes: Dict[Coordinate, tuple] = {}

        openNodes[pos_from] = (0, pos_from.getDistanceTo(pos_to), None)
        heappush(f_costs, (0, pos_from))

        while f_costs:
            _, currentCoord = heappop(f_costs)
            if currentCoord not in openNodes:
                continue
            currentNode = openNodes[currentCoord]

            closedNodes[currentCoord] = currentNode
            del openNodes[currentCoord]
            if currentCoord == pos_to:
                break

            for neighbour in self.getNeighboursOf(
                currentCoord, includeDefault=True, includeDiagonal=includeDiagonal
            ):
                if self.get(neighbour) in walls or neighbour in closedNodes:
                    continue

                if weighted:
                    neighbourDist = self.get(neighbour)
                elif not includeDiagonal:
                    neighbourDist = 1
                else:
                    neighbourDist = currentCoord.getDistanceTo(
                        neighbour, DistanceAlgorithm.MANHATTAN, includeDiagonal
                    )

                targetDist = neighbour.getDistanceTo(pos_to)
                f_cost = targetDist + neighbourDist + currentNode[1]

                if neighbour not in openNodes or f_cost < openNodes[neighbour][0]:
                    openNodes[neighbour] = (
                        f_cost,
                        currentNode[1] + neighbourDist,
                        currentCoord,
                    )
                    heappush(f_costs, (f_cost, neighbour))

        if pos_to not in closedNodes:
            return None
        else:
            currentNode = closedNodes[pos_to]
            pathCoords = [pos_to]
            while currentNode[2]:
                pathCoords.append(currentNode[2])
                currentNode = closedNodes[currentNode[2]]

            return pathCoords

    def sub_grid(
        self,
        from_x: int,
        from_y: int,
        to_x: int,
        to_y: int,
        from_z: int = None,
        to_z: int = None,
    ) -> "Grid":
        if self.mode3D and (from_z is None or to_z is None):
            raise ValueError(
                "sub_grid() on mode3d Grids requires from_z and to_z to be set"
            )
        count_x, count_y, count_z = 0, 0, 0
        new_grid = Grid(self.__default)
        for x in range(from_x, to_x + 1):
            for y in range(from_y, to_y + 1):
                if not self.mode3D:
                    new_grid.set(
                        Coordinate(count_x, count_y), self.get(Coordinate(x, y))
                    )
                else:
                    for z in range(from_z, to_z + 1):
                        new_grid.set(
                            Coordinate(count_x, count_y, count_z),
                            self.get(Coordinate(x, y, z)),
                        )
                        count_z += 1

                    count_z = 0
                count_y += 1
            count_y = 0
            count_x += 1

        return new_grid

    def update(self, x: int, y: int, grid: Grid) -> None:
        put_x, put_y = x, y
        for get_x in grid.rangeX():
            for get_y in grid.rangeY():
                self.set(Coordinate(put_x, put_y), grid.get(Coordinate(get_x, get_y)))
                put_y += 1
            put_y = y
            put_x += 1

    def print(
        self,
        spacer: str = "",
        true_char: str = "#",
        false_char: str = " ",
        translate: dict = None,
        mark: list = None,
        z_level: int = None,
        bool_mode: bool = False,
    ):
        if translate is None:
            translate = {}

        if true_char is not None and True not in translate:
            translate[True] = true_char
        if false_char is not None and False not in translate:
            translate[False] = false_char

        for y in range(self.minY, self.maxY + 1):
            for x in range(self.minX, self.maxX + 1):
                pos = Coordinate(x, y, z_level)

                if mark and pos in mark:
                    print("X", end="")
                elif bool_mode:
                    print(true_char if self.get(pos) else false_char, end="")
                else:
                    value = self.get(pos)
                    if isinstance(value, list):
                        value = len(value)

                    if isinstance(value, Enum):
                        value = value.value

                    print(value if value not in translate else translate[value], end="")
                print(spacer, end="")

            print()

    def get_aoc_ocr_string(self, x_shift: int = 0, y_shift: int = 0):
        return convert_array_6(
            [
                [
                    "#" if self.get(Coordinate(x + x_shift, y + y_shift)) else "."
                    for x in self.rangeX()
                ]
                for y in self.rangeY()
            ]
        )

    def __str__(self, true_char: str = "#", false_char: str = "."):
        return "/".join(
            "".join(
                true_char if self.get(Coordinate(x, y)) else false_char
                for x in range(self.minX, self.maxX + 1)
            )
            for y in range(self.minY, self.maxY + 1)
        )

    @classmethod
    def from_str(
        cls,
        grid_string: str,
        default: Any = False,
        true_char: str = "#",
        true_value: Any = True,
        translate: dict = None,
        mode3d: bool = False,
    ) -> "Grid":
        if translate is None:
            translate = {}
        if (
            true_char is not None
            and True not in translate.values()
            and true_char not in translate
        ):
            translate[true_char] = true_value if true_value is not None else True

        ret = cls(default=default)
        for y, line in enumerate(grid_string.split("/")):
            for x, c in enumerate(line):
                if mode3d:
                    coord = Coordinate(x, y, 0)
                else:
                    coord = Coordinate(x, y)

                if c in translate:
                    ret.set(coord, translate[c])
                else:
                    ret.set(coord, c)

        return ret

    def __eq__(self, other: Grid) -> bool:
        if not isinstance(other, Grid):
            return False

        other_active = set(other.getActiveCells())
        for c, v in self.__grid.items():
            if other.get(c) != v:
                return False
            other_active.remove(c)

        if other_active:
            return False

        return True
