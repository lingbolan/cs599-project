"""In-memory URL channel for local single-process runs."""

from __future__ import annotations

import asyncio
from collections import deque

from .base import URLChannel, URLTask


class MemoryURLChannel(URLChannel):
    """Simple in-process URL channel used for local demos and tests."""

    def __init__(self) -> None:
        self._queue: deque[str] = deque()
        self._known: set[str] = set()
        self._sealed = False
        self._closed_error = ""
        self._condition = asyncio.Condition()

    async def publish(self, url: str) -> None:
        if self._closed_error:
            raise RuntimeError(self._closed_error)
        if self._sealed:
            raise RuntimeError("channel_sealed")
        normalized = str(url or "").strip()
        if not normalized or normalized in self._known:
            return
        async with self._condition:
            self._known.add(normalized)
            self._queue.append(normalized)
            self._condition.notify_all()

    async def fetch(self, max_items: int, timeout_s: float | None) -> list[URLTask]:
        if self._closed_error:
            raise RuntimeError(self._closed_error)
        deadline = None if timeout_s is None else max(0.0, float(timeout_s))
        async with self._condition:
            if not self._queue and not self._sealed:
                try:
                    await asyncio.wait_for(self._condition.wait(), timeout=deadline)
                except asyncio.TimeoutError:
                    return []
            tasks: list[URLTask] = []
            while self._queue and len(tasks) < max(1, int(max_items)):
                tasks.append(URLTask(url=self._queue.popleft()))
            return tasks

    async def list_existing_urls(self) -> list[str]:
        return list(self._known)

    def persists_published_urls(self) -> bool:
        return True

    async def seal(self) -> None:
        async with self._condition:
            self._sealed = True
            self._condition.notify_all()

    async def is_drained(self) -> bool:
        return self._sealed and not self._queue

    async def close_with_error(self, reason: str) -> None:
        async with self._condition:
            self._closed_error = str(reason or "channel_closed")
            self._sealed = True
            self._condition.notify_all()
