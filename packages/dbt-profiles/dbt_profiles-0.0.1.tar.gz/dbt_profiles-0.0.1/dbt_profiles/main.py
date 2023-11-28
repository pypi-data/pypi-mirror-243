from pathlib import Path
from typing import Any, Dict, cast

from PyInquirer.prompt import prompt

from .dbt_utils import (
    DbtProfileNotFoundError,
    DbtProfileYAML,
    DbtProjectYAML,
    get_adapter_credentials,
    write_dbt_profile,
)
from .json_schema_prompt import Prompt


class NoDBTAdaptersInstalledException(Exception):
    ...


def single_prompt(prompt_kwargs):
    field_name = "field_name"
    response = prompt([{**prompt_kwargs, "name": field_name}])
    return response[field_name]


def main(dbt_profiles_dir: Path, dbt_project_dir: Path, required_fields_only: bool):
    dbt_project = DbtProjectYAML(dbt_project_dir)

    profile_set_in_project = dbt_project.profile_name is not None
    selected_profile = dbt_project.profile_name

    try:
        dbt_profiles = DbtProfileYAML(selected_profile, dbt_profiles_dir, False)
    except DbtProfileNotFoundError as error:
        create_profiles_dir = cast(
            bool,
            single_prompt(
                {
                    "type": "confirm",
                    "message": f"Could not find {dbt_profiles_dir}/profiles.yaml would you like to create this file? :",
                }
            ),
        )

        if not create_profiles_dir:
            raise error

        dbt_profiles = DbtProfileYAML(
            selected_profile, dbt_profiles_dir, create_profiles_dir
        )

    if not profile_set_in_project:
        if len(dbt_profiles.profile_names) == 0:
            new_profile_name = cast(
                str,
                single_prompt(
                    {
                        "type": "input",
                        "message": "New profile name :",
                    }
                ),
            )
            dbt_profiles.create_new_profile(new_profile_name)
        elif len(dbt_profiles.profile_names) == 1:
            new_profile_name = dbt_profiles.profile_names[0]
        else:
            new_profile_name = cast(
                str,
                single_prompt(
                    {
                        "type": "list",
                        "message": "Select DBT Profile to use :",
                        "choices": dbt_profiles.profile_names,
                    }
                ),
            )

        dbt_project.set_profile(new_profile_name)

    adapter = get_adapter_credentials()

    target_names = list(dbt_profiles.outputs.keys())
    creating_new_target = False

    if len(target_names) == 0:
        creating_new_target = True
        new_target_name = cast(
            str,
            single_prompt(
                {
                    "type": "input",
                    "message": "New target name :",
                }
            ),
        )
        dbt_profiles.create_new_target(new_target_name)

    if len(adapter) == 0:
        raise NoDBTAdaptersInstalledException(
            "No adapters found, install a dbt package"
        )
    elif len(adapter) > 1 and (
        creating_new_target or dbt_profiles.target.get("type") is None
    ):
        adapter_type_name = cast(
            str,
            single_prompt(
                {
                    "type": "list",
                    "message": "Select DBT Adapter to use for new target :",
                    "choices": list(adapter.keys()),
                }
            ),
        )
        dbt_profiles.set_adapter_name(adapter_type_name)
    elif len(adapter) > 1:
        # if this doesn't exist then prompt like above??
        adapter_type_name = dbt_profiles.target.get("type")
    else:
        adapter_type_name = list(adapter.keys())[0]

    if adapter_type_name not in adapter:
        raise Exception(
            f"Could not find adapter {adapter_type_name}, please install it"
        )

    schema = cast(
        Dict[str, Any],
        adapter[adapter_type_name].json_schema(),
    )

    already_have_profile_fields = [f for f in dbt_profiles.target.keys() if f != "type"]

    prompt_factory = Prompt(schema)

    if required_fields_only:
        required_fields = prompt_factory.json_schema.required
    else:
        required_fields = prompt_factory.json_schema.properties

    profile_fields_to_prompt = [
        required
        for required in required_fields
        if required not in already_have_profile_fields
    ]

    p = prompt_factory.questions_for_fields(profile_fields_to_prompt)
    inputs = p()

    combined = {**inputs, **dbt_profiles.target}
    for field_to_prompt in required_fields:
        assert field_to_prompt in combined, f"{field_to_prompt} not in user inputs"

    write_dbt_profile(
        dbt_profiles,
        inputs,
        adapter_type_name,
    )
