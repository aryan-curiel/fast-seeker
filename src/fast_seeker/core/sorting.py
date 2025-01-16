from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from pydantic import BaseModel

ASC_SIGN = "+"
DESC_SIGN = "-"


class SortDirection(StrEnum):
    """
    SortDirection is an enumeration that defines the possible directions for sorting.

    Attributes:
        ASC (str): Represents ascending sort direction.
        DESC (str): Represents descending sort direction.
    """

    ASC = ASC_SIGN
    DESC = DESC_SIGN


@dataclass
class OrderEntry:
    """
    Represents an entry in an order specification.

    Attributes:
        key (str): The key by which to sort.
        direction (SortDirection): The direction in which to sort (e.g., ascending or descending).
    """

    key: str
    direction: SortDirection

    @classmethod
    def asc(cls, key: str) -> Self:
        """
        Creates an OrderEntry object with the specified key and ascending direction.

        Args:
            key (str): The key by which to sort.

        Returns:
            OrderEntry: An OrderEntry object with the specified key and ascending direction.
        """
        return cls(key=key, direction=SortDirection.ASC)

    @classmethod
    def desc(cls, key: str) -> Self:
        """
        Creates an OrderEntry object with the specified key and descending direction.

        Args:
            key (str): The key by which to sort.

        Returns:
            OrderEntry: An OrderEntry object with the specified key and descending direction.
        """
        return cls(key=key, direction=SortDirection.DESC)


GenericOrdering = list[tuple[str, SortDirection]]


class SortingModel(BaseModel):
    """
    SortingModel is a data model for handling sorting operations.

    Attributes:
        order_by (list[str]): A list of strings representing the sorting order.
                            Assumed to follow format "[+]field" or "-field".

    Methods:
        _parse_entry(order: str) -> OrderEntry:
            Parses a sorting order string and returns an OrderEntry object.

        parsed -> Generator[OrderEntry]:
            A generator property that yields parsed OrderEntry objects from the order_by list.
    """

    order_by: list[str] = []

    @classmethod
    def _parse_entry(cls, order: str) -> OrderEntry:
        """
        Parses a sorting order string and returns an OrderEntry object.

        Args:
            order (str): The sorting order string. It should start with either
                         the ascending sign (ASC_SIGN) or the descending sign (DESC_SIGN).
                         If it does not, the ascending sign is prepended by default.

        Returns:
            OrderEntry: An object containing the key and the sorting direction.
        """
        order = order if order.startswith((ASC_SIGN, DESC_SIGN)) else f"{ASC_SIGN}{order}"
        return OrderEntry(key=order[1:], direction=SortDirection(order[0]))

    @property
    def parsed(self) -> Generator[OrderEntry]:
        """
        Parses the orders and yields `OrderEntry` objects.

        Yields:
            Generator[OrderEntry]: A generator that yields parsed `OrderEntry` objects.
        """
        return (SortingModel._parse_entry(order) for order in self.order_by)


class OrderBuilder[_SortArgs](ABC):
    """
    OrderBuilder is an abstract base class that defines the interface for building sorting orders.

    This class should be subclassed, and the subclass should implement the `get_order` method to provide
    the sorting order based on the provided sorting query.

    Methods:
        get_order(sort_query: SortingModel) -> _SortArgs:
    """

    @abstractmethod
    def get_order(self, sort_query: SortingModel) -> _SortArgs:
        """
        Abstract method to get the sorting order based on the provided sorting query.

        Args:
            sort_query (SortingModel): The sorting model containing the sorting criteria.

        Returns:
            _SortArgs: The sorting arguments derived from the sorting model.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError


class Sorter[_Data, _Result, _SortArgs](OrderBuilder[_SortArgs], ABC):
    """
    Abstract base class for sorting data.

    This class defines the interface for sorting data, which includes methods for
    applying an order to the data and retrieving the order based on a sorting query.

    Type Parameters:
        _Data: The type of the data to be sorted.
        _Result: The type of the result after sorting.
        _SortArgs: The type of the sorting arguments.

    Methods:
        _apply_order(data: _Data, order: _SortArgs) -> _Result:
            Abstract method to apply the sorting order to the data.
            Must be implemented by subclasses.

        get_order(sort_query: SortingModel) -> _SortArgs:
            Abstract method to retrieve the sorting order based on the sorting query.
            Must be implemented by subclasses.

        sort(data: _Data, sort_query: SortingModel) -> _Result:
            Sorts the data based on the provided sorting query.
            If the sorting query does not specify an order, the original data is returned.
    """

    @abstractmethod
    def _apply_order(self, data: _Data, order: _SortArgs) -> _Result:
        """
        Apply the specified order to the given data.

        This method should be implemented to sort or order the data based on the
        provided order arguments.

        Args:
            data (_Data): The data to be ordered.
            order (_SortArgs): The arguments specifying the order.

        Returns:
            _Result: The result after applying the order to the data.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError

    def sort(self, data: _Data, sort_query: SortingModel) -> _Result:
        """
        Sorts the given data based on the provided sorting query.

        Args:
            data (_Data): The data to be sorted.
            sort_query (SortingModel): The sorting criteria.

        Returns:
            _Result: The sorted data. If no sorting criteria is provided, returns the original data.
        """
        if not sort_query.order_by:
            return data
        order = self.get_order(sort_query)
        return self._apply_order(data, order)
