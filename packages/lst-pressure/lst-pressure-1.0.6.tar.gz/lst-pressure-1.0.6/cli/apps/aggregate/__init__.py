from ..AppInterface import AppInterface
from typing import Self
import os
import subprocess
from logger import error
import sys


SQL_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "sql")
existing_reports = [
    f.replace(".sql", "")
    for f in os.listdir(SQL_FOLDER_PATH)
    if os.path.isfile(os.path.join(SQL_FOLDER_PATH, f))
]
quoted_existing_reports = ", ".join([f'"{r}"' for r in existing_reports])


class Aggregate(AppInterface):
    id = "aggregate"
    usage = "lstpressure aggregate -h"
    description = "Aggregate observables using built-in reports or bespoke SQL commands"

    def build(self) -> Self:
        self.parser_sub.add_argument(
            "--input",
            required=False,
            type=str,
            metavar="",
            help="Path to lst-pressure output csv file (if not provided, stdin is used instead)",
        )
        self.parser_sub.add_argument(
            "--query",
            required=True,
            type=str,
            metavar="",
            help=f'SQL string to apply to input CSV (i.e. "select * from stdin"), or apply a built-in aggregation: {quoted_existing_reports}',
        )
        self.parser_sub.add_argument(
            "--echo",
            required=False,
            default=False,
            action="store_true",
            help=f"Echo the aggregation query back - useful for evaluating .sql file contents that would otherwise be opaque. For example: --echo --query {existing_reports[0]}",
        )

        return self

    def parse(self, args) -> Self:
        self.echo = args.echo
        self.input = args.input
        self.query = parse_sql_query(args.query)
        return self

    def exe(self) -> Self:
        if self.echo:
            print(self.query)
            exit()

        if not self.input:
            if not sys.stdin.isatty():
                input_csv = sys.stdin.read()
            else:
                error(
                    "No input provided. Please either provide a filepath (--input), or pipe a CSV-formatted string from stdin"
                )
                exit(1)
        else:
            with open(self.input, "r") as file:
                input_csv = file.read()

        result = execute_csvsql(input_csv, self.query)

        # Print result to stdout
        print(result)
        exit()


def parse_sql_query(text):
    # Check if the query_input is a file
    if os.path.isfile(text):
        with open(text, "r") as file:
            return file.read().strip()

    # Try to find the SQL file if it's included in the tool
    view_path = os.path.join(SQL_FOLDER_PATH, f"{text}")

    # Name of view without .sql
    if os.path.isfile(view_path):
        with open(view_path, "r") as file:
            return file.read().strip()

    # Name of view with .sql
    if os.path.isfile(view_path + ".sql"):
        with open(view_path + ".sql", "r") as file:
            return file.read().strip()

    # If not a file, assume it's a SQL string
    return text


def execute_csvsql(input_content, sql):
    command = ["csvsql", "--query", sql]

    try:
        # Use subprocess.Popen to run the command
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )

        # Pass input content to the subprocess
        output, _ = process.communicate(input=input_content)

        # Wait for the process to finish and get the return code
        return_code = process.wait()

        if return_code == 0:
            return output
        else:
            error(f"csvsql process returned a non-zero exit code: {return_code}")
            error(f"Command output: {output}")
            return None
    except Exception as e:
        raise e


__all__ = ["parse_sql_query", "Aggregate", "execute_csvsql"]
