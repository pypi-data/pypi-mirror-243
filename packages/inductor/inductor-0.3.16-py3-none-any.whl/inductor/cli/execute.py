# Copyright 2023 Inductor, Inc.
"""Functionality for executing a test suite run."""

import datetime
import inspect
import itertools
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import loky

import inductor
from inductor.cli import data_model
from inductor import backend_client, wire_model


def _execute_test_case(
    test_suite_run_id: int,
    llm_program_fully_qualified_name: str,
    test_case: wire_model.TestCase,
    test_case_id: int,
    test_case_replica_index: int,
    quality_measures: List[wire_model.QualityMeasure],
    quality_measure_ids: List[int],
    hparams: Dict[str, Any],
    auth_access_token: str,
    llm_program: Optional[Callable] = None
) -> Tuple[
    wire_model.LogTestCaseExecutionRequest,
    List[Dict[str, Union[
        int, str, wire_model.QualityMeasureExecutionDetails]]]]:
    """Run a test case and evaluate its quality measures.

    Sends the output of the test case and the outputs of the quality measures
    to the backend server.

    Args:
        test_suite_run_id: ID of test suite run.
        llm_program_fully_qualified_name: Fully qualified name of LLM program.
        test_case: Test case.
        test_case_id: ID of test case.
        test_case_replica_index: Index of test case replica.
        quality_measures: List of quality measures.
        quality_measure_ids: IDs of quality measures.
        hparams: Mapping from hyperparameter names to values.
        auth_access_token: Auth0 access token.
        llm_program: Callable object representing the LLM program. If
            None, then the LLM program will be imported from the fully
            qualified name.
    
    Returns:
        A tuple of the LogTestCaseExecutionRequest and a list of invalid
            quality measures if any. Each invalid quality measure is a
            Dictionary with the following keys:
                "id": ID of quality measure.
                "name": Name of quality measure.
                "execution_details": wire_model.QualityMeasureExecutionDetails
                    object.
    """
    started_at = datetime.datetime.now(datetime.timezone.utc)

    llm_program_stdout = None
    llm_program_stderr = None
    llm_program_error = None
    llm_program_output = None
    with (
        inductor._capture_stdout_stderr(suppress=True) as (stdout, stderr),  # pylint: disable=protected-access
        inductor._capture_logged_values() as logged_values,  # pylint: disable=protected-access
        inductor._configure_for_test(hparams)  # pylint: disable=protected-access
    ):
        try:
            # Run the LLM program.
            if llm_program is None:
                llm_program = data_model.LazyCallable(
                    llm_program_fully_qualified_name)
            llm_program_output = llm_program(**test_case.inputs)
            if inspect.isgenerator(llm_program_output):
                llm_program_output = list(llm_program_output)
                if all(isinstance(value, str) for value in llm_program_output):
                    llm_program_output = "".join(llm_program_output)

        except Exception as error:  # pylint: disable=broad-except
            llm_program_error = str(error)

        llm_program_stdout = stdout.getvalue()
        llm_program_stderr = stderr.getvalue()

    ended_at = datetime.datetime.now(datetime.timezone.utc)

    # If the LLM program completed without error, run the executable quality
    # measures to generate a list of direct evaluations.
    direct_evaluations = []
    # For any executable quality measures that raises an error, or returns a
    # non-integer, non-boolean output, add it to the list of invalid quality
    # measures. TODO: Log quality measure errors on the backend.
    invalid_quality_measures = []
    if llm_program_error is None:

        # Run the executable quality measures.
        quality_measures_outputs = []
        for quality_measure, quality_measure_id in zip(
            quality_measures, quality_measure_ids):
            if quality_measure.evaluator == "FUNCTION":

                # TODO: Record quality measure errors, stdout, and stderr on
                # the backend. See wire_model.QualityMeasureExecutionDetails
                # for the additional TODO of how these should be recorded.
                quality_measure_stdout = None
                quality_measure_stderr = None
                quality_measure_error = None
                quality_measure_output = None
                with inductor._capture_stdout_stderr(  # pylint: disable=protected-access
                    suppress=True) as (stdout, stderr):
                    try:
                        callable_object = data_model.LazyCallable(
                            quality_measure.spec)
                        quality_measure_output = callable_object(
                            llm_program_output)
                    except Exception as error:  # pylint: disable=broad-except
                        quality_measure_error = str(error)

                    quality_measure_stdout = stdout.getvalue()
                    quality_measure_stderr = stderr.getvalue()

                quality_measure_execution_details = (
                    wire_model.QualityMeasureExecutionDetails(
                        input=llm_program_output,
                        output=quality_measure_output,
                        error=quality_measure_error,
                        stdout=quality_measure_stdout,
                        stderr=quality_measure_stderr,
                    )
                )

                if quality_measure_error is not None:
                    invalid_quality_measures.append({
                        "id": quality_measure_id,
                        "name": quality_measure.name,
                        "execution_details": quality_measure_execution_details,
                    })

                else:
                    quality_measures_outputs.append((
                        quality_measure_id,
                        quality_measure,
                        quality_measure_execution_details,
                    ))


        # Create direct evaluations for the quality measures that are
        # executable and valid. If a quality measure that is executable
        # returns an output type that does not match the quality measure's
        # evaluation type, then add it to the list of invalid quality
        # measures and do not create a direct evaluation for it.
        for (
            quality_measure_id,
            quality_measure,
            quality_measure_execution_details,
        ) in quality_measures_outputs:
            quality_measure_output = quality_measure_execution_details.output
            if quality_measure.evaluation_type == "BINARY" and isinstance(
                quality_measure_output, bool):
                direct_evaluations.append(
                    wire_model.DirectEvaluation(
                        quality_measure_id=quality_measure_id,
                        value_bool=quality_measure_output))
            elif (quality_measure.evaluation_type == "RATING_INT" and
                    isinstance(quality_measure_output, int) and
                    # Required to prevent `bool` from being interpreted as
                    # `int`, since `bool` is a subclass of `int`.
                    not isinstance(quality_measure_output, bool)):
                direct_evaluations.append(
                    wire_model.DirectEvaluation(
                        quality_measure_id=quality_measure_id,
                        value_int=quality_measure_output))
            else:
                expected_output_type = (
                    type(True) if quality_measure.evaluation_type == "BINARY"
                    else type(5))
                quality_measure_execution_details.error = (
                    f"Invalid output type. Expected output type: "
                    f"{expected_output_type}. Actual output type: "
                    f"{type(quality_measure_output)}")
                invalid_quality_measures.append({
                    "id": quality_measure_id,
                    "name": quality_measure.name,
                    "execution_details": quality_measure_execution_details,
                })

    request_object = wire_model.LogTestCaseExecutionRequest(
        test_suite_run_id=test_suite_run_id,
        test_case_id=test_case_id,
        test_case_replica_index=test_case_replica_index,
        execution_details=wire_model.ExecutionDetails(
            mode="CLI",
            inputs=test_case.inputs,
            hparams=hparams or None,
            output=llm_program_output,
            error=llm_program_error,
            stdout=llm_program_stdout,
            stderr=llm_program_stderr,
            execution_time_secs=(ended_at - started_at).total_seconds(),
            started_at=started_at,
            ended_at=ended_at,
            logged_values=logged_values or None,
            direct_evaluations=direct_evaluations or None,
        )
    )

    backend_client.log_test_case_execution(request_object, auth_access_token)
    return request_object, invalid_quality_measures

