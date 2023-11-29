import pydantic


class BaseTectonConfig(pydantic.BaseModel):
    """Base class for repo configuration objects, i.e. data classes used FCO construction."""

    model_config = pydantic.ConfigDict(
        # Do not allow extra attributes during model initialization, i.e. providing kwargs that were not declared
        # fields.
        extra="forbid",
        # Config objects should be immutable. `frozen=True` will block re-assignments to fields. It does not enforce
        # that the value itself is immutable, so it is advised to use immutable types, e.g. tuples instead of lists.
        # TODO(jake): Make the model config frozen - requires updating some end to end tests.
        frozen=False,
        # Strictly enforce types. Do not attempt to coerce types, e.g. converting an int to a string.
        strict=True,
    )
