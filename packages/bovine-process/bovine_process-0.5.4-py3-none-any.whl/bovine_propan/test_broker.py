import aiohttp
import pytest

from faststream.rabbit import TestRabbitBroker
from faststream.annotations import ContextRepo
from unittest.mock import AsyncMock, MagicMock

from .actor import cache

from .broker import broker, inbox_queue
from bovine_propan.exchanges import processing


@pytest.fixture
async def test_broker():
    async with TestRabbitBroker(broker) as br:
        context = ContextRepo()
        context.set_global("session", AsyncMock(aiohttp.ClientSession))
        context.set_global("logger", AsyncMock())

        actor = AsyncMock()
        actor.actor_id = "http://local/actor"
        cache["bovine_name"] = actor
        actor.actor_object.build = MagicMock(
            return_value={"endpoints": {"eventSource": "xxxx"}}
        )
        actor.retrieve_own_object.return_value = MagicMock()

        yield br


async def test_inbox_handler(test_broker):
    remote_actor = "https://remote.example/actor"

    await test_broker.publish(
        {
            "bovine_name": "bovine_name",
            "submitter": remote_actor,
            "data": {
                "@context": "about:bovine",
                "actor": remote_actor,
                "type": "Like",
            },
        },
        exchange=processing,
        queue=inbox_queue,
    )
