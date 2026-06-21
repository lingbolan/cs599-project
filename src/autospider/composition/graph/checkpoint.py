"""LangGraph checkpoint helpers."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from urllib.parse import quote

from autospider.platform.config.runtime import config

_SETUP_COMPLETE: set[str] = set()
_MEMORY_CHECKPOINTER: Any | None = None


def graph_checkpoint_enabled() -> bool:
    """Return whether LangGraph checkpointing is enabled."""
    return bool(config.graph_checkpoint.enabled)


def _build_redis_conn_string() -> str:
    checkpoint_config = config.graph_checkpoint
    redis_url = str(checkpoint_config.redis_url or "").strip()
    if redis_url:
        return redis_url

    password = checkpoint_config.password
    auth = f":{quote(password, safe='')}@" if password else ""
    return (
        f"redis://{auth}{checkpoint_config.host}:{checkpoint_config.port}/"
        f"{checkpoint_config.db}"
    )


@asynccontextmanager
async def graph_checkpointer_session() -> AsyncIterator[Any | None]:
    """Create a LangGraph checkpointer on demand."""
    if not graph_checkpoint_enabled():
        yield None
        return

    backend = str(config.graph_checkpoint.backend or "redis").strip().lower()
    if backend == "memory":
        global _MEMORY_CHECKPOINTER
        if _MEMORY_CHECKPOINTER is None:
            from langgraph.checkpoint.memory import InMemorySaver

            _MEMORY_CHECKPOINTER = InMemorySaver()
        yield _MEMORY_CHECKPOINTER
        return

    if backend != "redis":
        raise RuntimeError(
            f"Unsupported GRAPH_CHECKPOINT_BACKEND: {backend}. "
            "Supported backends: redis, memory."
        )

    try:
        from langgraph.checkpoint.redis.aio import AsyncRedisSaver
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "GRAPH_CHECKPOINT_ENABLED is true, but the redis checkpointer "
            "dependency is not installed. Install `langgraph-checkpoint-redis`."
        ) from exc

    conn_string = _build_redis_conn_string()
    saver_cm = AsyncRedisSaver.from_conn_string(conn_string)
    async with saver_cm as checkpointer:
        if conn_string not in _SETUP_COMPLETE:
            await checkpointer.asetup()
            _SETUP_COMPLETE.add(conn_string)
        yield checkpointer
