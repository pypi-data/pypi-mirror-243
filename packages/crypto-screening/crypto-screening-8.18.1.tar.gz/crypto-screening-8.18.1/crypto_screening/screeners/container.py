# container.py

from crypto_screening.screeners.screener import (
    OHLCVScreener, OrderbookScreener, TradesScreener, TickersScreener
)
from crypto_screening.foundation.container import (
    BaseFrozenScreenersContainer, BaseScreenersContainer
)

__all__ = [
    "FrozenScreenersContainer",
    "ScreenersContainer"
]

class FrozenScreenersContainer(BaseFrozenScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects to form a market.

    >>> from crypto_screening.screeners.container import FrozenScreenersContainer
    >>> from crypto_screening.screeners import BaseScreener
    >>>
    >>> container = FrozenScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """

    @property
    def orderbook_screeners(self) -> list[OrderbookScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return self.find_screeners(base=OrderbookScreener)
    # end orderbook_screeners

    @property
    def tickers_screeners(self) -> list[TickersScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The orders screeners.
        """

        return self.find_screeners(base=TickersScreener)
    # end tickers_screeners

    @property
    def ohlcv_screeners(self) -> list[OHLCVScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The OHLCV screeners.
        """

        return self.find_screeners(base=OHLCVScreener)
    # end ohlcv_screeners

    @property
    def trades_screeners(self) -> list[TradesScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The trades screeners.
        """

        return self.find_screeners(base=TradesScreener)
    # end trades_screeners

    def orderbook_screener_in_market(self, exchange: str = None, symbol: str = None) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=OrderbookScreener
        )
    # end orderbook_screener_in_market

    def tickers_screener_in_market(self, exchange: str = None, symbol: str = None) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=TickersScreener
        )
    # end tickers_screener_in_market

    def find_orderbook_screener(
            self,
            exchange: str = None,
            symbol: str = None,
            index: int = None
    ) -> OrderbookScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param index: The index of the screener in the list.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol,
            base=OrderbookScreener, index=index
        )
    # end find_orderbook_screener

    def find_tickers_screener(
            self,
            exchange: str = None,
            symbol: str = None,
            index: int = None
    ) -> TickersScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param index: The index of the screener in the list.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol,
            base=TickersScreener, index=index
        )
    # end find_tickers_screener

    def find_orderbook_screeners(
            self,
            exchange: str = None,
            symbol: str = None,
            adjust: bool = True
    ) -> list[OrderbookScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol,
            base=OrderbookScreener, adjust=adjust
        )
    # end find_orderbook_screener

    def find_tickers_screeners(
            self,
            exchange: str = None,
            symbol: str = None,
            adjust: bool = True
    ) -> list[TickersScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol,
            base=TickersScreener, adjust=adjust
        )
    # end find_tickers_screeners

    def ohlcv_screener_in_market(
            self,
            exchange: str = None,
            symbol: str = None,
            interval: str = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the dataset.

        :return: The data.
        """

        try:
            self.find_ohlcv_screener(
                exchange=exchange, symbol=symbol, interval=interval
            )

            return True

        except ValueError:
            return False
    # end ohlcv_screener_in_market

    def trades_screener_in_market(self, exchange: str = None, symbol: str = None) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=TradesScreener
        )
    # end trades_screener_in_market

    def find_ohlcv_screener(
            self,
            exchange: str = None,
            symbol: str = None,
            interval: str = None,
            index: int = None
    ) -> OHLCVScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the dataset.
        :param index: The index for the screener.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol, base=OHLCVScreener,
            interval=interval, index=index
        )
    # end find_screeners

    def find_trades_screener(
            self,
            exchange: str = None,
            symbol: str = None,
            index: int = None
    ) -> TradesScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param index: The index for the screener.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol, base=TradesScreener,
            index=index
        )
    # end find_trades_screener

    def find_ohlcv_screeners(
            self,
            exchange: str = None,
            symbol: str = None,
            interval: str = None,
            adjust: bool = True
    ) -> list[OHLCVScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param interval: The interval for the datasets.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=OHLCVScreener,
            interval=interval, adjust=adjust
        )
    # end find_ohlcv_screeners

    def find_trades_screeners(
            self,
            exchange: str = None,
            symbol: str = None,
            adjust: bool = True
    ) -> list[TradesScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The symbol name.
        :param adjust: The value to adjust for the screeners.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=TradesScreener,
            adjust=adjust
        )
    # end find_trades_screeners
# end FrozenScreenersContainer

class ScreenersContainer(BaseScreenersContainer, FrozenScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects to form a market.

    >>> from crypto_screening.screeners.container import ScreenersContainer
    >>> from crypto_screening.screeners import BaseScreener
    >>>
    >>> container = ScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    """
# end ScreenersContainer