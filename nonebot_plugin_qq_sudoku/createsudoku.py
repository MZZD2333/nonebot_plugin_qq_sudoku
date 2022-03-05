import base64
import re
from io import BytesIO

import requests
from PIL import Image


def get_qq_img(msg: str) -> bytes:
    '''获取QQ聊天图片'''
    _data = requests.get(url=re.search(r'\[(.*)\]',msg).group(1).split(',')[2][4:])
    return BytesIO(_data.content)
        
class sudoku:
    def __init__(self, bimg: bytes) -> None:
        self.p = 0.75
        self.img = Image.open(bimg)
        self.w, self.h = self.img.size
        # 初步处理图片使其长宽比为 3:4
        # 若不符合 3:4 则从左上角截取
        if self.w/self.h > self.p:
            self.w = self.h*self.p
            self.img = self.img.crop((0, 0, int(self.w), self.h))
        elif self.w/self.h < self.p:
            self.h = self.w/self.p
            self.img = self.img.crop((0, 0, self.w, int(self.h)))

    def get_sudoku(self):
        '''返回bs4图片列表'''
        bs4imglist = []
        a = int(self.w/3) # 三分之一宽
        b = int(self.h/4) # 四分之一高
        img9 = self.img.crop((0, 0, 2*a, 2*b)) # 图 9
        img8 = self.img.crop((2*a, 0, 3*a, b)) # 图 8
        img7 = self.img.crop((2*a, b, 3*a, 2*b)) # 图 7
        img6 = self.img.crop((0, 2*b, a, 3*b)) # 图 6
        img5 = self.img.crop((a, 2*b, 2*a, 3*b)) # 图 5
        img4 = self.img.crop((2*a, 2*b, 3*a, 3*b)) # 图 4
        img3 = self.img.crop((0, 3*b, a, 4*b)) # 图 3
        img2 = self.img.crop((a, 3*b, 2*a, 4*b)) # 图 2
        img1 = self.img.crop((2*a, 3*b, 3*a, 4*b)) # 图 1
        imglist = [img1, img2, img3, img4, img5, img6, img7, img8, img9]
        for i in imglist:
            # 转base64
            img = BytesIO()
            i.save(img, format='PNG')
            base64_str = base64.b64encode(img.getvalue()).decode()
            bs4imglist.append('base64://' + base64_str)
        
        return bs4imglist
