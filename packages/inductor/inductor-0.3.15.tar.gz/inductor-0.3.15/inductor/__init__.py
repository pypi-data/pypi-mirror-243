# Copyright 2023 Inductor, Inc.
"""Inductor client library."""

import contextlib
import contextvars
import copy
import datetime
import functools
import inspect
import io
import sys
from typing import Any, Callable, Dict, Generator, List, Optional, TextIO, Tuple, TypeVar, Union

from inductor import auth_session, backend_client, config, wire_model
from inductor.cli import cli, data_model
from inductor.wire_model import TestCase, QualityMeasure, HparamSpec


# Test suite components are classes that can be added to a test suite,
# i.e., test cases, quality measures, and hyperparameter specifications.
_TestSuiteComponent = Union[TestCase, QualityMeasure, HparamSpec]


class TestSuite:
    """Test suite.
    
    A collection of test cases, quality measures, and hyperparameter
    specifications that can be run together.
    
    Attributes:
        id_or_name: ID or name of the test suite.
        llm_program: LLM program to test. Either a Python object or a string
            containing the fully qualified name of the Python object. The
            Python object can be either a Python function or LangChain chain.
            If a string is passed, it must be in the format:
            `<fully qualified module name>:<fully qualified object name>`.
        test_cases: List of test cases to run.
        quality_measures: List of quality measures to compute.
        hparam_specs: List of hyperparameter specifications.
    """
    def __init__(
        self,
        id_or_name: Union[int, str],
        llm_program: Union[Callable, str]):
        """Create a test suite.
        
        Args:
            id_or_name: ID or name of the test suite.
            llm_program: LLM program to test. Either a Python object or a
                string containing the fully qualified name of the Python
                object. The Python object can be either a Python function or
                LangChain chain. If a string is passed, it must be in the
                format:
                `<fully qualified module name>:<fully qualified object name>`.
        """
        self.id_or_name = id_or_name
        self.llm_program = data_model.LazyCallable(llm_program)

        self.test_cases = []
        self.quality_measures = []
        self.hparam_specs = []


    def add(self, *args: Union[_TestSuiteComponent, List[_TestSuiteComponent]]):
        """Add test cases, quality measures, or hyperparameter specifications.
        
        Args:
            *args: One or more test cases, quality measures, or hyperparameter
                specifications to add to the test suite. If a list is passed,
                each item in the list is added to the test suite.
        """
        for arg in args:
            if isinstance(arg, TestCase):
                self.test_cases.append(arg)
            elif isinstance(arg, QualityMeasure):
                self.quality_measures.append(arg)
            elif isinstance(arg, HparamSpec):
                self.hparam_specs.append(arg)
            elif isinstance(arg, list):
                for item in arg:
                    self.add(item)
            else:
                raise TypeError(
                    "Invalid type. Expected TestCase, QualityMeasure, or HparamSpec, "
                    f"but got {type(arg)}.")
    
    def run(self, replicas: int = 1, parallelize: int = 1):
        """Run the test suite.

        Args:
            replicas: Number of replicated executions to perform for each
                (test case, unique set of hyperparameter values) pair.
            parallelize: Number of LLM program executions to run in parallel.
        """
        run_request = wire_model.CreateTestSuiteRunRequest(
            test_suite_id_or_name=self.id_or_name,
            test_cases=self.test_cases,
            quality_measures=self.quality_measures,
            hparam_specs=self.hparam_specs,
            llm_program_details=self.llm_program.get_details(),
            replicas=replicas,
            parallelize=parallelize,
        )
        cli.execute_test_suite_run(
            test_suite_run=run_request,
            auth_access_token=auth_session.get_auth_session().access_token,
            llm_program=self.llm_program.get_callable(),
        )


# The following module-private variables are used by the functions in
# the rest of this module to transmit information to and from LLM program
# executions.
# Whether the logger decorator (inductor.logger) is enabled. This is set to
# False when running tests to prevent the logger from sending duplicate data to
# the backend, in the case that the LLM program being tested uses the logger
# decorator.
_logger_decorator_enabled = True
# Context variable used to store the logged values for the current LLM program
# execution. This is a context variable instead of a global variable so that
# the logger will work correctly when running mutliple threads that each use
# the logger decorator. However, an exception will be raised if the logger
# decorated function itself uses multiple threads that each call inductor.log.
_logged_values = contextvars.ContextVar("logged_values", default=None)
# Dictionary of hyperparameter values for the current LLM program execution.
_hparams = {}
# Context variable used to store whether the current LLM program execution is
# the primary execution.
_primary_execution = contextvars.ContextVar("active_execution", default=True)


