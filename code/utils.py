import random
import asyncio
import re
from datetime import datetime
import pytz
from colorama import init, Fore, Style
from telethon.tl import functions, types



def logger(text, type):

    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)
    formatted_time = moscow_time.strftime('%d.%m-%H:%M')

    text = "[" + formatted_time + "]" + "    " + text

    if type == "stat-error":
        print(Fore.RED + text + Style.RESET_ALL)
    if type == "error":
        print("")
        print(Fore.RED + text + Style.RESET_ALL)
        print("")
    if type == "warn":
        print(Fore.YELLOW + text + Style.RESET_ALL)
    if type == "silly":
        print(Fore.GREEN + text + Style.RESET_ALL)
    if type == "info":
        print(Fore.WHITE + text + Style.RESET_ALL)

    with open('./logs.txt', 'a', encoding='utf-8') as f:
        f.write(text + '\n')


def getSetting(path, named):
    with open(f"{path}.config", 'r', encoding='utf-8') as file:
        CONFIG = list(filter(None, file.read().split('\n')))
        file.close()

    for item in CONFIG:
        if named in item:
            return item.split(" = ")[1]
    

def setSetting(path, named, value):
    with open(f"{path}.config", 'a', encoding='utf-8') as file:
        file.write(f"{named} = {value}")
        file.write("\n")


async def getSaved(client):
    while True:
        try:
            text = await client.get_messages("me", limit = 1)
            text = text[0].message
            if text:
                return text
            else:
                logger(f"[SAVED] [ERROR] Нет сообщения в Избранном. Ожидаю 30...", "error")
                await asyncio.sleep(30)

        except Exception as e:
            logger(f"[SAVED] [ERROR] Нет сообщения в Избранном. Ожидаю 30...", "error")
            await asyncio.sleep(30)


def randomText(text):
    n = True
    while n:
        text, n = re.subn(r"{([^{}]+)}", lambda x: random.choice(x.group(1).split("|")), text)

    message = ""
    for letter in text:
        convert = {
        'А': ['А', 'Α'],
        # 'а': ['а', 'α'],
        'Р': ['Р', 'Ρ'],
        'р': ['р', 'ρ'],
        'В': ['В', 'Β'],
        'К': ['К', 'Κ'],
        'к': ['к', 'κ'],
        'Т': ['Т', 'Τ'],
        'Г': ['Г', 'Γ'],
        # 'Л': ['Л', 'Λ'],
        'М': ['М', 'Μ'],
        'Н': ['Н', 'Η'],
        'О': ['О', 'Ο'],
        'о': ['о', 'ο'],
        'П': ['П', 'Π'],
        'п': ['п', 'п'],
        'Е': ['Е', 'Ε']
        }

        if letter in convert and len(convert[letter]) > 1:
            message += random.choice(convert[letter])
        else:
            message += letter

    return message


async def sendComment(client, channel_id, message, post_id):
    try:
        await client.send_message(
            entity = channel_id,
            message = message,
            comment_to = post_id
        )

        return "sended"
    except Exception as e:
        if "The message ID used in the peer was invalid" in repr(e):
            return "no_comments"
        
        if "The channel specified is private and you lack permission to access it" in repr(e):
            return "banned"
        
        if "You can't write in this chat" in repr(e):
            return "banned"
        
        return repr(e)


async def sendMessage(client, group_entity, group_id, text, params):
    try:    
        if params["tager"] > 0:
            logger(f"[INFO] Собираю людей для тега...", "info")
            new_text = "Привет "
            admin_usernames = []
            async for admin in client.iter_participants(group_id, filter = types.ChannelParticipantsAdmins):
                try:
                    if admin.username:
                        admin_usernames.append(admin.username)
                except Exception as e:
                    pass
            count = 0
            while count < params["tager"]:
                await asyncio.sleep(1)
                writed = (random.randint(30, int(group_entity.participants_count)//10))
                writed = await client(functions.channels.GetParticipantsRequest(
                    group_entity, 
                    types.ChannelParticipantsSearch(''), 
                    offset = writed, 
                    limit = params["tager"],
                    hash = 0
                ))
                logger(f"[INFO] Взял людей", "info")
                if not writed.users:
                    break
                for user in writed.users:
                    if user.username:
                        logger(f"[INFO] Проверяю {user.username}...", "info")
                        if user.bot:
                            logger(f"[INFO] Бот", "info")
                            continue
                        if user.username in admin_usernames:
                            logger(f"[INFO] Админ", "info")
                            continue
                        if user.premium:
                            logger(f"[INFO] Потенциально кадровик", "info")
                            continue
                        status = user.status
                        if status:
                            status = status.stringify()
                            if status.split("(")[0] == "UserStatusOffline":
                                writed = status.split("(")[2].split(",")
                                status_time = int(writed[0])*31536000 + int(writed[1])*2678400 + int(writed[2])*86400
                                writed = datetime.now()
                                current_time = writed.year*31536000 + writed.month*2678400 + writed.day*86400
                                if current_time - status_time > 604800:
                                    logger(f"[INFO] Давно не в сети", "info")
                                    continue
                            else:
                                if status.split("(")[0] != "UserStatusRecently" and status.split("(")[0] != "UserStatusOnline":
                                    logger(f"[INFO] Давно не в сети", "info")
                                    continue

                        new_text = new_text + " @" + user.username
                        count += 1
                        logger(f"[INFO] Прошел {count}", "info")

            logger(f"[INFO] Отправляю {new_text}...", "info")
            message = await client.send_message(group_id, new_text)
            try:
                logger(f"[INFO] Редактирую на {text}...", "info")
                await client.edit_message(group_id, message.id, text)
            except Exception as e:
                logger(f"[INFO] Не позволило отредактировать", "info")

            del new_text
            del message
        else:
            logger(f"[INFO] Отправляю {text}...", "info")
            await client.send_message(group_id, text)
        
        return "sended"
        
    except Exception as e:
        error_message = str(e)
        if "seconds is required before sending another message in this chat" in error_message.lower():
            return "no_send_time"
        if "you can't write in this chat" in error_message.lower():
            return "no_send_ban"
        if "topic_closed" in error_message.lower():
            return "topic_closed"
        if "you're banned from sending messages" in error_message.lower():
            return "spam"
        if "CHAT_SEND_PLAIN_FORBIDDEN" in str(repr(e)):
            return "forbidden"
        return repr(e)
    

async def joinRequest(client, group):
        try:
            await client(functions.channels.JoinChannelRequest(group))
            return "joined"

        except Exception as e:
            error_message = str(e)
            if "you have successfully requested to join this chat or channel" in error_message.lower():
                return "join_request"
            return(repr(e))