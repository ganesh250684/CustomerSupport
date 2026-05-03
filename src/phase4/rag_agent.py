from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


@dataclass
class RagResponse:
    mode: str
    response_draft: str
    confidence: str
    citations: List[Dict[str, str]]
    escalate: bool
    escalation_reason: str
    uncertainty_note: str

    def to_dict(self) -> dict:
        return asdict(self)


class Phase4RagAgent:
    def __init__(self, model_name: str = "gpt-4o-mini") -> None:
        self.llm = ChatOpenAI(model=model_name, temperature=0.1, max_retries=2)

    def respond_without_retrieval(self, user_message: str) -> RagResponse:
        system = (
            "You are a SaaS support assistant. Answer safely and briefly. "
            "If policy is unknown, say uncertain and recommend escalation. "
            "Do not fabricate policy details."
        )
        output = self._run_llm(system, user_message)
        return RagResponse(
            mode="without_retrieval",
            response_draft=output,
            confidence="medium",
            citations=[],
            escalate=self._needs_escalation(user_message, output),
            escalation_reason="possible_unresolved_case" if self._needs_escalation(user_message, output) else "",
            uncertainty_note="No KB retrieval used in this mode.",
        )

    def respond_with_retrieval(
        self,
        user_message: str,
        retrieved: List[Tuple[Document, float]],
    ) -> RagResponse:
        if not retrieved:
            return RagResponse(
                mode="with_retrieval",
                response_draft=(
                    "I do not have enough verified policy evidence in the knowledge base "
                    "to provide a final answer. I will escalate this case to a specialist."
                ),
                confidence="low",
                citations=[],
                escalate=True,
                escalation_reason="missing_kb_evidence",
                uncertainty_note="No relevant retrieval results found.",
            )

        context_lines: List[str] = []
        citations: List[Dict[str, str]] = []
        for doc, score in retrieved:
            source = str(doc.metadata.get("source", "unknown"))
            excerpt = doc.page_content[:300].replace("\n", " ")
            context_lines.append(f"SOURCE: {source} | SCORE: {score:.4f} | EXCERPT: {excerpt}")
            citations.append({"source": source, "score": f"{score:.4f}"})

        system = (
            "You are a safety-first SaaS support assistant. "
            "Use only retrieved context for policy claims. "
            "If context is insufficient, explicitly say uncertain and escalate. "
            "Return concise answer in plain text."
        )
        user_prompt = (
            f"User request: {user_message}\n\n"
            f"Retrieved context:\n" + "\n".join(context_lines)
        )
        output = self._run_llm(system, user_prompt)

        escalate = self._needs_escalation(user_message, output)
        return RagResponse(
            mode="with_retrieval",
            response_draft=output,
            confidence="high" if citations else "low",
            citations=citations,
            escalate=escalate,
            escalation_reason="sensitive_or_unresolved" if escalate else "",
            uncertainty_note="",
        )

    def _run_llm(self, system_prompt: str, user_message: str) -> str:
        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message),
            ]
        )
        text = response.content if isinstance(response.content, str) else json.dumps(response.content)
        return text.strip()

    @staticmethod
    def _needs_escalation(user_message: str, output: str) -> bool:
        text = f"{user_message} {output}".lower()
        risk_tokens = [
            "suspicious",
            "unauthorized",
            "legal",
            "abuse",
            "cannot",
            "uncertain",
            "escalate",
        ]
        return any(token in text for token in risk_tokens)
