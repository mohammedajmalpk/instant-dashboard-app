from pydantic import BaseModel, field_validator

class DashboardRequestModel(BaseModel):
    """
        payload data from dashboard
    """
    json_data: str
    prompt: str


class DashboardResponse(BaseModel):
    """
        Response data
    """
    html: str
    status: int
    details: str
