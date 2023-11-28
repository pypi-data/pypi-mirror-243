from typing import Optional

from mashumaro.jsonschema.models import Context, JSONSchema
from mashumaro.jsonschema.schema import Instance, Registry, get_schema


def on_new_type(instance: Instance, ctx: Context) -> Optional[JSONSchema]:
    # The 'Port' in PostgresCredentials is a NewType(int) and for some reason
    # that does not work, however if it was just an 'int' it would correctly include
    # the minimum and maximum constraints
    #
    # This forces the NewTypes of ints to call the base on number
    super_type = getattr(instance.origin_type, "__supertype__", None)  # type: ignore

    if super_type is None:
        return

    instance.type = super_type
    instance.origin_type = super_type

    return get_schema(instance, Context())


# needs to come first: (using the decorator will put last)
Registry._registry = [on_new_type, *Registry._registry]  # type: ignore
