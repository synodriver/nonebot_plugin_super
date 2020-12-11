# -*- coding: utf-8 -*-
import json
import traceback

import aiohttp
import nonebot
from nonebot import require
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, Message

ALLOW_BOTS = ["1793268622"]
config: nonebot.config.Config = nonebot.get_driver().config


async def check_bot(bot: Bot, event: Event, state: dict) -> bool:
    """
    只有规定的bot才能触发
    """
    return True if event.self_id in ALLOW_BOTS else False


headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'tool.runoob.com',
           'Origin': 'https://c.runoob.com', 'Referer': 'https://c.runoob.com/compile/66', 'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

language_map: dict = {"php": 3, "py": 0, "py3": 15, "java": 8, "c": 7, "cpp": 7, "rb": 1, "cs": 10, "scala": 5,
                      "erl": 12, "pl": 14, "sh": 11, "rs": 9, "swift": 16, "go": 6, "node.js": 4, "lua": 17, "pas": 18,
                      "kt": 19, "ts": 1001, "vb": 84, "R": 80}


async def execute(code: str, language: str, user_id: int):
    if language == "js":
        language = "node.js"
    if "sql" not in language:
        async with aiohttp.ClientSession() as session:
            data = {"code": code, "token": "4381fe197827ec87cbac9552f14ec62a", "stdin": "",
                    "language": language_map[language],
                    "fileext": language}
            async with session.post("https://tool.runoob.com/compile2.php", data=data, headers=headers) as resp:
                data = await resp.json()
                print(data)
            return data["output"], data["errors"]
    else:  # super mysql
        if user_id not in config.superusers or not config.navicat_execute_sql:
            return "", ""
        try:
            export = require("nonebot_plugin_navicat")
            if export is None:
                return "", ""
            pool_name = language + "_pool"
            if pool_name in export:
                rows = await export[pool_name].fetch_all(code)
                rows = list(map(list, rows))
                return json.dumps(rows, ensure_ascii=False), ""
        except Exception:
            return "", traceback.format_exc()


super_ = on_command("super", rule=check_bot)


@super_.handle()
async def handle_super_(bot: Bot, event: Event, state: dict):
    try:
        language, code = str(event.message).split("\n", 1)
        language: str = language.strip()
        if code:
            # print(code)
            stdout, stderr = await execute(code, language, event.user_id)
            if temp := stdout.strip():
                await bot.send(event, temp)
            if temp := stderr.strip():
                await bot.send(event, temp)
    except ValueError:  # 只发送了super py 没有参数 \n就弄出来一个
        pass
