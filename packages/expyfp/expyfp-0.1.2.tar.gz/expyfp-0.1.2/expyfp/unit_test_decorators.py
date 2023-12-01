from __future__ import annotations
from enum import Enum
from typing import Callable, TypeVar, Iterable, Optional, Any, ParamSpec, Self

class TestCase:
    class _Mode(Enum):
        match = 0  # pass same args, see if output matches
        validate = 1  # pass same args to both, see if kwargs.get("validator") passes

    def __init__(
        self,
        function=(lambda *args, **kwargs: ((args), kwargs) if kwargs else args),
        *_,
        **kwargs,
    ):
        if len(kwargs) == 0:
            self.mode = TestCase._Mode.match
        elif len(kwargs) == 1 and ("validator" in kwargs):
            self.mode = TestCase._Mode.validate
            self.validator = kwargs["validator"]
        else:
            raise ValueError("Currently a not supported case")
        self.function = function

    def __repr__(self) -> str:
        return f"Case(function = {self.function.__name__}, mode = {self.mode})"


def parametrized(
    expected_io: list[
        (tuple[tuple[Any, ...] | list[Any], Any | TestCase | Exception])
        | (
            tuple[
                tuple[Any, ...] | list[Any], dict[str, Any], Any | TestCase | Exception
            ]
        )
        | (list[tuple[Any, ...] | list[Any], Any | TestCase | Exception])
        | (
            list[
                tuple[Any, ...] | list[Any], dict[str, Any], Any | TestCase | Exception
            ]
        )
        # problem? :trollface: :union_type: :trollge:
    ]
) -> Callable[[Callable], Callable]:  # returns a decorator
    class _TestMode(Enum):
        normal_case: int = 0
        case_test: int = 1
        exception_test: int = 2

        @classmethod
        def from_expect(
            cls: _TestMode, expect: Any | TestCase | Exception
        ) -> _TestMode:
            # Exception test:
            try:
                if isinstance(expect(), Exception):
                    return cls.exception_test
            except:
                if isinstance(expect, Exception):
                    return cls.exception_test
            if isinstance(expect, Case):
                return cls.case_test
            else:
                return cls.normal_case

    def parametrized_decorator(function):
        def parse_case(
            *,
            args: Optional[tuple[Any, ...] | list[Any]] = (),
            kwargs: Optional[dict[str, Any]] = {},
            expect: Any | TestCase | Exception,
        ) -> None:
            test_mode: _TestMode = _TestMode.from_expect(expect=expect)
            info: str = f"{function.__name__}({repr(args)*bool(args)}{(', '*(bool(args) and bool(kwargs)))+repr(kwargs)*bool(kwargs)})"
            match test_mode:
                case _TestMode.normal_case:
                    # in a normal case, we just call the function with the provided arguments, and check if the result matches expectations
                    try:
                        result = (
                            function(*args, **kwargs) if kwargs else function(*args)
                        )
                        callable_expect = callable(expect)
                        expectation_passed = (
                            expect(result) if callable_expect else expect == result
                        )
                        if expectation_passed:
                            print(
                                f"\x1B[38;5;154mTest passed: {info} -> {repr(result)} {f'so {expect.__name__}({repr(result)}) was truthy' if callable_expect else f'== {repr(expect)}'}\x1B[0m"
                            )
                        else:
                            print(
                                f"\x1B[38;5;196mTest failed: {info} -> {repr(result)} {f'so {expect.__name__}({repr(result)}) was falsy' if callable_expect else f'instead of {expect}'}\x1B[0m"
                            )
                    except Exception as exc:
                        print(
                            f"\x1B[38;5;99mTest raised an exception: {info} -> {repr(exc)}\x1B[0m"
                        )  # something gone wrong, because this is not an exception test, so the test basically "failed"
                case _TestMode.case_test:
                    buf_info: str = f"{expect.function.__name__}({repr(args)*bool(args)}{(', '*(bool(args) and bool(kwargs)))+repr(kwargs)*bool(kwargs)})"
                    # in a `case test`, we call 2 functions with the same arguments: the one we're decorating, and the one provided in the case instance, BUT the test case itself has multiple modes: match and validate.
                    # if mode is match, we just compare if the function we're decorating and the function in the case instance give the same arguments
                    # if mode is validate, we get results of both functions, and see if the result of calling case.validator with those results is truthy
                    # in both cases the first function will be needed to be run, so call it before matching the mode & handle the exception:
                    exc_0: Exception | None = None
                    exc_1: Exception | None = None
                    # Gather expections from both functions to indicate the messages
                    try:
                        result_0 = (
                            function(*args, **kwargs) if kwargs else function(*args)
                        )
                    except Exception as exc_0_buf:
                        exc_0 = exc_0_buf
                    try:
                        result_1 = (
                            expect.function(*args, **kwargs)
                            if kwargs
                            else expect.function(*args)
                        )
                    except Exception as exc_1_buf:
                        exc_1 = exc_1_buf
                    if exc_0 and exc_1:
                        print(
                            f"\x1B[38;5;196mCase test failed: both functions raised an exception: {repr(exc_0)} : {repr(exc_1)}\x1B[0m"
                        )  # Both functions raised an exception
                    elif exc_0 and not exc_1:
                        print(
                            f"\x1B[38;5;196mCase test failed: {function.__name__} raised an exception {repr(exc_0)}\x1B[0m"
                        )  # Only the first (decorated) function raised an exception
                    elif exc_1 and not exc_0:
                        print(
                            f"\x1B[38;5;196mCase test failed: {expect.function.__name__} raised an exception {repr(exc_1)}\x1B[0m"
                        )  # Only the second (provided in the case instance) function raised an exception
                    if exc_0 or exc_1:
                        return None
                    match expect.mode:
                        case TestCase._Mode.match:
                            if result_0 == result_1:
                                print(
                                    f"\x1B[38;5;154mMatch case passed: {info} == {buf_info} -> {repr(result_0)} | {repr(result_1)}\x1B[0m"
                                )  # Match passed
                            else:
                                print(
                                    f"\x1B[38;5;196mMatch case failed: {info} -> {repr(result_0)} ; {buf_info} -> {repr(result_1)}\x1B[0m"
                                )  # Match failed
                        case TestCase._Mode.validate:
                            buf_res: Any = expect.validator(result_0, result_1)
                            buf_info: str = f"{expect.validator.__name__}({repr(result_0)}, {repr(result_1)})"
                            if buf_res:
                                print(
                                    f"\x1B[38;5;154mValidation case passed: {buf_info} -> {buf_res} [is truthy]\x1B[0m"
                                )  # Validation passed
                            else:
                                print(
                                    f"\x1B[38;5;196mValidation case failed: {buf_info} -> {buf_res} [is falsy]\x1B[0m"
                                )  # Validation failed
                case _TestMode.exception_test:
                    # in an exception test, we call the function with the provided arguments, and see if the catched expection matches the expected one.
                    try:
                        result = (
                            function(*args, **kwargs) if kwargs else function(*args)
                        )
                        print(
                            f"\x1B[38;5;202mException test didnt result in an exception {info} -> {repr(result)} instead of raising {repr(expect())}\x1B[0m"
                        )
                    except Exception as exc:
                        if type(exc) == expect:
                            print(
                                f"\x1B[38;5;50mException test passed: {info} -> {repr(exc)}\x1B[0m"
                            )
                        else:
                            print(
                                f"\x1B[38;5;196mException test failed: {info} -> {repr(exc)} instead of {repr(expect())}\x1B[0m"
                            )

        def test_cases() -> None:
            for test_case in expected_io:
                if len(test_case) == 2:
                    if isinstance(test_case[0], dict):
                        parse_case(kwargs=test_case[0], expect=test_case[1])
                    else:
                        parse_case(args=test_case[0], expect=test_case[1])
                elif len(test_case) == 3:
                    parse_case(
                        args=test_case[0], kwargs=test_case[1], expect=test_case[2]
                    )

        test_cases()
        return function

    return parametrized_decorator