def hparam(name: str, default_value: Any) -> Any:
    """Return the value of the hyperparameter having the given name.

    Args:
        name: Name of hyperparameter value to be returned.
        default_value: Value that will be returned if a value has not
            been specified for the given name.
    """
    return _hparams.get(name, default_value)


def _log(
    value: Any, *, after_complete: bool, description: Optional[str] = None):
    """Log a value and associate it with the current LLM program execution.

    Args:
        value: The value to be logged.
        after_complete: Whether the value was logged after the LLM
            program execution completed.
        description: An optional human-readable description of the logged
            value.
    
    Raises:
        RuntimeError: If the LLM program execution was not initiated via the
            Inductor CLI, and the LLM program is not decorated with
            @inductor.logger.
    """
    logged_values = _logged_values.get()
    if logged_values is None:
        # We can not distinguish between the below two cases described in the
        # exception message, so we raise the same exception in both cases.
        raise RuntimeError(
            "Cannot call inductor.log outside of a function decorated with "
            "@inductor.logger, unless you are running `inductor test`. "
            "Also note that invoking inductor.log from a thread different "
            "from the one that initialized the logger (via the decorator or "
            "the CLI tool) is currently unsupported. If you require support "
            "for this, please contact Inductor support to submit a feature "
            "request.")
    logged_values.append(
        wire_model.LoggedValue(
            value=copy.deepcopy(value),
            description=description,
            after_complete=after_complete))


def log(value: Any, *, name: Optional[str] = None):
    """Log a value and associate it with the current LLM program execution.

    Args:
        value: The value to be logged.
        name: An optional human-readable name for the logged value.
    
    Raises:
        RuntimeError: If the LLM program execution was not initiated via the
            Inductor CLI, and the LLM program is not decorated with
            @inductor.logger.
    """
    _log(value, description=name, after_complete=False)


@contextlib.contextmanager
def _configure_for_test(hparams: Dict[str, Any]):
    """Configure the Inductor library for a test suite run.
    
    Disable the inductor.logger decorator by setting
    `inductor._logger_decorator_enabled` to False and set the inductor._hparams
    to the given hyperparameters. On exit, restore the original value of
    `inductor._logger_decorator_enabled` and set `inductor._hparams` to an
    empty dictionary.

    Args:
        hparams: A dictionary mapping hyperparameter names to values.
    """
    global _hparams
    global _logger_decorator_enabled
    orig_logger_decorator_enabled = _logger_decorator_enabled
    try:
        _hparams = hparams
        _logger_decorator_enabled = False
        yield
    finally:
        _hparams = {}
        _logger_decorator_enabled = orig_logger_decorator_enabled


@contextlib.contextmanager
def _capture_logged_values():
    """Capture values logged via log() calls.
    
    If logging has not already been initialized, initialize logging by setting
    the logged values context variable (`_logged_values`) to an empty list,
    and, on exit, set `_logged_values` to `None`.
    If logging has already been initialized, do nothing.
    In either case, yield the list of logged values.

    The purpose of this context manager is to manage the state of the
    logged values context variable, which should only be initialized
    once per LLM program execution.

    Yields:
        The list of logged values.
    """
    logged_values = _logged_values.get()
    initializing_logged_values = logged_values is None
    try:
        if initializing_logged_values:
            _logged_values.set([])
        yield _logged_values.get()
    finally:
        if initializing_logged_values:
            _logged_values.set(None)


