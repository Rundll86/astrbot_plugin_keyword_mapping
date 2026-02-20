import random

from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Star


class KeywordMappingPlugin(Star):
    def __init__(self, context, config):
        super().__init__(context, config)
        self.config = config or {}

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def all_message(self, event: AstrMessageEvent):
        mappings = self.config.get("mappings", [])
        values = []
        for pair in mappings:
            if pair["key"] in event.message_str:
                values.append(pair["value"])
        if len(values) > 0:
            yield event.plain_result(random.choice(values))
