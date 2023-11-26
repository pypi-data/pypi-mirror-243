# sockets.py

import json
import time
import datetime as dt
from multiprocessing import Process
from typing import Iterable, Any

from looperator import Operator, Superator

from socketsio import Server, BHP, TCP, Client, find_available_port

from crypto_screening.screeners.container import ScreenersContainer
from crypto_screening.screeners.combined import (
    combined_market_screener, CategoryBase, Categories
)
from crypto_screening.screeners.orchestration.method import (
    OrchestrationMethod, split_screeners_data
)
from crypto_screening.screeners.collectors import (
    SocketScreenersDataCollector
)
from crypto_screening.screeners.callbacks import SocketCallback
from crypto_screening.screeners.orchestration.publisher import (
    DataPublisher
)
from crypto_screening.screeners.orchestration.controller import (
    DataPublisherController
)

__all__ = [
    "DataPublisherSocketClient",
    "DataPublisherSocketServer",
    "SocketOrchestrator",
    "create_run_data_publisher_socket_server",
    "data_publisher_socket_server",
    "create_screening_orchestration",
    "connect_screening_socket_orchestration",
    "connect_screening_socket_orchestrator",
    "create_screening_orchestrator"
]

class DataPublisherSocketClient(DataPublisherController):
    """A server to run the data publisher on."""

    def __init__(
            self,
            client: Client = None,
            process: Process = None
    ) -> None:
        """
        Defines the attributes of the controller client.

        :param client: The client object.
        :param process: The process to control.
        """

        super().__init__()

        self.client = client
        self.process = process
    # end __init__

    @property
    def controlling(self) -> bool:
        """
        Checks if the client is controlling the service.

        :return: The validation value.
        """

        return all(
            (
                self.process,
                self.process.is_alive(),
                self.client
            )
        )
    # end controlling
# end DataPublisherServer

class DataPublisherSocketServer(Superator):
    """A server to run the data publisher on."""

    def __init__(self, publisher: DataPublisher, server: Server) -> None:
        """
        Defines the attributes of the data publisher server.

        :param publisher: The data publisher object.
        :param server: The control server object.
        """

        self.publisher = publisher
        self.server = server

        self._operator = Operator(
            operation=lambda: (
                server.handle(
                    action=lambda connection, address, protocol: (
                        self.publisher.commit(
                            receive=lambda: (
                                json.loads(
                                    protocol.receive(
                                        connection=connection
                                    )[0].decode()
                                )
                            ),
                            send=lambda data: (
                                protocol.send(
                                    connection=connection,
                                    address=address,
                                    data=json.dumps(data).encode()
                                )
                            )
                        )
                    ), sequential=True
                )
            ),
            termination=lambda: (
                self.publisher.market.stop(),
                self.publisher.callback.stop()
            )
        )

        super().__init__(operators=[self._operator])
    # end __init__
# end DataPublisherServer

def create_run_data_publisher_socket_server(
        control_address: str,
        control_port: int,
        data_address: str,
        data_port: int,
        parameters: dict[str, Any],
        control: bool = False,
        run: bool = False
) -> None:
    """
    Creates the market screener object for the data.

    :param control_address: The address for the control server.
    :param control_port: The port for the control server.
    :param data_address: The address for the data server.
    :param data_port: The port for the data server.
    :param parameters: The parameters for the market screener.
    :param control: The value to control the process.
    :param run: The value to run the screening process.

    :return: The data publisher server object.
    """

    service = data_publisher_socket_server(
        control_address=control_address,
        control_port=control_port,
        data_address=data_address,
        data_port=data_port,
        parameters=parameters
    )

    if control:
        service.server.listen()
        service.run(block=False)
    # end if

    if (not control) or run:
        service.publisher.market.run(block=True, save=False)
    # end if
# end create_run_data_publisher_socket_server

def data_publisher_socket_server(
        control_address: str,
        control_port: int,
        data_address: str,
        data_port: int,
        parameters: dict[str, Any]
) -> DataPublisherSocketServer:
    """
    Creates the market screener object for the data.

    :param control_address: The address for the control server.
    :param control_port: The port for the control server.
    :param data_address: The address for the data server.
    :param data_port: The port for the data server.
    :param parameters: The parameters for the market screener.

    :return: The data publisher server object.
    """

    server = Server(BHP(TCP()))
    server.bind((control_address, control_port))

    callback = SocketCallback(address=data_address, port=data_port)

    market = combined_market_screener(**parameters, callbacks=[callback])

    publisher = DataPublisher(market=market, callback=callback)

    return DataPublisherSocketServer(publisher=publisher, server=server)
# end data_publisher_http_server

Data = dict[str, Iterable[str | dict[str, Iterable[str]]]]
Collectors = dict[
    SocketScreenersDataCollector,
    list[DataPublisherSocketClient]
]

