"""Base schema with OpenAI structured output compatibility.

OpenAI's structured output API requires all JSON schemas to have
`additionalProperties: false` set. This base class configures Pydantic
to generate compliant schemas automatically.
"""

from pydantic import BaseModel, ConfigDict


class StrictSchema(BaseModel):
    """
    Base model for all schemas used with OpenAI structured output.

    This ensures the generated JSON schema includes `additionalProperties: false`
    and all fields are marked as required, which is mandatory for OpenAI's strict mode.
    """

    model_config = ConfigDict(
        # This adds "additionalProperties": false to the JSON schema
        extra="forbid",
    )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        """
        Custom schema generation to ensure compatibility with OpenAI Structured Outputs.
        OpenAI requires all fields to be listed in 'required'.
        """
        json_schema = handler(core_schema)
        json_schema = cls._make_schema_strict(json_schema)
        return json_schema

    @classmethod
    def _make_schema_strict(cls, schema: dict) -> dict:
        """Recursively make schema strict for OpenAI."""
        if schema.get("type") == "object" and "properties" in schema:
            # Force all properties to be required
            schema["required"] = list(schema["properties"].keys())
            schema["additionalProperties"] = False

        # Recurse into definitions if present
        if "$defs" in schema:
            for def_name, def_schema in schema["$defs"].items():
                cls._make_schema_strict(def_schema)

        return schema