def parametrized_wrap(
    inputs: list[Any] | tuple[Any],
    outputs: list[Any] | tuple[Any],
    function=lambda arg, ans: ([arg], ans),
) -> Callable[[Callable], Callable]:
    return parametrized(
        expected_io=[function(arg, ans) for arg, ans in zip(inputs, outputs)]
    )


# --- #
def parametrized_kwrap(
    inputs: list[Any] | tuple[Any] | None = None,
    kw_inputs: list[dict[str, Any]] | None = None,
    outputs: list[Any] | tuple[Any] | None = None,
    function=None,
) -> Callable[[Callable], Callable]:
    if inputs and kw_inputs:
        if function is None:

            def function(arg, ans, **kwargs):
                return [arg], kwargs, ans

        assert len(inputs) == len(kw_inputs) == len(outputs)
        return parametrized(
            expected_io=[
                function(arg, ans, **kwargs)
                for arg, ans, kwargs in zip(inputs, outputs, kw_inputs)
            ]
        )
    elif inputs and not kw_inputs:
        if function is None:

            def function(arg, ans):
                return [arg], ans

        assert len(inputs) == len(outputs)
        return parametrized(
            expected_io=[function(arg, ans) for arg, ans in zip(inputs, outputs)]
        )
    elif not inputs and kw_inputs:
        if function is None:

            def function(ans, **kwargs):
                return [], kwargs, ans

        assert len(kw_inputs) == len(outputs)
        return parametrized(
            expected_io=[
                function(ans, **kwargs) for ans, kwargs in zip(outputs, kw_inputs)
            ]
        )
    else:
        ...


