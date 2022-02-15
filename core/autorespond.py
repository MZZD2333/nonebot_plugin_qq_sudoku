import json
import random
import nonebot
from nonebot.adapters.onebot.v11 import *
from .configs import (DEFAULT_REPLY_P, FRIENDS, GROUP_INFO_PATH, HEADER,
                      KW_DICT_PATH, MUZI_HELP)
from .update_info import update_all_group_info
from .utils import check_badwords, check_role


async def add_keyword_handle(bot: Bot, event: GroupMessageEvent, msg: str):
    id = event.get_session_id().split("_")[1]
    gf = json.load(open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))
    _list = str(msg).split()
    if len(_list) > 1:
        kw = _list[0]
        rps = list(set(_list[1:]))
        if check_badwords(_list):
            if kw in gf["keywords"]:
                await bot.send(event, f"关键字\n>>>{kw}<<<\n已存在")
                for rp in rps:
                    if rp not in gf["keywords"][kw]:
                        gf["keywords"][kw].append(rp)
                        await bot.send(event, Message(f"已为>>>{kw}<<<添加回复\n>>>{rp}"))
                    else:
                        await bot.send(event, Message(f"回复已存在\n>>>{rp}"))
            else:
                gf["keywords"][kw] = rps
                await bot.send(event, Message(f"已为>>>{kw}<<<\n添加回复\n" + '\n'.join(rps)))
            with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as file:
                json.dump(gf, file, ensure_ascii=False, indent=4)
        else:
            await bot.send(event, "含有敏感词")
    else:
        await bot.send(event, f"格式错误\nkw add <str> <*str>(使用空格间隔每个回复)")
