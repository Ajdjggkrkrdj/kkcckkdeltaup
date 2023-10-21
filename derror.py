import simplebot
from deltachat import Message
from simplebot.bot import Replies


@simplebot.filter(tryfirst=True)
def filter_messages(message: Message, replies: Replies) -> bool:
    """Para el uso del bot primero tiene que contactar al administrador"""
    if message.error:
        replies.add(
            text="No se pudo desencriptar, por favor reenvia el mensaje :D", quote=message
        )
        return True
    return False
