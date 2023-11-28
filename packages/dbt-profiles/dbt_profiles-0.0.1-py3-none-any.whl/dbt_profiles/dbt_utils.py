import importlib
from inspect import isclass
from pathlib import Path
from typing import Any, Dict, List, Type, Union

import yaml
from dbt.contracts.connection import Credentials
from dbt.version import _get_adapter_plugin_names  # type: ignore
from ruamel.yaml import YAML


def get_adapter_credentials() -> Dict[str, Type[Credentials]]:
    output: Dict[str, Type[Credentials]] = {}

    for adapter_name in _get_adapter_plugin_names():
        adapter_module = importlib.import_module(f"dbt.adapters.{adapter_name}")

        for obj_name in dir(adapter_module):
            adapter = getattr(adapter_module, obj_name)

            if (
                isclass(adapter)
                and issubclass(adapter, Credentials)
                and adapter != Credentials
            ):
                output[adapter_name] = adapter

    return output


class DbtProjectNotFoundError(Exception):
    ...


class DbtProfileNotFoundError(Exception):
    ...


def create_yaml() -> YAML:
    y = YAML()
    y.explicit_start = True
    y.indent(mapping=3)
    y.preserve_quotes = True
    return y


class DbtProjectYAML:
    def __init__(self, project_path: Path):
        self._project_path = project_path

        self._project_yaml: YAML = create_yaml()
        self._project: Dict[str, Any] = {}
        self._setup_project()

    def _setup_project(self):
        self._project = self._read_file()

    def _read_file(self) -> Dict[str, Any]:
        file_path = self._project_path / "dbt_project.yml"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError as error:
            msg = f"Could not find DBT Project at {file_path}"
            raise DbtProjectNotFoundError(msg) from error

    @property
    def project(self) -> Dict[str, Any]:
        return self._project

    @property
    def profile_name(self) -> Union[str, None]:
        return self.project.get("profile")

    def set_profile(self, profile_name: str) -> None:
        self._project["profile"] = profile_name
        self._write(self.project)

    def _write(self, data: Dict[str, Any]) -> None:
        with open(self._project_path / "dbt_project.yml", "w") as file:
            self._project_yaml.dump(data, file)


class DbtProfileYAML:
    def __init__(
        self,
        profile_name: Union[str, None],
        profiles_path: Path,
        create_file_if_not_exists: bool = False,
    ):
        self._profile_name = profile_name
        self._profiles_path = profiles_path
        self._create_file_if_not_exists = create_file_if_not_exists

        self._profiles_yaml: YAML = create_yaml()
        self._profiles: Dict[str, Any] = {}
        self._setup_profiles()

    def _setup_profiles(self):
        val = self._read_file()

        if val is None:
            return

        self._profiles = val

    def _read_file(self) -> Union[Dict[str, Any], None]:
        try:
            return self._read_file_raw()
        except FileNotFoundError as error:
            if self._create_file_if_not_exists:
                return

            raise DbtProfileNotFoundError(
                f"Could not file profiles.yml at {self._profiles_path}"
            ) from error

    def _read_file_raw(self) -> Union[Dict[str, Any], None]:
        with open(self._profiles_path / "profiles.yml", "r", encoding="utf-8") as file:
            return self._profiles_yaml.load(file)

    def create_new_profile(self, profile_name: str):
        self._profile_name = profile_name
        self._profiles = {profile_name: {}, **self._profiles}

    def create_new_target(self, target_name: str):
        self._profiles[self.profile_name] = {
            "target": target_name,
            "outputs": {
                **self.outputs,
                target_name: {},
            },
        }

    def set_adapter_name(self, adapter_name: str):
        self._profiles[self.profile_name]["outputs"][self.target_name][
            "type"
        ] = adapter_name

    @property
    def profiles(self) -> Dict[str, Any]:
        return self._profiles

    @property
    def file_path(self) -> Path:
        return self._profiles_path

    @property
    def profile_name(self) -> str:
        if self._profile_name is not None:
            return self._profile_name

        if (
            len(self.profiles) == 1
            and len(self.profiles[list(self.profiles.keys())[0]].get("outputs", {}))
            == 1
        ):
            return list(self.profiles.keys())[0]

        return ""

    @property
    def profile_names(self) -> List[str]:
        return list(self.profiles.keys())

    @property
    def selected_profile(self) -> Dict[str, Any]:
        return self.profiles.get(self.profile_name, {})

    @property
    def outputs(self) -> Dict[str, Any]:
        return self.selected_profile.get("outputs", {})

    @property
    def target_name(self) -> Union[str, None]:
        return self.selected_profile.get("target")

    @property
    def target(self) -> Dict[str, Any]:
        if self.target_name is None:
            return {}

        return self.outputs.get(self.target_name, {})

    def write(self, new_profile_data: Dict[str, Any]) -> None:
        with open(self.file_path / "profiles.yml", "w", encoding="utf-8") as file:
            self._profiles_yaml.dump(new_profile_data, file)


def write_dbt_profile(
    profiles_yaml: DbtProfileYAML,
    inputs: Dict[str, Any],
    adapter_type_name: str,
) -> None:
    profiles_yaml._profiles[profiles_yaml.profile_name]["outputs"][
        profiles_yaml.target_name
    ] = {
        "type": adapter_type_name,
        **profiles_yaml.target,
        **inputs,
    }

    profiles_yaml.write(profiles_yaml._profiles)
