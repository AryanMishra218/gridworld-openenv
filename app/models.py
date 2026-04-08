from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any


# -----------------------------
# State Model (Observation)
# -----------------------------

class State(BaseModel):
    agent: List[int]
    goal: List[int]
    obstacles: List[List[int]]
    traps: List[List[int]]
    enemy: Optional[List[int]] = None

    @field_validator("agent", "goal", "enemy")
    def check_len_2(cls, v):
        if v is not None and len(v) != 2:
            raise ValueError("Must be [x, y]")
        return v

# -----------------------------
# Reset Response
# -----------------------------
class ResetResponse(BaseModel):
    state: State
    info: Dict[str, Any] = {}


# -----------------------------
# Step Request
# -----------------------------
class StepRequest(BaseModel):
    action: int


# -----------------------------
# Step Response
# -----------------------------
class StepResponse(BaseModel):
    state: State
    reward: float
    terminated: bool
    truncated: bool
    info: Dict[str, Any] = {}
