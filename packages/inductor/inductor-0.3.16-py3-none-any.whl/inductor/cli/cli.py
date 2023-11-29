# Copyright 2023 Inductor, Inc.
"""Entrypoint for the Inductor CLI."""

import contextlib
import datetime
import textwrap
from typing import Annotated, Any, Callable, Dict, List, Optional
from pathlib import Path

import inquirer
import loky
import rich
from rich import console, progress, syntax
import typer
import yaml

from inductor.cli import data_model, execute, questions
from inductor import auth_session, backend_client, config, wire_model


app = typer.Typer()


def _create_test_suite_file(
    auth_access_token: str,
    default_vars: Optional[Dict[str, Any]] = None,):
    """Prompt user for test suite info to create a test suite file.

    1. Prompt user to create a new test suite or use an existing one.
    2. If creating a new test suite, prompt user for test suite info.
    3. If using an existing test suite, prompt user to select one.
    4. Create a test suite file with the provided info.
    
    Args:
        auth_access_token: Auth0 access token.
        default_vars: Optional dictionary containing default values for
            populating the test suite file. Only items with keys that are
            in the `model.TestSuiteRun` dataclass will be used.
    """
    if default_vars is None:
        default_vars = {}
    test_suite_args = data_model.process_test_suite_args(default_vars)

    create_new_test_suite = questions.choose_new_test_suite()

    if create_new_test_suite:
        rich.print("Creating a new test suite file ...")
        test_suite_file_path = questions.get_new_test_suite_file_path()
        test_suite_args["name"] = questions.get_test_suite_name()
        test_suite_args["description"] = questions.get_test_suite_description()

        if test_suite_args.get("llm_program_fully_qualified_name") is None:
            test_suite_args["llm_program_fully_qualified_name"] = (
                questions.get_llm_program_fully_qualified_name())

        test_suite_args["id"] = None

    else:
        # TODO: This `else` block is a placeholder until the backend is
        # implemented.
        # existing_test_suites = backend_client.get_existing_test_suites()
        # inquirer.list_input(
        #     "Select test suite to use", choices=existing_test_suites)
        # existing_test_suite_args = {}
        # test_suite_args["llm_program_fully_qualified_name"] = "module:object"
        # test_suite_args["id"] = "123"
        # test_suite_args = data_model.merge_test_suite_args(
        #     priority_1_dict=test_suite_args,
        #     priority_2_dict=existing_test_suite_args)
        # raise NotImplementedError("Use existing test suite not implemented.")
        rich.print("To use an existing test suite, run `inductor test "
                   "\[TEST_SUITE_FILE_PATH]`.")  # pylint: disable=anomalous-backslash-in-string
        raise typer.Exit()

    # Get parameter keys from LLM program to populate
    # the test suite file's test case section.
    llm_program = data_model.LazyCallable(
        test_suite_args["llm_program_fully_qualified_name"])
    llm_program_param_keys = llm_program.inputs_signature.keys()
    inputs = {}
    for key in llm_program_param_keys:
        inputs[key] = "<REPLACE WITH VALUE>"

    # Create test suite file contents.
    newline = "\n"
    yaml_string = textwrap.dedent(f"""
    # Test suite file

    # Test suite configuration
    - config:
        id: <WILL BE POPULATED AUTOMATICALLY>
        # name: {test_suite_args["name"]}
        # description: {
            test_suite_args["description"]
            if test_suite_args["description"] is not None
            else ""}
        llm_program_fully_qualified_name: {
            test_suite_args["llm_program_fully_qualified_name"]}
        replicas: {test_suite_args.get("replicas", 1)}
        
    # A test case (add more `- test:` blocks to add more test cases)
    - test:
        inputs:
          {yaml.dump(inputs, sort_keys=False).strip().replace(
            newline, newline + "          ")}
    
    # Sample quality measure (add more `- quality:` blocks to add more
    # quality measures)
    # - quality:
    #     name: <REPLACE WITH HUMAN-READABLE NAME FOR QUALITY MEASURE>
    #     evaluator: <REPLACE WITH "FUNCTION" OR "HUMAN">
    #     evaluation_type: <REPLACE WITH "BINARY" OR "RATING_INT">
    #     # If evaluator is "FUNCTION", spec should be the fully qualified
    #     # name of your quality measure function (e.g., "my.module:my_function").
    #     # If evaluator is "HUMAN", spec should be the instruction or question
    #     # to be posed to a human evaluator.
    #     spec: <REPLACE WITH VALUE>

    # Sample hyperparameter specification (add more `- hparam:` blocks to add more
    # hyperparameters)
    # - hparam:
    #     name: <REPLACE WITH STRING-VALUED NAME FOR HYPERPARAMETER>
    #     type: <REPLACE WITH "SHORT_STRING", "TEXT", OR "NUMBER">
    #     values: <REPLACE WITH LIST OF VALUES FOR HYPERPARAMETER>
    """).lstrip()

    rich.print("\nTest suite file path:")
    rich.print(test_suite_file_path)
    rich.print("\nTest suite file contents:")
    yaml_string_with_syntax = syntax.Syntax(
        yaml_string, "yaml", theme="ansi_dark", line_numbers=True)
    rich_console = console.Console()
    rich_console.print(yaml_string_with_syntax)

    # Write the test suite file.
    confirm = inquirer.confirm(
        "Create test suite and write contents?",
        default=True)
    if confirm:
        # Create test suite on server if it does not already exist.
        if test_suite_args.get("id") is None:
            response = backend_client.create_test_suite(
                wire_model.CreateTestSuiteRequest(
                    name=test_suite_args["name"],
                    description=test_suite_args.get("description")),
                auth_access_token
            )
            test_suite_args["id"] = response.id
        rich.print("Test suite created.")
        # Replace the `id` field in the test suite file with the ID of the
        # test suite created on the server.
        yaml_string = yaml_string.replace(
            "<WILL BE POPULATED AUTOMATICALLY>", str(test_suite_args["id"]))

        # Write the test suite file.
        with open(test_suite_file_path, "w") as file:
            file.write(yaml_string)
        rich.print("Next, add test cases and quality measures to the file, "
                   "and run your test suite via `inductor test "
                   f"{test_suite_file_path}`")


