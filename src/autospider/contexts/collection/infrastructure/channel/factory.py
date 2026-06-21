"""URL channel factory."""

from __future__ import annotations

from autospider.platform.config.runtime import config, normalize_pipeline_mode

from .base import URLChannel
from .memory_channel import MemoryURLChannel
from .redis_channel import RedisURLChannel


def create_url_channel(
    mode: str | None = None,
    output_dir: str = "output",
    redis_key_prefix: str | None = None,
) -> URLChannel:
    """Create a URL channel according to runtime configuration."""
    resolved_mode = normalize_pipeline_mode(config.pipeline.mode if mode is None else mode)
    if resolved_mode == "memory":
        return MemoryURLChannel()

    _ = output_dir
    from autospider.platform.persistence.redis.queue_manager import RedisQueueManager

    key_prefix = (redis_key_prefix or config.redis.key_prefix).strip() or config.redis.key_prefix
    manager = RedisQueueManager(
        host=config.redis.host,
        port=config.redis.port,
        password=config.redis.password,
        db=config.redis.db,
        key_prefix=key_prefix,
    )
    return RedisURLChannel(
        manager=manager,
        consumer_name=config.redis.consumer_name,
        block_ms=config.redis.fetch_block_ms,
        max_retries=config.redis.max_retries,
    )
