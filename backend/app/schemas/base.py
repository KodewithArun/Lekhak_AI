"""Base schema with OpenAI structured output compatibility.

OpenAI's structured output API requires all JSON schemas to have
all fields marked as required. This base class configures Pydantic
to generate compliant schemas automatically.
"""

from pydantic import BaseModel, ConfigDict


class StrictSchema(BaseModel):
    """
    Base model for all schemas used with structured output.

    This ensures the generated JSON schema includes all fields
    marked as required, ensuring compatibility across different providers.
    """

    model_config = ConfigDict(
        extra="ignore",
        # used ignore to avoid automatic "additionalProperties": false
        # which Gemini does not support. OpenAI compatibility is handled via LiteLLM patch.
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
            schema["required"] = list(schema["properties"].keys())

        if "$defs" in schema:
            for def_name, def_schema in schema["$defs"].items():
                cls._make_schema_strict(def_schema)

        return schema
