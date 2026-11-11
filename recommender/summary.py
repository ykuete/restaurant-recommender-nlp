"""Generative summary: two sentences on why each restaurant fits the request.

Uses the LLM set by LLM_PROVIDER (anthropic | openai | none). Every result
gets a template summary built from its aspect scores whenever the LLM is
off, missing a key, fails, or misses the time budget, so results always show.
"""

from __future__ import annotations

import asyncio
import os

from recommender import config
from recommender.sentiment import ASPECT_LABELS

DEFAULT_MODELS = {"anthropic": "claude-haiku-5-5", "openai": "gpt-4o-mini"}
KEY_VARS = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}

SYSTEM_PROMPT = (
    "You explain restaurant recommendations. In at most two short sentences, say why "
    "the restaurant fits the user's request, using ONLY the facts given (aspect scores "
    "and review quotes). Mention one drawback if the facts show one. Never invent "
    "dishes, prices or details. No preamble."
)


def _label(key: str) -> str:
    return ASPECT_LABELS.get(key, key).lower()


def template_summary(result: dict) -> str:
    """Rule-based summary from the aspect profile (the fallback)."""
    aspects = {a["key"]: a for a in result.get("aspects", []) if a["mentions"] >= 2}
    if not aspects:
        return f"Matches {result.get('match', 0)}% of your request based on its reviews."
    asked = [aspects[k] for k in result.get("query_aspects", []) if k in aspects]
    strengths = sorted(asked or aspects.values(), key=lambda a: -a["positive"])[:2]
    parts = [f"{_label(a['key'])} ({a['positive']}% positive)" for a in strengths]
    text = "Reviewers rate the " + " and ".join(parts) + " highly."
    weakest = max(aspects.values(), key=lambda a: a["negative"])
    if weakest["negative"] >= 25 and weakest not in strengths:
        text += f" The most common complaint is {_label(weakest['key'])} ({weakest['negative']}% negative)."
    return text


def build_prompt(query: str, result: dict) -> str:
    aspects = "\n".join(
        f"- {a['label']}: {a['positive']}% positive, {a['negative']}% negative "
        f"({a['mentions']} mentions)"
        for a in result.get("aspects", [])
    )
    quote = (result.get("snippet") or {}).get("text", "")
    return (
        f"User request: {query}\n"
        f"Restaurant: {result['name']} ({', '.join(result.get('categories', [])[:3])}), "
        f"{result['stars']} stars from {result['review_count']} reviews\n"
        f"Aspect scores from review sentences:\n{aspects or '- none'}\n"
        f"Review quote: \"{quote}\""
    )


def _provider() -> str | None:
    provider = config.LLM_PROVIDER
    if provider in KEY_VARS and os.getenv(KEY_VARS[provider]):
        return provider
    return None


async def _call_llm(provider: str, prompt: str) -> str:
    model = config.LLM_MODEL or DEFAULT_MODELS[provider]
    if provider == "anthropic":
        from anthropic import AsyncAnthropic

        resp = await AsyncAnthropic().messages.create(
            model=model,
            max_tokens=160,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    from openai import AsyncOpenAI

    resp = await AsyncOpenAI().chat.completions.create(
        model=model,
        max_tokens=160,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


async def summarize(query: str, results: list[dict], timeout: float = config.LLM_TIMEOUT_S) -> list[str]:
    """One summary per result. LLM calls run in parallel within `timeout`
    seconds in total; any that fail or are late get the template."""
    fallback = [template_summary(r) for r in results]
    provider = _provider()
    if provider is None or not results:
        return fallback

    tasks = [asyncio.create_task(_call_llm(provider, build_prompt(query, r))) for r in results]
    done, pending = await asyncio.wait(tasks, timeout=timeout)
    for task in pending:
        task.cancel()
    summaries = []
    for task, default in zip(tasks, fallback, strict=True):
        if task in done and task.exception() is None and task.result():
            summaries.append(task.result())
        else:
            summaries.append(default)
    return summaries
