import json
import random
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import (Bot, Event, MessageEvent,
                                         PrivateMessageEvent)
from nonebot.log import logger

from nonebot.permission import Permission

QID = 3285540558

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43'}
"""* 请求头"""


MUZI_HELP = '''符号说明:\n<>必选参数 []可选参数 {}相同参数 ()注释\n指令后第一个参数前可以不加空格\n# help (需@机器人) 帮助\n# 自动回复\n    {回复率,RPR} [int](1-100) 设置/查看自动回复回复率\n    kw add <str> <*str>(使用空格间隔每个回复) 添加关键字\n    kw del <str> 删除关键字\n    kw list 查看所有关键字\n    kw check <str> 查看关键字回复\n# 封面 <str>(avxxx,bv/BVxxx)'''


driver = nonebot.get_driver()
MUZI_DATE_PATH = Path("data/muzi_data").absolute()
GROUP_INFO_PATH = MUZI_DATE_PATH / "groups_info"
FRIEND_INFO_PATH = MUZI_DATE_PATH / "friends_info"
@driver.on_startup
async def _():
    if not GROUP_INFO_PATH.exists():
        GROUP_INFO_PATH.mkdir(parents=True)
        logger.warning("muzi_groups_info: 配置文件不存在,已重新生成配置文件......")
    if not FRIEND_INFO_PATH.exists():
        FRIEND_INFO_PATH.mkdir(parents=True)
        logger.warning("muzi_friends_info: 配置文件不存在,已重新生成配置文件......")

