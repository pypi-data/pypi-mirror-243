import asyncio
import sys
import unittest.mock as mock

import pytest
from httpx import ConnectError

from yatbaf import LongPolling
from yatbaf.exceptions import RequestTimeoutError

MODULE = "yatbaf.long_polling"
module_obj = sys.modules[MODULE]


@pytest.fixture
def asyncio_mock():
    asyncio_module = mock.Mock()
    asyncio_module.gather = mock.AsyncMock()
    asyncio_module.sleep = mock.AsyncMock()
    asyncio_module.wait_for = mock.AsyncMock()
    return asyncio_module


@pytest.fixture(autouse=True)
def __mock(monkeypatch, asyncio_mock):
    monkeypatch.setattr(module_obj, "asyncio", asyncio_mock)


@pytest.fixture
def bot_mock():
    bot = mock.AsyncMock()
    bot.tasks = mock.AsyncMock()
    bot.tasks.add = mock.Mock()
    bot.tasks._create_task = mock.Mock()
    bot._api_client = mock.Mock()
    bot._api_client.invoke = mock.AsyncMock()
    bot._api_client.close = mock.AsyncMock()
    return bot


@pytest.mark.asyncio
async def test_startup_running(asyncio_mock):
    polling = LongPolling(None)
    polling._running = True

    await polling._startup()
    asyncio_mock.get_running_loop.assert_not_called()


@pytest.mark.asyncio
async def test_startup(asyncio_mock):
    polling = LongPolling(None)
    asyncio_mock.get_running_loop.return_value = loop = mock.Mock()

    await polling._startup()
    polling._event.clear.assert_called_once()
    asyncio_mock.get_running_loop.assert_called_once()
    loop.add_signal_handler.assert_any_call(mock.ANY, polling.stop)
    assert polling._running


@pytest.mark.asyncio
async def test_startup_func(asyncio_mock, bot_mock):
    polling = LongPolling(
        bot_mock, on_startup=[
            mock.AsyncMock(),
            mock.AsyncMock(),
        ]
    )
    asyncio_mock.get_running_loop.return_value = mock.Mock()
    await polling._startup()
    for func in polling._on_startup:
        func.assert_awaited_once_with(bot_mock)


@pytest.mark.asyncio
async def test_startup_func_error(asyncio_mock, bot_mock):
    polling = LongPolling(
        bot_mock, on_startup=[
            mock.AsyncMock(side_effect=ValueError()),
        ]
    )
    with pytest.raises(ValueError):
        await polling._startup()
    assert not polling._running
    asyncio_mock.get_running_loop.assert_not_called()


@pytest.mark.asyncio
async def test_shutdown_not_running(bot_mock):
    polling = LongPolling(bot_mock)
    polling._running = False
    await polling._shutdown()
    bot_mock.shutdown.assert_not_awaited()
    bot_mock.tasks.wait_all.assert_not_awaited()


@pytest.mark.asyncio
async def test_shutdown_func(bot_mock):
    polling = LongPolling(
        bot_mock, on_shutdown=[
            mock.AsyncMock(),
            mock.AsyncMock(),
        ]
    )
    polling._running = True

    await polling._shutdown()
    bot_mock.tasks.wait_all.assert_awaited_once()
    bot_mock.shutdown.assert_awaited_once()
    for func in polling._on_shutdown:
        func.assert_awaited_once_with(bot_mock)


@pytest.mark.asyncio
async def test_shutdown_func_error(bot_mock):
    polling = LongPolling(
        bot_mock, on_shutdown=[
            mock.AsyncMock(side_effect=ValueError()),
        ]
    )
    polling._running = True
    with pytest.raises(ValueError):
        await polling._shutdown()
    bot_mock.shutdown.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_updates_params(bot_mock):
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.return_value = result
    queue = mock.Mock()

    await polling._get_updates(queue)
    queue.put_nowait.assert_not_called()
    bot_mock._api_client.invoke.assert_awaited_once_with(
        polling._method,
        timeout=(polling._method.timeout + 5),
    )


@pytest.mark.asyncio
async def test_get_updates(bot_mock):
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.return_value = result
    queue = mock.Mock()

    await polling._get_updates(queue)
    queue.put_nowait.assert_not_called()
    bot_mock._api_client.invoke.assert_awaited()
    assert bot_mock._api_client.invoke.call_count == 2


@pytest.mark.asyncio
async def test_get_updates_queue(bot_mock, update):
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, True]
    result = mock.Mock(result=[object(), update])
    bot_mock._api_client.invoke.return_value = result
    queue = mock.Mock()

    await polling._get_updates(queue)
    queue.put_nowait.assert_called_once_with(result.result)
    bot_mock._api_client.invoke.assert_awaited_once()
    assert polling._method.offset == update.update_id + 1
    assert bot_mock._api_client.invoke.call_count == 1


