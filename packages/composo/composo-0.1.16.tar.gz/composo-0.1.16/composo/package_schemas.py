from typing import List, Union, Any, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class CaseTrigger(BaseModel):
    vars: dict


class RunTrigger(BaseModel):
    run_id: UUID
    cases: List[CaseTrigger]

    
class PollResponse(BaseModel):
    registered_apps: List[UUID]
    run_trigger: Optional[RunTrigger] = None
    

class AppDeletionEvent(BaseModel):
    type: str = Field(..., const="app_deletion")
        

class CaseResult(BaseModel):
    value: Optional[Union[str, int, float]] = None
    error: Optional[str] = None
    

class RunResult(BaseModel):
    results: Optional[List[CaseResult]] = None
    error: Optional[str] = None
    progress: int


class AppRegistration(BaseModel):
    api_key: str
    parameters: List[str]
    types: List[str]  # This needs to be a string because you can't send the frontend a 'type'
    demo_values: List[Union[int, float, str]]
    descriptions: List[Optional[str]]
    constraints: List[Optional[str]]
