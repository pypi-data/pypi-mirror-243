# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Interpreter system methods.
"""


from typing import Any, List, Dict, Tuple, Iterable, Type, Literal, Optional, Callable, Union, NoReturn, overload
from types import TracebackType
from inspect import signature as inspect_signature, _ParameterKind, _empty
from sys import path as sys_path, modules as sys_modules, exc_info as sys_exc_info
from os.path import exists as os_exists, abspath as os_abspath
from traceback import format_exc, format_stack, extract_stack
from warnings import warn as warnings_warn
from subprocess import Popen, PIPE
from argparse import ArgumentParser
from varname import argname


__all__ = (
    "add_env_path",
    "reset_env_path",
    "throw",
    "warn",
    "catch_exc",
    "check_least_one",
    "check_most_one",
    "check_file_found",
    "check_file_exist",
    "check_response_code",
    "is_iterable",
    "is_table",
    "is_number_str",
    "get_first_notnull",
    "get_name",
    "get_stack_text",
    "get_stack_param",
    "dos_command",
    "del_modules",
    "get_arg_info",
    "dos_command"
)


# Added environment path.
_add_env_paths: List[str] = []


def add_env_path(path: str) -> List[str]:
    """
    Add environment variable path.

    Parameters
    ----------
    path : Path, can be a relative path.

    Returns
    -------
    Added environment variables list.
    """

    # Absolute path.
    abs_path = os_abspath(path)

    # Add.
    global _add_env_paths
    _add_env_paths.append(abs_path)
    sys_path.append(abs_path)

    return sys_path


def reset_env_path() -> None:
    """
    Reset environment variable path.
    """

    # Delete.
    global _add_env_paths
    for path in _add_env_paths:
        sys_path.remove(path)
    _add_env_paths = []


def throw(
    exception: Type[BaseException] = AssertionError,
    value: Optional[Any] = None,
    frame: int = 2
) -> NoReturn:
    """
    Throw exception.

    Parameters
    ----------
    exception : Exception Type.
    value : Exception value.
    frame : Number of code to upper level.
    """

    # Get parameter.

    ## Value name.
    if value is not None:
        name = get_name(value, frame)
        if name is None:
            value_name = "now"
        else:
            value_name = "parameter '%s'" % name

    ## Text.
    if exception == AssertionError:
        text = "use error"
    elif exception == ValueError:
        text = "value error"
    elif exception == TypeError:
        text = "value type error"
        if value is not None:
            value = value.__class__
    elif exception == FileNotFoundError:
        text = "file path not found"
    elif exception == FileExistsError:
        text = "file path already exists"
    elif exception == TimeoutError:
        text = "execute timeout"
        if value.__class__ == float:
            value = round(value, 3)
            if value % 1 == 0:
                value = int(value)
    elif exception == ConnectionError:
        text = "connection fail"

    ### Other.
    else:
        exception = AssertionError
        text = "use error"

    ### Join.
    if value is not None:
        text += ", %s is %s" % (value_name, repr(value))

    # Raise.
    exception = exception(text)
    raise exception


def warn(
    *infos: Any,
    exception: Type[BaseException] = UserWarning,
    stacklevel: int = 3
) -> None:
    """
    Throw warning.

    Parameters
    ----------
    infos : Warn informations.
    exception : Exception type.
    stacklevel : Warning code location, number of recursions up the code level.
    """

    # Handle parameter.
    if infos == ():
        infos = "Warning!"
    elif len(infos) == 1:
        if infos[0].__class__ == str:
            infos = infos[0]
        else:
            infos = str(infos[0])
    else:
        infos = str(infos)

    # Throw warning.
    warnings_warn(infos, exception, stacklevel)


def catch_exc(
    title: Optional[str] = None
) -> Tuple[str, Type[BaseException], BaseException, TracebackType]:
    """
    Catch exception information and print, must used in `except` syntax.

    Parameters
    ----------
    title : Print title.
        - `None` : Not print.
        - `str` : Print and use this title.

    Returns
    -------
    Exception report text and exception type and exception instance and exception position instance.
    """

    # Get parameter.
    exception_report = format_exc()
    exception_report = exception_report.strip()
    exception_type, exception, traceback = sys_exc_info()

    # Print.
    if title is not None:

        ## Import.
        from .rstdout import echo

        ## Execute.
        echo(exception_report, title=title, frame="half")

    return exception_report, exception_type, exception, traceback


def check_least_one(*values: Any) -> None:
    """
    Check that at least one of multiple values is not null, when check fail, then throw exception.

    Parameters
    ----------
    values : Check values.
    """

    # Check.
    for value in values:
        if value is not None:
            return

    # Throw exception.
    vars_name = get_name(values)
    if vars_name is not None:
        vars_name_de_dup = list(set(vars_name))
        vars_name_de_dup.sort(key=vars_name.index)
        vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
    else:
        vars_name_str = ""
    raise TypeError(f"at least one of parameters{vars_name_str} is not None")


def check_most_one(*values: Any) -> None:
    """
    Check that at most one of multiple values is not null, when check fail, then throw exception.

    Parameters
    ----------
    values : Check values.
    """

    # Check.
    none_count = 0
    for value in values:
        if value is not None:
            none_count += 1

    # Throw exception.
    if none_count > 1:
        vars_name = get_name(values)
        if vars_name is not None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise TypeError(f"at most one of parameters{vars_name_str} is not None")


def check_file_found(path: str) -> None:
    """
    Check if file path found, if not, throw exception.

    Parameters
    ----------
    path : File path.
    """

    # Check.
    exist = os_exists(path)

    # Raise.
    if not exist:
        throw(FileNotFoundError, path, 3)


def check_file_exist(path: str) -> None:
    """
    Check if file path exist, if found, throw exception.

    Parameters
    ----------
    path : File path.
    """

    # Check.
    exist = os_exists(path)

    # Raise.
    if exist:
        throw(FileExistsError, path, 3)


def check_response_code(
    code: int,
    range_: Optional[Union[int, Iterable[int]]] = None
) -> bool:
    """
    Check if the response code is in range.

    Parameters
    ----------
    code : Response code.
    range_ : Pass the code range.
        - `None`: Check if is between 200 and 299.
        - `int` : Check if is this value.
        - `Iterable` : Check if is in sequence.

    Returns
    -------
    Check result.
    """

    # Check.
    if range_ is None:
        result = code // 100 == 2
    elif range_.__class__ == int:
        result = code == range_
    elif hasattr(range_, "__contains__"):
        result = code in range_
    else:
        throw(TypeError, range_)

    # Raise.
    if not result:
        throw(value=code, frame=3)

    return result


def is_iterable(
    obj: Any,
    exclude_types: Iterable[Type] = [str, bytes]
) -> bool:
    """
    Judge whether it is iterable.

    Parameters
    ----------
    obj : Judge object.
    exclude_types : Non iterative types.

    Returns
    -------
    Judgment result.
    """

    # Exclude types.
    if obj.__class__ in exclude_types:
        return False

    # Judge.
    if hasattr(obj, "__iter__"):
        return True
    else:
        return False


def is_table(
    obj: Any,
    check_fields: bool = True
) -> bool:
    """
    Judge whether it is `List[Dict]` table format and keys and keys sort of the Dict are the same.

    Parameters
    ----------
    obj : Judge object.
    check_fields : Do you want to check the keys and keys sort of the Dict are the same.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    if obj.__class__ != list:
        return False
    for element in obj:
        if element.__class__ != dict:
            return False

    ## Check fields of table.
    if check_fields:
        keys_strs = [
            ":".join([str(key) for key in element.keys()])
            for element in obj
        ]
        keys_strs_only = set(keys_strs)
        if len(keys_strs_only) != 1:
            return False

    return True


