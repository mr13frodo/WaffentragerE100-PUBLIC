import os
import random
import asyncio
import re
from datetime import datetime
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')



print(f"")
print(f"")
print(f" .oooooo..o            .o88o.     .       .o8                      oooooooooooo                          .o8")
print(f"d8P'    `Y8            888 `    .o8       888                      `888'     `8                          888")
print(f"Y88bo.       .ooooo.  o888oo  .o888oo     888oooo.  oooo    ooo     888         oooo d8b  .ooooo.   .oooo888   .ooooo.")
print(f" ` Y8888o.  d88' `88b  888      888       d88' `88b  `88.  .8'      888oooo8    `888''8P d88' `88b d88' `888  d88' `88b")
print(f"     ` Y88b 888   888  888      888       888   888   `88..8'       888          888     888   888 888   888  888   888")
print(f"oo     .d8P 888   888  888      888 .     888   888    `888'        888          888     888   888 888   888  888   888")
print(f"`8888888P'  `Y8bod8P' o888o      888      `Y8bod8P'     .8'        o888o        d888b    `Y8bod8P' `Y8bod88P  `Y8bod8P'")
print(f"                                                     .o..P'")
print(f"                                                     `Y8P'")
print(f"")
print(f"")



####################################
#
#   Обновление модулей
#
####################################



try:
    import python_socks
    os.system("pip install --upgrade python_socks")
except ImportError:
    os.system("pip install python_socks")
    import python_socks

try:
    import async_timeout
    os.system("pip install --upgrade async_timeout")
except ImportError:
    os.system("pip install async_timeout")
    import async_timeout

try:
    import pytz
    os.system("pip install --upgrade pytz")
except ImportError:
    os.system("pip install pytz")
    import pytz

try:
    from colorama import init, Fore, Style
    os.system("pip install --upgrade colorama")
except ImportError:
    os.system("pip install colorama")
    from colorama import init, Fore, Style

try:
    from telethon import TelegramClient, events
    from telethon.tl import functions, types
    from telethon.tl.functions.messages import GetPeerDialogsRequest
    from telethon.tl.functions.channels import JoinChannelRequest
    os.system("pip install --upgrade telethon")
except ImportError:
    os.system("pip install telethon")
    from telethon import TelegramClient, events
    from telethon.tl import functions, types
    from telethon.tl.functions.messages import GetPeerDialogsRequest
    from telethon.tl.functions.channels import JoinChannelRequest

clear()



####################################
#
#   Основной скрипт
#
####################################



async def main():
    init()

    logger(f"   [MAIN] Запускаюсь...", "silly")

    sessions = [file for file in os.listdir() if file.endswith('.session')]
    if sessions:
        logger(f"   [MAIN] Собираю конфиг...", "silly")
        session = sessions[0][:-8]
        api_id = int(getSetting(session, "API_ID"))
        api_hash = getSetting(session, "API_HASH")
    else:
        logger(f"   [MAIN] Формирую конфиг...", "silly")
        while True:
            try:
                session = input("   Введите название сессии: ")
                api_id = int(input("   Введите api_id сессии: "))
                api_hash = input("   Введите api_hash сессии: ")

                open(f"{session}.config", 'w').close()
                with open(f"{session}.config", 'a', encoding='utf-8') as file:
                    file.write(f"API_ID = {api_id}")
                    file.write("\n")
                    file.write(f"API_HASH = {api_hash}")
                    file.write("\n")
                    file.close()
                break
            except Exception as e:
                print(" ")
                logger(f"   [MAIN] [ERROR] {repr(e)}", "error")
                print(" ")

    proxy_input = input("Введите прокси (IP:PORT:LOGIN:PASSWORD) или нажмите Enter для пропуска: ")
    proxy = None
    if proxy_input:
        proxy_parts = proxy_input.split(':')
        if len(proxy_parts) == 4:
            proxy = {
                'proxy_type': python_socks.ProxyType.HTTP,
                'addr': proxy_parts[0],
                'port': int(proxy_parts[1]),
                'username': proxy_parts[2],
                'password': proxy_parts[3]
            }
    
    async with TelegramClient(session, api_id, api_hash, proxy = proxy) as client:
        while True:
            try:
                clear()
                print(" ")
                print(" ")
                print("     1 - Заполнение аккаунта")
                print("     2 - Заполнение чатами")
                print("     3 - Спам")
                print("   - - - - - -")
                mode = input("   Выберите режим работы: ")

                if mode == "1":
                    await accounter(client, session)
                if mode == "2":
                    await chater(client, session)
                if mode == "3":
                    await spamer(client, session)

            except Exception as e:
                print(" ")
                logger(f"   [MAIN] [ERROR] {repr(e)}", "error")
                print(" ")



