from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.lead import LeadState


class LeadRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    resume_filename: str
    state: LeadState
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadStateUpdate(BaseModel):
    state: LeadState
