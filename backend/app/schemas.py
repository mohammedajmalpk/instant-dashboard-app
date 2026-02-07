from pydantic import BaseModel, field_validator
from fastapi import HTTPException
import json

class DashboardRequestModel(BaseModel):
    """
        payload data from dashboard
    """
    json_data: str
    prompt: str

    @field_validator("json_data")
    def validate_json_data(cls, v):
        """
            validate json data
        """
        try:
            json.loads(v)
            return v
        except json.JSONDecodeError as err:
            raise HTTPException(status_code=400, detail="Invalid JSON format")

    @field_validator("prompt")
    def validate_prompt(cls, v):
        """
            validate prompt
            ensure the prompt is not empty
        """
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        return v.strip()


class DashboardResponseModel(BaseModel):
    """
        Response data
    """
    html: str
    status: int
    detail: str
