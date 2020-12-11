# -*- coding: utf-8 -*-
import asyncio

import aiohttp
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, Message

"""
LUA_PATH = r"F:\miraiok\lua-5.4.1_Win64_bin\lua.exe"

async def execute_lua(code: str):
    process = await asyncio.create_subprocess_exec(LUA_PATH, "-e", code, stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout = await process.stdout.read().decode()
    stderr = await process.stderr.read().decode()
    return stdout, stderr
"""
headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'tool.runoob.com',
           'Origin': 'https://c.runoob.com', 'Referer': 'https://c.runoob.com/compile/66', 'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}


async def execute_lua(code: str):
    async with aiohttp.ClientSession() as session:
        data = {"code": code, "token": "4381fe197827ec87cbac9552f14ec62a", "stdin": "", "language": 17,
                "fileext": "lua"}
        async with session.post("https://tool.runoob.com/compile2.php", data=data, headers=headers) as resp:
            data = await resp.json()
            print(data)
        return data["output"], data["errors"]


super_lua = on_command("super lua")


@super_lua.handle()
async def handle_lua(bot: Bot, event: Event, state: dict):
    # print(type(asyncio.get_running_loop()))
    # assert isinstance(asyncio.get_running_loop(), asyncio.ProactorEventLoop)
    if code := str(event.message):
        stdout, stderr = await execute_lua(code)
        if temp := stdout.strip():
            await bot.send(event, temp)
        if temp := stderr.strip():
            await bot.send(event, temp)


if __name__ == "__main__":
    stdout, stderr = asyncio.run(execute_lua("print(1)"))
    print(stdout)
