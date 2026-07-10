from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import EmailStr
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.models.lead import Lead, LeadState
from app.schemas.lead import LeadRead, LeadStateUpdate
from app.services.auth import require_internal_user
from app.services.emailer import EmailService
from app.services.storage import store_resume


router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadRead, status_code=status.HTTP_201_CREATED)
def create_lead(
    first_name: str = Form(..., min_length=1, max_length=100),
    last_name: str = Form(..., min_length=1, max_length=100),
    email: EmailStr = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> Lead:
    resume_filename, resume_path = store_resume(resume, settings)
    lead = Lead(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=str(email).strip().lower(),
        resume_filename=resume_filename,
        resume_path=resume_path,
        state=LeadState.PENDING,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    EmailService(settings).send_lead_notifications(lead)
    return lead


@router.get("", response_model=list[LeadRead], dependencies=[Depends(require_internal_user)])
def list_leads(db: Session = Depends(get_db)) -> list[Lead]:
    return list(db.scalars(select(Lead).order_by(desc(Lead.created_at))).all())


@router.patch("/{lead_id}", response_model=LeadRead, dependencies=[Depends(require_internal_user)])
def update_lead_state(lead_id: int, payload: LeadStateUpdate, db: Session = Depends(get_db)) -> Lead:
    lead = db.get(Lead, lead_id)
    if lead is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    lead.state = payload.state
    db.commit()
    db.refresh(lead)
    return lead
