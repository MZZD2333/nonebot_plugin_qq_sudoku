import json
from nonebot.adapters.onebot.v11 import *
from nonebot.rule import KeywordsRule, Rule
from .configs import  GROUP_INFO_PATH

# def check_badwords(words):
#     for w in BAD_WORDS:
#         if w in '/'.join(words):
#             return False
#     else:
#         return True

def check_role(group_id,role):
    return json.load(open(GROUP_INFO_PATH/f"{group_id}.json", 'r', encoding='utf-8'))["role"] is role

def get_group_keywords(id: int):
    return 