def get_hparams_combinations(
    hparam_specs: Optional[List[wire_model.HparamSpec]] = None
    ) -> List[Dict[str, Any]]:
    """Get all combinations of hyperparameters.

    Given a list of hyperparameters and their possible values, return a list of
    dictionaries, where each dictionary represents a unique combination of
    hyperparameters.

    For example, if the given hyperparameters are:
    [
        wire_model.HparamSpec(
            hparam_name="a",
            values=[1, 2],
        ),
        wire_model.HparamSpec(
            hparam_name="b",
            values=[3, 4],
        ),
    ]
    then the returned list will be:
    [
        {"a": 1, "b": 3},
        {"a": 1, "b": 4},
        {"a": 2, "b": 3},
        {"a": 2, "b": 4},
    ]

    Args:
        hparam_specs: List of hyperparameters specs, where all hyperparameter
            specs have distinct names.

    Returns:
        A list of dictionaries, where each dictionary represents a unique
            combination of hyperparameters.

    Raises:
        ValueError: If hyperparameter names are not distinct.
    """
    if hparam_specs is None:
        return [{}]

    # Convert list of HparamSpec to dictionary
    hparams_dict = {
        hparam.hparam_name: hparam.values for hparam in hparam_specs}

    # Ensure that all hyperparameter names in hparam_specs are distinct.
    if len(hparams_dict) != len(hparam_specs):
        raise ValueError(
            "Hyperparameter names in hparam_specs must be distinct.")

    keys = list(hparams_dict.keys())
    value_lists = [hparams_dict[key] for key in keys]

    # Generate combinations.
    value_combinations = list(itertools.product(*value_lists))

    # Convert to dictionaries.
    hparam_combinations = []
    for value_combination in value_combinations:
        hparam_combinations.append(
            {k: v for k, v in zip(keys, value_combination)})

    return hparam_combinations


def execute_test_suite_run(
    test_suite_run: wire_model.CreateTestSuiteRunRequest,
    test_suite_run_metadata: wire_model.CreateTestSuiteRunResponse,
    executor: loky.Executor,
    auth_access_token: str,
    llm_program: Optional[Callable] = None
) -> List[loky.Future]:
    """Execute a test suite run.

    Args:
        test_suite_run: Test suite run.
        test_suite_run_metadata: Test suite run metadata.
        executor: Executor for running test cases.
        auth_access_token: Auth0 access token.
        llm_program: Callable object representing the LLM program. If
            None, then the LLM program will be imported from the fully
            qualified name specified in test_suite_run.

    Returns:
        List of futures for the test case outputs.
    """
    test_case_futures = []
    for test_case_replica_index in range(test_suite_run.replicas):
        for hparams in get_hparams_combinations(test_suite_run.hparam_specs):
            for test_case, test_case_id in zip(
                test_suite_run.test_cases,
                test_suite_run_metadata.test_case_ids):
                test_case_futures.append(executor.submit(
                    _execute_test_case,
                    test_suite_run_id=
                        test_suite_run_metadata.test_suite_run_id,
                    llm_program_fully_qualified_name=
                        test_suite_run.llm_program_details.fully_qualified_name,
                    test_case=test_case,
                    test_case_id=test_case_id,
                    test_case_replica_index=test_case_replica_index,
                    quality_measures=test_suite_run.quality_measures,
                    quality_measure_ids=
                        test_suite_run_metadata.quality_measure_ids,
                    hparams=hparams,
                    auth_access_token=auth_access_token,
                    llm_program=llm_program,
                ))
    return test_case_futures
