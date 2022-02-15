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
from .configs import (DEFAULT_REPLY_P, FRIENDS, GROUP_INFO_PATH, HEADER,
                      KW_DICT_PATH, MUZI_HELP)
from .update_info import update_all_group_info
from .utils import check_badwords, check_role
from .autorespond import add_keyword_handle
flag_1 = True
reply_p = DEFAULT_REPLY_P

KW_DICT: dict = json.load(open(KW_DICT_PATH, 'r', encoding='utf-8'))


def probability():
    async def _probability() -> bool:
        global reply_p
        return True if random.randint(1, 100) <= reply_p else False
    return Rule(_probability)


autoresponder = on_message(rule=probability(), priority=10)

muzi_help = on_command("help", rule=to_me(), priority=1, block=True)
check_probability = on_command("回复率", aliases={"RPR"}, priority=1, block=True)
tiaojiao = on_command("调教", permission=FRIENDS, priority=1, block=True)
add_keyword = on_command("kw add", priority=1, block=True)
del_keyword = on_command("kw del", priority=1, block=True)
del_all_keyword = on_command(
    "kw del_all", permission=SUPERUSER, priority=1, block=True)
del_reply = on_command("kw del rp", priority=1, block=True)
check_KW_DICT = on_command("kw list", priority=1, block=True)
check_kw = on_command("kw check", priority=1, block=True)
plugin_test = on_command("test", permission=SUPERUSER, priority=1, block=True)
get_cover = on_command("封面", priority=1, block=True)
set_title = on_command("头衔", priority=1, block=True)
notice_event = on_notice()


@autoresponder.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.get_plaintext()
    id = event.get_session_id().split("_")[1]
    kws = json.load(
        open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))["keywords"]
    for kw in kws:
        if kw in msg:
            await autoresponder.send(Message(random.choice(kws[kw])))
            break


@muzi_help.handle()
async def _(bot: Bot, event: MessageEvent):
    await tiaojiao.send(MUZI_HELP)


@tiaojiao.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await tiaojiao.send("""kw add <str> <*str>(使用空格间隔每个回复) 添加关键字\nkw list 查看所有关键字\nkw check <str> 查看关键字回复""")


@add_keyword.handle()
async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    await add_keyword_handle(bot, event, str(msg))

@del_all_keyword.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    id = event.get_session_id().split("_")[1]
    gf = json.load(open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))
    gf["keywords"] = {}
    with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as file:
        json.dump(gf, file, ensure_ascii=False, indent=4)


@del_keyword.handle()
async def _(bot: Bot, event: GroupMessageEvent, kw: Message = CommandArg()):
    if kw:
        kw = str(kw)
        id = event.get_session_id().split("_")[1]
        gf = json.load(
            open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))
        if kw in gf["keywords"]:
            del gf["keywords"][kw]
            with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as file:
                json.dump(gf, file, ensure_ascii=False, indent=4)
            await del_keyword.send(f">>>{kw}<<<\n已删除")
        else:
            await del_keyword.send(f"{kw}不存在")
    else:
        await del_keyword.send("格式错误\nkw del <str>")


@check_probability.handle()
async def _(bot: Bot, n: Message = CommandArg()):
    if n:
        n = str(n)
        if n.isdigit() and 0 <= int(n) <= 100:
            global reply_p
            reply_p = int(n)
            await check_probability.send(f"当前回复率:{reply_p}%")
        else:
            await check_probability.send("格式错误\n{回复率,RPR} [int](0-100)整数")

    else:
        await check_probability.send(f"当前回复率:{reply_p}%")


@check_KW_DICT.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    id = event.get_session_id().split("_")[1]
    kws = json.load(
        open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))["keywords"]
    await check_KW_DICT.send("本群关键词\n> "+'\n> '.join(list(kws.keys())))


@check_kw.handle()
async def _(bot: Bot, event: GroupMessageEvent, kw: Message = CommandArg()):
    kw = str(kw)
    id = event.get_session_id().split("_")[1]
    kws = json.load(
        open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))["keywords"]
    if kw in kws:
        await check_KW_DICT.send(Message("\n".join(list(kws[kw]))))
    else:
        await check_KW_DICT.send(f">>>{kw}<<<不存在")


@get_cover.handle()
async def _(bot: Bot, event: MessageEvent, abv: Message = CommandArg()):
    if abv:
        abv = str(abv)
        bid = f'aid={abv[2:]}' if 'av' == abv[:2].lower() else f'bvid={abv}'
        _url = 'https://api.bilibili.com/x/web-interface/view?' + bid
        r = urllib3.PoolManager().request('GET', _url, headers=HEADER)
        try:
            _img_url = json.loads(r.data.decode())['data']['pic']
            await get_cover.send(Message(f"[CQ:image,file={_img_url},id=40000]"))
        except:
            await get_cover.send(f"{abv}不见了哦")
    else:
        await get_cover.send("请输入正确格式:\n/封面AV/BV号")


@set_title.handle()
async def _(bot: Bot, event: GroupMessageEvent, title: Message = CommandArg()):
    id = event.get_session_id().split("_")[1:]
    if check_role(id[0], "owner"):
        await bot.set_group_special_title(group_id=int(id[0]), user_id=int(id[1]), special_title=str(title))
        await set_title.send("头衔设置成功", at_sender=True)
    else:
        await set_title.send("muzi还不是本群群主呢 不能使用这个功能哦 >_<")


@plugin_test.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event,'233')


@notice_event.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    await notice_event.send('加入了我们\n来和muzi玩吧', at_sender=True)


@notice_event.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent):
    await notice_event.send('离开了我们\nmuzi会想念你的', at_sender=True)

driver = nonebot.get_driver()


@driver.on_bot_connect
async def _(self):
    await update_all_group_info()
