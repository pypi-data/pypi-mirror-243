# assets.py

from typing import Iterable

from crypto_screening.utils.process import mutual_string_values
from crypto_screening.symbols import symbol_to_parts, symbol_to_pair
from crypto_screening.collect.foundation.exchanges import exchanges_data
from crypto_screening.collect.symbols import (
    all_exchange_symbols, exchange_symbols
)

__all__ = [
    "exchanges_assets",
    "mutual_exchanges_assets",
    "exchange_assets",
    "exchange_quote_assets",
    "exchange_base_assets",
    "all_exchange_assets",
    "all_exchange_base_assets",
    "all_exchange_quote_assets",
    "exchanges_base_assets",
    "exchanges_quote_assets",
    "mutual_exchanges_base_assets",
    "mutual_exchanges_quote_assets",
    "exchanges_symbols_assets",
    "exchanges_symbols_quote_assets",
    "exchanges_symbols_base_assets"
]

def all_exchange_assets(
        exchange: str,
        separator: str = None,
        adjust: bool = True
) -> set[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    symbols = all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    assets = set()

    for symbol in symbols:
        assets.update(symbol_to_parts(symbol=symbol, separator=separator))
    # end for

    return assets
# end all_exchange_assets

def all_exchange_base_assets(
        exchange: str,
        separator: str = None,
        adjust: bool = True,
) -> set[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    symbols = all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    assets = set()

    for symbol in symbols:
        base, _ = symbol_to_parts(symbol=symbol, separator=separator)

        assets.add(base)
    # end for

    return assets
# end all_exchange_base_assets

def all_exchange_quote_assets(
        exchange: str,
        separator: str = None,
        adjust: bool = True,
) -> set[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    symbols = all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    assets = set()

    for symbol in symbols:
        _, quote = symbol_to_parts(symbol=symbol, separator=separator)

        assets.add(quote)
    # end for

    return assets
# end all_exchange_quote_assets

def exchange_assets(
        exchange: str,
        separator: str = None,
        adjust: bool = True,
        bases: Iterable[str] = None,
        quotes: Iterable[str] = None,
        included: Iterable[str] = None,
        excluded: Iterable[str] = None
) -> set[str]:
    """
    Collects the assets from the exchanges.

    :param exchange: The name of the exchange.
    :param bases: The bases of the asset pairs.
    :param quotes: The quotes of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator for the symbols.
    :param included: The symbols to include.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = exchange_symbols(
        exchange=exchange, separator=separator, bases=bases,
        quotes=quotes, excluded=excluded, adjust=adjust, included=included
    )

    assets = set()

    for symbol in symbols:
        assets.update(symbol_to_parts(symbol=symbol, separator=separator))
    # end for

    return assets
# end exchange_assets

def exchange_base_assets(
        exchange: str,
        separator: str = None,
        adjust: bool = True,
        bases: Iterable[str] = None,
        quotes: Iterable[str] = None,
        included: Iterable[str] = None,
        excluded: Iterable[str] = None
) -> set[str]:
    """
    Collects the assets from the exchanges.

    :param exchange: The name of the exchange.
    :param bases: The bases of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param quotes: The quotes of the asset pairs.
    :param separator: The separator for the symbols.
    :param included: The symbols to include.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = exchange_symbols(
        exchange=exchange, separator=separator, bases=bases,
        quotes=quotes, excluded=excluded, adjust=adjust, included=included
    )

    assets = set()

    for symbol in symbols:
        base, _ = symbol_to_parts(symbol=symbol, separator=separator)

        assets.add(base)
    # end for

    return assets
# end exchange_assets

def exchange_quote_assets(
        exchange: str,
        separator: str = None,
        adjust: bool = True,
        bases: Iterable[str] = None,
        quotes: Iterable[str] = None,
        included: Iterable[str] = None,
        excluded: Iterable[str] = None
) -> set[str]:
    """
    Collects the assets from the exchanges.

    :param exchange: The name of the exchange.
    :param bases: The bases of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param quotes: The quotes of the asset pairs.
    :param separator: The separator for the symbols.
    :param included: The symbols to include.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = exchange_symbols(
        exchange=exchange, separator=separator, bases=bases,
        quotes=quotes, excluded=excluded, adjust=adjust, included=included
    )

    assets = set()

    for symbol in symbols:
        _, quote = symbol_to_parts(symbol=symbol, separator=separator)

        assets.add(quote)
    # end for

    return assets
# end exchange_assets

def exchanges_assets(
        exchanges: Iterable[str] = None,
        adjust: bool = True,
        separator: str = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    return exchanges_data(
        collector=exchange_assets,
        exchanges=exchanges, quotes=quotes, excluded=excluded,
        adjust=adjust, separator=separator, bases=bases, included=included
    )
# end exchanges_assets

def exchanges_base_assets(
        exchanges: Iterable[str] = None,
        adjust: bool = True,
        separator: str = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    return exchanges_data(
        collector=exchange_base_assets,
        exchanges=exchanges, quotes=quotes, excluded=excluded,
        adjust=adjust, separator=separator, bases=bases, included=included
    )
# end exchanges_assets

def exchanges_quote_assets(
        exchanges: Iterable[str] = None,
        adjust: bool = True,
        separator: str = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param included: The symbols to include.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    return exchanges_data(
        collector=exchange_quote_assets,
        exchanges=exchanges, quotes=quotes, excluded=excluded,
        adjust=adjust, separator=separator, bases=bases, included=included
    )
# end exchanges_quote_assets

def exchanges_symbols_assets(
        data: dict[str, Iterable[str]],
        separator: str = None
) -> dict[str, set[str]]:
    """
    Finds the currencies from the screeners.

    :param data: The data to process.
    :param separator: The separator of the assets.

    :return: The currencies from the screeners.
    """

    result = {}

    for exchange, symbols in data.items():
        result.setdefault(exchange, []).extend(symbols)
    # end for

    results = {}

    for exchange, symbols in result.items():
        assets = set()

        for symbol in set(symbols):
            assets.update(symbol_to_parts(symbol=symbol, separator=separator))
        # end for

        results.setdefault(exchange, assets)
    # end for

    return results
# end exchanges_symbols_assets

def exchanges_symbols_base_assets(
        data: dict[str, Iterable[str]],
        separator: str = None
) -> dict[str, set[str]]:
    """
    Finds the currencies from the screeners.

    :param data: The data to process.
    :param separator: The separator of the assets.

    :return: The currencies from the screeners.
    """

    result: dict[str, list[str]] = {}

    for exchange, symbols in data.items():
        result.setdefault(exchange, []).extend(symbols)
    # end for

    result: dict[str, set[str]] = {
        exchange: set(
            symbol_to_pair(symbol=symbol, separator=separator).base
            for symbol in set(symbols)
        ) for exchange, symbols in result.items()
    }

    return {exchange: assets for exchange, assets in result.items() if assets}
# end exchanges_symbols_base_assets

def exchanges_symbols_quote_assets(
        data: dict[str, Iterable[str]],
        separator: str = None
) -> dict[str, set[str]]:
    """
    Finds the currencies from the screeners.

    :param data: The data to process.
    :param separator: The separator of the assets.

    :return: The currencies from the screeners.
    """

    result: dict[str, list[str]] = {}

    for exchange, symbols in data.items():
        result.setdefault(exchange, []).extend(symbols)
    # end for

    result: dict[str, set[str]] = {
        exchange: set(
            symbol_to_pair(symbol=symbol, separator=separator).quote
            for symbol in set(symbols)
        ) for exchange, symbols in result.items()
    }

    return {exchange: assets for exchange, assets in result.items() if assets}
# end exchanges_symbols_quote_assets

def mutual_exchanges_assets(
        exchanges: Iterable[str] = None,
        adjust: bool = True,
        separator: str = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None,
        data: dict[str, Iterable[str]] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param data: The data to search in.
    :param included: The symbols to include.

    :return: The data of the exchanges.
    """

    return mutual_string_values(
        data=data or exchanges_assets(
            exchanges=exchanges, quotes=quotes, bases=bases, included=included,
            excluded=excluded, adjust=adjust, separator=separator
        )
    )
# end mutual_exchanges_assets

def mutual_exchanges_base_assets(
        exchanges: Iterable[str] = None,
        adjust: bool = True,
        separator: str = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None,
        data: dict[str, Iterable[str]] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param data: The data to search in.
    :param included: The symbols to include.

    :return: The data of the exchanges.
    """

    return mutual_string_values(
        data=data or exchanges_base_assets(
            exchanges=exchanges, quotes=quotes, bases=bases, included=included,
            excluded=excluded, adjust=adjust, separator=separator
        )
    )
# end mutual_exchanges_base_assets

def mutual_exchanges_quote_assets(
        exchanges: Iterable[str] = None,
        adjust: bool = True,
        separator: str = None,
        bases: dict[str, Iterable[str]] | Iterable[str] = None,
        quotes: dict[str, Iterable[str]] | Iterable[str] = None,
        included: dict[str, Iterable[str]] | Iterable[str] = None,
        excluded: dict[str, Iterable[str]] | Iterable[str] = None,
        data: dict[str, Iterable[str]] = None
) -> dict[str, set[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param data: The data to search in.
    :param included: The symbols to include.

    :return: The data of the exchanges.
    """

    return mutual_string_values(
        data=data or exchanges_quote_assets(
            exchanges=exchanges, quotes=quotes, bases=bases, included=included,
            excluded=excluded, adjust=adjust, separator=separator
        )
    )
# end mutual_exchanges_quote_assets