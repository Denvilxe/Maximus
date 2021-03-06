# Copyright (C) 2018 Raphielscape LLC.
#
# Licensed under the Raphielscape Public License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import re
import sqlite3
import time

from sqlalchemy import (Boolean, Column, Integer, String, UnicodeText,
                        distinct, func)

from userbot import LOGGER, LOGGER_GROUP
from userbot.events import register


@register(incoming=True)
async def filter_incoming_handler(e):
    try:
        if not (await e.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.filter_sql import get_filters
            except:
                await e.edit("`Running on Non-SQL mode!`")
                return
            listes = e.text.split(" ")
            filters = get_filters(e.chat_id)
            for t in filters:
                for r in listes:
                    pro = re.fullmatch(t.keyword, r, flags=re.IGNORECASE)
                    if pro:
                        await e.reply(t.reply)
                        return
    except:
        pass


@register(outgoing=True, pattern="^.filter\\s.*")
async def add_filter(e):
    chat = await e.get_chat()
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.filter_sql import add_filter
        except:
            await e.edit("`Running on Non-SQL mode!`")
            return
        message = e.text
        kek = message.split()
        string = ""
        for i in range(2, len(kek)):
            string = string + " " + str(kek[i])
        add_filter(str(e.chat_id), kek[1], string)
        await e.edit(f"Filter `{string}` added successfully in {e.chat.title}.")


@register(outgoing=True, pattern="^.stop\\s.*")
async def remove_filter(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.filter_sql import remove_filter
        except:
            await e.edit("`Running on Non-SQL mode!`")
            return
        message = e.text
        kek = message.split(" ")
        remove_filter(e.chat_id, kek[1])
        await e.edit(f"```That filter has been removed successfully from {e.chat.title}```")


@register(outgoing=True, pattern="^.rmfilters$")
async def kick_marie_filter(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("```Will be kicking away all Marie filters.```")
        time.sleep(3)
        r = await e.get_reply_message()
        filters = r.text.split("-")[1:]
        for filter in filters:
            await e.reply("/stop %s" % (filter.strip()))
            await asyncio.sleep(0.3)
        await e.respond(
            "```Successfully purged Marie filters yaay!```\n Gimme cookies!"
        )
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP, "I cleaned all Marie filters at " +
                str(e.chat_id)
            )


@register(outgoing=True, pattern="^.filters$")
async def filters_active(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        try:
            from userbot.modules.sql_helper.filter_sql import get_filters
        except:
            return
        transact = f"Filters active in {e.chat.title}: \n\n"
        filters = get_filters(e.chat_id)
        for i in filters:
            transact = transact + "??? " + i.keyword + "\n"
        await e.edit(transact)
