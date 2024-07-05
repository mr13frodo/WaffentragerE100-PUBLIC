import os
import re
import random
import asyncio
import utils
from telethon.tl import functions, types
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


async def spamer(client, params):
    clear()
    utils.logger(f"[SPAM] Запускаюсь...", "silly")
    params["me"] = await client.get_me()

    while True:
        try:
            writed = utils.getSetting(params["session"], "MIN_AWAIT")
            if writed:
                utils.logger(f"[SPAM] Минимальная задержка между сообщениями {writed}", "warn")
                check = input("Введите свое значение или Enter чтоб продолжить: ")
                if check:
                    params["min_await"] = int(check)
                else:
                    params["min_await"] = int(writed)
                del check
            else:
                params["min_await"] = int(input("Минимальная задержка между сообщениями: "))
                utils.setSetting(params["session"], "MIN_AWAIT", params["min_await"])
            del writed

            writed = utils.getSetting(params["session"], "MAX_AWAIT")
            if writed:
                utils.logger(f"[SPAM] Максимальная задержка между сообщениями {writed}", "warn")
                check = input("Введите свое значение или Enter чтоб продолжить: ")
                if check:
                    params["max_await"] = int(check)
                else:
                    params["max_await"] = int(writed)
                del check
            else:
                params["max_await"] = int(input("Максимальная задержка между сообщениями: "))
                utils.setSetting(params["session"], "MAX_AWAIT", params["max_await"])
            del writed

            writed = utils.getSetting(params["session"], "MIN_LOOP")
            if writed:
                utils.logger(f"[SPAM] Минимальная задержка между циклами {writed}", "warn")
                check = input("Введите свое значение или Enter чтоб продолжить: ")
                if check:
                    params["min_loop"] = int(check)
                else:
                    params["min_loop"] = int(writed)
                del check
            else:
                params["min_loop"] = int(input("Минимальная задержка между циклами: "))
                utils.setSetting(params["session"], "MIN_LOOP", params["min_loop"])
            del writed

            writed = utils.getSetting(params["session"], "MAX_LOOP")
            if writed:
                utils.logger(f"[SPAM] Максимальная задержка между циклами {writed}", "warn")
                check = input("Введите свое значение или Enter чтоб продолжить: ")
                if check:
                    params["max_loop"] = int(check)
                else:
                    params["max_loop"] = int(writed)
                del check
            else:
                params["max_loop"] = int(input("Максимальная задержка между циклами: "))
                utils.setSetting(params["session"], "MAX_LOOP", params["max_loop"])
            del writed

            writed = utils.getSetting(params["session"], "SPAM_LIMIT")
            if writed:
                utils.logger(f"[SPAM] Минимальное количество сообщений перед отправкой {writed}", "warn")
                check = input("Введите свое значение или Enter чтоб продолжить: ")
                if check:
                    params["spam_limit"] = int(check)
                else:
                    params["spam_limit"] = int(writed)
                del check
            else:
                params["spam_limit"] = int(input("Минимальное количество сообщений перед отправкой: "))
                utils.setSetting(params["session"], "SPAM_LIMIT", params["spam_limit"])
            del writed
            
            writed = utils.getSetting(params["session"], "TAGER")
            if writed:
                utils.logger(f"[SPAM] Количество тегуемых участников {writed}", "warn")
                check = input("Введите свое значение или Enter чтоб продолжить: ")
                if check:
                    params["tager"] = int(check)
                else:
                    params["tager"] = int(writed)
                del check
            else:
                params["tager"] = int(input("Количество тегуемых участников: "))
                utils.setSetting(params["session"], "TAGER", params["tager"])
            del writed

            break
        except Exception as e:
            utils.logger(f"[SPAM] [ERROR]: {repr(e)}", "error")

    params["sended"] = 0
    while True:
        await spam_loop(client, params)
        
        await_loop = (random.randint(params["min_loop"], params["max_loop"]))
        utils.logger(f"[SPAM] [{params['session']}] Закончил круг, жду {await_loop}...", "silly")
        await asyncio.sleep(await_loop)

        del await_loop
    

async def spam_loop(client, params):
    clear()
    try:
        utils.logger(f"[INFO] Собираю чаты...", "info")
        dialogs = await client.get_dialogs()
        groups = []
        for dialog in dialogs:
            if dialog.is_group:
                groups.append(dialog)

        stats = {
            "loop_sended": 0,
            "loop_no_active": 0,
            "loop_no_send_time": 0,
            "loop_no_send_ban": 0,
            "loop_no_send_error": 0,
            "loop_no_send_spam": 0
        }
        
        for group in groups:
            try:
                if group.entity.deactivated:
                    continue
            except Exception as e:
                    pass
            await spam_item(client, group, params, stats)

        del groups
        del dialogs
        del stats

    except Exception as e:
        utils.logger(f"[SPAM] [ERROR] {repr(e)}", "error")