@pytest.mark.asyncio
async def test_get_updates_timeout_error(bot_mock, asyncio_mock):
    bot_mock._error_handler = error_handler = mock.AsyncMock()
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.side_effect = [
        result, RequestTimeoutError("", None), result
    ]
    queue = mock.Mock()

    await polling._get_updates(queue)
    error_handler.on_error.assert_not_awaited()
    asyncio_mock.sleep.assert_awaited_once_with(polling._timeout_delay)
    assert bot_mock._api_client.invoke.call_count == 2


@pytest.mark.asyncio
async def test_get_updates_connection_error(bot_mock, asyncio_mock):
    bot_mock._error_handler = error_handler = mock.AsyncMock()
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, False, True]
    result = mock.Mock(result=[])
    bot_mock._api_client.invoke.side_effect = [result, ConnectError(""), result]
    queue = mock.Mock()

    await polling._get_updates(queue)
    error_handler.on_error.assert_not_awaited()
    asyncio_mock.sleep.assert_awaited_once_with(polling._connection_delay)
    assert bot_mock._api_client.invoke.call_count == 2


@pytest.mark.asyncio
async def test_get_updates_error(bot_mock):
    bot_mock._error_handler = error_handler = mock.AsyncMock()
    polling = LongPolling(bot_mock)
    polling._event = asyncio.Event()
    bot_mock._api_client.invoke.side_effect = exc = ValueError()
    queue = mock.Mock()
    await polling._get_updates(queue)
    error_handler.on_error.assert_awaited_once_with(exc)


@pytest.mark.asyncio
async def test_main_loop(monkeypatch, bot_mock, asyncio_mock, update):
    bot_mock.process_update = mock.Mock(
        return_value=(process_update_coro := object())
    )
    asyncio_mock.Queue.return_value = queue = mock.Mock()
    asyncio_mock.wait_for.return_value = [update]
    queue.get.return_value = get_coro = object()

    monkeypatch.setattr(
        LongPolling,
        "_get_updates",
        get_updates := mock.Mock(return_value=(updates_coro := object()))
    )
    asyncio_mock.create_task.side_effect = [updates_task := mock.Mock()]
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, True]

    await polling._main_loop()

    get_updates.assert_called_once_with(queue)
    asyncio_mock.create_task.assert_any_call(updates_coro)
    bot_mock.tasks._create_task.assert_any_call(
        process_update_coro,
        name=f"update-task-{update.update_id}",
    )
    bot_mock.process_update.assert_called_once_with(update)
    asyncio_mock.wait_for.assert_awaited_once_with(get_coro, 0.2)
    bot_mock.tasks.kill.assert_awaited_once_with(updates_task)


@pytest.mark.asyncio
async def test_main_loop_timeout(monkeypatch, bot_mock, asyncio_mock):
    bot_mock.process_update = mock.Mock(return_value=object())
    asyncio_mock.Queue.return_value = mock.Mock()
    asyncio_mock.wait_for.side_effect = TimeoutError()

    monkeypatch.setattr(LongPolling, "_get_updates", mock.Mock())
    asyncio_mock.create_task.return_value = updates_task = mock.Mock()
    polling = LongPolling(bot_mock)
    polling._event.is_set.side_effect = [False, False, True]

    await polling._main_loop()

    assert asyncio_mock.create_task.call_count == 1
    assert asyncio_mock.wait_for.call_count == 2
    bot_mock.task._create_task.assert_not_called()
    bot_mock.process_update.assert_not_called()
    bot_mock.tasks.kill.assert_awaited_once_with(updates_task)


@pytest.mark.asyncio
async def test_run(monkeypatch):
    monkeypatch.setattr(LongPolling, "_startup", startup := mock.AsyncMock())
    monkeypatch.setattr(LongPolling, "_main_loop", loop := mock.AsyncMock())
    monkeypatch.setattr(LongPolling, "_shutdown", shutdown := mock.AsyncMock())

    polling = LongPolling(None)
    await polling._run()
    startup.assert_awaited_once()
    loop.assert_awaited_once()
    shutdown.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_startup_error(monkeypatch):
    monkeypatch.setattr(
        LongPolling,
        "_startup",
        startup := mock.AsyncMock(side_effect=ValueError())
    )
    monkeypatch.setattr(LongPolling, "_main_loop", loop := mock.AsyncMock())
    monkeypatch.setattr(LongPolling, "_shutdown", shutdown := mock.AsyncMock())

    polling = LongPolling(None)
    await polling._run()
    assert not polling._running
    startup.assert_awaited_once()
    loop.assert_not_awaited()
    shutdown.assert_not_awaited()


def test_start(monkeypatch, asyncio_mock):
    monkeypatch.setattr(
        LongPolling,
        "_run",
        mock.Mock(return_value=(coro := mock.Mock())),
    )
    LongPolling(None).start()
    asyncio_mock.run.assert_called_once_with(coro)


def test_stop():
    polling = LongPolling(None)
    polling.stop()
    polling._event.set.assert_called_once()
