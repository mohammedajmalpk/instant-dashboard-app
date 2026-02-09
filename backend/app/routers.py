import json
import os

from fastapi import APIRouter, HTTPException, status
from groq import Groq
from dotenv import load_dotenv

from .prompts import system_prompt
from .schemas import DashboardRequestModel, DashboardResponseModel
from .utils import extract_numeric_values, clean_validate_html

load_dotenv()

router = APIRouter(
    prefix="/api/v1",
    tags=["Dashboard APIs"],
    responses={404: {"description": "Not found"}},
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@router.post("/generate-dashboard", response_model=DashboardResponseModel)
async def generate_dashboard(request: DashboardRequestModel):
    """
        main endpoint for generate dashboard from user's
            - json_data
            - prompt
        - validate json_data and user prompt
        - Use system prompt for the accuracy
        - return html with status and detail
    """
    try:
        parsed_json = json.loads(request.json_data)
        total = sum(extract_numeric_values(parsed_json))

        data_summary = {
            "keys": list(parsed_json.keys()),
            "structure": type(parsed_json).__name__
        }

        user_message = f"""Here is the JSON data:

        {request.json_data}
        
        User Instructions:
        {request.user_prompt}
        
        PRE-CALCULATED TOTAL:
        {total} USD
        
        IMPORTANT:
        The total above is computed by the backend.
        Do NOT recalculate it.
        Display it exactly as provided.
        
        Create a professional dashboard with proper data visualization.
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=4000
        )

        generated_html = chat_completion.choices[0].message.content.strip()
        cleaned_html = clean_validate_html(generated_html)

        return DashboardResponseModel(
            status=status.HTTP_200_OK,
            html=cleaned_html,
            detail="dashboard generated successfully",
            data_summary=data_summary
        )
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except json.JSONDecodeError as err:
        raise HTTPException(status_code=400, detail=f"Invalid JSON Format: {str(err)}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))