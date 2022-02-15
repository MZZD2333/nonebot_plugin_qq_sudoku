import json
import random

import nonebot
import urllib3
from nonebot.adapters.onebot.v11 import *
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.params import Arg, ArgPlainText, CommandArg, Depends, State
from nonebot.permission import SUPERUSER
from nonebot.plugin import (on_command, on_keyword, on_message, on_notice,
                            on_regex)
from nonebot.rule import Rule, to_me
from nonebot.typing import T_State

# import nonebot_plugin_guild_patch
from .configs import (HEADER, MUZI_HELP, GROUP_INFO_PATH)
from .updata_info import updata_all_group_info, updata_group_info,GroupInfo
from .autorespond import kw_handle
# 消息响应器
# autoresponder = on_message(rule=probability(), priority=10)

# 命令响应器
muzi_help = on_command("help", rule=to_me(), priority=1, block=True)
kw_macther = on_command("kw", priority=1, block=True)
check_probability = on_command("回复率", aliases={"RPR"}, priority=1, block=True)
plugin_test = on_command("test", permission=SUPERUSER, priority=1, block=True)
get_cover = on_command("封面", priority=1, block=True)
set_title = on_command("头衔", priority=1, block=True)

# 通知响应器
notice_event = on_notice()

@notice_event.handle()
async def _(bot: Bot, event: GroupAdminNoticeEvent):
    await updata_group_info(event.group_id)
@notice_event.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    await updata_group_info(event.group_id)
@notice_event.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    await updata_group_info(event.group_id)

@notice_event.handle()
async def _(bot: Bot, event: GroupAdminNoticeEvent):
    await updata_group_info(event.group_id)

@muzi_help.handle()
async def _(bot: Bot, event: MessageEvent):
    await muzi_help.send(MUZI_HELP)


@kw_macther.handle()
async def _(bot: Bot, event: MessageEvent):
    await kw_handle(bot, event)


@get_cover.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    bvids = str(msg)
    if bvids:
        for bvid in bvids.split():
            try:
                bvid = f'aid={bvid[2:]}' if 'av' == bvid[:2].lower() else f'bvid={bvid}'
                _url = 'https://api.bilibili.com/x/web-interface/view?' + bvid
                _img_url = json.loads(urllib3.PoolManager().request('GET', _url, headers=HEADER).data.decode())['data']['pic']
                await get_cover.send(Message(f"[CQ:image,file={_img_url},id=40000]"))
            except:
                await get_cover.send(f"{bvid}不见了哦")
    else:
        await get_cover.send("请输入正确格式:\n封面 <str>(正确的av/bv号)")


@set_title.handle()
async def _(bot: Bot, event: GroupMessageEvent, title: Message = CommandArg()):
    info = await bot.get_group_member_info(group_id=event.group_id, user_id=bot.self_id)
    if info["role"] == 'owner':
        await bot.set_group_special_title(group_id=event.group_id, user_id=event.user_id, special_title=str(title))
        await set_title.send("头衔设置成功", at_sender=True)
    else:
        await set_title.send("muzi还不是本群群主呢 不能使用这个功能哦 >_<")


@plugin_test.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    # await bot.send(event, event.message)
    # await bot.send(event, event.get_event_name())
    # await bot.send(event, str(event.self_id))
    # await bot.send(event, event.message_type)
    # await bot.send(event, str(event.time))
    # await bot.send(event, event.raw_message)
    # await bot.send(event, str(event.sender.user_id))
    await updata_group_info(event.group_id)
    await plugin_test.send(str(await bot.get_group_member_info(group_id=event.group_id, user_id=bot.self_id, no_cache=True)))
@notice_event.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    await notice_event.send('加入了我们\n来和muzi玩吧', at_sender=True)


@notice_event.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    await notice_event.send('离开了我们\nmuzi会想念你的', at_sender=True)

driver = nonebot.get_driver()


@driver.on_bot_connect
async def _(self):
    await updata_all_group_info()
