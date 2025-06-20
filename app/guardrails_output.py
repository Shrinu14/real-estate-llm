from guardrails import Guard
from guardrails.validators import Validator, register_validator
from pydantic import BaseModel, Field
from typing import Any
from app.utils import log_error

# --------------------------------------------------
# ✅ Register Custom Validator for string field
# --------------------------------------------------
@register_validator(name="min_text_length", data_type="string")
class MinTextLength(Validator):
    """Ensure the text has a minimum acceptable length."""

    def validate(self, value: Any, **kwargs):
        if not isinstance(value, str):
            return self.fail("Invalid input: must be a string.")
        if len(value.strip()) < 50:
            return self.fail(f"Text too short: only {len(value.strip())} characters.")
        return self.pass_()

# --------------------------------------------------
# ✅ Define Output Schema using Pydantic
# --------------------------------------------------
class RAGResponse(BaseModel):
    id: str = Field(..., description="Document ID")
    text: str = Field(
        ..., 
        description="Real estate related document text",
        json_schema_extra={"validators": ["min_text_length"]}  # Link validator
    )

# --------------------------------------------------
# ✅ Instantiate Guard from Pydantic Model
# --------------------------------------------------
guard = Guard.from_pydantic(RAGResponse)

# --------------------------------------------------
# ✅ Validation Wrapper Function
# --------------------------------------------------
def validate_property_output(doc_id: str, text: str):
    """
    Validate RAG output using Guardrails schema.

    Args:
        doc_id (str): UUID of the document.
        text (str): Text to validate.

    Returns:
        dict: Validated output.

    Raises:
        ValueError: If validation fails.
    """
    output = {"id": doc_id, "text": text}
    
    validated_output, validation_results = guard.validate(output)

    if not validation_results.passed:
        error_msg = f"Validation failed: {validation_results}"
        log_error(error_msg, tag="VALIDATION")
        raise ValueError(error_msg)
    
    return validated_output