# --- #
ClsVar = TypeVar("ClsVar")
Param = ParamSpec("Param")
RetType = TypeVar("RetType")


class ANSI:
    reset = "\x1B[0m"
    passed_0 = "\x1B[38;5;46m"
    failed_0 = "\x1B[38;5;196m"
    unexpected_exception_0 = "\x1B[38;5;129m"
    unexpected_return_0 = "\x1B[38;5;160m"


class Args:
    instances: list[Self] = []

    @classmethod
    def pop(cls: ClsVar, /, true_pop: bool = False) -> ClsVar:
        if true_pop:
            return cls.instances.pop()
        else:
            return cls.instances[-1]

    def __init__(
        self: Self, /, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        Args.instances.append(self)

    def __getitem__(self: Self, /, key: slice | Any) -> list | tuple:
        if isinstance(key, slice):
            return [
                self,
                key.step if key.step else (key.stop if key.stop else (key.start)),
            ]
        else:
            return self, key

    def __call__(self: Self, /, function: Callable[Param, RetType]) -> RetType:
        return function(*self.args, **self.kwargs)

    def call_string(self: Self, /, function: Callable[Param, RetType]) -> str:
        return f"{function.__name__}({f'*args = {repr(self.args)}'*bool(self.args)}{(', '*(bool(self.args) and bool(self.kwargs)))+f'**kwargs = {repr(self.kwargs)}'*bool(self.kwargs)})"

    def __repr__(self: Self) -> str:
        return f"Args(*args = {repr(self.args)} ; **kwargs = {repr(self.kwargs)})"


class Case:
    @classmethod
    def condition_test(
        cls: ClsVar,
        /,
        args: Args,
        condition: Callable[Param, bool],
        name: str = "Meta test",
    ) -> ClsVar:
        def get_response(self: Self, /, function: Callable[Param, RetType]) -> str:
            call_string = self.args.call_string(function=function)
            try:
                result: RetType = args(function=function)
                condition_string = f"{condition.__name__}({repr(result)})"
                if condition(result):
                    return f"{ANSI.passed_0}{name} passed: {call_string} -> {repr(result)}, and {condition_string} is truthy{ANSI.reset}"  # test pass
                else:
                    return f"{ANSI.failed_0}{name} failed: {call_string} -> {repr(result)}, and {condition_string} is falsy{ANSI.reset}"  # test fail
            except Exception as exc:
                return f"{ANSI.unexpected_exception_0}Unexpected exception raised: {call_string} -> {repr(exc)}{ANSI.reset}"  # test raised unexpected exception

        return cls(args=args, get_response=get_response)

    @classmethod
    def equal(cls: ClsVar, /, args: Args, expected_result: Any) -> ClsVar:
        def get_response(self: Self, /, function: Callable[Param, RetType]) -> str:
            call_string = self.args.call_string(function=function)
            try:
                result: RetType = args(function=function)
                if result == expected_result:
                    return f"{ANSI.passed_0}Equal test passed: {call_string} -> {repr(result)} == {repr(expected_result)}{ANSI.reset}"  # test pass
                else:
                    return f"{ANSI.failed_0}Equal test failed: {call_string} -> {repr(result)} instead of {repr(expected_result)}{ANSI.reset}"  # test fail
            except Exception as exc:
                return f"{ANSI.unexpected_exception_0}Equal test raised an unexpected exception: {call_string} -> {repr(exc)} instead of {repr(expected_result)}{ANSI.reset}"  # test raised unexpected exception

        return cls(args=args, get_response=get_response)

    @classmethod
    def expect(cls: ClsVar, /, args: Args, exception: Exception) -> ClsVar:
        def get_response(self: Self, /, function: Callable[Param, RetType]) -> str:
            call_string = self.args.call_string(function)
            try:
                result: RetType = self.args(function=function)
                return f"{ANSI.unexpected_return_0}Exception test didnt raise an exception: {call_string} -> {repr(result)} instead of {repr(exception())}{ANSI.reset}"
            except Exception as exc:
                if type(exc) == exception:
                    return f"{ANSI.passed_0}Exception test passed: {call_string} -> {repr(exception())}{ANSI.reset}"
                else:
                    return f"{ANSI.failed_0}Exception test failed: {call_string} -> {repr(exc)} instead of {repr(exception())}{ANSI.reset}"

        return cls(args=args, get_response=get_response)

    def __init__(
        self: Self,
        /,
        args: Args,
        get_response: Callable[[Self, Callable[Param, RetType]], str],
    ) -> None:
        self.args = args
        self.get_response = get_response

    @classmethod
    def copycat(
        cls: ClsVar, /, args: Args, copycat_function: Callable[Param, RetType]
    ) -> ClsVar:
        def get_response(self: Self, /, function: Callable[Param, RetType]) -> str:
            call_string_0: str = self.args.call_string(function)
            call_string_1: str = self.args.call_string(copycat_function)
            res_0: Any | None = None
            res_1: Any | None = None
            exc_0: Exception | None = None
            exc_1: Exception | None = None
            try:
                res_0 = args(function)
            except Exception as buf_exc_0:
                exc_0 = buf_exc_0
            try:
                res_1 = args(copycat_function)
            except Exception as buf_exc_1:
                exc_1 = buf_exc_1
            if exc_0 or exc_1:
                if exc_0 and exc_1:
                    return f"{ANSI.unexpected_exception_0}Copycat test raised an unexpected exception: {call_string_0} -> {repr(exc_0)} || {call_string_1} -> {repr(exc_1)}{ANSI.reset}"
                elif exc_0 and not exc_1:
                    return f"{ANSI.unexpected_exception_0}Copycat test raised an unexpected exception: {call_string_0} -> {repr(exc_0)} || {call_string_1} -> {repr(res_1)}{ANSI.reset}"
                elif not exc_0 and exc_1:
                    return f"{ANSI.unexpected_exception_0}Copycat test raised an unexpected exception: {call_string_0} -> {repr(res_0)} || {call_string_1} -> {repr(exc_1)}{ANSI.reset}"
            else:
                if res_0 == res_1:
                    return f"{ANSI.passed_0}Copycat test passed: {call_string_0} -> {repr(res_0)} == {call_string_1} (which is {repr(res_1)}){ANSI.reset}"
                else:
                    return f"{ANSI.failed_0}Copycat test failed: {call_string_0} -> {repr(res_0)} buf {call_string_1} -> {repr(res_1)}{ANSI.reset}"

        return cls(args=args, get_response=get_response)

    def __call__(self: Self, /, function: Callable[Param, RetType]) -> str:
        return self.get_response(function)

    def __repr__(self: Self) -> str:
        return f"Case({self.args}, {self.get_response.__name__})"


def test(
    cases: Iterable[Case],
) -> Callable[
    [Callable[Param, RetType]], Callable[Param, RetType]
]:  # returns a decorator [parametrized decorator implementation]
    def test_decorator(function: Callable[Param, RetType]) -> Callable[Param, RetType]:
        for case in cases:
            print(case.get_response(case, function=function))
        return function

    return test_decorator