@contextlib.contextmanager
def _manage_test_suite_run(
    test_suite_run: wire_model.CreateTestSuiteRunRequest,
    auth_access_token: str) -> wire_model.CreateTestSuiteRunResponse:
    """Send requests to the server to manage the creation/completion of a run.
    
    Send a request to the server to create a test suite run. Then, yield the
    response, which contains test suite run metadata. On exit, send a request
    to the server to mark the test suite run as complete.

    Args:
        test_suite_run: CreateTestSuiteRunRequest object.
        auth_access_token: Auth0 access token.

    Yields:
        CreateTestSuiteRunResponse object.
    """
    test_suite_run_metadata = backend_client.create_test_suite_run(
        test_suite_run, auth_access_token)
    try:
        yield test_suite_run_metadata
    finally:
        backend_client.complete_test_suite_run(
            wire_model.CompleteTestSuiteRunRequest(
                test_suite_run_id=
                    test_suite_run_metadata.test_suite_run_id,
                ended_at=
                    datetime.datetime.now(datetime.timezone.utc)),
            auth_access_token)


@app.command("test")
def test(
    test_suite_file_paths: Annotated[Optional[List[Path]], typer.Argument(help=(
        "One or more paths to test suites to run, separated by spaces."
    ))] = None,
    llm_program_fully_qualified_name: Annotated[Optional[str], typer.Option(  # pylint: disable=unused-argument
        "-l",
        "--llm_program",
        help=(
            "Fully qualified name of the Python object (in particular, a "
            "Python function or LangChain chain) representing this LLM "
            "program, in the format: "
            "`<fully qualified module name>:<fully qualified object name>` "
            "(e.g., `my.module:object`). <fully qualified module name> can be "
            "in the format: `path.to.module` or `path/to/module.py`."
    ))] = None,
    replicas: Annotated[Optional[int], typer.Option(  # pylint: disable=unused-argument
        "-r",
        "--replicas",
        help="Number of runs to execute for each test case in test suite(s)."
    )] = None,
    parallelize: Annotated[Optional[int], typer.Option(  # pylint: disable=unused-argument
        "-p",
        "--parallelize",
        help="Maximum number of test cases to run simultaneously in parallel."
    )] = None,
    # TODO: Add support for imports.
    # imports: Annotated[Optional[List[Path]], typer.Option(  # pylint: disable=unused-argument
    #     "-i",
    #     "--imports",
    #     help=("One or more paths to files containing additional test cases or "
    #           "quality measures to include in the test suite(s).")
    # )] = None,
    verbose: Annotated[Optional[bool], typer.Option(
        "-v",
        "--verbose",
        help="Print verbose output.",
    )] = False,
):
    """Run one or more Inductor test suites."""
    local_vars = locals()

    # TODO: Add verbose flag for the main CLI application.
    config.verbose = verbose

    # Every time the access token is requested from the session, it is
    # refreshed if it is expired.
    auth_access_token = auth_session.get_auth_session().access_token

    if not test_suite_file_paths:
        _create_test_suite_file(auth_access_token, local_vars)
        raise typer.Exit()
    test_suite_runs = data_model.get_test_suite_runs(local_vars)
    multiple_runs = len(test_suite_runs) > 1

    for i, test_suite_run in enumerate(test_suite_runs):

        if multiple_runs:
            rich.print(rich.rule.Rule(
                f"Test Suite {i+1} of {len(test_suite_file_paths)}",
                style="bold #ffffff"))

        def pluralize(count: int) -> str:
            return "s" if count != 1 else ""
        rich.print(f"Running {len(test_suite_run.test_cases)} test case"
              f"{pluralize(len(test_suite_run.test_cases))} "
              f"({test_suite_run.replicas} run"
              f"{pluralize(test_suite_run.replicas)} each) ...")

        execute_test_suite_run(
            test_suite_run,
            auth_access_token,
            prompt_open_results=not multiple_runs)