@contextlib.contextmanager
def _capture_stdout_stderr(
    suppress: bool = False) -> Tuple[io.StringIO, io.StringIO]:
    """Capture stdout and stderr.
    
    On exit, restore the original stdout and stderr and close the yielded
    StringIO buffers (i.e., the yielded buffers' contents will be discarded
    when context manager exits).
    
    Args:
        suppress: Whether to suppress stdout and stderr. If True, the
            contents of stdout and stderr will be suppressed after being
            captured. If False, stdout and stderr will behave as normal,
            but their contents will still be captured.

    Yields:
        A tuple of streams used to capture stdout and stderr.
    """
    class Tee(io.StringIO):
        """A StringIO buffer that optionally writes to a file in addition to
        capturing the written string."""
        def __init__(self, file: Optional[TextIO]):
            """Override the constructor to store the file to which to write."""
            self.file = file
            super().__init__()

        def write(self, s: str):
            """Override the write method to write to the file (as merited)
            in addition to capturing the written string."""
            if self.file is not None:
                self.file.write(s)
            return super().write(s)

    stdout_capture = Tee(
        sys.stdout if not suppress else None)
    stderr_capture = Tee(
        sys.stderr if not suppress else None)

    # Save the original stdout and stderr.
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    # Redirect stdout and stderr to the Tee objects.
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture
    try:
        yield (stdout_capture, stderr_capture)
    finally:
        # Restore the original stdout and stderr.
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        # Close the StringIO buffers.
        stdout_capture.close()
        stderr_capture.close()


@contextlib.contextmanager
def _manage_executions():
    """Manage the state of the primary execution context variable.

    Manage the state of the primary execution context variable
    (_primary_execution). If the variable is initially True, it is set to
    False and True is yielded. If the variable is initially False, False is
    yielded. On exit, the variable is restored to its original value.

    The purpose of this context manager is to allow the logger decorator to
    determine whether it is the primary (top-level) execution. This is
    necessary because the logger decorator should only send data to the
    backend if it is the primary execution. For example, when the logger
    decorator decorates a function that is called by another function also
    decorated with the logger decorator, the logger decorator should not send
    data to the backend during the inner function call.

    Yields:
        True if the primary execution context variable was True, False
        otherwise.
    """
    primary_execution = _primary_execution.get()
    if primary_execution:
        _primary_execution.set(False)
    try:
        yield primary_execution
    finally:
        _primary_execution.set(primary_execution)


# Type variable for the _GeneratorWrapper class.
_T_GeneratorWrapper = TypeVar("_T_GeneratorWrapper", bound="_GeneratorWrapper")  # pylint: disable=invalid-name


class _GeneratorWrapper:
    """Wrapper for a generator that captures the values yielded.

    When the generator is exhausted, the wrapper logs the completion of the
    LLM program execution to Inductor.
    """
    def __init__(
        self,
        generator: Generator[Any, Any, Any],
        *,
        primary_execution: bool,
        llm_program: data_model.LazyCallable,
        input_args: Dict[str, Any],
        started_at: datetime.datetime,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
        logged_values: Optional[List[wire_model.LoggedValue]] = None,
        auth_access_token: str,):
        """Create a GeneratorWrapper.
        
        Args:
            generator: Generator to wrap.
            primary_execution: Whether the LLM program execution is the
                primary execution.
            llm_program: LLM program that was executed.
            input_args: Input arguments to the LLM program.
            started_at: Time at which the LLM program execution started.
            stdout: Captured stdout from the LLM program execution.
            stderr: Captured stderr from the LLM program execution.
            logged_values: Values logged during the LLM program execution.
            auth_access_token: Access token used to authenticate the request
                to the backend.
        """
        self._generator = generator
        self._completed_values = []

        self._primary_execution = primary_execution
        self._llm_program = llm_program
        self._input_args = input_args
        self._started_at = started_at
        self._stdout = stdout
        self._stderr = stderr
        self._logged_values = logged_values
        self._auth_access_token = auth_access_token

    def __iter__(self) -> _T_GeneratorWrapper:
        return self

    def __next__(self) -> Any:
        try:
            value = next(self._generator)
            self._completed_values.append(copy.deepcopy(value))
        except StopIteration as stop_signal:
            if all(isinstance(value, str) for value in self._completed_values):
                self._completed_values = "".join(self._completed_values)
            _log_completed_execution(
                output=self._completed_values,
                primary_execution=self._primary_execution,
                llm_program=self._llm_program,
                input_args=self._input_args,
                started_at=self._started_at,
                stdout=self._stdout,
                stderr=self._stderr,
                logged_values=self._logged_values,
                auth_access_token=self._auth_access_token,
            )
            raise stop_signal
        return value


