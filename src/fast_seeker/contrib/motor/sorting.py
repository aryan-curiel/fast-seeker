from typing import Literal

from motor.core import AgnosticCursor as Cursor

from fast_seeker.core.sorting import SortDirection, Sorter, SortingQuery

MOTOR_DIRECTION_MAP = {
    SortDirection.ASC: 1,
    SortDirection.DESC: -1,
}


MotorSortArgs = list[tuple[str, Literal[1] | Literal[-1]]]


class MotorSorter(Sorter[Cursor, Cursor, MotorSortArgs]):
    def translate(self, data: Cursor, query: SortingQuery) -> MotorSortArgs:
        return [(entry.key, MOTOR_DIRECTION_MAP[entry.direction]) for entry in query.parsed]

    def execute(self, data: Cursor, order: MotorSortArgs) -> Cursor:
        return data.sort(order)
