from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union

class UserInput(BaseModel):
    problem: str
    assumptions: Optional[str] = ""
    framework: Optional[str] = "auto"

class AgentResponse(BaseModel):
    status: str = Field(..., description="'success' or 'needs_info'")
    structured_problem: Optional[str] = None
    selected_framework: Optional[str] = None
    framework_output: Optional[Dict[str, List[str]]] = None
    solution: Optional[str] = None
    execution_plan: Optional[List[str]] = None
    clarifying_questions: Optional[List[str]] = None
