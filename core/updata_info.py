import json
import time
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Bot
from nonebot.log import logger

from .configs import GROUP_INFO_PATH, QID

class GroupInfo:
    '''
    群信息类
    * group_id  群号
    * group_name  群名
    * count  群成员总数
    * role  机器人权限
    * join_time  机器人账号入群时间
    * state  机器人是否启用
    * reply_rate  自动回复回复率
    * plugins  启用插件
    * keywords  自动回复关键字
    * badwords  群屏蔽词
    '''
    def __init__(self,
                 group_id=0,
                 group_name="",
                 count=0,
                 join_time=0,
                 role="member",
                 state="enable",
                 reply_rate=50,
                 plugins=[],
                 keywords={},
                 badwords=[]):
        self.group_id = int(group_id)
        self.group_name = str(group_name)
        self.count = int(count)
        self.role = str(role)
        self.join_time = str(join_time)
        self.state = str(state)
        self.reply_rate = int(reply_rate)
        try:
            _data = json.load(open(GROUP_INFO_PATH/f"{self.group_id}.json", 'r', encoding='utf-8'))
            self.plugins = _data["plugins"]
            self.keywords = _data["keywords"]
            self.badwords = _data["badwords"]
        except:
            self.plugins = plugins
            self.keywords = keywords
            self.badwords = badwords

    async def get(self) -> dict:
        '''获取最新群信息'''
        bot: Bot = nonebot.get_bot()
        group_info = await bot.get_group_info(group_id=self.group_id, no_cache=True)
        personal_info = await bot.get_group_member_info(group_id=self.group_id, user_id=bot.self_id, no_cache=True)
        self.group_name = group_info["group_name"]
        self.count = group_info["member_count"]
        self.role = personal_info["role"]
        self.join_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(personal_info["join_time"]))
        return self.__dict__

    def default(self) -> dict:
        '''返回默认群信息'''
        return self.__dict__

async def updata_all_group_info():
    _bot: Bot = nonebot.get_bot()
    all_group_info_list = await _bot.get_group_list()
    all_group = [g['group_id'] for g in all_group_info_list]
    for id in all_group:
        await updata_group_info(id)

async def updata_group_info(id, state="enable"):
    group_info = GroupInfo(id, state)
    if not Path(GROUP_INFO_PATH/f"{id}.json").exists():
        logger.info(f'群{id}信息不存在 正在生成')
        try:
            data = await group_info.get()
            with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except:
            logger.warning(f'群{id}信息 生成失败')
    elif json.load(open(GROUP_INFO_PATH/f"{id}.json", 'r', encoding='utf-8')).keys() != group_info.default().keys():
        logger.warning(f'群{id}信息格式错误 正在重新生成')
        try:
            data = await group_info.get()
            with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except:
            logger.warning(f'群{id}信息 生成失败')
    else:
        try:
            data = await group_info.get()
            with open(GROUP_INFO_PATH/f"{id}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f'群{id}信息 已更新')
        except:
            logger.warning(f'群{id}信息 更新失败')
