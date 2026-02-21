import random

from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Star

from .util import GroupState, use_group_state


class KeywordMappingPlugin(Star):
    def __init__(self, context, config):
        super().__init__(context, config)
        self.config = config or {}

    @filter.event_message_type(filter.EventMessageType.ALL)
    @use_group_state(False, False)
    async def all_message(self, state: GroupState, event: AstrMessageEvent):
        if state.switch:
            mappings = self.config.get("mappings", [])
            values = []
            count = 0
            for pair in mappings:
                if (
                    pair["key"] not in state.ban_keywords
                    and pair["key"] in event.message_str
                ):
                    values.append(pair["value"])
                    count += 1
            if len(values) > 0:
                for _ in range(count if self.config["time_sync_count"] else 1):
                    yield event.plain_result(random.choice(values))

    @filter.command_group(
        "kwm",
        alias={
            "keywords-mapping",
            "keyword-mapping",
            "kw-mapping",
            "keywords-map",
            "keyword-map",
            "kw-map",
            "keywords",
            "keyword",
            "kw",
            "mapping",
            "map",
            "关键词映射",
            "关键词",
            "映射",
        },
    )
    def kwm_command(self):
        pass

    @kwm_command.command("view")
    @use_group_state(False, True)
    async def view(self, state: GroupState, event: AstrMessageEvent):
        yield event.plain_result(f"群聊 {event.get_group_id()} 状态如下：")

    @kwm_command.command("on")
    @use_group_state(True, True)
    async def on(self, state: GroupState, event: AstrMessageEvent):
        state.switch = True

    @kwm_command.command("off")
    @use_group_state(True, True)
    async def off(self, state: GroupState, event: AstrMessageEvent):
        state.switch = False

    @kwm_command.command("ban")
    async def ban(self, event: AstrMessageEvent, keyword: str):
        async def ban(self, state: GroupState, event: AstrMessageEvent):
            if keyword in state.ban_keywords:
                yield event.plain_result("关键词已经剔除了！")
            else:
                state.ban_keywords.append(keyword)

        keyword = keyword.strip()
        use_group_state(True, True)(ban)(self, event)

    @kwm_command.command("unban")
    async def unban(self, event: AstrMessageEvent, keyword: str):
        async def unban(self, state: GroupState, event: AstrMessageEvent):
            if keyword not in state.ban_keywords:
                yield event.plain_result("关键词还没有被剔除！")
            else:
                state.ban_keywords.remove(keyword)

        keyword = keyword.strip()
        use_group_state(True, True)(unban)(self, event)
