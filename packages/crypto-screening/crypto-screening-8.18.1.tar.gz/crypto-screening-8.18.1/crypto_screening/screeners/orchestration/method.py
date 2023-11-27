# method.py

from typing import Iterable
from enum import Enum

from crypto_screening.screeners.combined import (
    CategoryBase, Categories
)
from crypto_screening.screeners.container import ScreenersContainer

__all__ = [
    "OrchestrationMethod",
    "split_screeners_data"
]

class OrchestrationMethod(Enum):
    """A class to represent an enum of an orchestration method."""

    INDIVIDUALS = "individuals"
    EXCHANGES = "exchanges"
    CATEGORIES = "categories"
    CATEGORIES_EXCHANGES = "categories_exchanges"
    ALL = "all"
# end OrchestrationMethod

Data = dict[CategoryBase, dict[str, str | dict[str, Iterable[str]]]]

def split_screeners_data(
        container: ScreenersContainer,
        method: OrchestrationMethod
) -> list[Data]:
    """
    Creates the market screener object for the data.

    :param container: The collector to create a process for.
    :param method: The orchestration method.

    :return: The data publisher server object.
    """

    data: Data = {}

    for category in Categories.categories:
        screeners = container.find_screeners(base=category.screener)

        if screeners:
            new_container = ScreenersContainer(screeners=screeners)
            data[category] = (
                new_container.map()
                if new_container is Categories.ohlcv else
                new_container.structure()
            )
        # end if
    # end for

    datas: list[Data] = []

    if method == OrchestrationMethod.ALL:
        datas.append(data)

    elif method == OrchestrationMethod.CATEGORIES:
        for category, category_data in data.items():
            datas.append({category: category_data})
        # end for

    elif method == OrchestrationMethod.EXCHANGES:
        for exchange in container.structure().keys():
            datas.append(
                {
                    category: {exchange: category_data[exchange]}
                    for category, category_data in data.items()
                }
            )
        # end for

    elif method == OrchestrationMethod.CATEGORIES_EXCHANGES:
        for category, category_data in data.items():
            for exchange, exchange_data in category_data.items():
                datas.append({category: {exchange: exchange_data}})
            # end for
        # end for

    elif method == OrchestrationMethod.INDIVIDUALS:
        for category, category_data in data.items():
            for exchange, exchange_data in category_data.items():
                for symbol in exchange_data:
                    datas.append(
                        {
                            category: {
                                exchange: (
                                    {symbol} if
                                    not isinstance(exchange_data, dict) else
                                    {symbol: exchange_data[symbol]}
                                )
                            }
                        }
                    )
                # end for
            # end for
        # end for
    # end if

    return datas
# end split_screeners_data