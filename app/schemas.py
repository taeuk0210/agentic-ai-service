from typing import List, Dict, Any

from pydantic import BaseModel

# ---------------------------- #
# Infra-structure layer schema #
# ---------------------------- #


class Message(BaseModel):
    role: str
    content: str


class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    messages: List[Message]
    temperature: float


class LLMResponse(BaseModel):
    message: str
    latency: float
    prompt_tokens: int
    completion_tokens: int


class VectorCollection(BaseModel):
    collection: str
    dimension: int
    metric_type: str


class VectorItem(BaseModel):
    uuid: Any
    vector: List[float]
    properties: Dict[str, Any]


# -------------------- #
# Service layer schema #
# -------------------- #


class VerifyUserRequest(BaseModel):
    user_id: str
    session_id: str
    client_address: str


class VerifyUserResponse(BaseModel):
    user_id: str
    user_role: str
    session_id: str
    availables: List[Dict[str, Any]]


# --------------------- #
# Workflow layer schema #
# --------------------- #


class UserRequest(BaseModel):
    pass


class UserResponse(BaseModel):
    pass