def _log_completed_execution(
    *,
    output: Any,
    primary_execution: bool,
    llm_program: data_model.LazyCallable,
    input_args: Dict[str, Any],
    error: Optional[str] = None,
    stdout: Optional[str] = None,
    stderr: Optional[str] = None,
    logged_values: Optional[List[wire_model.LoggedValue]] = None,
    started_at: datetime.datetime,
    auth_access_token: str,
    ) -> Any:
    """Log the completion of an LLM program execution.

    If the LLM program execution is the primary execution, send the execution
    data to the backend. Otherwise, call the Inductor client's `log()`
    function to log this execution as part of the current overarching
    primary execution.

    Args:
        output: Result of the LLM program execution.
        primary_execution: Whether the LLM program execution is the primary
            execution.
        llm_program: LLM program that was executed.
        input_args: Input arguments to the LLM program.
        error: Error message, if any, that occurred during the LLM program
            execution.
        stdout: Captured stdout from the LLM program execution.
        stderr: Captured stderr from the LLM program execution.
        logged_values: Values logged during the LLM program execution.
        started_at: Time at which the LLM program execution started.
        auth_access_token: Access token used to authenticate the request to
            the backend.
    """
    ended_at = datetime.datetime.now(datetime.timezone.utc)

    if primary_execution:
        backend_client.log_llm_program_execution_request(
            wire_model.LogLlmProgramExecutionRequest(
                program_details=llm_program.get_details(),
                execution_details=wire_model.ExecutionDetails(
                    mode="DEPLOYED",
                    inputs=input_args,
                    hparams=_hparams or None,
                    output=output,
                    error=error,
                    stdout=stdout,
                    stderr=stderr,
                    logged_values=logged_values or None,
                    execution_time_secs=(
                        ended_at - started_at).total_seconds(),
                    started_at=started_at,
                    ended_at=ended_at,)),
            auth_access_token)

    else:
        log(
            {
                "llm_program":
                llm_program.fully_qualified_name,
                "inputs": input_args,
                "output": output
            },
            name="Nested LLM program execution")


def logger(func: Callable) -> Callable:
    """Log the inputs, outputs, and inductor.log calls of func.

    Use `logger` as a decorator to automatically log the arguments and return
    value of, as well as calls to inductor.log within, the decorated function.
    For example:
        @inductor.logger
        def hello_world(name: str) -> str:
            inductor.log(len(name), description="name length")
            return f"Hello {name}!"

    Args:
        func: The decorated function.
    
    Returns:
        Wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if _logger_decorator_enabled:
            with (
                _capture_logged_values() as logged_values,
                _manage_executions() as primary_execution,
                # TODO: We don't need to capture stdout and stderr if we are
                # not in the primary execution. However since the stdout and
                # stderr are not suppressed, the user will not notice the
                # difference.
                _capture_stdout_stderr(suppress=False) as (stdout, stderr)
            ):
                auth_access_token = auth_session.get_auth_session().access_token

                llm_program = data_model.LazyCallable(func)

                # Get input arguments using the function's signature.
                signature = inspect.signature(func)
                bound_arguments = signature.bind(*args, **kwargs)
                bound_arguments.apply_defaults()
                input_args = copy.deepcopy(bound_arguments.arguments)

                started_at = datetime.datetime.now(datetime.timezone.utc)
                result = None
                error = None
                try:
                    result = func(*args, **kwargs)
                    if inspect.isgenerator(result):
                        return _GeneratorWrapper(
                            result,
                            primary_execution=primary_execution,
                            llm_program=llm_program,
                            input_args=input_args,
                            started_at=started_at,
                            stdout=stdout.getvalue(),
                            stderr=stderr.getvalue(),
                            logged_values=logged_values,
                            auth_access_token=auth_access_token,
                        )
                except Exception as e:  # pylint: disable=broad-except
                    error = str(e)

                _log_completed_execution(
                    output=copy.deepcopy(result),
                    primary_execution=primary_execution,
                    llm_program=llm_program,
                    input_args=input_args,
                    started_at=started_at,
                    error=error,
                    stdout=stdout.getvalue(),
                    stderr=stderr.getvalue(),
                    logged_values=logged_values,
                    auth_access_token=auth_access_token,
                )
                return result
        else:
            return func(*args, **kwargs)
    return wrapper
