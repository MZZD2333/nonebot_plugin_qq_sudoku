import json
import random
from tokenize import group
import nonebot
from nonebot.adapters.onebot.v11 import *
# add_keyword = on_command("kw add", priority=1, block=True)
# del_keyword = on_command("kw del", priority=1, block=True)
# del_all_keyword = on_command(
#     "kw del_all", permission=SUPERUSER, priority=1, block=True)
# del_reply = on_command("kw del rp", priority=1, block=True)
# check_KW_DICT = on_command("kw list", priority=1, block=True)
# check_kw = on_command("kw check", priority=1, block=True)

# def probability():
#     async def _probability() -> bool:
#         global reply_p
#         return True if random.randint(1, 100) <= reply_p else False
#     return Rule(_probability)

'''@autoresponder.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.get_plaintext()
    id = event.get_session_id().split("_")[1]
    kws = json.load(
        open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))["keywords"]
    for kw in kws:
        if kw in msg:
            await autoresponder.send(Message(random.choice(kws[kw])))
            break
'''
async def kw_handle(bot: Bot, event: GroupMessageEvent):
    msg = event.raw_message
    cmd_list = ('kw add','kw del','kw del_all','kw list','kw check','kw list','kw eq')
# async def add_keyword_handle(bot: Bot, event: GroupMessageEvent, msg: str):
#     id = event.get_session_id().split("_")[1]
#     gf = json.load(open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))
#     _list = str(msg).split()
#     if len(_list) > 1:
#         kw = _list[0]
#         rps = list(set(_list[1:]))
#         if check_badwords(_list):
#             if kw in gf["keywords"]:
#                 await bot.send(event, f"关键字\n>>>{kw}<<<\n已存在")
#                 for rp in rps:
#                     if rp not in gf["keywords"][kw]:
#                         gf["keywords"][kw].append(rp)
#                         await bot.send(event, Message(f"已为>>>{kw}<<<添加回复\n>>>{rp}"))
#                     else:
#                         await bot.send(event, Message(f"回复已存在\n>>>{rp}"))
#             else:
#                 gf["keywords"][kw] = rps
#                 await bot.send(event, Message(f"已为>>>{kw}<<<\n添加回复\n" + '\n'.join(rps)))
#             with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as file:
#                 json.dump(gf, file, ensure_ascii=False, indent=4)
#         else:
#             await bot.send(event, "含有敏感词")
#     else:
#         await bot.send(event, f"格式错误\nkw add <str> <*str>(使用空格间隔每个回复)")
# 
# @kw_macther.handle()
# @add_keyword.handle()
# async def _(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
#     await add_keyword_handle(bot, event, str(msg))

# @del_all_keyword.handle()
# async def _(bot: Bot, event: GroupMessageEvent):
#     id = event.get_session_id().split("_")[1]
#     gf = json.load(open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))
#     gf["keywords"] = {}
#     with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as file:
#         json.dump(gf, file, ensure_ascii=False, indent=4)


# @del_keyword.handle()
# async def _(bot: Bot, event: GroupMessageEvent, kw: Message = CommandArg()):
#     if kw:
#         kw = str(kw)
#         id = event.get_session_id().split("_")[1]
#         gf = json.load(
#             open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))
#         if kw in gf["keywords"]:
#             del gf["keywords"][kw]
#             with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as file:
#                 json.dump(gf, file, ensure_ascii=False, indent=4)
#             await del_keyword.send(f">>>{kw}<<<\n已删除")
#         else:
#             await del_keyword.send(f"{kw}不存在")
#     else:
#         await del_keyword.send("格式错误\nkw del <str>")


# @check_probability.handle()
# async def _(bot: Bot, n: Message = CommandArg()):
#     if n:
#         n = str(n)
#         if n.isdigit() and 0 <= int(n) <= 100:
#             global reply_p
#             reply_p = int(n)
#             await check_probability.send(f"当前回复率:{reply_p}%")
#         else:
#             await check_probability.send("格式错误\n{回复率,RPR} [int](0-100)整数")

#     else:
#         await check_probability.send(f"当前回复率:{reply_p}%")


# @check_KW_DICT.handle()
# async def _(bot: Bot, event: GroupMessageEvent):
#     id = event.get_session_id().split("_")[1]
#     kws = json.load(
#         open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))["keywords"]
#     await check_KW_DICT.send("本群关键词\n> "+'\n> '.join(list(kws.keys())))


# @check_kw.handle()
# async def _(bot: Bot, event: GroupMessageEvent, kw: Message = CommandArg()):
#     kw = str(kw)
#     id = event.get_session_id().split("_")[1]
#     kws = json.load(
#         open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8'))["keywords"]
#     if kw in kws:
#         await check_KW_DICT.send(Message("\n".join(list(kws[kw]))))
#     else:
#         await check_KW_DICT.send(f">>>{kw}<<<不存在")