####################################
#
#   Заполнение аккаунта
#
####################################



async def accounter(client, session):
    clear()
    logger(f"   [ACCOUNT] Запускаюсь...", "silly")

    while True:
        try:
            input("  Убедитесь в наличии аваторок в папке avatar внутри base")
            AVATARS = []
            try:
                for item in os.listdir("./base/avatar"):
                    AVATARS.append(item)
                if len(AVATARS) == 0:
                    logger(f"[ACCOUNT] [{session}] Аватаров нет, пропускаю...", "warn")
                    AVATARS = None
            except Exception as e:
                logger(f"[ACCOUNT] [{session}] Аватаров нет, пропускаю...", "warn")

            input("  Убедитесь в наличии имен в файле first_name.txt внутри base")
            try:
                with open('./base/first_name.txt', 'r', encoding='utf-8') as file:
                    FIRST_NAMES = list(filter(None, file.read().split('\n')))
                    file.close()
                if len(FIRST_NAMES) == 0:
                    logger(f"[ACCOUNT] [{session}] Имен нет, пропускаю...", "warn")
                    AVATARS = None
            except Exception as e:
                logger(f"[ACCOUNT] [{session}] Имен нет, пропускаю...", "warn")

            input("  Убедитесь в наличии фамилий в файле last_name.txt внутри base")
            try:
                with open('./base/last_name.txt', 'r', encoding='utf-8') as file:
                    LAST_NAMES = list(filter(None, file.read().split('\n')))
                    file.close()
                if len(LAST_NAMES) == 0:
                    logger(f"[ACCOUNT] [{session}] Фамилий нет, пропускаю...", "warn")
                    AVATARS = None
            except Exception as e:
                logger(f"[ACCOUNT] [{session}] Фамилий нет, пропускаю...", "warn")

            try:
                input("  Убедитесь в наличии био в файле status.txt внутри base")
                with open('./base/status.txt', 'r', encoding='utf-8') as file:
                    STATUSES = list(filter(None, file.read().split('\n')))
                    file.close()
                if len(STATUSES) == 0:
                    logger(f"[ACCOUNT] [{session}] Био нет, пропускаю...", "warn")
                    AVATARS = None
            except Exception as e:
                logger(f"[ACCOUNT] [{session}] Био нет, пропускаю...", "warn")

            break

        except Exception as e:
            logger(f"[ACCOUNT] [{session}] [ERROR] {repr(e)}", "error")

    try:
        logger(f"  [ACCOUNT] [{session}] Меняю информацию...", "silly")

        if FIRST_NAMES:
            first_name = FIRST_NAMES[random.randint(0, len(FIRST_NAMES) - 1)]
            await client(functions.account.UpdateProfileRequest(
                first_name = first_name
            ))

        if LAST_NAMES:
            last_name = LAST_NAMES[random.randint(0, len(LAST_NAMES) - 1)]
            await client(functions.account.UpdateProfileRequest(
                last_name = last_name
            ))

        if STATUSES:
            status = STATUSES[random.randint(0, len(STATUSES) - 1)]
            await client(functions.account.UpdateProfileRequest(
                about = status
            ))

        if AVATARS:
            logger(f"  [ACCOUNT] [{session}] Гружу аватар...", "silly")
            avatar = f"./base/avatar/{AVATARS[random.randint(0, len(AVATARS) - 1)]}"
            await client(functions.photos.UploadProfilePhotoRequest(
                file = await client.upload_file(avatar)
            ))

        logger(f"  [ACCOUNT] [{session}] Запрещаю пересылать сообщения...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyForwards(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        logger(f"  [ACCOUNT] [{session}] Запрещаю звонить...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneCall(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        logger(f"  [ACCOUNT] [{session}] Запрещаю добавлять в чаты...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyChatInvite(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        logger(f"  [ACCOUNT] [{session}] Скрываю номер...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneNumber(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        logger(f"  [ACCOUNT] [{session}] Создаю папки...", "silly")
        try:
            await client(functions.messages.UpdateDialogFilterRequest(
                id=10,
                filter=types.DialogFilter(
                    id=10,
                    title="Люди",
                    pinned_peers=[],
                    include_peers=[],
                    exclude_peers=[],
                    contacts=True,
                    non_contacts=True
                )
            ))
        except Exception as e:
            pass

        try:
            await client(functions.messages.UpdateDialogFilterRequest(
                id=20,
                filter=types.DialogFilter(
                    id=20,
                    title="Группы",
                    pinned_peers=[],
                    include_peers=[],
                    exclude_peers=[],
                    groups=True
                )
            ))
        except Exception as e:
            pass

        try:
            await client(functions.messages.UpdateDialogFilterRequest(
                id=30,
                filter=types.DialogFilter(
                    id=30,
                    title="Каналы",
                    pinned_peers=[],
                    include_peers=[],
                    exclude_peers=[],
                    broadcasts=True
                )
            ))
        except Exception as e:
            pass

    except Exception as e:
        print(" ")
        print(" ")
        logger(f"[ACCOUNT] [{session}] [ERROR] {repr(e)}", "error")
        print(" ")

    input("Чтобы выйти нажмите Enter...")



####################################
#
#   Заполнение чатами
#
####################################



async def chater(client, session):
    clear()
    logger(f"   [CHAT] Запускаюсь...", "silly")

    print(" ")
    print(" ")
    print(' 1 - Вступление в чаты')
    print(' 2 - Предварительная чистка чатов')
    print(' 3 - Создание папки со всеми чатами')
    print(' 4 - Расширенное вступление в чаты')
    print("   - - - - - -")
    mode = input("   Выберите режим работы: ")

    if mode == '1':
        await AutoJoin(client, session)
    if mode == '2':
        await ChatCleaner(client, False, session)
    if mode == '3':
        await FolderCreator(client, session)
    if mode == '4':
        await AutoCleaner(client, session)
    
    input("Чтобы выйти нажмите Enter...")

async def AutoJoin(client, session):
    clear()
    while True:
        try:
            input("Убедитель в наличии файла groups.txt")
            group_list = 'groups.txt'
            join_interval = int(input("Интервал между вступлениями в чаты: "))
            break
        except Exception as e:
            print(" ")
            logger(f"   [CHAT] [ERROR] {repr(e)}", "error")
            print(" ")

    with open(group_list, 'r') as file:
            groups = file.read().splitlines()

    for group in groups:
        try:
            await client(JoinChannelRequest(group))
            logger(f"  [CHAT] [{session}] Вступил в группу: {group}...", "silly")
            await asyncio.sleep(join_interval)

        except Exception as e:
            error_message = str(e)
            match = re.search(r"A wait of (\d+) seconds is required", error_message)

            if match:
                wait_seconds = int(match.group(1))
                logger(f"  [CHAT] [{session}] Требуется ожидание в течение {wait_seconds} секунд...", "warn")
                await asyncio.sleep(wait_seconds)
            else:
                logger(f"  [CHAT] [{session}] Ошибка при вступлении в группу: {group}, пропускаем...", "error")
                continue

async def ChatCleaner(client, auto, session):
        clear()
        dialogs = await client.get_dialogs()
        count = 1
        if not auto:
            count = int(input("Минимальное количество непрочитанных сообщений: "))


        for dialog in dialogs:
            try:
                if dialog.is_group or dialog.is_channel:
                    chat = await client(GetPeerDialogsRequest(
                        peers=[dialog]
                    ))

                    unread = chat.dialogs[0].unread_count

                    await asyncio.sleep(0.5)
                    if unread < count:
                        await client(functions.channels.LeaveChannelRequest(
                            channel=dialog.id
                        ))
                        logger(f"  [CHAT] [{session}] Покидаем чат {dialog.title}. Неактив...", "warn")
                        continue
                    logger(f"  [CHAT] [{session}] Чат {dialog.title} прошел. Далее...", "silly")
            except Exception as e:
                 error_message = str(e)
                 match = re.search(r"A wait of (\d+) seconds is required", error_message)
                 if match:
                    wait_seconds = 10
                    logger(f"  [CHAT] [{session}] Требуется ожидание в течение {wait_seconds} секунд...", "warn")
                    await asyncio.sleep(wait_seconds)

async def FolderCreator(client, session):
    clear()
    try:
        dialogs = await client.get_dialogs()
        chat_filter=[]
        input("Количество чатов на аккаунте не должно превышать 100")
        name = (input("Название папки для чатов: "))

        logger(f"  [CHAT] [{session}] Собираю информацию о чатах...", "silly")
        for dialog in dialogs:
                try:
                    if dialog.is_group or dialog.is_channel:
                        chat = await client(GetPeerDialogsRequest(
                            peers=[dialog]
                        ))

                        chat_id=chat.dialogs[0].peer.channel_id
                        chat_acces=chat.chats[0].access_hash
                        chat_filter.append(types.InputPeerChannel(channel_id=chat_id, access_hash=-chat_acces))

                except Exception as e:
                    error_message = str(e)
                    match = re.search(r"A wait of (\d+) seconds is required", error_message)
                    if match:
                        wait_seconds = 10
                        print(f"Требуется ожидание в течение {wait_seconds} секунд")
                        await asyncio.sleep(wait_seconds)

        logger(f"  [CHAT] [{session}] Создаю папку {name}...", "silly")
        await client(functions.messages.UpdateDialogFilterRequest(
            id=42,
            filter=types.DialogFilter(
                id=42,
                title=name,
                pinned_peers=[],
                include_peers=chat_filter,
                exclude_peers=[]
            )
        ))
        logger(f"  [CHAT] [{session}] Создал папку {name}...", "silly")

    except Exception as e:
        print(" ")
        logger(f"   [CHAT] [ERROR] {repr(e)}", "error")
        print(" ")

async def AutoCleaner(client, session):
    clear()
    while True:
        try:
            input("Убедитель в наличии файла groups.txt")
            group_list = 'groups.txt'
            count = int(input("Необходимое количество чатов (до 100): "))
            groups_counter = 0
            join_interval = int(input("Интервал между вступлениями в чаты: "))

            break
        except Exception as e:
            print(" ")
            logger(f"   [CHAT] [ERROR] {repr(e)}", "error")
            print(" ")

    with open(group_list, 'r') as file:
            groups = file.read().splitlines()

    for group in groups:
        groups_counter+=1
        try:
            await client(JoinChannelRequest(group))
            logger(f"  [CHAT] [{session}] Вступил в группу: {group}...", "silly")
            await asyncio.sleep(join_interval)

        except Exception as e:
            error_message = str(e)
            match = re.search(r"A wait of (\d+) seconds is required", error_message)

            if match:
                wait_seconds = int(match.group(1))
                logger(f"  [CHAT] [{session}] Требуется ожидание в течение {wait_seconds} секунд...", "warn")
                await asyncio.sleep(wait_seconds)
                logger(f"  [CHAT] [{session}] Начинаю чистку чатов...", "silly")
                await ChatCleaner(client, True, session)
                dialogs = await client.get_dialogs()
                print('')
                logger(f"  [CHAT] [{session}] Количество чатов на аккаунта: {len(dialogs)}", "silly")

                new_groups = groups[groups_counter:len(groups)]
                with open('groups.txt', 'w') as file:
                    for group in new_groups:
                        file.write(str(group) + '\n')
                if len(dialogs) > count:
                    break
            else:
                logger(f"  [CHAT] [{session}] Ошибка при вступлении в группу: {group}, пропускаем...", "error")
                continue



####################################
#
#   Спам
#
####################################



async def spamer(client, session):
    clear()
    logger(f"   [SPAM] Запускаюсь...", "silly")
    while True:
        try:
            min_await = int(input("  Минимальная задержка между сообщениями: "))
            max_await = int(input("  Максимальная задержка между сообщениями: "))

            min_loop = int(input("  Минимальная задержка между циклами: "))
            max_loop = int(input("  Максимальная задержка между циклами: "))

            spam_limit = int(input("  Минимальное количество сообщений перед отправкой: "))

            break
        except Exception as e:
            print(" ")
            logger(f"   [SPAM] [ERROR]: {repr(e)}", "error")
            print(" ")

    sended = 0
    while True:
        clear()
        try:
            dialogs = await client.get_dialogs()
            groups = []
            for dialog in dialogs:
                if dialog.is_group:
                    groups.append(dialog)
            me = await client.get_me()

            loop_sended = 0
            loop_no_active = 0
            loop_no_send_time = 0
            loop_no_send_ban = 0
            
            for group in groups:
                try:
                    clear()
                    group_entity = group.entity
                    group_id = group.id
                    group_title = group.title
                    group_username = group.entity.username
                    group_permissions = await client.get_permissions(group_id)

                    getStat(session, sended, loop_sended, loop_no_active, loop_no_send_time, loop_no_send_ban)

                    if group_permissions.send_messages:
                        logger(f"   [SPAM] [GROUP] В чате {group_title} участникам запрещено писать, выхожу...", "error")
                        await client(functions.channels.LeaveChannelRequest(
                            channel=group_id
                        ))

                    message = await setMessage(client, me)
                    send_status = await sendMessage(client, session, group_entity, group_id, group_title, group_username, message, me, spam_limit)

                    if send_status == "sended":
                        loop_sended += 1
                        sended += 1
                    if send_status == "no_active":
                        loop_no_active += 1
                    if send_status == "no_send_time":
                        loop_no_send_time += 1
                    if send_status == "no_send_ban":
                        loop_no_send_ban += 1
                    
                    await_send = (random.randint(min_await, max_await))
                    await asyncio.sleep(await_send)
                except Exception as e:
                    print(" ")
                    logger(f"   [GROUP] [ERROR] Неизвестная ошибка при работе с чатом {group_title}: {repr(e)}", "error")
                    print(" ")

        except Exception as e:
            print(" ")
            logger(f"   [SPAM] [ERROR] {repr(e)}", "error")
            print(" ")
        
        await_loop = (random.randint(min_loop, max_loop))
        logger(f"   [SPAM] [{session}] Закончил круг, жду {await_loop}...", "silly")
        await asyncio.sleep(await_loop)



####################################
#
#   Вспомогательное
#
####################################



def logger(text, type):

    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)
    formatted_time = moscow_time.strftime('%d.%m-%H:%M')

    text = "[" + formatted_time + "]" + " " + text

    if type == "error":
        print(Fore.RED + text + Style.RESET_ALL)
    if type == "warn":
        print(Fore.YELLOW + text + Style.RESET_ALL)
    if type == "silly":
        print(Fore.GREEN + text + Style.RESET_ALL)

    with open('./logs.txt', 'a', encoding='utf-8') as f:
        f.write(text + '\n')


def getSetting(path, named):
    with open(f"{path}.config", 'r', encoding='utf-8') as file:
        CONFIG = list(filter(None, file.read().split('\n')))
        file.close()

    for item in CONFIG:
        if named in item:
            return item.split(" = ")[1]


def getStat(session, sended, loop_sended, loop_no_active, loop_no_send_time, loop_no_send_ban):

    print(" ")
    logger(f"   [STAT] [{session}] Успешных отправок за запуск: {sended}", "silly")
    logger(f"   [STAT] [{session}] Успешных отправок за круг: {loop_sended}", "silly")
    logger(f"   [STAT] [{session}] Неудачно отправлено за круг - нету активности: {loop_no_active}", "warn")
    logger(f"   [STAT] [{session}] Неудачно отправлено за круг - временное ограничение: {loop_no_send_time}", "warn")
    logger(f"   [STAT] [{session}] Неудачно отправлено за круг - бан: {loop_no_send_ban}", "error")
    print(" ")


async def setMessage(client, me):
    while True:
        try:
            text = await client.get_messages("me", limit=1)
            text = text[0].message
            if text:
                break
            else:
                print(" ")
                logger(f"   [SAVED] [ERROR] Нет сообщения в Избранном. Ожидаю 30...", "error")
                print(" ")
                await asyncio.sleep(30)
        except Exception as e:
            print(" ")
            logger(f"   [SAVED] [ERROR] Нет сообщения в Избранном. Ожидаю 30...", "error")
            print(" ")
            await asyncio.sleep(30)

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


async def sendMessage(client, session, group_entity, group_id, group_title, group_username, message, me, spam_limit):
    try:
        last_messages = await client.get_messages(group_entity, limit=spam_limit)
        for item in last_messages:
            if item.sender.id == me.id:
                logger(f"   [SEND] [{session}] Мало актива в {group_title}. Пропускаю...", "warn")
                return "no_active"
            
        await client.send_message(group_id, message)
        logger(f"   [SEND] [{session}] Отправил успешно в {group_title}", "silly")
        
        return "sended"
        
    except Exception as e:
        error_message = str(e)
        if "wait" in error_message.lower():
            print(" ")
            logger(f"   [SEND] [ERROR] Ошибка отправки в {group_title} - Таймер", "warn")
            print(" ")

            return "no_send_time"
        
        if "you can't write in this chat" in error_message.lower():
            print(" ")
            logger(f"   [SEND] [ERROR] Ошибка отправки в {group_title} - Нету прав писать в чат, покидаю его...", "error")
            print(" ")
            await client(functions.channels.LeaveChannelRequest(
                channel=group_id
            ))

            with open(f"cant_send.txt", 'a', encoding='utf-8') as file:
                file.write(group_username)
                file.write("\n")

            return "no_send_ban"
        
        if "topic_closed" in error_message.lower():
            print(" ")
            logger(f"   [SEND] [ERROR] Ошибка отправки в {group_title} - Тема закрыта, покидаю его...", "error")
            print(" ")
            await client(functions.channels.LeaveChannelRequest(
                channel=group_id
            ))

            with open(f"topic_closed.txt", 'a', encoding='utf-8') as file:
                file.write(group_username)
                file.write("\n")

            return "spam"
        
        if "you're banned from sending messages" in error_message.lower():
            print(" ")
            logger(f"   [SEND] [ERROR] Ошибка отправки в {group_title} - Спам.", "error")
            print(" ")

            return "no_send_ban"

        if "CHAT_SEND_PLAIN_FORBIDDEN" in str(repr(e)):
            print(" ")
            logger(f"   [SEND] [ERROR] Ошибка отправки в {group_title} - В чате запрещено отправлять текст, покидаю его...", "error")
            print(" ")
            await client(functions.channels.LeaveChannelRequest(
                channel=group_id
            ))

            return "no_send_ban"
            
        print(" ")
        logger(f"   [SEND] [ERROR] Неизвестная ошибка отправки в {group_title}: {repr(e)}", "error")
        print(" ")

        return "no_send_ban"



####################################
#
#   Запуск
#
####################################



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(main())
