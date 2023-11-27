# Copyright (c) 2020-present Benjamin Soyka
# Original and Licence at https://github.com/bsoyka/advent-of-code-ocr

from __future__ import annotations
from collections.abc import Sequence

ALPHABET_6 = {
    ".##.\n#..#\n#..#\n####\n#..#\n#..#": "A",
    "###.\n#..#\n###.\n#..#\n#..#\n###.": "B",
    ".##.\n#..#\n#...\n#...\n#..#\n.##.": "C",
    "####\n#...\n###.\n#...\n#...\n####": "E",
    "####\n#...\n###.\n#...\n#...\n#...": "F",
    ".##.\n#..#\n#...\n#.##\n#..#\n.###": "G",
    "#..#\n#..#\n####\n#..#\n#..#\n#..#": "H",
    ".###\n..#.\n..#.\n..#.\n..#.\n.###": "I",
    "..##\n...#\n...#\n...#\n#..#\n.##.": "J",
    "#..#\n#.#.\n##..\n#.#.\n#.#.\n#..#": "K",
    "#...\n#...\n#...\n#...\n#...\n####": "L",
    ".##.\n#..#\n#..#\n#..#\n#..#\n.##.": "O",
    "###.\n#..#\n#..#\n###.\n#...\n#...": "P",
    "###.\n#..#\n#..#\n###.\n#.#.\n#..#": "R",
    ".###\n#...\n#...\n.##.\n...#\n###.": "S",
    "#..#\n#..#\n#..#\n#..#\n#..#\n.##.": "U",
    "#...\n#...\n.#.#\n..#.\n..#.\n..#.": "Y",
    "####\n...#\n..#.\n.#..\n#...\n####": "Z",
}


def convert_6(input_text: str, *, fill_pixel: str = "#", empty_pixel: str = ".") -> str:
    """Convert height 6 text to characters"""
    input_text = input_text.replace(fill_pixel, "#").replace(empty_pixel, ".")
    prepared_array = [list(line) for line in input_text.split("\n")]
    return _convert_6(prepared_array)


def convert_array_6(
    array: Sequence[Sequence[str | int]],
    *,
    fill_pixel: str | int = "#",
    empty_pixel: str | int = ".",
) -> str:
    """Convert a height 6 NumPy array or nested list to characters"""
    prepared_array = [
        [
            "#" if pixel == fill_pixel else "." if pixel == empty_pixel else ""
            for pixel in line
        ]
        for line in array
    ]
    return _convert_6(prepared_array)


def _convert_6(array: list[list[str]]) -> str:
    """Convert a prepared height 6 array to characters"""
    rows, cols = len(array), len(array[0])
    if any(len(row) != cols for row in array):
        raise ValueError("all rows should have the same number of columns")
    if rows != 6:
        raise ValueError("incorrect number of rows (expected 6)")

    indices = [slice(start, start + 4) for start in range(0, cols, 5)]
    result = [
        ALPHABET_6["\n".join("".join(row[index]) for row in array)] for index in indices
    ]

    return "".join(result)