def create_screening_orchestration(
        data: Data | dict[type[CategoryBase], Data],
        method: OrchestrationMethod,
        address: str = None,
        port: int = None,
        categories: type[CategoryBase] = None,
        cancel: float | dt.timedelta = None,
        delay: float | dt.timedelta = None,
        refresh: float | dt.timedelta | bool = None,
        location: str = None,
        limited: bool = None,
        amount: int = None,
        memory: int = None,
        control_address: str = None,
        control: bool = False,
        run: bool = False
) -> dict[SocketScreenersDataCollector, list[DataPublisherSocketClient]]:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param method: The orchestration method.
    :param categories: The categories for the markets.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param memory: The memory limitation of the market dataset.
    :param control_address: The address for the control server.
    :param address: The address for the data server.
    :param port: The port for the data server.
    :param control: The value to control the process.
    :param run: The value to run the screening process.

    :return: The data publisher server object.
    """

    screeners = combined_market_screener(
        data=data, location=location,
        memory=memory, categories=categories
    ).screeners

    if address is None:
        address = "127.0.0.1"
    # end if

    if port is None:
        port = find_available_port(address)
    # end if

    collector = SocketScreenersDataCollector(
        address=address, port=port, screeners=screeners
    )

    return connect_screening_socket_orchestration(
        collector=collector,
        method=method,
        cancel=cancel,
        delay=delay,
        limited=limited,
        amount=amount,
        refresh=refresh,
        address=control_address,
        control=control,
        run=run
    )
# end create

def connect_screening_socket_orchestration(
        collector: SocketScreenersDataCollector,
        method: OrchestrationMethod,
        address: str = None,
        cancel: float | dt.timedelta = None,
        delay: float | dt.timedelta = None,
        refresh: float | dt.timedelta | bool = None,
        limited: bool = None,
        amount: int = None,
        control: bool = False,
        run: bool = False
) -> dict[SocketScreenersDataCollector, list[DataPublisherSocketClient]]:
    """
    Creates the market screener object for the data.

    :param collector: The collector to create a process for.
    :param method: The orchestration method.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param address: The address for the control server.
    :param control: The value to control the process.
    :param run: The value to run the screening process.

    :return: The data publisher server object.
    """

    if address is None:
        address = "127.0.0.1"
    # end if

    data: dict[CategoryBase, dict[str, str | dict[str, Iterable[str]]]] = {}

    for category in Categories.categories:
        screeners = collector.find_screeners(base=category.screener)

        if screeners:
            container = ScreenersContainer(screeners=screeners)
            data[category] = (
                container.map()
                if container is Categories.ohlcv else
                container.structure()
            )
        # end if
    # end for

    processes = []

    create = lambda d, p: Process(
        target=create_run_data_publisher_socket_server,
        kwargs=dict(
            control_address=address,
            control_port=p,
            data_address=collector.address,
            data_port=collector.port,
            control=control,
            run=run,
            parameters=dict(
                data=d,
                cancel=cancel,
                delay=delay,
                limited=limited,
                amount=amount,
                memory=1,
                refresh=refresh
            )
        )
    )

    for data in split_screeners_data(container=collector, method=method):
        port = find_available_port(address)
        process = create(data, port)

        processes.append((process, port))

        process.start()
    # end for

    collectors = []

    for process, port in processes:
        client = None

        if control:
            client = Client(BHP(TCP()))

            count = 0

            while not client.connected:
                try:
                    client.connect((address, port))

                except ConnectionError as e:
                    if count == 5:
                        raise e
                    # end if

                    time.sleep(1)

                    count += 1
                # end try
            # end while
        # end if

        collectors.append(
            DataPublisherSocketClient(client=client, process=process)
        )
    # end for

    return {collector: collectors}
# end connect_screening_socket_orchestration

class SocketOrchestrator:
    """A class to represent an orchestrator of market screeners."""

    def __init__(self, collectors: Collectors = None) -> None:
        """
        Defines the connection attributes of the orchestrator.

        :param collectors: The collectors to run.
        """

        if collectors is None:
            collectors = {}
        # end if

        self.collectors: Collectors = collectors
    # end __init__

    def create(
            self,
            data: Data | dict[type[CategoryBase], Data],
            method: OrchestrationMethod,
            address: str = None,
            port: int = None,
            categories: type[CategoryBase] = None,
            cancel: float | dt.timedelta = None,
            delay: float | dt.timedelta = None,
            refresh: float | dt.timedelta | bool = None,
            location: str = None,
            limited: bool = None,
            amount: int = None,
            memory: int = None,
            control_address: str = None,
            control: bool = False,
            run: bool = False
    ) -> dict[SocketScreenersDataCollector, list[DataPublisherSocketClient]]:
        """
        Creates the market screener object for the data.

        :param data: The market data.
        :param method: The orchestration method.
        :param categories: The categories for the markets.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param amount: The maximum amount of symbols for each feed.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param memory: The memory limitation of the market dataset.
        :param control_address: The address for the control server.
        :param address: The address for the data server.
        :param port: The port for the data server.
        :param control: The value to control the process.
        :param run: The value to run the screening process.

        :return: The data publisher server object.
        """

        controllers = create_screening_orchestration(
            data=data,
            categories=categories,
            memory=memory,
            location=location,
            port=port,
            address=address,
            method=method,
            cancel=cancel,
            delay=delay,
            limited=limited,
            amount=amount,
            refresh=refresh,
            control_address=control_address,
            control=control,
            run=run
        )

        self.collectors.update(controllers)

        return controllers
    # end create

    def connect(
            self,
            collector: SocketScreenersDataCollector,
            method: OrchestrationMethod,
            address: str = None,
            cancel: float | dt.timedelta = None,
            delay: float | dt.timedelta = None,
            refresh: float | dt.timedelta | bool = None,
            limited: bool = None,
            amount: int = None,
            control: bool = False,
            run: bool = False
    ) -> dict[SocketScreenersDataCollector, list[DataPublisherSocketClient]]:
        """
        Creates the market screener object for the data.

        :param collector: The collector to create a process for.
        :param method: The orchestration method.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param amount: The maximum amount of symbols for each feed.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param address: The address for the control server.
        :param control: The value to control the process.
        :param run: The value to run the screening process.

        :return: The data publisher server object.
        """

        controllers = connect_screening_socket_orchestration(
            collector=collector,
            method=method,
            cancel=cancel,
            delay=delay,
            limited=limited,
            amount=amount,
            refresh=refresh,
            address=address,
            control=control,
            run=run
        )

        self.collectors.update(controllers)

        return controllers
    # end connect

    def start_screening(self) -> None:
        """Starts collecting the data."""

        for controllers in self.collectors.values():
            for controller in controllers:
                if controller.controlling:
                    controller.client.send(controller.run())
                    controller.receive(controller.client.receive()[0])
                # end if
            # end for
        # end for
    # end start_screening

    def stop_screening(self) -> None:
        """Starts collecting the data."""

        for controllers in self.collectors.values():
            for controller in controllers:
                if controller.controlling:
                    controller.client.send(controller.stop())
                # end if
            # end for
        # end for
    # end stop_screening

    def terminate(self) -> None:
        """Starts collecting the data."""

        self.stop_screening()

        for controllers in self.collectors.values():
            for controller in controllers:
                if controller.process:
                    controller.process.terminate()
                # end if
            # end for
        # end for
    # end terminate

    def start_collecting(self) -> None:
        """Starts collecting the data."""

        for collector in self.collectors:
            if not collector.screening:
                collector.start_screening()
            # end if
        # end for
    # end start_collecting

    def stop_collecting(self) -> None:
        """Starts collecting the data."""

        for collector in self.collectors:
            if not collector.screening:
                collector.stop_screening()
            # end if
        # end for
    # end stop_collecting
# end SocketOrchestrator

def create_screening_orchestrator(
        data: Data | dict[type[CategoryBase], Data],
        method: OrchestrationMethod,
        address: str = None,
        port: int = None,
        categories: type[CategoryBase] = None,
        cancel: float | dt.timedelta = None,
        delay: float | dt.timedelta = None,
        refresh: float | dt.timedelta | bool = None,
        location: str = None,
        limited: bool = None,
        amount: int = None,
        memory: int = None,
        control_address: str = None,
        control: bool = False,
        run: bool = False
) -> SocketOrchestrator:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param method: The orchestration method.
    :param categories: The categories for the markets.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param memory: The memory limitation of the market dataset.
    :param control_address: The address for the control server.
    :param address: The address for the data server.
    :param port: The port for the data server.
    :param control: The value to control the process.
    :param run: The value to run the screening process.

    :return: The data publisher server object.
    """

    return SocketOrchestrator(
        create_screening_orchestration(
            data=data,
            categories=categories,
            memory=memory,
            location=location,
            port=port,
            address=address,
            method=method,
            cancel=cancel,
            delay=delay,
            limited=limited,
            amount=amount,
            refresh=refresh,
            control_address=control_address,
            control=control,
            run=run
        )
    )
# end create_screening_http_orchestrator

def connect_screening_socket_orchestrator(
        collector: SocketScreenersDataCollector,
        method: OrchestrationMethod,
        address: str = None,
        cancel: float | dt.timedelta = None,
        delay: float | dt.timedelta = None,
        refresh: float | dt.timedelta | bool = None,
        limited: bool = None,
        amount: int = None,
        control: bool = False,
        run: bool = False
) -> SocketOrchestrator:
    """
    Creates the market screener object for the data.

    :param collector: The collector to create a process for.
    :param method: The orchestration method.
    :param limited: The value to limit the screeners to active only.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.
    :param address: The address for the control server.
    :param control: The value to control the process.
    :param run: The value to run the screening process.

    :return: The data publisher server object.
    """

    return SocketOrchestrator(
        connect_screening_socket_orchestration(
            collector=collector,
            method=method,
            cancel=cancel,
            delay=delay,
            limited=limited,
            amount=amount,
            refresh=refresh,
            address=address,
            control=control,
            run=run
        )
    )
# end connect_screening_socket_orchestrator