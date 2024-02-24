# SPDX-FileCopyrightText: sousuke0422 and All Contributor
# SPDX-License-Identifier: MIT

import asyncio

from aiohttp import ClientWebSocketResponse
from loguru import logger
from mipa import Note
from mipa.ext.commands.bot import Bot

from src.env import URL, TOKEN
from src.func import spam_action, text_helper
from src.target import TARGETS


class SpamKiller(Bot):
    def __init__(self):
        super().__init__()

    async def _connect_channel(self):
        await self.router.connect_channel(['main', 'global', 'home'])

    async def on_ready(self, ws: ClientWebSocketResponse):
        await self._connect_channel()
        logger.success(f'Logged in: {self.user.username}')

    async def on_reconnect(self, ws: ClientWebSocketResponse):
        await self._connect_channel()
        logger.info('再接続しました')

    async def on_note(self, note: Note):
        if note.user.host and len(note.mentions) >= 2:
            logger.info(f'スパムチェック開始: {URL}/notes/{note.id}')

            for target in TARGETS:
                if note.text is None:
                    continue

                text = text_helper(note.text)
                if target['key'] in text:
                    logger.success(f'パターン一致: {target['key']}')
                    await spam_action(note, self.client, target)
                elif len(note.user.username) == 10:
                    logger.warning(
                        f'spamの可能性があります: @{note.user.username}@{note.user.host} ⚠️'
                    )


if __name__ == '__main__':
    bot = SpamKiller()
    asyncio.run(bot.start(f'{URL}', TOKEN))
