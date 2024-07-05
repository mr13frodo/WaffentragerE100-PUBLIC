import os
import utils
from telethon.tl import functions, types
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


async def cleaner(client, session):
    clear()
    utils.logger(f"[CLEAN] Запускаюсь...", "silly")

    print("")
    print("")
    print('1 - Диалоги')
    print('2 - Группы')
    print('3 - Каналы')
    print('4 - Боты')
    print("- - - - - -")
    mode = input("Выберите режим работы: ")

    if mode == '1':
        await Dialog(client, session)
    if mode == '2':
        await Group(client, session)
    if mode == '3':
        await Channel(client, session)
    if mode == '4':
        await Bot(client, session)
    
    input("Чтобы выйти нажмите Enter...")

async def Dialog(client, session):
    clear()
    me = await client.get_me()
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        try:
            if dialog.is_user:
                chat = await client(functions.messages.GetPeerDialogsRequest(
                    peers=[dialog]
                ))
                if not chat.users[0].bot:
                    if chat.users[0].id == 777000 or chat.users[0].id == 178220800 or chat.users[0].id == me.id:
                        continue
                    else:
                        await client.delete_dialog(dialog, revoke = True)

        except Exception as e:
            utils.logger(f"[CLEAN] [ERROR]: {repr(e)}", "error")
    utils.logger(f"[CLEAN] [{session}] Работа окончена...", "silly")

async def Group(client, session):
    clear()
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        try:
            if dialog.is_group:
                    await client(functions.channels.LeaveChannelRequest(
                        channel=dialog.id
                    ))
        except Exception as e:
            utils.logger(f"[CLEAN] [ERROR]: {repr(e)}", "error")
    utils.logger(f"[CLEAN] [{session}] Работа окончена...", "silly")

async def Channel(client, session):
    clear()
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        try:
            if dialog.is_channel:
                    await client(functions.channels.LeaveChannelRequest(
                        channel=dialog.id
                    ))
        except Exception as e:
            utils.logger(f"[CLEAN] [ERROR]: {repr(e)}", "error")
    utils.logger(f"[CLEAN] [{session}] Работа окончена...", "silly")

async def Bot(client, session):
    clear()
    me = await client.get_me()
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        try:
            if dialog.is_user:
                chat = await client(functions.messages.GetPeerDialogsRequest(
                    peers=[dialog]
                ))
                if chat.users[0].bot:
                    if chat.users[0].id == 777000 or chat.users[0].id == 178220800 or chat.users[0].id == me.id:
                        continue
                    else:
                        await client.delete_dialog(dialog, revoke = True)

        except Exception as e:
            utils.logger(f"[CLEAN] [ERROR]: {repr(e)}", "error")
    utils.logger(f"[CLEAN] [{session}] Работа окончена...", "silly")