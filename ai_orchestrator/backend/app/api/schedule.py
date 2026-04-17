from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.scheduler import find_substitution

router = APIRouter()

class SubstitutionRequest(BaseModel):
    teacher_name: str
    date: Optional[str] = None

@router.post("/substitute")
async def schedule_substitute(req: SubstitutionRequest):
    plan = find_substitution(req.teacher_name, req.date)
    return {"substitution_plan": plan}
