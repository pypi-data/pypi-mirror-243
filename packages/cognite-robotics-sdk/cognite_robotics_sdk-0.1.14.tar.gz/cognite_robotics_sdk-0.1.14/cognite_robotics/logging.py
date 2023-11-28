# -*- coding: utf-8 -*-
"""cognite logging."""
import asyncio
import logging
import logging.handlers
import threading
import time
import typing
from collections.abc import Callable

from cognite_robotics.protos.messages import robot_state_pb2
from cognite_robotics.protos.messages.robot_state_pb2 import LogMessage, LogSeverity, RobotState, RobotStateMessage

_baseLogger = logging.getLogger("cognite")

_Level = typing.Union[int, str]

_fileHandler = logging.handlers.RotatingFileHandler("./device-agent.log", maxBytes=(1024**3) // 2, backupCount=5)


def setCommonLevel(level: _Level = logging.CRITICAL) -> None:
    """setCommandLevel."""
    logging.getLogger().setLevel(level)


def setLevel(level: _Level = logging.INFO) -> None:
    """setLevel."""
    _baseLogger.setLevel(level)


def getLogger(name: str) -> logging.Logger:
    """getLogger."""
    return _baseLogger.getChild(name)


# Todo set format for handler
def setupRobotLogLogger(queue: asyncio.Queue[RobotStateMessage]) -> logging.Handler:
    """setupRobotLogLogger."""
    return enableRoboticsServicesLogHandler(getRobotLogLogger())(queue)


def getRobotLogLogger(name: typing.Optional[str] = None) -> logging.Logger:
    """getRobotLogLogger."""
    logger = getLogger(
        "inrobot",
    )
    if name is not None:
        logger = logger.getChild(name)
    return logger


def enableFileLogging() -> logging.Handler:
    """enableFileLogging."""
    _baseLogger.addHandler(_fileHandler)
    return _fileHandler


# Todo: Handle logging shutdown and shutdown signal
# Note: the logging task in main should shut down last to prevent logs from being lost


class RoboticsServicesLogHandler(logging.Handler):
    """RoboticsServicesLogHandler."""

    def __init__(self, queue: asyncio.Queue[RobotStateMessage], level: _Level = logging.NOTSET):
        """__init__."""
        super().__init__(level)
        self.records: typing.List[logging.LogRecord] = []
        self._handle: typing.Optional[asyncio.Handle] = None
        self._lock = threading.Lock()
        self._task: typing.Optional[asyncio.Task[None]] = None
        self._dead = False
        self.queue = queue

    async def _asyncFlush(self, records: typing.List[logging.LogRecord], ptask: typing.Optional[asyncio.Task[None]]) -> None:
        """_asyncFlush."""
        if ptask is not None:
            await ptask
        for record in records:
            await createRobotLog(self.format(record), logLevelToSeverity(record.levelno), self.queue)

    def close(self) -> None:
        """
        close handle, no further logging can happen.

        https://docs.python.org/3/library/logging.html#logging.Handler.close
        """
        super().close()
        self._dead = True

    def flush(self) -> None:
        """
        flush logs, spawn an asyncio task which will push the logs to the handle's provided queue.

        https://docs.python.org/3/library/logging.html#logging.Handler.flush
        """
        if self._dead:
            return
        with self._lock:
            try:
                # call to create_task will raise a RuntimeError if flush is called outside of the asyncio thread
                # (the logging module will call flush 'on cleanup')
                # resulting in a dangling coroutine that is never awaited (self._asyncFlush)
                # calling get_running_loop prior to create_task will result in an RuntimeError before a coroutine for ._asyncFlush
                # has been created
                asyncio.get_running_loop()
                self._task = asyncio.create_task(self._asyncFlush(list(self.records), self._task), name="robotics-log-handler-flush")
                self.records.clear()
                self._handle = None
            except RuntimeError as e:
                self._dead = True
                logging.getLogger().exception("RuntimeError while flushing robotics services log handler", exc_info=e)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Handle a log message, called on logger.info, logger.error, etc.

        https://docs.python.org/3/library/logging.html#logging.Handler.emit
        """
        with self._lock:
            self.records.append(record)
            if self._handle is not None:
                self._handle.cancel()
            try:
                loop = asyncio.get_event_loop()
                self._handle = loop.call_soon_threadsafe(self.flush)
            except RuntimeError as e:
                logging.getLogger().exception("Logger used outside of asyncio", exc_info=e)


def logLevelToSeverity(level: int) -> robot_state_pb2.LogSeverity.ValueType:
    """logLevelToSeverity."""
    if level <= logging.DEBUG:  # 10
        return LogSeverity.DEBUG
    if level <= logging.INFO:  # 20
        return LogSeverity.INFO
    if level <= logging.WARNING:  # 30
        return LogSeverity.WARNING
    if level <= logging.CRITICAL:  # 50 (logging.ERROR = 40)
        return LogSeverity.ERROR

    return LogSeverity.UNKNOWN


async def createRobotLog(
    message: str, severity: robot_state_pb2.LogSeverity.ValueType, robot_status_queue: asyncio.Queue[robot_state_pb2.RobotStateMessage]
) -> None:
    """
    Log a log message and send it as a robot status.

    Args:
    ----
        message: (str) log message to send
        severity: (robot_state_pb2.LogSeverity) severity of the log message
        robot_status_queue: asyncio.Queue[robot_state_pb2.RobotStateMessage] queue of messages to be sent
    """
    log_message = LogMessage(severity=severity, message=message)
    log_message_state_message = RobotState(log_message=log_message)
    log_message_robot_status_message = RobotStateMessage(ping_sent=int(time.time() * 1000))
    log_message_robot_status_message.robot_state.CopyFrom(log_message_state_message)
    await robot_status_queue.put(log_message_robot_status_message)


def enableRoboticsServicesLogHandler(logger: logging.Logger) -> Callable[[asyncio.Queue[RobotStateMessage]], RoboticsServicesLogHandler]:
    """enableRoboticsServicesLogHandler."""
    _handler: typing.Optional[logging.Handler] = None

    def _inner(queue: asyncio.Queue[RobotStateMessage]) -> RoboticsServicesLogHandler:
        nonlocal _handler
        if _handler is not None:
            logger.removeHandler(_handler)
        _handler = RoboticsServicesLogHandler(queue)
        logger.addHandler(_handler)
        return _handler

    return _inner
