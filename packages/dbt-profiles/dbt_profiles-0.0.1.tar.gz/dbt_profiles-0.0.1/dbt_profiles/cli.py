import argparse
import os
from pathlib import Path
from typing import Dict, cast

from PyInquirer.prompt import prompt
from rcheck import r

from .main import main

parser = argparse.ArgumentParser(
    prog="dbt_profiles_setup",
    description="CLI to setup your dbt profile",
)
parser.add_argument("-p", "--project-path", default=".", required=False)
parser.add_argument("-r", "--required-only", action="store_true")
# parser.add_argument("-r", "--required-only", action=argparse.BooleanOptionalAction)


def cli_main():
    args = parser.parse_args()

    dbt_project_dir = r.check_str("--project-path", args.project_path)
    required_only = r.check_bool("--required-only", args.required_only)

    dbt_profiles_dir = os.environ.get("DBT_PROFILES_DIR")

    if dbt_profiles_dir is None:
        var_name = "dbt_profiles_dir"
        response = cast(
            Dict[str, str],
            prompt(
                [
                    {
                        "type": "input",
                        "name": var_name,
                        "message": "Path to DBT profiles directory :",
                        "default": "~/.dbt",
                    }
                ]
            ),
        )
        dbt_profiles_dir = response[var_name]

    dbt_profiles_dir = os.path.expanduser(dbt_profiles_dir)

    main(
        Path(os.path.abspath(dbt_profiles_dir)),
        Path(os.path.abspath(dbt_project_dir)),
        required_only,
    )
