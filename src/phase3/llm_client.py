from __future__ import annotations

import os
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


class Phase3LLMClient:
    """Thin wrapper around ChatOpenAI for Phase 3 prompt evaluation."""

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.2) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Set it in your environment before running Phase 3."
            )

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_retries=2,
        )

    def generate(self, system_prompt: str, user_message: str) -> str:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]
        response = self.llm.invoke(messages)
        content: Optional[str] = getattr(response, "content", None)
        if not content:
            return ""
        return content.strip()
