'''
Created on 2 сент. 2016 г.

@author: garet
'''

from contextlib import suppress
from io import BytesIO
import asyncio as aio
#import aiohttp
import pycurl
import atexit


# Curl event loop:
class CurlLoop:
    class Error(Exception): pass

    _multi = pycurl.CurlMulti()
    atexit.register(_multi.close)
    _futures = {}

    @classmethod
    async def handler_ready(cls, ch):
        cls._futures[ch] = aio.Future()
        cls._multi.add_handle(ch)
        try:
            return await cls._futures[ch]
        finally:
            cls._multi.remove_handle(ch)

    @classmethod
    def perform(cls):
        if cls._futures:
            status, num_active = cls._multi.perform()
            _, success, fail = cls._multi.info_read()
            for ch in success:
                cls._futures.pop(ch).set_result('')
            for ch, err_num, err_msg in fail:
                cls._futures.pop(ch).set_exception(CurlLoop.Error(err_msg))
"""
    @classmethod
    def perform(cls):
        if cls._futures:
            while True:
                status, num_active = cls._multi.perform()
                if status != pycurl.E_CALL_MULTI_PERFORM:
                    break
            while True:
                num_ready, success, fail = cls._multi.info_read()
                for ch in success:
                    cls._futures.pop(ch).set_result('')
                for ch, err_num, err_msg in fail:
                    cls._futures.pop(ch).set_exception(CurlLoop.Error(err_msg))
                if num_ready == 0:
                    break
"""

# Single curl request:
async def request(url, timeout=5):
    ch = pycurl.Curl()
    try:
        ch.setopt(pycurl.URL, url.encode('utf-8'))
        ch.setopt(pycurl.FOLLOWLOCATION, 1)
        ch.setopt(pycurl.MAXREDIRS, 5)

        raw_text_buf = BytesIO()
        ch.setopt(pycurl.WRITEFUNCTION, raw_text_buf.write)

        with Timeout(timeout):
            await CurlLoop.handler_ready(ch)
            return raw_text_buf.getvalue().decode('utf-8', 'ignore')
    finally:
        ch.close()


# Asyncio event loop + CurlLoop:
def run_until_complete(coro):
    async def main_task():
        pycurl_task = aio.ensure_future(_pycurl_loop())
        try:
            await coro
        finally:
            pycurl_task.cancel()
            with suppress(aio.CancelledError):
                await pycurl_task
    # Run asyncio event loop:
    loop = aio.get_event_loop()
    loop.run_until_complete(main_task())


async def _pycurl_loop():
    while True:
        await aio.sleep(0)
        CurlLoop.perform()

# Test it:
async def main():
    #url = 'http://httpbin.org/delay/0'
    url = 'https://habrahabr.ru/post/282972/'
    res = await aio.gather(
        request(url),
        request(url),
        request(url),
        request(url),
        request(url),
    )
    print(len(res[0]))  # to see result

class Timeout:
    """Timeout context manager.
    Useful in cases when you want to apply timeout logic around block
    of code or in cases when asyncio.wait_for is not suitable. For example:
    >>> with aiohttp.Timeout(0.001):
    ...     async with aiohttp.get('https://github.com') as r:
    ...         await r.text()
    :param timeout: timeout value in seconds or None to disable timeout logic
    :param loop: asyncio compatible event loop
    """
    def __init__(self, timeout, *, loop=None):
        self._timeout = timeout
        if loop is None:
            loop = aio.get_event_loop()
        self._loop = loop
        self._task = None
        self._cancelled = False
        self._cancel_handler = None

    def __enter__(self):
        self._task = aio.Task.current_task(loop=self._loop)
        if self._task is None:
            raise RuntimeError('Timeout context manager should be used '
                               'inside a task')
        if self._timeout is not None:
            self._cancel_handler = self._loop.call_later(
                self._timeout, self._cancel_task)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is aio.CancelledError and self._cancelled:
            self._cancel_handler = None
            self._task = None
            raise aio.TimeoutError from None
        if self._timeout is not None:
            self._cancel_handler.cancel()
            self._cancel_handler = None
        self._task = None

    def _cancel_task(self):
        self._cancelled = self._task.cancel()



if __name__ == "__main__":
    run_until_complete(main())