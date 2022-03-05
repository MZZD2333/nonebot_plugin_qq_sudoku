from nonebot.adapters.onebot.v11 import *
from nonebot.plugin import on_command

from .createsudoku import get_qq_img, sudoku

sudoku_matcher = on_command("九宫格")

@sudoku_matcher.handle()
async def _(bot: Bot, event: MessageEvent):
    imgs = sudoku(get_qq_img(str(event.get_message()))).get_sudoku()
    for img in imgs:
        await sudoku_matcher.send(MessageSegment.image(img))
    await sudoku_matcher.send("按此顺序长传至精选图片即可")

__plugin_name__ = "QQ精选图片九宫格制作"