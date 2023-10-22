"""simplebot_upload_free : Descargador basado en simplebot_downloader, el mismo crea enlaces de descarga gratuitos :D"""
import simplebot
from deltachat import Message, Chat, Contact
from simplebot.bot import DeltaBot, Replies
import psutil
import sys
from cliente import *
import os
from downloader import FileTooBig, download_file, split_download, get_setting
import time
from threading import Thread
from typing import Callable, Dict, Generator

#==============================#
           #Power by FrancyJ2M#
                      #Ver: 1.1
#==============================#

ADMIN = "frankramiro.martinez@nauta.cu" #ser supremo v:,<
USERS = ['frankramiro.martinez@nauta.cu'] #usuarios permitidos 
CHAT_ID = None
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
    bot.account.set_config("displayname","[Delta] maxUpload")
    #bot.account.set_config("delete_device_after","3600")
    bot.account.set_config('selfstatus', 'Hola soy un robot de correo electrónico 🤖. Power by simplebot_uploader_free\n\n👨🏼‍💻Dev: frankramiro.martinez@nauta.cu')
     
    if mode == "filter":
        bot.filters.register(download_filter)
    else:
        bot.commands.register(download_cmd, name="/download")


@simplebot.hookimpl
def deltabot_start(bot: DeltaBot) -> None:
    Thread(target=_send_files, args=(bot,)).start()
    bot.get_chat(ADMIN).send_text("Me eh reiniciado ☁️⚡")


def download_filter(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Enviame un enlace de descarga directa y te devolvere un enlace de descarga gratuita :D\n\nPower by FrancyJ2M
    """
    addr = message.get_sender_contact().addr
    if addr not in USERS:
    	replies.add("**⚠️ ⟨ACCESO DENEGADO⟩ ⚠️**\nPara poder utilizarme primero debe de hacerle **un pequeño favor** al dev.\n*No se preocupe no es dinero solo es algo que le tomará 15min máximo.Contáctelo para que obtenga acceso gratis* 🙂⬇️\n`frankramiro.martinez@nauta.cu`")
    #	replies.add(f"[{contacto.name}]({addr}) envio un mensaje:\n`{message.text}`", sender = "User not loged!",  chat = CHAT_ID)
    	return
    	if message.chat.is_multiuser() or not message.text.startswith("http"):
    	   replies.add("Sorry no puedo hablar, solo mandame enlaces directos pndj 🙂",quote=message)
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
                client.upload(path, chat, replies, addr)
                if num == parts_count:
                    next(parts, None)  # close context
                    downloads.pop(addr, None)
            except FileTooBig as ex:
                downloads.pop(addr, None)
                replies.add(text=f"{ex}", chat=chat)
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

"""@simplebot.command(admin=False)
def stats(bot, replies) -> None:
    Informacion y estado actual del bot :D
    cont = 0
    for i in USER:
        cont+=1
    
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage(os.path.expanduser("~/.simplebot/"))
    proc = psutil.Process()
    botmem = proc.memory_full_info()
    size = 0
    bot_path = os.path.expanduser("~/.simplebot/accounts/"+encode_bot_addr)
    for path, dirs, files in os.walk(bot_path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    replies.add(
        text="**🖥️ Etado de la PC:**\n"
        f"*CPU* : `{psutil.cpu_percent(interval=0.1)}%`\n"
        f"*Memory* : `{sizeof_fmt(mem.used)}/{sizeof_fmt(mem.total)}`\n"
        f"*Swap* : `{sizeof_fmt(swap.used)}/{sizeof_fmt(swap.total)}`\n"
        f"*Disk* : `{sizeof_fmt(disk.used)}/{sizeof_fmt(disk.total)}`\n\n"
        "**🤖 Estado del Bot:**\n"
        f"*CPU* : `{proc.cpu_percent(interval=0.1)}%`\n"
        f"*Memory* : `{sizeof_fmt(botmem.rss)}`\n"
        f"*Swap* : `{sizeof_fmt(botmem.swap if 'swap' in botmem._fields else 0)}`\n"
        f"*Path* : `{sizeof_fmt(size)}`\n"
        f"*SimpleBot* : `{simplebot.__version__}`\n"
        f"*DeltaChat* : `{deltachat.__version__}`\n"
        f"*Telethon* : `{TC.__version__}`\n"
        f"*simplebot_tg* : `{version}`\n"
        f"*Users logueados* : `{cont}`\n",
        html=bot.account.get_connectivity_html()
    )"""

@simplebot.command(admin=False)
def verify(bot: DeltaBot, replies: Replies) -> None:
    """Obten el enlace de verificacion del bot."""
    replies.add(text=bot.account.get_setup_contact_qr())
    
@simplebot.command(admin=False)
def report(bot, message, payload, replies):
    """Reportar errores!.Si hace preguntas estupidas o spam puede ser banneado para siempre del bot\nEj: /report Ocurrió ****"""
    addr = message.get_sender_contact().addr
    contacto = message.get_sender_contact().name
    
    bot.get_chat(ADMIN).send_text('🤖 **Msg de ['+contacto+']('+addr+')** :\n'+payload)
    replies.add("✔️ *Reporte enviado* ")
        
@simplebot.command(admin=True)
def responder(bot, payload, replies):
    """ Responderle a un usuario a traves del bot :v """
    correo = payload.split()
    msg = payload
    msg = payload.replace(correo[0] , '')
    bot.get_chat(correo[0]).send_text('🖥️ **Mensaje del admin** 🤖\n'+msg)
    replies.add("✔️ *Mensaje enviado*")
    
@simplebot.command(admin=True)
def msg_global(bot, payload, replies):
    """ Enviar msg a todos los usuarios logueados """
    #correo = payload.split()
    msg = payload
    con=0  
    for correos in USERS1:
        con+=1
        bot.get_chat(correos).send_text('# ⚠️ **Mensaje Global** ⚠️\n'+msg)
    replies.add("🤖 Mensaje recivido por **"+str(con)+"** users")
    
@simplebot.command(admin=True)    
def sett(bot, payload, replies):
    """Ejecutar codigo Python al vuelo.Ej: /eval 2+2"""
    try:
       code = str(eval(payload))
    except:
       code = str(sys.exc_info())
    replies.add(text=code or "echo")
    
@simplebot.command(admin=True)    
def add(bot, payload, replies):
    """Dar permiso para el uso del bot papu :v"""
    try:
    	USERS.append(payload)
    	replies.add(f"Permiso concedido para {payload}")
    	bot.get_chat(CHAT_ID).send_text(USERS+"\n\n#users")
    except Exception as ex:
    	replies.add(f"{ex}")
    
@simplebot.command(admin=True)    
def del_user(bot, payload, replies):
    """Quitar permiso para el uso del bot papu :v"""
    USERS.remove(payload)
    replies.add(f"Permiso eliminado para {payload}")
    bot.get_chat(CHAT_ID).send_text(USERS+"\n\n#users")
    
@simplebot.command(admin=True)
def grupo(bot,payload,replies,message):
	 try:
	 	global CHAT_ID
	 	contacto = message.get_sender_contact()
	 	titulo = "[DB] maxUpload 💽"
	 	chat_id = bot.create_group(titulo, [contacto])
	 	CHAT_ID = chat_id
	 	#replies.add(text=str(chat_id))
	 except Exception as ex:
	 	replies.add(f"{ex}")