def is_number_str(
    string: str
) -> bool:
    """
    Judge whether it is number string.

    Parameters
    ----------
    string : String.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    try:
        int(string)
    except (ValueError, TypeError):
        return False

    return True


def get_first_notnull(
    *values: Any,
    default: Union[None, Any, Literal["exception"]] = None,
    nulls: Tuple = (None,)) -> Any:
    """
    Get the first value that is not null.

    Parameters
    ----------
    values : Check values.
    default : When all are null, then return this is value, or throw exception.
        - `Any` : Return this is value.
        - `Literal['exception']` : Throw `exception`.

    nulls : Range of null values.

    Returns
    -------
    Return first not null value, when all are `None`, then return default value.
    """

    # Get value.
    for value in values:
        if value not in nulls:
            return value

    # Throw exception.
    if default == "exception":
        vars_name = get_name(values)
        if vars_name is not None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join([f"'{var_name}'" for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise ValueError(f"at least one of parameters{vars_name_str} is not None")

    return default


def get_name(obj: Any, frame: int = 2) -> Optional[Union[str, Tuple[str, ...]]]:
    """
    Get object name.

    Parameters
    ----------
    obj : Object.
    frame : Number of code to upper level.

    Returns
    -------
    Object name or None.
    """

    # Get name using built in method.
    try:
        name = obj.__name__
    except AttributeError:

        # Get name using module method.
        name = "obj"
        try:
            for _frame in range(1, frame + 1):
                name = argname(name, frame=_frame)
            if name.__class__ != str:
                if "".join(name) == "":
                    name = None
        except:
            name = None

    return name


def get_stack_text(format_: Literal["plain", "full"] = "plain", limit: int = 2) -> str:
    """
    Get code stack text.

    Parameters
    ----------
    format_ : Stack text format.
        - `Literal['plain']` : Floor stack position.
        - `Literal['full']` : Full stack information.

    limit : Stack limit level.

    Returns
    -------
    Code stack text.
    """

    # Plain.
    if format_ == "plain":
        limit += 1
        stacks = format_stack(limit=limit)

        ## Check.
        if len(stacks) != limit:
            throw(value=limit)

        ## Convert.
        text = stacks[0]
        index_end = text.find(", in ")
        text = text[2:index_end]

    # Full.
    elif format_ == "full":
        stacks = format_stack()
        index_limit = len(stacks) - limit
        stacks = stacks[:index_limit]

        ## Check.
        if len(stacks) == 0:
            throw(value=limit)

        ## Convert.
        stacks = [
            stack[2:].replace("\n  ", "\n", 1)
            for stack in stacks
        ]
        text = "".join(stacks)
        text = text[:-1]

    # Raise.
    else:
        throw(ValueError, format_)

    return text


@overload
def get_stack_param(format_: Literal["floor"] = "floor", limit: int = 2) -> Dict: ...

@overload
def get_stack_param(format_: Literal["full"] = "floor", limit: int = 2) -> List[Dict]: ...

def get_stack_param(format_: Literal["floor", "full"] = "floor", limit: int = 2) -> Union[Dict, List[Dict]]:
    """
    Get code stack parameters.

    Parameters
    ----------
    format_ : Stack parameters format.
        - `Literal['floor']` : Floor stack parameters.
        - `Literal['full']` : Full stack parameters.

    limit : Stack limit level.

    Returns
    -------
    Code stack parameters.
    """

    # Get.
    stacks = extract_stack()
    index_limit = len(stacks) - limit
    stacks = stacks[:index_limit]

    # Check.
    if len(stacks) == 0:
        throw(value=limit)

    # Convert.

    ## Floor.
    if format_ == "floor":
        stack = stacks[-1]
        params = {
            "filename": stack.filename,
            "lineno": stack.lineno,
            "name": stack.name,
            "line": stack.line
        }

    ## Full.
    elif format_ == "full":
        params = [
            {
                "filename": stack.filename,
                "lineno": stack.lineno,
                "name": stack.name,
                "line": stack.line
            }
            for stack in stacks
        ]

    return params


def dos_command(command: Union[str, Iterable[str]]) -> str:
    """
    Execute DOS command.

    Parameters
    ----------
    command : DOS command.
        - `str` : Use this command.
        - `Iterable[str]` : Join strings with space as command.
            When space in the string, automatic add quotation mark (e.g., ['echo', 'a b'] -> 'echo "a b"').

    Returns
    -------
    Command standard output.
    """

    # Execute.
    popen = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)

    # Check.
    error_bytes: bytes = popen.stderr.read()
    if error_bytes != b"":
        error = error_bytes.decode("GBK")
        throw(value=error)

    # Standard output.
    output_bytes: bytes = popen.stdout.read()
    output = output_bytes.decode("GBK")

    return output


def del_modules(path: str) -> List[str]:
    """
    Delete record of modules import dictionary.

    Parameters
    ----------
    path : Module path, use regular match.

    Returns
    -------
    Deleted modules dictionary.
    """

    # Import.
    from .rregular import search

    # Set parameter.
    deleted_dict = {}
    module_keys = tuple(sys_modules.keys())

    # Delete.
    for key in module_keys:
        module = sys_modules.get(key)

        ## Filter non file module.
        if (
            not hasattr(module, "__file__")
            or module.__file__ is None
        ):
            continue

        ## Match.
        result = search(path, module.__file__)
        if result is None:
            continue

        ## Take out.
        deleted_dict[key] = sys_modules.pop(key)

    return deleted_dict


def get_arg_info(func: Callable) -> List[
    Dict[
        Literal["name", "type", "annotation", "default"],
        Optional[str]
    ]
]:
    """
    Get function arguments information.

    Parameters
    ----------
    func : Function.

    Returns
    -------
    Arguments information.
        - `Value of key 'name'` : Argument name.
        - `Value of key 'type'` : Argument bind type.
            * `Literal['position_or_keyword']` : Is positional argument or keyword argument.
            * `Literal['var_position']` : Is variable length positional argument.
            * `Literal['var_keyword']` : Is variable length keyword argument.
            * `Literal['only_position']` : Is positional only argument.
            * `Literal['only_keyword']` : Is keyword only argument.
        - `Value of key 'annotation'` : Argument annotation.
        - `Value of key 'default'` : Argument default value.
    """

    # Get signature.
    signature = inspect_signature(func)

    # Get information.
    info = [
        {
            "name": name,
            "type": (
                "position_or_keyword"
                if parameter.kind == _ParameterKind.POSITIONAL_OR_KEYWORD
                else "var_position"
                if parameter.kind == _ParameterKind.VAR_POSITIONAL
                else "var_keyword"
                if parameter.kind == _ParameterKind.VAR_KEYWORD
                else "only_position"
                if parameter.kind == _ParameterKind.POSITIONAL_ONLY
                else "only_keyword"
                if parameter.kind == _ParameterKind.KEYWORD_ONLY
                else None
            ),
            "annotation": parameter.annotation,
            "default": parameter.default
        }
        for name, parameter in signature.parameters.items()
    ]

    # Replace empty.
    for row in info:
        for key, value in row.items():
            if value == _empty:
                row[key] = None

    return info


def dos_command(*vars: Any) -> List[Any]:
    """
    Use DOS command to input arguments to variables.
    Use DOS command `python file --help` to view help information.

    Parameters
    ----------
    vars : Variables.

    Returns
    -------
    Value of variables.

    Exsamples
    ---------
    >>> var1 = 1
    >>> var2 = 2
    >>> var3 = 3
    >>> var1, var2, var3 = dos_command(var1, var2, var3)
    >>> print(var1, var2, var3)
    >>> # Use DOS command 'python file.py 10 --var2 20 21'
    10 [20, 21] 3
    """

    # Get parameter.
    vars_name = get_name(vars)
    vars_info = tuple(zip(vars_name, vars))

    # Set DOS command.
    usage = "input arguments to variables"
    parser = ArgumentParser(usage=usage)
    for name, value in vars_info:
        if value is None:
            var_type = str
            var_help = None
        else:
            var_type = value.__class__
            var_help = str(value.__class__)

        ## Position argument.
        parser.add_argument(
            name,
            nargs="?",
            type=var_type,
            help=var_help
        )

        ## Keyword argument.
        kw_name = "--" + name
        parser.add_argument(
            kw_name,
            nargs="*",
            type=var_type,
            help=var_help,
            metavar="value",
            dest=kw_name
        )

    # Get argument.
    namespace = parser.parse_args()
    values = []
    for name, value in vars_info:
        kw_name = "--" + name

        ## Position argument.
        dos_value = getattr(namespace, name)
        if dos_value is not None:
            values.append(dos_value)
            continue

        ## Keyword argument.
        dos_value = getattr(namespace, kw_name)
        if dos_value.__class__ == list:
            value_len = len(dos_value)
            if value_len == 0:
                dos_value = None
            elif value_len == 1:
                dos_value = dos_value[0]
            values.append(dos_value)
            continue

        values.append(value)

    return values