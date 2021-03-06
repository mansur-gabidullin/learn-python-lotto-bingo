"""Card Entity."""
import random
from functools import total_ordering
from typing import List, Iterator, Any

from src.lotto_bingo.constants import CARD_ROWS_COUNT, CARD_COLS_COUNT, CARD_NUMBERS_COUNT_IN_ROW, KEGS_COUNT
from src.lotto_bingo.utils import striked


def get_cells(numbers: List[int], numbers_count: int | None = None, cells_count: int | None = None) -> Iterator[str]:
    """Card cells generator"""
    number_index = 0
    rest_numbers = numbers_count or CARD_NUMBERS_COUNT_IN_ROW
    rest_cells = cells_count or CARD_COLS_COUNT
    length = len(numbers)

    for _ in range(rest_cells):
        if number_index < length and rest_cells and rest_numbers / rest_cells > random.random():
            yield str(numbers[number_index])
            number_index += 1
            rest_numbers -= 1
        else:
            yield ""
        rest_cells -= 1


@total_ordering
class Card:
    """Card class"""

    _numbers: List[int]
    _grid: List[List[str]]

    def __init__(self, numbers: List[int] | None = None):
        if numbers is not None:
            self._numbers = numbers.copy()
        else:
            numbers_count = CARD_ROWS_COUNT * CARD_NUMBERS_COUNT_IN_ROW
            numbers_range = range(1, KEGS_COUNT + 1)
            self._numbers = random.sample(numbers_range, numbers_count)

        self._grid = [
            list(
                get_cells(
                    sorted(
                        self._numbers[
                            i * CARD_NUMBERS_COUNT_IN_ROW : i * CARD_NUMBERS_COUNT_IN_ROW + CARD_NUMBERS_COUNT_IN_ROW
                        ]
                    )
                )
            )
            for i in range(CARD_ROWS_COUNT)
        ]

    def __contains__(self, key: int) -> bool:
        return key in self._numbers

    def __str__(self) -> str:
        columns = CARD_NUMBERS_COUNT_IN_ROW + (CARD_NUMBERS_COUNT_IN_ROW - 1)
        return "\n".join(
            [
                "-".join(["--"] * columns),
                *(" ".join(map(lambda cell: cell.rjust(2), row)) for row in self._grid),
                "-".join(["--"] * columns),
            ]
        )

    def __len__(self) -> int:
        return len(self._numbers)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(self, other.__class__):
            return False
        return all((number in other._numbers for number in self._numbers))

    def __gt__(self, other: Any) -> bool:
        return len(self) > len(other)

    def strike_out(self, number: int) -> None:
        """Strike out given keg number from card"""
        self._numbers.remove(number)
        cell = str(number)
        for row in self._grid:
            if cell in row:
                cell_index = row.index(str(number))
                row[cell_index] = striked(row[cell_index])
