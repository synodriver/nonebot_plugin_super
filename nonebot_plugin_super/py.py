# -*- coding: utf-8 -*-
import asyncio

import aiohttp
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, Message

headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'tool.runoob.com',
           'Origin': 'https://c.runoob.com', 'Referer': 'https://c.runoob.com/compile/66', 'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}


async def execute_py(code: str):
    async with aiohttp.ClientSession() as session:
        data = {"code": code, "token": "4381fe197827ec87cbac9552f14ec62a", "stdin": "", "language": 15,
                "fileext": "py3"}
        async with session.post("https://tool.runoob.com/compile2.php", data=data, headers=headers) as resp:
            data = await resp.json()
            print(data)
        return data["output"], data["errors"]


super_py = on_command("super py")


@super_py.handle()
async def handle_lua(bot: Bot, event: Event, state: dict):
    # print(type(asyncio.get_running_loop()))
    # assert isinstance(asyncio.get_running_loop(), asyncio.ProactorEventLoop)
    if code := str(event.message):
        stdout, stderr = await execute_py(code)
        if temp := stdout.strip():
            await bot.send(event, temp)
        if temp := stderr.strip():
            await bot.send(event, temp)