"""simplebot_upload_free : Descargador basado en simplebot_downloader, el mismo crea enlaces de descarga gratuitos :D"""
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from cliente import *
import os
from .downloader import FileTooBig, download_file, get_setting, split_download
import time
from threading import Thread
from typing import Callable, Dict, Generator

#==============================#
           #Power by FrancyJ2M#
                      #Ver: 1.1
#==============================#

DEF_MAX_SIZE = str(1024**2 * 100)
DEF_PART_SIZE = str(1024**2 * 100)
MAX_QUEUE_SIZE = 5
DEF_DELAY = "30"
downloads: Dict[str, Generator] = {}


@simplebot.hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    get_setting(bot, "max_size", DEF_MAX_SIZE)
    get_setting(bot, "part_size", DEF_PART_SIZE)
    get_setting(bot, "delay", DEF_DELAY)
    mode = get_setting(bot, "mode", "filter")

    if mode == "filter":
        bot.filters.register(download_filter)
    else:
        bot.commands.register(download_cmd, name="/download")


@simplebot.hookimpl
def deltabot_start(bot: DeltaBot) -> None:
    Thread(target=_send_files, args=(bot,)).start()


def download_filter(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Enviame un enlace de descarga directa y te devolvere un enlace de descarga gratuita :D
    
    Power by FrancyJ2M
    """
    if message.chat.is_multiuser() or not message.text.startswith("http"):
        replies.add("Sorry no puedo hablar, solo mandame enlaces directo pndj 🙂",quote=message)
        return
    queue_download(message.text, bot, message, replies)


def download_cmd(
    bot: DeltaBot, payload: str, message: Message, replies: Replies
) -> None:
    """Download the given file link.

    Example:
    /download https://example.com/path/to/file.zip
    """
    queue_download(payload, bot, message, replies)


def queue_download(
    url: str,
    bot: DeltaBot,
    message: Message,
    replies: Replies,
    downloader: Callable = download_file,
) -> None:
    addr = message.get_sender_contact().addr
    if addr in downloads:
        replies.add(text="Espere, ya tiene un proceso en curso 😴", quote=message)
    elif len(downloads) >= MAX_QUEUE_SIZE:
        replies.add(
            text="😬 Ya estoy procesando ** 5 subidas a la vez,** por favor reintente más tarde ⚠️",
            quote=message,
        )
    else:
        replies.add(text="**✅ Solicitud agregada/procesando ✅**", quote=message)
        part_size = int(get_setting(bot, "part_size"))
        max_size = int(get_setting(bot, "max_size"))
        downloads[addr] = split_download(url, part_size, max_size, downloader)


def _send_files(bot: DeltaBot) -> None:
    replies = Replies(bot, bot.logger)
    while True:
        items = list(downloads.items())
        bot.logger.debug("Processing downloads queue (%s)", len(items))
        start = time.time()
        for addr, parts in items:
            chat = bot.get_chat(addr)
            try:
                path, num, parts_count = next(parts)
                #text = f"Part {num}/{parts_count}"
                client = RUVSUpload()
                client.init('julio','UploadZ0*')
                client.upload(path, chat)
                if num == parts_count:
                    next(parts, None)  # close context
                    downloads.pop(addr, None)
            except FileTooBig as ex:
                downloads.pop(addr, None)
                replies.add(text=f"# ⚠️ERROR⚠️\n```{ex}```", chat=chat)
                replies.send_reply_messages()
            except (StopIteration, Exception) as ex:
                bot.logger.exception(ex)
                downloads.pop(addr, None)
                replies.add(
                    text="*🚫 Error en el enlace de descarga, revise que sea directo 😐*", chat=chat
                )
                replies.send_reply_messages()
        delay = int(get_setting(bot, "delay")) - time.time() + start
        if delay > 0:
            time.sleep(delay)
