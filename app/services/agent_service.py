from abc import ABC, abstractmethod
from typing import List, Dict, Any


@abstractmethod
def route_user_intent(
    self,
    user_input: str,
    accessible_collections: List[str],
) -> List[Dict[str, Any]]:
    pass


@abstractmethod
def request_user_input(
    self,
    user_input: str,
    tool_contexts: List[Dict[str, Any]],
) -> str:
    pass


from typing import Dict

from app.schemas import UserRequest, UserResponse, UserContext, LLMChat
from app.services.chat import BaseChatService
from app.services.tool import BaseToolService
from app.services.llm import BaseLLMService


class AgenticService:
    def __init__(
        self,
        chat_service: BaseChatService,
        llm_service: BaseLLMService,
        tool_services: Dict[str, BaseToolService],
    ):
        self.chat_service: BaseChatService = chat_service
        self.llm_service: BaseLLMService = llm_service
        self.tool_services: Dict[str, BaseToolService] = tool_services

    def chat(self, request: UserRequest) -> UserResponse:
        user_context = UserContext.model_validate(request)

        self.chat_service.validate_user(session_id=user_context.session_id)

        is_valid_input = self.chat_service.validate_content(
            content=user_context.user_input
        )

        user_context.chat_histories = self.chat_service.get_chat_histories(
            session_id=user_context.session_id
        )

        user_context.tool_actions = self.llm_service.route_user_intent(
            user_input=user_context.user_input,
            accessible_collections=user_context.accessible_collections,
        )

        user_context.tool_contexts = [
            # TODO: async tool execution
        ]

        user_context.agent_response = self.llm_service.request_user_input(
            user_input=user_context.user_input,
            tool_contexts=user_context.tool_contexts,
        )

        is_valid_output = self.chat_service.validate_content(
            content=user_context.agent_response
        )

        self.chat_service.set_chat_histories(
            session_id=user_context.session_id,
            chats=[
                LLMChat(role="user", content=user_context.user_input),
                LLMChat(role="assistant", content=user_context.agent_response),
            ],
        )

        return UserResponse(
            session_id=user_context.session_id,
            agent_response=user_context.agent_response,
        )


agentic_service = AgenticService()
