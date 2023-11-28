from __future__ import print_function, unicode_literals

from typing import Any, Dict, List, Optional, Type, cast

from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError, Validator
from PyInquirer.prompt import prompt


def integer_validator(
    min_value: Optional[int] = None, max_value: Optional[int] = None
) -> Type[Validator]:
    class IntegerRange(Validator):
        def validate(self, document: Document):
            try:
                value = int(document.text)
            except Exception as ex:
                raise ValidationError(
                    message="Please enter a valid integer",
                    cursor_position=len(document.text),
                ) from ex

            if min_value is not None and value < min_value:
                raise ValidationError(
                    message=f"Please enter a number greater than {min_value}",
                    cursor_position=len(str(value)),
                )

            if max_value is not None and value > max_value:
                raise ValidationError(
                    message=f"Please enter a number less than {max_value}",
                    cursor_position=len(str(value)),
                )

    return IntegerRange


class JsonSchema:
    def __init__(self, json: Dict[str, Any]):
        # use to validate?
        # https://pypi.org/project/jsonschema/
        #
        # TODO: use the mashumaro class???
        self._json = json

    @property
    def json(self):
        return self._json

    @property
    def required(self) -> List[str]:
        return self.json["required"]

    @property
    def properties(self) -> Dict[str, Any]:
        return self._json["properties"]

    def is_requied_field(self, field_name: str) -> bool:
        return field_name in self.required

    def is_optional_field(self, field_name: str) -> bool:
        return not self.is_requied_field(field_name)

    @property
    def required_fields(self):
        return {
            field_name: property_value
            for field_name, property_value in self.properties.items()
            if self.is_requied_field(field_name)
        }

    @property
    def optional_fields(self):
        return {
            field_name: property_value
            for field_name, property_value in self.properties.items()
            if self.is_optional_field(field_name)
        }

    def get_default_value(self, field: Dict[str, Any]):
        if "default" in field:
            return True, field["default"]

        return False, None
        # todo: deal with oneOf with null's, i.e. optional
        # type_ = field["type"]
        # if "null" in type_

    def get_validator(self, field: Dict[str, Any]):
        if "integer" in field["type"]:
            return True, integer_validator(field.get("minimum"), field.get("maximum"))

        return False, None


class Promptable:
    def __init__(self, json_schema: JsonSchema, questions: List[Dict[str, str]]):
        self._json_schema: JsonSchema = json_schema
        self._questions = questions

    def __call__(self) -> Dict[str, Any]:
        # post process, return
        # TODO: validate input data as entered
        # TODO: as part of ^ convert ints, floats from str to data type
        output: Dict[str, Any] = cast(Dict[str, str], prompt(self._questions))

        for output_name, output_value in output.items():
            type_ = self._json_schema.properties[output_name]["type"]

            if type_ == "integer":
                output[output_name] = int(output_value)
            if type_ == "number":
                output[output_name] = float(output_value)

        return output


class Prompt:
    def __init__(self, json: Dict[str, Any]):
        self.json_schema = JsonSchema(json)

    def format_field_name(self, field_name: str):
        field = self.json_schema.properties[field_name]
        type_ = field["type"] # TODO: this fails

        if "default" in field:
            default = field["default"]
            default_value = f" (default={default})"
        else:
            default_value = ""

        if type_ == "integer":
            min_ = field.get("minimum")
            max_ = field.get("maximum")

            if min_ is not None and max_ is not None:
                return f"{field_name}{default_value} [{min_}-{max_}]:"
            elif min_ is not None:
                return f"{field_name}{default_value} [>={min_}]:"
            elif max_ is not None:
                return f"{field_name}{default_value} [<={max_}]:"

            return f"{field_name}{default_value}:"

        return f"{field_name} {default_value}:"

    def create_field_question(self, field_name: str):
        field = self.json_schema.properties[field_name]
        question_type = "input"

        if field_name.lower() == "password":
            question_type = "password"

        question = {
            "type": question_type,
            "name": field_name,
            "message": self.format_field_name(field_name),
        }

        has_default_value, default_value = self.json_schema.get_default_value(field)
        if has_default_value:
            question["default"] = default_value

        has_validator, validator = self.json_schema.get_validator(field)
        if has_validator:
            question["validate"] = validator

        return question

    def required_questions(self):
        return Promptable(
            self.json_schema,
            [
                self.create_field_question(required_field_name)
                for required_field_name in self.json_schema.required
            ],
        )

    def questions_for_fields(self, fields: List[str]) -> Promptable:
        return Promptable(
            self.json_schema,
            [self.create_field_question(field_name) for field_name in fields],
        )
