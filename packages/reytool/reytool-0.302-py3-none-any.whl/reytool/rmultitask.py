# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-19 20:06:20
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Multi task methods.
"""


from __future__ import annotations
from typing import Any, List, Tuple, Dict, Optional, Literal, Iterable, Callable, Generator, Coroutine, Union
from threading import RLock as TRLock, get_ident as threading_get_ident
from concurrent.futures import ThreadPoolExecutor, Future as CFuture, as_completed as concurrent_as_completed
from asyncio import run as asyncio_run, gather as asyncio_gather, Future as AFuture, iscoroutine
from aiohttp import ClientSession, ClientResponse

from .rsystem import check_most_one, check_response_code


__all__ = (
    "RThreadPool",
    "RLock",
    "sync_run",
    "sync_request"
)


class RThreadPool(object):
    """
    Rey's `thread pool` type.
    """


    def __init__(
        self,
        func: Callable,
        *args: Any,
        _max_workers: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Build `thread pool` instance.

        Parameters
        ----------
        func : Thread task.
        args : Task default arguments.
        max_workers: Maximum number of threads.
            - `None` : Number of CPU + 4, 32 maximum.
            - `int` : Use this value, no maximum limit.

        kwargs : Task default keyword arguments.
        """

        # Set attribute.
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread_pool = ThreadPoolExecutor(
            _max_workers,
            func.__name__
        )
        self.futures: List[CFuture] = []


    def one(
        self,
        *args: Any,
        **kwargs: Any
    ) -> CFuture:
        """
        Add and start a task to the thread pool.

        Parameters
        ----------
        args : Task arguments, after default arguments.
        kwargs : Task keyword arguments, after default keyword arguments.

        Returns
        -------
        Task instance.
        """

        # Set parameter.
        func_args = (
            *self.args,
            *args
        )
        func_kwargs = {
            **self.kwargs,
            **kwargs
        }

        # Submit.
        future = self.thread_pool.submit(
            self.func,
            *func_args,
            **func_kwargs
        )

        # Save.
        self.futures.append(future)

        return future


    def batch(
        self,
        *args: Tuple,
        **kwargs: Tuple
    ) -> List[CFuture]:
        """
        Add and start a batch of tasks to the thread pool.
        parameters sequence will combine one by one, and discard excess parameters.

        Parameters
        ----------
        args : Sequence of task arguments, after default arguments.
        kwargs : Sequence of task keyword arguments, after default keyword arguments.

        Returns
        -------
        Task instance list.

        Examples
        --------
        >>> func = lambda *args, **kwargs: print(args, kwargs)
        >>> a = (1, 2)
        >>> b = (3, 4, 5)
        >>> c = (11, 12)
        >>> d = (13, 14, 15)
        >>> thread_pool = RThreadPool(func, 0, z=0)
        >>> thread_pool.batch(a, b, c, d)
        (0, 1, 3) {'z': 0, 'c': 11, 'd': 13}
        (0, 2, 4) {'z': 0, 'c': 12, 'd': 14}
        """

        # Combine.
        args_zip = zip(*args)
        kwargs_zip = zip(
            *[
                [
                    (key, value)
                    for value in values
                ]
                for key, values in kwargs.items()
            ]
        )
        params_zip = zip(args_zip, kwargs_zip)

        # Batch submit.
        futures = [
            self.one(*args_, **dict(kwargs_))
            for args_, kwargs_ in params_zip
        ]

        # Save.
        self.futures.extend(futures)

        return futures


    def generate(
        self,
        timeout: Optional[float] = None
    ) -> Generator[CFuture]:
        """
        Return the generator of added task instance.

        Parameters
        ----------
        timeout : Call generator maximum waiting seconds, timeout throw exception.
            - `None` : Infinite.
            - `float` : Set this seconds.

        Returns
        -------
        Generator of added task instance.
        """

        # Build.
        generator = concurrent_as_completed(
            self.futures,
            timeout
        )

        return generator


    def repeat(
        self,
        number: int
    ) -> List[CFuture]:
        """
        Add and start a batch of tasks to the thread pool, and only with default parameters.

        Parameters
        ----------
        number : Number of add.

        Returns
        -------
        Task instance list.
        """

        # Batch submit.
        futures = [
            self.one()
            for n in range(number)
        ]

        # Save.
        self.futures.extend(futures)

        return futures


    __call__ = one


    __mul__ = repeat


