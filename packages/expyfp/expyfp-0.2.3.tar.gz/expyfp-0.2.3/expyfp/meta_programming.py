"""
There will be going to be a lot of evals and execs because funny lmao haha xd i will try to keep it typesafe
"""

from typing import Callable, TypeVar, Any, TypeAlias, ParamSpec
from types import ModuleType
import textwrap

T = TypeVar("T")
W = TypeVar("W")
PatternMap: TypeAlias = dict[str, str]
Params = ParamSpec("Params")


def splittwo(string: str, delim: str) -> tuple[str, str]:
    left, right = string.split(delim, maxsplit=1)
    return (left, right)


def tryexcept(
    default: T,
    function: Callable[Params, T],
    *args: Params.args,
    **kwargs: Params.kwargs,
) -> T:
    try:
        return function(*args, **kwargs)
    except Exception:
        return default


def identity(obj: T) -> T:
    return obj


def match_expr(
    pattern: str,
    in_type: type[T] | object = Any,
    out_type: type[W] | object = Any,
    pattern_prefix: str = "?",
    return_partition: str = "->",
    pre_pattern: str = "\n" + (" " * 4),
    pre_return: str = "\n" + (" " * 8),
    dedent: bool = True,
    argument_name: str = "__expr",
    pattern_transformer: Callable[[PatternMap], PatternMap] = identity,
    return_func_name: str = "__",
    set_code_attr: bool = True,
    code_attr_name: str = "match_code",
    clear_return: bool = True,
    global_scope: dict[str, Any] = globals(),
    local_scope: dict[str, Any] = locals(),
) -> Callable[[T], W]:
    """
    Syntax:
        (<pattern_prefix> <pattern> <return_partition> <return_expression>)*
    Transforms into:
        match <argument_name>:(<pre_pattern>case <pattern>:<return_func_name(<return_expression>)>)*

    The returned function can raise a NameError if the match wont match the expression
    """
    if len(pattern_prefix) == 0 or len(return_partition) == 0:
        raise ValueError("Pattern prefix and return partition need to be not empty.")

    return_value: W

    def env_set_return(value: W) -> None:  # Unpure
        nonlocal return_value
        return_value = value

    def env_clear_return() -> None:  # Unpure
        nonlocal return_value
        try:
            return_value
        except NameError:
            pass
        else:
            del return_value

    local_scope[return_func_name] = env_set_return

    if dedent is True:
        pattern = textwrap.dedent(pattern)

    patterns: PatternMap = {}
    capture = ""

    for line in map(str.strip, filter(None, pattern.splitlines())):
        if line.startswith(pattern_prefix):
            capture, expression = splittwo(line.removeprefix(pattern_prefix), return_partition)
            capture = capture.rstrip()
            expression = expression.lstrip()
            patterns[capture] = expression
        else:
            patterns[capture] += line

    patterns = pattern_transformer(patterns)

    new_code = f"match {argument_name}:" + "".join(
        f"{pre_pattern}case {capture_pattern}:{pre_return}{return_func_name}({return_expression})"
        for (capture_pattern, return_expression) in patterns.items()
    )
    code_object = compile(new_code, "<string>", "exec")

    def pattern_match(expr: T) -> W:  # assume that those typehints are correct, you passed them yourselves :skull:
        needed = {argument_name: expr}
        exec(code_object, global_scope, local_scope | needed)
        buffer = return_value # noqa
        if clear_return is True:
            env_clear_return()
        return buffer

    if set_code_attr is True:
        setattr(pattern_match, code_attr_name, new_code)

    return pattern_match


def source_to_module(source: str, name: str = "<dynamic>", doc: str = "") -> ModuleType:
    code_obj = compile(source, "<string>", "exec")
    module = ModuleType(name, doc)
    exec(code_obj, module.__dict__)
    return module


def parse_clike_body(source: str, indent_level: int = 0) -> str:
    python_body: str = ""
    if ";" not in source:
        python_body += f"return {source}"
    else:
        for char in source:
            if char == "\n": # idk
                continue
            if char == "{":
                indent_level += 1
                python_body += f"\n{' '*(4*indent_level)}"
            elif char == "}":
                indent_level -= 1
            elif char == ";":
                python_body += f"\n{' '*(4*indent_level)}"
            else:
                python_body += char

    return python_body


def parse_clike_signature(sig: str, argsplit: str = ",") -> tuple[str, str, list[str]]:
    ret_type, funcdef = splittwo(sig, " ")
    func_name, argsig = splittwo(funcdef, "(")
    argsig = argsig.strip()[:-1]  # -)
    parsed_args: list[str] = []
    for arg in map(str.strip, argsig.split(argsplit)):
        typesig = arg.partition(" ")
        deflpart = arg.partition("=")
        if deflpart[2]:
            arginfo = deflpart[0].partition(" ")
            parsed_args.append(f"{arginfo[2]}: {typesig[0]} = {deflpart[2]}")
        else:
            parsed_args.append(f"{typesig[2]}: {typesig[0]}")
    return ret_type, func_name, parsed_args


def c_func_def(
    code: str,
    out_type: type[T] | object = Any,
    argsplit: str = ",",
    set_code_attr: bool = True,
    code_attr_name: str = "source",
) -> T:
    code = code.replace("\n", "")
    sig, body = splittwo(code, "{")
    body = body[:-1]
    ret_type, func_name, parsed_args = parse_clike_signature(sig, argsplit)
    python_body = f"def {func_name}({', '.join(parsed_args)}) -> {ret_type}:\n{' '*4}" + parse_clike_body(body, indent_level=1)
    module = source_to_module(python_body)
    func = getattr(module, func_name, None)
    if set_code_attr:
        setattr(func, code_attr_name, python_body)

    return func  # type: ignore


def cpy_func_def(
    code: str,
    out_type: type[T] | object = Any,
    set_code_attr: bool = True,
    code_attr_name: str = "source",
) -> T:
    sig, body = splittwo(code, "{")
    func_name = splittwo(sig, "(")[0]
    body = body[:-1]
    python_body = f"def {sig.strip()}:\n{' '*4}" + parse_clike_body(body, indent_level=1)
    module = source_to_module(python_body)
    func = getattr(module, func_name, None)
    if set_code_attr:
        setattr(func, code_attr_name, python_body)

    return func  # type: ignore