async def spam_item(client, group, params, stats):
    try:
        clear()
        group_entity = group.entity
        group_id = group.id
        group_title = group.title
        group_username = group.entity.username
        group_permissions = await client.get_permissions(group_id)

        print("")
        utils.logger(f"[STAT] [{params['session']}] Успешных отправок за запуск: {params['sended']}", "silly")
        utils.logger(f"[STAT] [{params['session']}] Успешных отправок за круг: {stats['loop_sended']}", "silly")
        utils.logger(f"[STAT] [{params['session']}] Неудачно отправлено за круг - нету активности: {stats['loop_no_active']}", "warn")
        utils.logger(f"[STAT] [{params['session']}] Неудачно отправлено за круг - временное ограничение: {stats['loop_no_send_time']}", "warn")
        utils.logger(f"[STAT] [{params['session']}] Неудачно отправлено за круг - бан: {stats['loop_no_send_ban']}", "stat-error")
        utils.logger(f"[STAT] [{params['session']}] Неудачно отправлено за круг - ошибка: {stats['loop_no_send_error']}", "stat-error")
        utils.logger(f"[STAT] [{params['session']}] Неудачно отправлено за круг - спам: {stats['loop_no_send_spam']}", "stat-error")
        print("")

        utils.logger(f"[INFO] Проверяю чат {group_title}...", "info")
        if group_permissions.send_messages:
            utils.logger(f"[SPAM] В чате {group_title} участникам запрещено писать, выхожу...", "error")
            await client(functions.channels.LeaveChannelRequest(
                channel = group_id
            ))
            return 0
        last_messages = await client.get_messages(group_entity, limit = params["spam_limit"])
        for item in last_messages:
            try:
                if item.sender.id == params["me"].id:
                    utils.logger(f"[SPAM] [{params['session']}] Мало актива в {group_title}. Пропускаю...", "warn")
                    stats["loop_no_active"] += 1
                    return 0
            except Exception as e:
                pass

        utils.logger(f"[INFO] Считываю Избранное...", "info")
        text = await utils.getSaved(client)
        utils.logger(f"[INFO] Рандомизирую текст...", "info")
        message = utils.randomText(text)
        send_status = await utils.sendMessage(client, group_entity, group_id, message, params)

        match send_status:
            case "sended":
                utils.logger(f"[SEND] [{params['session']}] Отправил успешно в {group_title}", "silly")
                params["sended"] += 1
                stats["loop_sended"] += 1
            case "no_send_time":
                utils.logger(f"[SEND] [ERROR] Ошибка отправки в {group_title} - Таймер", "warn")
                stats["loop_no_send_time"] += 1
            case "no_send_ban":
                utils.logger(f"[SEND] [ERROR] Ошибка отправки в {group_title} - Нету прав писать в чат, покидаю его...", "error")
                stats["loop_no_send_ban"] += 1
                await client(functions.channels.LeaveChannelRequest(
                    channel=group_id
                ))
                with open(f"cant_send.txt", 'a', encoding='utf-8') as file:
                    file.write(group_username)
                    file.write("\n")
            case "topic_closed":
                utils.logger(f"[SEND] [ERROR] Ошибка отправки в {group_title} - Тема закрыта, покидаю его...", "error")
                stats["loop_no_send_error"] += 1
                await client(functions.channels.LeaveChannelRequest(
                    channel=group_id
                ))
                with open(f"topic_closed.txt", 'a', encoding='utf-8') as file:
                    file.write(group_username)
                    file.write("\n")
            case "forbidden":
                utils.logger(f"[SEND] [ERROR] Ошибка отправки в {group_title} - В чате запрещено отправлять текст, покидаю его...", "error")
                stats["loop_no_send_error"] += 1
                await client(functions.channels.LeaveChannelRequest(
                    channel=group_id
                ))
            case "spam":
                utils.logger(f"[SEND] [ERROR] Ошибка отправки в {group_title} - Спам.", "error")
                stats["loop_no_send_spam"] += 1
                await client.send_message("@SpamBot", "/start")
                await asyncio.sleep((random.randint(2, 5)))
                await client.send_message("@SpamBot", "/start")
            case _:
                flood_timer = re.search(r"A wait of (\d+) seconds is required", send_status)
                if flood_timer:
                    wait_seconds = int(flood_timer.group(1))
                    utils.logger(f"[SEND] [ERROR] Требуется ожидание в течение {wait_seconds} секунд...", "warn")
                    await asyncio.sleep(wait_seconds + 5)
                    return False
                else:
                    utils.logger(f"[SEND] [ERROR] Неизвестная ошибка отправки в {group_title}: {send_status}", "error")
                    stats["loop_no_send_error"] += 1

        await_send = (random.randint(params["min_await"], params["max_await"]))
        utils.logger(f"[INFO] Ожидаю {await_send}...", "info")
        await asyncio.sleep(await_send)

        del message
        del send_status
        del group_entity
        del group_id
        del group_permissions
        del group_title
        del group_username
        del await_send

    except Exception as e:
        utils.logger(f"[SPAM] [ERROR] Неизвестная ошибка при работе с чатом {group_title}: {repr(e)}", "error")