class RLock():
    """
    Rey's `thread lock` type.
    """


    def __init__(self) -> None:
        """
        Build `thread lock` instance.
        """

        # Set attribute.
        self.lock = TRLock()
        self._occupy_thread_id: Optional[int] = None


    def acquire(
        self,
        timeout: float = None
    ) -> bool:
        """
        Wait and acquire thread lock.

        Parameters
        ----------
        timeout : Maximum wait seconds.
            - `None` : Not limit.
            - `float` : Use this value.

        Returns
        -------
        Whether acquire success.
        """

        # Handle parameter.
        if timeout is None:
            timeout = -1

        # Acquire.
        result = self.lock.acquire(timeout=timeout)

        # Update state.
        if result:
            thread_id = threading_get_ident()
            self._occupy_thread_id = thread_id

        return result


    def release(self) -> None:
        """
        Release thread lock.
        """

        # Release.
        self.lock.release()

        # Update state.
        self._occupy_thread_id = None


    def __call__(self) -> None:
        """
        Automatic judge, wait and acquire thread lock, or release thread lock.
        """

        # Release.
        thread_id = threading_get_ident()
        if thread_id == self._occupy_thread_id:
            self.release()

        # Acquire.
        else:
            self.acquire()


def sync_run(*coroutine: Coroutine) -> List:
    """
    Run `Coroutine` instances.

    Returns
    -------
    Run result list.
    """


    # Define.
    async def gather_coroutine() -> AFuture:
        """
        Get `Future` instance.

        Returns
        -------
        Future instance.
        """

        # Gather.
        future = await asyncio_gather(*coroutine)

        return future


    # Run.
    result = asyncio_run(gather_coroutine())

    return result


def sync_request(
    url: str,
    params: Optional[Dict] = None,
    data: Optional[Union[Dict, str, bytes]] = None,
    json: Optional[Dict] = None,
    headers: Dict[str, str] = {},
    timeout: Optional[float] = None,
    proxy: Optional[str] = None,
    method: Optional[Literal["get", "post", "put", "patch", "delete", "options", "head"]] = None,
    check: Union[bool, int, Iterable[int]] = False,
    receiver: Optional[Callable[[ClientResponse], Union[Coroutine, Any]]] = None
) -> Coroutine:
    """
    Get `Coroutine` instance of send request.

    Parameters
    ----------
    url : Request URL.
    params : Request URL add parameters.
    data : Request body data. Conflict with parameter `json`.
        - `Dict` : Convert to `key=value&...` format bytes.
            Automatic set `Content-Type` to `application/x-www-form-urlencoded`.
        - `Dict and a certain value is 'bytes' type` : Key is parameter name and file name, value is file data.
            Automatic set `Content-Type` to `multipart/form-data`.
        - `str` : File path to read file bytes data.
            Automatic set `Content-Type` to file media type, and `filename` to file name.
        - `bytes` : File bytes data.
            Automatic set `Content-Type` to file media type.

    json : Request body data, convert to `JSON` format. Conflict with parameter `data`.
        Automatic set `Content-Type` to `application/json`.

    headers : Request header data.
    timeout : Request maximun waiting time.
    proxy : Proxy URL.
    method : Request method.
        - `None` : Automatic judge.
            * When parameter `data` or `json` not has value, then request method is `get`.
            * When parameter `data` or `json` has value, then request method is `post`.
        - `Literal['get', 'post', 'put', 'patch', 'delete', 'options', 'head']` : Use this request method.

    check : Check response code, and throw exception.
        - `Literal[False]`: Not check.
        - `Literal[True]`: Check if is between 200 and 299.
        - `int` : Check if is this value.
        - `Iterable` : Check if is in sequence.

    receiver: Reponse handle receiver.
        - `None` : Automatic handle.
            * `Response 'Content-Type' is 'application/json'` : Use `ClientResponse.json` method.
            * `Response 'Content-Type' is 'text/plain; charset=utf-8'` : Use `ClientResponse.text` method.
            * `Other` : Use `ClientResponse.read` method.
        - `Callable` : Use this method, if it return is `Coroutine`, the `await` syntax will execute.

    Returns
    -------
    Coroutine instance.
    """

    # Check.
    check_most_one(data, json)

    # Handle parameter.
    if method is None:
        if data is None and json is None:
            method = "get"
        else:
            method = "post"


    # Define.
    async def session_request() -> Any:
        """
        Asynchronous request.

        Returns
        -------
        Response result.
        """

        # Session.
        async with ClientSession() as session:

            # Request.
            async with session.request(
                method,
                url,
                data=data,
                json=json,
                headers=headers,
                timeout=timeout,
                proxy=proxy
            ) as response:

                # Check code.
                if check is not False:
                    if check is True:
                        range_ = None
                    else:
                        range_ = check
                    check_response_code(response.status, range_)

                # Set encod type.
                if response.get_encoding() == "ISO-8859-1":
                    encoding = "utf-8"
                else:
                    encoding = None

                # Receive.
                if receiver is None:
                    if response.content_type == "application/json":
                        result = await response.json(encoding=encoding)
                    elif response.content_type == "text/plain; charset=utf-8":
                        result = await response.text(encoding=encoding)
                    else:
                        result = await response.read()
                else:
                    result = receiver(response)
                    if iscoroutine(result):
                        result = await result

                return result


    coroutine = session_request()

    return coroutine