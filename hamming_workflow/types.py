from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel


class Score(BaseModel):
    value: float
    reason: Optional[str] = None


class Call(BaseModel):
    id: str
    status: str
    scores: Dict[str, Score]


class ExperimentResult(BaseModel):
    calls: List[Call]


class ExperimentStatus(Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    SCORING = "SCORING"
    SCORING_FAILED = "SCORING_FAILED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
