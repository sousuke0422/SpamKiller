from loguru import logger
from mipac import Note
from mipac.client import ClientManager

from src.punycode import convert_punycode_to_unicode
from src.type import TTarget


def text_helper(note_text: str) -> str:
    if note_text not in 'xn--':
        return note_text
    else:
        return convert_punycode_to_unicode(note_text)


async def spam_action(note: Note, client: ClientManager, target: TTarget) -> None:
    logger.info('fire 🔥')
    if not target['dry_run']:
        await note.api.action.delete()
        for i in note.file_ids:
            await client.drive.files.action.delete(file_id=i)
            logger.info(f'{note.id} のファイル {i} を削除しました。')

        found_user = await client.user.action.get(note.user.id)
        # 傾向が変わった際に変更
        if len(found_user.username) == 10:
            await found_user.api.admin.action.suspend()
            logger.success(f'@{note.user.username}@{note.user.host} suspend ❄')
        else:
            logger.success(f'@{note.user.username}@{note.user.host} hit user ⚠️')
            logger.info('投稿のみを削除しました 🗑')
    else:
        logger.info('no action by dry_run')
