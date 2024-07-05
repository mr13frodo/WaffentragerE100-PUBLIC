import os
import asyncio
import utils
import re
from telethon.tl import functions, types
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


async def chater(client, session):
    clear()
    utils.logger(f"[CHAT] Запускаюсь...", "silly")

    print("")
    print("")
    print('1 - Вступление в чаты')
    print('2 - Предварительная чистка чатов')
    print('3 - Создание папки со всеми чатами')
    print('4 - Расширенное вступление в чаты')
    print("- - - - - -")
    mode = input("Выберите режим работы: ")

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
            utils.logger(f"[CHAT] [ERROR] {repr(e)}", "error")

    with open(group_list, 'r') as file:
            groups = file.read().splitlines()

    for group in groups:
        status = await join(client, session, group)
        if status:
            await asyncio.sleep(join_interval)


async def ChatCleaner(client, auto, session):
        clear()
        dialogs = await client.get_dialogs()
        count = 2
        if not auto:
            count = int(input("Минимальное количество непрочитанных сообщений: "))


        for dialog in dialogs:
            try:
                if dialog.is_group or dialog.is_channel:
                    chat = await client(functions.messages.GetPeerDialogsRequest(
                        peers=[dialog]
                    ))

                    unread = chat.dialogs[0].unread_count

                    await asyncio.sleep(0.5)
                    if unread < count:
                        await client(functions.channels.LeaveChannelRequest(
                            channel=dialog.id
                        ))
                        utils.logger(f"[CHAT] [{session}] Покидаю чат {dialog.title}. Неактив...", "warn")
                        continue
                    utils.logger(f"[CHAT] [{session}] Чат {dialog.title} прошел. Далее...", "silly")
            except Exception as e:
                utils.logger(f"[CHAT] [ERROR] {repr(e)}", "error")

async def FolderCreator(client, session):
    clear()
    try:
        utils.logger(f"[CHAT] [{session}] Собираю информацию о чатах...", "silly")
        dialogs = await client.get_dialogs()
        groupsss = []
        num = int(input(" По сколько чатов в одной папке (до 100): "))
        for item in dialogs:
            if item.is_group or item.is_channel:
                groupsss.append(item)
        groupss = [groupsss[i:i + num] for i in range(0, len(groupsss), num)]
        del dialogs
        del groupsss
        name = input(" Название папки: ")
        count = 1

        for groups in groupss:
            chat_filter = []
            for group in groups:
                try:
                    chat = await client(functions.messages.GetPeerDialogsRequest(
                        peers = [group]
                    ))

                    chat_id = chat.dialogs[0].peer.channel_id
                    chat_acces = chat.chats[0].access_hash
                    chat_filter.append(types.InputPeerChannel(channel_id = chat_id, access_hash = -chat_acces))

                except Exception as e:
                    utils.logger(f"[CHAT] [ERROR] {repr(e)}", "error")

            utils.logger(f"[CHAT] [{session}] Создаю папку {name} {count}...", "silly")

            await client(functions.messages.UpdateDialogFilterRequest(
                id = 20 + count,
                filter=types.DialogFilter(
                    id = 10 + count,
                    title = f"{name} {count}",
                    pinned_peers = [],
                    include_peers = chat_filter,
                    exclude_peers = []
                )
            ))

            utils.logger(f"[CHAT] [{session}] Создал папку {name} {count}...", "silly")
            count += 1

    except Exception as e:
        utils.logger(f"[CHAT] [ERROR] {repr(e)}", "error")

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
            utils.logger(f"[CHAT] [ERROR] {repr(e)}", "error")

    with open(group_list, 'r') as file:
            groups = file.read().splitlines()

    for group in groups:
        groups_counter+=1
        status = await join(client, session, group)
        if status:
            await asyncio.sleep(join_interval)

        if groups_counter == 30:
            utils.logger(f"[CHAT] [{session}] Начинаю чистку чатов...", "silly")
            await ChatCleaner(client, True, session)
            dialogs = await client.get_dialogs()
            print("")
            utils.logger(f"[CHAT] [{session}] Количество чатов на аккаунта: {len(dialogs)}", "silly")

            new_groups = groups[groups_counter:len(groups)]
            with open('groups.txt', 'w') as file:
                for group in new_groups:
                    file.write(str(group) + '\n')
            if len(dialogs) > count:
                break

            groups_counter = 0


async def join(client, session, group):
        join_status = await utils.joinRequest(client, group)

        match join_status:
            case "joined":
                utils.logger(f"[CHAT] [{session}] Вступил в группу {group}...", "silly")
            case "join_request":
                utils.logger(f"[CHAT] [{session}] Отправил заявку в группу {group}...", "silly")
            case _:
                flood_timer = re.search(r"A wait of (\d+) seconds is required", join_status)
                if flood_timer:
                    wait_seconds = int(flood_timer.group(1))
                    utils.logger(f"[CHAT] [{session}] Требуется ожидание в течение {wait_seconds} секунд...", "warn")
                    await asyncio.sleep(wait_seconds + 5)
                    return False
                else:
                    utils.logger(f"[CHAT] [{session}] Ошибка при вступлении в группу {group}: {join_status}", "error")
                    return False
        return True