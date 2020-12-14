#!/usr/bin/env python
#_*_coding:utf-8_*_

from hoshino import Service,aiorequests
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import base64

import os

FILE_PATH = os.path.dirname(__file__)
字体路径 =  os.path.join(FILE_PATH,"字体.ttf")


装饰器 = Service("大佬九宫格")




大佬们 = {

    "四糸佬":{"QQ号":"380426446","阵营":"守序善良","颜色":"#ff0000ff","位置":(0,0),"名言":"出售小鸡鸡"},
    "咖啡佬":{"QQ号":"438971718","阵营":"中立善良","颜色":"#ffff00ff","位置":(0,1),"名言":"HoshinoBot V2绝赞开发中"},
    "雨滴佬":{"QQ号":"3500549279","阵营":"混乱善良","颜色":"#00ff00ff","位置":(0,2),"名言":"你们赶紧开源"},
    "咯咯佬":{"QQ号":"403729332","阵营":"守序中立","颜色":"#ff8888ff","位置":(1,0),"名言":"在做了（新建文件夹）"},
    "待月佬":{"QQ号":"2813349544","阵营":"绝对中立","颜色":"#ffffffff","位置":(1,1),"名言":"跑路了，跑路了"},
    "明见佬":{"QQ号":"839592615","阵营":"混乱中立","颜色":"#88ff88ff","位置":(1,2),"名言":"我要摸鱼我要摸鱼"},
    "lan佬":{"QQ号":"464331809","阵营":"守序邪恶","颜色":"#ff00ffff","位置":(2,0),"名言":"说了闭源就是闭源"},
    "地河佬":{"QQ号":"2715437140","阵营":"中立邪恶","颜色":"#0000ffff","位置":(2,1),"名言":"我不会我不给"},
    "A佬":{"QQ号":"997460364","阵营":"混乱邪恶","颜色":"#00ffffff","位置":(2,2),"名言":"再这样我private了"}
        }




async def 获取大佬头像(QQ号:str):
    高清头像链接 = f"http://q2.qlogo.cn/headimg_dl?dst_uin={QQ号}&spec=640"
    低清头像链接 = f"http://q2.qlogo.cn/headimg_dl?dst_uin={QQ号}&spec=140"
    头 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

    resp = await aiorequests.get(高清头像链接)
    resp_cont = await resp.content
    头像 = Image.open(BytesIO(resp_cont))
    if 头像.size[0] > 600:
        return 头像

    resp = await aiorequests.get(低清头像链接)
    resp_cont = await resp.content
    头像 = Image.open(BytesIO(resp_cont))
    return 头像






async def 生成九宫格():
    背景 = Image.new("RGBA",(900,1000),"#000000")

    标题字体 = ImageFont.truetype(字体路径, size=70)
    阵营字体 = ImageFont.truetype(字体路径, size=30)
    名言字体 = ImageFont.truetype(字体路径, size=15)

    标题 = ImageDraw.Draw(背景)
    标题.text((450,60),"Pcrbot 阵营九宫格",fill="#ffffffff",font=标题字体,anchor="mm",align="center")

    for 大佬 in 大佬们:

        大佬图片背景 = Image.new("RGBA",(300,300),"#000000ff")
        大佬颜色 = 大佬们[大佬]["颜色"]

        边框1 = Image.new("RGBA",(280,200),大佬颜色)
        边框2 = Image.new("RGBA",(278,198),"#000000ff")
        边框1.paste(边框2,(1,1))

        大佬头像 = await 获取大佬头像(大佬们[大佬]["QQ号"])
        大佬头像 = 大佬头像.resize((180,180))


        大佬图片背景.paste(边框1,(10,10))
        大佬图片背景.paste(大佬头像,(60,20))

        大佬文字 = ImageDraw.Draw(大佬图片背景)
        大佬文字.text((150, 240), 大佬们[大佬]["阵营"], fill=大佬颜色, font=阵营字体, anchor="mm", align="center")
        大佬文字.text((150, 270), 大佬们[大佬]["名言"], fill=大佬颜色, font=名言字体, anchor="mm", align="center")


        大佬X坐标 = 大佬们[大佬]["位置"][1] * 300
        大佬Y坐标 = 大佬们[大佬]["位置"][0] * 300 + 100

        背景.paste(大佬图片背景,(大佬X坐标,大佬Y坐标))

    bio = BytesIO()
    背景.save(bio, format='PNG')
    base64_字符串 = 'base64://' + base64.b64encode(bio.getvalue()).decode()

    return f"[CQ:image,file={base64_字符串}]"




@装饰器.on_fullmatch("大佬九宫格")
async def _大佬九宫格(bot, ev):
    await bot.send(ev, await 生成九宫格())




