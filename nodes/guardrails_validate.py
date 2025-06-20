# nodes/guardrails_validate.py

from guardrails import Guard
from pathlib import Path
import json

rail_path = Path("guardrails/property_schema.rail")
guard = Guard.from_rail(rail_path.read_text())

def validate_with_guardrails(inputs: dict) -> dict:
    output, validated_output = guard(
        prompt_params={"input": inputs.get("raw_text", "")},
        output=inputs.get("llm_output", "")
    )
    return {"validated": validated_output}
