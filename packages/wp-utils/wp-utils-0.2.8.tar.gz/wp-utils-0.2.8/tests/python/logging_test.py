import pytest
from utils import Logger, LoggerType


def test_init_release() -> None:
    # Should be able to initialize without exceptions thrown
    Logger.Init()
    # The logger should be READY by now
    assert Logger.GetInstance().ready == True
    # By default, the logger is initialized to console-logger
    assert Logger.GetInstance().type == LoggerType.CONSOLE_LOGGER
    # Should be able to log some messages to the console
    Logger.CoreTrace("Just a simple core TRACE log")
    Logger.CoreInfo("Just a simple core INFO log")
    Logger.CoreWarn("Just a simple core WARN log")
    Logger.CoreError("Just a simple core ERROR log")
    Logger.CoreAssert(2 + 2 == 4, "Just a simple core ASSERT statement")

    Logger.Trace("Just a simple client TRACE log")
    Logger.Info("Just a simple client INFO log")
    Logger.Warn("Just a simple client WARN log")
    Logger.Error("Just a simple client ERROR log")
    Logger.Assert(1 + 3 == 4, "Just a simple client ASSERT statement")
    # Should be able to release without exceptions being thrown
    Logger.Release()

    # Should be able to initialize again; will create new spdloggers internally
    Logger.Init(LoggerType.FILE_LOGGER)
    # The logger should be READY by now
    assert Logger.GetInstance().ready == True
    # The logger should be initialized to file-logger
    assert Logger.GetInstance().type == LoggerType.FILE_LOGGER
    # Should be able to log to a file
    Logger.CoreTrace("Just a simple core TRACE log")
    Logger.CoreInfo("Just a simple core INFO log")
    Logger.CoreWarn("Just a simple core WARN log")
    Logger.CoreError("Just a simple core ERROR log")
    Logger.CoreAssert(2 + 2 == 4, "Just a simple core ASSERT statement")

    Logger.Trace("Just a simple client TRACE log")
    Logger.Info("Just a simple client INFO log")
    Logger.Warn("Just a simple client WARN log")
    Logger.Error("Just a simple client ERROR log")
    Logger.Assert(1 + 3 == 4, "Just a simple client ASSERT statement")
    # Should be able to release without exceptions being thrown
    Logger.Release()


def test_auto_initialization() -> None:
    # Should be fine to call the logger directly. If no instance, it should be
    # created on the fly to allow the log call to work
    Logger.CoreTrace("Should be able to log directly. Creates a console logger")
    assert Logger.GetInstance().ready == True
    assert Logger.GetInstance().type == LoggerType.CONSOLE_LOGGER
    Logger.Release()
