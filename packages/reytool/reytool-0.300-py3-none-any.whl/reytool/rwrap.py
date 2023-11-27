# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:12:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Decorator methods.
"""


from typing import Any, Tuple, Callable, Optional, Union, Literal, overload
from functools import wraps as functools_wraps
from threading import Thread

from .rstdout import echo
from .rsystem import throw, catch_exc
from .rtime import now, time_to, sleep, RTimeMark


__all__ = (
    "wrap_frame",
    "wrap_runtime",
    "wrap_thread",
    "wrap_exc",
    "wrap_retry",
    "wrap_wait"
)


def wrap_frame(decorator: Callable) -> Callable:
    """
    Decorative frame.

    Parameters
    ----------
    decorator : Decorator function.

    Retuens
    -------
    Decorated decorator.

    Examples
    --------
    Decoration function method one.
    >>> @wrap_func
    >>> def func(): ...
    >>> result = func(param_a, param_b, param_c=1, param_d=2)

    Decoration function method two.
    >>> def func(): ...
    >>> result = wrap_func(func, param_a, param_b, param_c=1, param_d=2)

    Decoration function method three.
    >>> def func(): ...
    >>> result = wrap_func(func, _execute=True)
    
    Decoration function method four.
    >>> def func(): ...
    >>> func = wrap_func(func)
    >>> result = func(param_a, param_b, param_c=1, param_d=2)

    Decoration function method five.
    >>> def func(): ...
    >>> func = wrap_func(func, param_a, param_c=1, _execute=False)
    >>> result = func(param_b, param_d=2)
    """


    # Decorate Decorator.
    @overload
    def wrap(func: Callable, *args: Any, _execute: None = None, **kwargs: Any) -> Union[Callable, Any]: ...

    @overload
    def wrap(func: Callable, *args: Any, _execute: Literal[True] = None, **kwargs: Any) -> Any: ...

    @overload
    def wrap(func: Callable, *args: Any, _execute: Literal[False] = None, **kwargs: Any) -> Callable: ...

    @functools_wraps(decorator)
    def wrap(func: Callable, *args: Any, _execute: Optional[bool] = None, **kwargs: Any) -> Union[Callable, Any]:
        """
        Decorative shell.

        Parameters
        ----------
        func : Function.
        args : Position arguments of function.
        _execute : Whether execute function, otherwise decorate function.
            - `None` : When parameter `args` or `kwargs` have values, then True, otherwise False.
            - `bool` : Use this value.

        kwargs : Keyword arguments of function.

        Returns
        -------
        Decorated function or function return.
        """

        # Handle parameter.
        if _execute is None:
            if args != () or kwargs != {}:
                _execute = True
            else:
                _execute = False

        # Direct execution.
        if _execute:
            result = decorator(func, *args, **kwargs)
            return result


        # Decorate function.
        @functools_wraps(func)
        def wrap_sub(*_args: Any, **_kwargs: Any) -> Any:
            """
            Decorative sub shell.

            Parameters
            ----------
            args : Position arguments of function.
            kwargs : Keyword arguments of function.

            Returns
            -------
            Function return.
            """

            # Decorate function.
            result = decorator(func, *args, *_args, **kwargs, **_kwargs)

            return result


        return wrap_sub


    return wrap


@overload
def wrap_runtime(func: Callable, *args: Any, _return_report: Literal[False] = False, **kwargs: Any) -> Any: ...

@overload
def wrap_runtime(func: Callable, *args: Any, _return_report: Literal[True] = False, **kwargs: Any) -> Tuple[Any, str]: ...

@wrap_frame
def wrap_runtime(func: Callable, *args: Any, _return_report: bool = False, **kwargs: Any) -> Union[Any, Tuple[Any, str]]:
    """
    Decorator, print or return runtime report of the function.

    Parameters
    ----------
    func : Function to be decorated.
    args : Position arguments of decorated function.
    _return_report : Whether return report, otherwise print report.
    kwargs : Keyword arguments of decorated function.

    Returns
    -------
    Function execute result and runtime report.
    """

    # Execute function and marking time.
    rtm = RTimeMark()
    rtm()
    result = func(*args, **kwargs)
    rtm()

    # Generate report.
    start_time = rtm.record[0]["datetime"]
    spend_time = rtm.record[1]["timedelta"]
    end_time = rtm.record[1]["datetime"]
    start_str = time_to(start_time, True)[:-3]
    spend_str = time_to(spend_time, True)[:-3]
    end_str = time_to(end_time, True)[:-3]
    report = "Start: %s -> Spend: %ss -> End: %s" % (
        start_str,
        spend_str,
        end_str
    )
    title = func.__name__

    # Return report.
    if _return_report:
        return result, report

    # Print report.
    echo(report, title=title)

    return result


@overload
def wrap_thread(func: Callable, *args: Any, _daemon: bool = True, **kwargs: Any) -> Thread: ...

@wrap_frame
def wrap_thread(func: Callable, *args: Any, _daemon: bool = True, **kwargs: Any) -> Thread:
    """
    Decorator, function start in thread.

    Parameters
    ----------
    func : Function to be decorated.
    args : Position arguments of decorated function.
    _daemon : Whether it is a daemon thread.
    kwargs : Keyword arguments of decorated function.

    Returns
    -------
    Thread object.
    """

    # Handle parameter.
    thread_name = "%s_%d" % (func.__name__, now("timestamp"))

    # Create thread.
    thread = Thread(target=func, name=thread_name, args=args, kwargs=kwargs)
    thread.daemon = _daemon

    # Start thread.
    thread.start()

    return thread


@overload
def wrap_exc(
    func: Callable,
    *args: Any,
    _exception: Union[BaseException, Tuple[BaseException, ...]] = BaseException,
    _handler: Optional[Callable] = None,
    **kwargs: Any
) -> Optional[Any]: ...

@wrap_frame
def wrap_exc(
    func: Callable,
    *args: Any,
    _exception: Union[BaseException, Tuple[BaseException, ...]] = BaseException,
    _handler: Optional[Callable] = None,
    **kwargs: Any
) -> Optional[Any]:
    """
    Decorator, execute function with try syntax and print exception information.

    Parameters
    ----------
    func : Function to be decorated.
    args : Position arguments of decorated function.
    _exception : Catch exception types.
    _handler : Exception handle method.
        - `None` : Use `.rsystem.RException.catch` method print exception text.
        - `Callable` : Use this method.

    kwargs : Keyword arguments of decorated function.

    Returns
    -------
    Function execute result or no return.
    """

    # Execute function.
    try:
        result = func(*args, **kwargs)

    # Print exception information.
    except _exception:
        if _handler is None:
            func_name = func.__name__
            catch_exc(func_name)
        else:
            _handler()

    # Return function result.
    else:
        return result


@overload
def wrap_retry(
    func: Callable,
    *args: Any,
    _report: Optional[str] = None,
    _exception: Union[BaseException, Tuple[BaseException, ...]] = BaseException,
    _try_total: int = 1,
    _try_count: int = 0,
    **kwargs: Any
) -> Any: ...

@wrap_frame
def wrap_retry(
    func: Callable,
    *args: Any,
    _report: Optional[str] = None,
    _exception: Union[BaseException, Tuple[BaseException, ...]] = BaseException,
    _try_total: int = 1,
    _try_count: int = 0,
    **kwargs: Any
) -> Any:
    """
    Decorator, try again.

    Parameters
    ----------
    func : Function to be decorated.
    args : Position arguments of decorated function.
    _report : Print report title.
        - `None` : Not print.
        - `str` : Print and use this title.

    _exception : Catch exception types.
    _try_total : Retry total.
    _try_count : Retry count.
    kwargs : Keyword arguments of decorated function.

    Returns
    -------
    Function execute result.
    """

    # Try count not full.
    if _try_count < _try_total:

        ## Try.
        try:
            result = func(*args, **kwargs)
        except _exception:

            ## Report.
            if _report is not None:
                exception_msg, _, _, _ = catch_exc()
                echo(
                    exception_msg,
                    "Retrying...",
                    title=_report,
                    frame="half"
                )

            ### Retry.
            _try_count += 1
            result = wrap_retry(
                func,
                *args,
                _report=_report,
                _exception=_exception,
                _try_total=_try_total,
                _try_count=_try_count,
                **kwargs
            )

    # Try count full.
    else:
        result = func(*args, **kwargs)

    return result


@overload
def wrap_wait(
    func: Callable[[Any], bool],
    *args: Any,
    _interval: float = 1,
    _timeout: Optional[float] = None,
    **kwargs: Any
) -> float: ...

@wrap_frame
def wrap_wait(
    func: Callable[[Any], bool],
    *args: Any,
    _interval: float = 1,
    _timeout: Optional[float] = None,
    **kwargs: Any
) -> float:
    """
    Decorator, wait success, timeout throw exception.

    Parameters
    ----------
    func : Function to be decorated, must return `bool` value.
    args : Position arguments of decorated function.
    _interval : Interval seconds.
    _timeout : Timeout seconds, timeout throw exception.
        - `None` : Infinite time.
        - `float` : Use this time.

    kwargs : Keyword arguments of decorated function.

    Returns
    -------
    Total spend seconds.
    """

    # Set parameter.
    rtm = RTimeMark()
    rtm()

    # Not set timeout.
    if _timeout is None:

        ## Wait.
        while True:
            success = func(*args, **kwargs)
            if success: break
            sleep(_interval)

    # Set timeout.
    else:
        count = 0

        ## Wait.
        while True:
            success = func(*args, **kwargs)
            if success: break
            sleep(_interval)
            count += _interval
            if count > _timeout:
                throw(FileNotFoundError, count)

    ## Return.
    rtm()
    return rtm.total_spend