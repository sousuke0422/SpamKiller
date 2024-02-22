import asyncio
from loguru import logger
from punycode import convert_punycode_to_unicode
from type import TTarget

from mipac import Note
from mipac.client import ClientManager


def text_helper(note_text: str) -> str:
    if note_text not in 'xn--':
        return note_text
    else:
        return convert_punycode_to_unicode(text_helper)

async def spam_action(note: Note, client: ClientManager, target: TTarget) -> None:
    logger.info('fire 🔥')
    if not target['dry_run']:
        await note.api.action.delete()
        for i in note.file_ids:
            await client.drive.files.action.delete(file_id=i)
            logger.info(f'{note.id} のファイル {i} を削除しました。')

        fu = await client.user.action.get(note.user.id)
        await fu.api.admin.action.suspend()
        logger.success(f'@{note.user.username}@{note.user.host} suspend ❄')
    else:
        logger.info('no action by dry_run')
