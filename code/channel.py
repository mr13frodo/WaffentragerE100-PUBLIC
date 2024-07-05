import os
import re
import asyncio
import utils
import random
from telethon.tl import functions, types
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


async def channel(client, session):
    clear()
    utils.logger(f"[CHANNEL] Запускаюсь...", "silly")

    print("")
    print("")
    print('1 - Комментирование новых постов')
    print('2 - Комментирование старых постов')
    print("- - - - - -")
    mode = input("Выберите режим работы: ")

    if mode == '1':
        await new_post(client, session)
    if mode == '2':
        await old_post(client, session)

    input("Нажмите Enter для выхода...")

async def new_post(client, session):
    clear()
    while True:
        try:
            saved = await utils.getSaved(client)

            dialogs = await client.get_dialogs()
            channels = []
            for dialog in dialogs:
                if dialog.is_channel:
                    channels.append(dialog)

            for channel in channels:
                channel_entity = channel.entity
                channel_id = channel.id
                channel_title = channel.title
                channel_username = channel_entity.username

                count = channel.unread_count
                counter_try = 0
                counter_send = 0
                        
                if count > 0:
                    utils.logger(f"[CHANNEL] [{session}] обнаружил новый пост в {channel_title}", "silly")
                    while True:
                        post = await client.get_messages(channel_entity, limit = 1, add_offset = counter_try)
                        await client.send_read_acknowledge(channel_entity, post)
                        post_id = post[0].id
                        message = utils.randomText(saved)
                        status = await utils.sendComment(client, channel_entity, channel_id, message, post_id)

                        match status:
                            case "sended":
                                utils.logger(f"[CHANNEL] [{session}] Отправил комментарий в {channel_title}", "silly")
                                counter_send += 1
                            case "banned":
                                utils.logger(f"[CHANNEL] [ERROR] Заблокирована отправка сообщений в {channel_title}, покидаю его...", "error")
                                await client(functions.channels.LeaveChannelRequest(
                                    channel=channel_id
                                ))
                                break
                            case "no_comments":
                                pass
                            case _:
                                utils.logger(f"[ERROR] [CHANNEL] [{session}] Неизвестная ошибка при работе с каналом {channel_title}: {status}", "silly")
                                counter_send += 1

                        if counter_send == count:
                            break
                        
                        counter_try += 1
            
            await asyncio.sleep(5)

        except Exception as e:
            utils.logger(f"[CHANNEL] [ERROR] {repr(e)}", "error")

async def old_post(client, session):
    clear()

    while True:
        try:
            min_await = int(input("Минимальная задержка между комментариями: "))
            max_await = int(input("Максимальная задержка между комментариями: "))

            min_channel = int(input("Минимальная задержка между каналами: "))
            max_channel = int(input("Максимальная задержка между каналами: "))

            min_loop = int(input("Минимальная задержка между кругами: "))
            max_loop = int(input("Максимальная задержка между кругами: "))

            spam_limit = int(input("Сколько последних постов комментировать: "))

            break
        except Exception as e:
            utils.logger(f"[SPAM] [ERROR]: {repr(e)}", "error")

    try:
        while True:
            saved = await utils.getSaved(client)
            dialogs = await client.get_dialogs()
            channels = []
            for dialog in dialogs:
                if dialog.is_channel:
                    channels.append(dialog)

            for channel in channels:
                try:
                    clear()
                    channel_entity = channel.entity
                    channel_id = channel.id
                    channel_title = channel.title
                    channel_username = channel_entity.username
                    utils.logger(f"[CHANNEL] [{session}] Начинаю работу с {channel_title}...", "silly")
                    print("")

                    counter_try = 0
                    counter_send = 0
                    counter_false = 0
                    while True:
                        post = await client.get_messages(channel_entity, limit = 1, add_offset = counter_try)
                        await client.send_read_acknowledge(channel_entity, post)
                        post_id = post[0].id
                        message = utils.randomText(saved)
                        status = await utils.sendComment(client, channel_id, message, post_id)

                        match status:
                            case "sended":
                                utils.logger(f"[CHANNEL] [{session}] Отправил комментарий в {channel_title}", "silly")
                                counter_send += 1
                            case "banned":
                                utils.logger(f"[CHANNEL] [ERROR] Заблокирована отправка сообщений в {channel_title}, покидаю его...", "error")
                                await client(functions.channels.LeaveChannelRequest(
                                    channel=channel_id
                                ))
                                break
                            case "no_comments":
                                counter_false += 1
                            case _:
                                if "A wait of" in status:
                                    writed = re.search(r"A wait of (\d+) seconds is required", status)
                                    wait_seconds = int(writed.group(1))
                                    utils.logger(f"[ERROR] [CHANNEL] [{session}] Требуется ожидание в течение {wait_seconds} секунд...", "warn")
                                    await asyncio.sleep(wait_seconds)
                                else:
                                    utils.logger(f"[ERROR] [CHANNEL] [{session}] Неизвестная ошибка при работе с каналом {channel_title}: {status}", "error")
                                    counter_send += 1
                                    break

                        if counter_false == 30:
                            utils.logger(f"[CHANNEL] [ERROR] В канале {channel_title} недоступны комментарии, покидаю его...", "error")
                            await client(functions.channels.LeaveChannelRequest(
                                channel=channel_id
                            ))
                            break

                        if counter_send == spam_limit:
                            break
                        
                        counter_try += 1
                        if status == "sended":
                            await_send = (random.randint(min_await, max_await))
                            await asyncio.sleep(await_send)

                    await_channel = (random.randint(min_channel, max_channel))
                    print("")
                    utils.logger(f"[CHANNEL] [{session}] Закончил работу с каналом, жду {await_channel}...", "silly")
                    await asyncio.sleep(await_channel)

                except Exception as e:
                    utils.logger(f"[CHANNEL] [ERROR] Неизвестная ошибка при работе с каналом {channel_title}: {repr(e)}", "error")

            await_loop = (random.randint(min_loop, max_loop))
            print("")
            utils.logger(f"[CHANNEL] [{session}] Круг окончен, жду {await_loop}", "silly")
            await asyncio.sleep(await_loop)

    except Exception as e:
        utils.logger(f"[CHANNEL] [ERROR] {repr(e)}", "error")