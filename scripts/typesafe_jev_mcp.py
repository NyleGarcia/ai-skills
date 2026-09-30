# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=2", "httpx>=0.27"]
# ///
"""MCP server exposing TypeSafe System One (Jev) typed judgments to Claude.

Run: uv run --env-file <path>/.env --script scripts/typesafe_jev_mcp.py
Needs TYPESAFE_API_KEY in env. Docs: https://docs.typesafe.ai/api.md
"""

import os
from typing import Any

import httpx
from mcp.server.mcpserver import MCPServer

API_URL = "https://api.typesafe.ai/v1/systemone"
DEFAULT_MODEL = os.environ.get("TYPESAFE_MODEL", "jev-latest")

mcp = MCPServer("jev")


async def _call(state: Any, questions: dict[str, Any], model: str) -> dict[str, Any]:
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise RuntimeError("TYPESAFE_API_KEY not set")
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            API_URL,
            headers={"Authorization": f"Bearer {key}"},
            json={"state": state, "model": model, "questions": questions},
        )
    if resp.status_code >= 400:
        raise RuntimeError(f"TypeSafe API {resp.status_code}: {resp.text[:500]}")
    return resp.json()


@mcp.tool()
async def evaluate(
    state: str | dict | list,
    questions: dict[str, dict],
    model: str = DEFAULT_MODEL,
) -> dict:
    """Ask Jev several typed questions about one state in a single parallel call.

    questions: map of id -> question. Each question has "type" and "instructions":
      - {"type": "noul", "instructions": "...", "criteria": {"true": "...", "false": "..."}}
        -> probability of yes (criteria optional)
      - {"type": "choice", "instructions": "...", "criteria": {"opt": "desc" | null, ...}}
        -> chosen option + distribution (max 255 options)
      - {"type": "score", "instructions": "...", "criteria": ["low level", ..., "high level"]}
        -> probability-weighted position across 2-10 ordered levels
    Question ids are not sent to the model; put full meaning in instructions.
    Reference nested state fields with backticked paths, e.g. `ticket.body`.
    Questions run independently and cannot see each other's answers.
    """
    return await _call(state, questions, model)


@mcp.tool()
async def noul(
    state: str | dict | list,
    question: str,
    true_means: str | None = None,
    false_means: str | None = None,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Yes/no judgment: returns probability (0-1) that the answer is yes."""
    q: dict[str, Any] = {"type": "noul", "instructions": question}
    if true_means or false_means:
        q["criteria"] = {k: v for k, v in (("true", true_means), ("false", false_means)) if v}
    return await _call(state, {"answer": q}, model)


@mcp.tool()
async def choice(
    state: str | dict | list,
    question: str,
    options: dict[str, str | None],
    model: str = DEFAULT_MODEL,
) -> dict:
    """Pick one option. options: map of option key -> description (or null)."""
    q = {"type": "choice", "instructions": question, "criteria": options}
    return await _call(state, {"answer": q}, model)


@mcp.tool()
async def score(
    state: str | dict | list,
    question: str,
    levels: list[str],
    model: str = DEFAULT_MODEL,
) -> dict:
    """Rate along ordered levels (2-10, lowest first); returns weighted position."""
    q = {"type": "score", "instructions": question, "criteria": levels}
    return await _call(state, {"answer": q}, model)


if __name__ == "__main__":
    mcp.run()
