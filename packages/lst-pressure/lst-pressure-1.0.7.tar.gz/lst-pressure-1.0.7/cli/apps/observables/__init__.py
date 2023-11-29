from typing import Self
from datetime import datetime, timedelta
import re
from conf import Conf, SunProvider
from lstpressure import LSTIntervalType as I, Observation, LST
from ..AppInterface import AppInterface
from ..aggregate import parse_sql_query, execute_csvsql, quoted_existing_reports
from logger import error
import sys
import pandas as pd
from io import StringIO

conf = Conf()

filter_mapping = {
    I.NIGHT.name: I.NIGHT,
    I.SUNRISE_SUNSET.name: I.SUNRISE_SUNSET,
    I.ALL_DAY.name: I.ALL_DAY,
    I.SUNSET_SUNRISE.name: I.SUNSET_SUNRISE,
    I.OBSERVATION_WINDOW.name: I.OBSERVATION_WINDOW,
}


def parseDateInput(input: str) -> str:
    # Check if the input is a direct date
    if re.match(r"^\d{8}$", input):
        return input

    # Handle relative date inputs
    input = input.upper()
    current_date = datetime.now()
    match = re.match(r"^([-+])(\d+)([DMY])$", input)
    if match:
        sign, value, unit = match.groups()
        value = int(value)

        if unit == "D":
            # Add or subtract days
            if sign == "+":
                new_date = current_date + timedelta(days=value)
            else:
                new_date = current_date - timedelta(days=value)
        elif unit == "M":
            # Add or subtract months
            if sign == "+":
                new_month = current_date.month - 1 + value
            else:
                new_month = current_date.month - 1 - value

            year = current_date.year + new_month // 12
            month = new_month % 12 + 1
            day = min(
                current_date.day,
                [
                    31,
                    29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28,
                    31,
                    30,
                    31,
                    30,
                    31,
                    31,
                    30,
                    31,
                    30,
                    31,
                ][new_month % 12],
            )
            new_date = datetime(year, month, day)
        elif unit == "Y":
            # Add or subtract years
            if sign == "+":
                new_date = current_date.replace(year=current_date.year + value)
            else:
                new_date = current_date.replace(year=current_date.year - value)

        return new_date.strftime("%Y%m%d")

    # If the input format is unrecognized
    raise ValueError("Invalid input format")


class Observables(AppInterface):
    id = "observables"
    usage = "lstpressure observables -h"
    description = "Generate a list of observables (slots where OPT observations can be observed)"

    def build(self) -> Self:
        self.parser_sub.add_argument(
            "--start",
            type=str,
            default=datetime.today().strftime("%Y%m%d"),
            help="The start date in the format 'YYYYMMDD'. Defaults to today",
            metavar="",
        )

        self.parser_sub.add_argument(
            "--end",
            type=str,
            required=False,
            default=None,
            help="The end date in the format 'YYYYMMDD'. Defaults to --start",
            metavar="",
        )

        self.parser_sub.add_argument(
            "--input",
            required=False,
            type=str,
            help="Path to an OPT csv download. If this is omitted, provide the CSV file contents via stdin",
            metavar="",
        )

        self.parser_sub.add_argument(
            "--output",
            type=str,
            help="Path to the output csv file",
            metavar="",
        )

        self.parser_sub.add_argument(
            "--sun-provider",
            type=lambda s: s.upper(),
            choices=list(SunProvider.__members__),
            default="ASTRAL",
            help="Specify the sun provider for calculating sun statistics and for calculating intervals. Defaults to use the Astral library, intervals using the dawn, sunrise, sunset, dusk events. Choose between: ASTRAL (default) or MEERKAT",
            metavar="",
        )

        self.parser_sub.add_argument(
            "--filter",
            type=str,
            required=False,
            metavar="",
            help=f"Select from: {', '.join(list(filter_mapping.keys()))}",
        )

        self.parser_sub.add_argument(
            "--lat",
            metavar="D:M:S",
            default=None,
            nargs="?",
            type=str,
            help="The latitude for the observation in the format 'D:M:S'. Default is '-30:42:39.8' (value must be quoted --lat=\"location\")",
        )

        self.parser_sub.add_argument(
            "--long",
            metavar="D:M:S",
            default=None,
            nargs="?",
            type=str,
            help="The longitude for the observation in the format 'D:M:S'. Default is '21:26:38.0' (value must be quoted --long=\"location\")",
        )

        self.parser_sub.add_argument(
            "--aggregate",
            required=False,
            type=str,
            metavar="",
            help=f'Apply a SQL aggregation to the CSV before printing to a file/stdout, or apply a built-in aggregation: {quoted_existing_reports}. The CSV is provided as a relation called "stdin"',
        )

        return self

    def parse(self, args) -> Self:
        if args.lat or args.long:
            if SunProvider[args.sun_provider] == SunProvider.MEERKAT:
                error(
                    "The MEERKAT provider has set lat/long coordinates that can't be overriden. Either use a different sun-provider or don't specify --lat and --long"
                )
                exit(1)

        if args.lat and args.lat != "":
            conf.LATITUDE = args.lat
        if args.long and args.long != "":
            conf.LONGITUDE = args.long
        self.input = args.input
        self.start = parseDateInput(args.start)
        self.end = parseDateInput(args.end) if args.end else self.start
        conf.SUN_PROVIDER = SunProvider[args.sun_provider]

        filter_name = args.filter
        if filter_name and not filter_mapping.get(filter_name.upper()):
            error(f"Invalid filter name, valid options: {', '.join(list(filter_mapping.keys()))}")
            exit(1)
        self.filter_value = (
            None if not filter_name else filter_mapping.get(filter_name.upper(), None)
        )

        self.output = args.output if args.output else None
        self.aggregate = args.aggregate if args.aggregate else None
        return self

    def exe(self) -> Self:
        sql = parse_sql_query(self.aggregate) if self.aggregate else None

        def observation_filter(observation: Observation):
            if self.filter_value in observation.utc_constraints:
                return True
            return False

        if not self.input:
            if not sys.stdin.isatty():
                input = pd.read_csv(StringIO(sys.stdin.read()))
            else:
                error(
                    "No input provided. Please either provide a filepath (--input), or pipe a CSV-formatted string from stdin"
                )
                exit(1)
        else:
            input = self.input

        output_csv_string = LST(
            input,
            calendar_start=self.start,
            calendar_end=self.end,
            observation_filter=observation_filter if self.filter_value else None,
            latitude=conf.LATITUDE,
            longitude=conf.LONGITUDE,
        ).to_csv_string()

        output_string = execute_csvsql(output_csv_string, sql) if sql else output_csv_string

        if self.output:
            with open(self.output, "w") as f:
                f.write(output_string)
        else:
            print(output_string)

        return self
