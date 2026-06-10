from uuid import UUID
from typing import Optional, Dict, List, Any

from pydantic import BaseModel

from openai.types.chat import ChatCompletion


class VectorCreateRequest(BaseModel):
    uuid: Optional[UUID] = None
    vector: List[float]
    properties: Optional[Dict[str, Any]] = {}


class VectorQueryResponse(BaseModel):
    uuid: UUID


class LLMChat(BaseModel):
    role: str
    content: str


class UserRequest(BaseModel):
    session_id: Optional[UUID] = None
    user_input: str


class UserContext(BaseModel):
    session_id: Optional[UUID] = None
    user_input: str
    accessible_collections: List[str] = []
    chat_histories: List[LLMChat]
    tool_actions: List[Dict[str, Any]] = []
    tool_contexts: List[Dict[str, Any]] = []
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    agent_response: Optional[str] = None


class UserResponse(BaseModel):
    session_id: UUID
    agent_response: str
