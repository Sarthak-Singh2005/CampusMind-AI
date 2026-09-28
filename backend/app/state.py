from typing import TypedDict, Any


class AgentState(TypedDict):
    query: str
    role: str
    user_id: str
    language: str

    intent: str
    entities: dict[str, Any]

    answer: str
    authorized: bool
    tool_result: dict[str, Any]

    conversation_history: list[dict[str, str]]
    pending_action: dict[str, Any] | None
    security_blocked: bool