def execute_test_suite_run(
    test_suite_run: wire_model.CreateTestSuiteRunRequest,
    auth_access_token: str,
    *,
    llm_program: Optional[Callable] = None,
    prompt_open_results: bool = False):
    """Execute a test suite run.
    
    Execute a test suite run while displaying relevant information to the user,
    including a progress bar.
    
    Args:
        test_suite_run: CreateTestSuiteRunRequest object.
        auth_access_token: Auth0 access token.
        llm_program: Callable object representing the LLM program. If
            None, then the LLM program will be imported from the fully
            qualified name specified in test_suite_run.
        prompt_open_results: Whether to prompt the user to open the test
            suite run results in a browser.
    """
    with (
        loky.get_reusable_executor(
            max_workers=test_suite_run.parallelize) as executor,
        _manage_test_suite_run(
            test_suite_run, auth_access_token) as test_suite_run_metadata
    ):
        test_case_futures = execute.execute_test_suite_run(
            test_suite_run,
            test_suite_run_metadata,
            executor,
            auth_access_token,
            llm_program)

        rich.print(f"Go to {test_suite_run_metadata.url} to view results.")
        if prompt_open_results:
            open_url = inquirer.confirm(
                message="Open in browser?", default=True)
            if open_url:
                typer.launch(test_suite_run_metadata.url)

        # Display progress bar and optionally print test outputs.
        with progress.Progress() as progress_bar:
            progress_task = progress_bar.add_task(
                "Test Cases",
                total=(test_suite_run.replicas *
                        len(test_suite_run.test_cases) *
                        len(execute.get_hparams_combinations(
                            test_suite_run.hparam_specs))))

            for future in loky.as_completed(test_case_futures):
                progress_bar.advance(progress_task)
                test_output, invalid_quality_measures = future.result()
                if test_output.execution_details.error is not None:
                    progress_bar.console.print(
                        "\n[red][bold][ERROR] Test case execution "
                        "raised an exception.[/bold] The following "
                        "execution will be recorded as FAILED and "
                        "quality measures will not be evaluated:[/red]")
                    progress_bar.console.print(test_output)
                elif config.verbose:
                    progress_bar.console.print(test_output)
                if invalid_quality_measures:
                    progress_bar.console.print(
                        "\n[red][bold][ERROR] One or more quality "
                        "measures raised an exception or returned an "
                        "invalid value.[/bold] The following quality "
                        "measures will not be recorded as part of this "
                        "test case execution:[/red]")
                    progress_bar.console.print(invalid_quality_measures)

        rich.print("Run complete.")


# Required to enable subcommands with only one command.
# For more information, see:
# https://typer.tiangolo.com/tutorial/commands/one-or-multiple/#one-command-and-one-callback
# NOTE: This function should be removed when we add a second command.
# NOTE: The above is written as a comment, rather than a docstring, to prevent
#       it from displaying when the CLI is run with the --help flag.
@app.callback()
def callback():  # pylint: disable=missing-function-docstring
    pass
