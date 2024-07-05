import os
import asyncio
import utils
import json
from accounter import accounter
from channel import channel
from chater import chater
from cleaner import cleaner
from spamer import spamer
from pars_people import pars_people
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



os.system("python.exe -m pip install --upgrade pip")

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
    from colorama import init
    os.system("pip install --upgrade colorama")
except ImportError:
    os.system("pip install colorama")
    from colorama import init

try:
    from telethon import errors
    from telethon import TelegramClient
    os.system("pip install --upgrade telethon")
except ImportError:
    os.system("pip install telethon")
    from telethon import errors
    from telethon import TelegramClient

clear()

async def main():
    init()
    params = {}
    utils.logger(f"[MAIN] Запускаюсь...", "silly")


    writed = [file for file in os.listdir() if file.endswith('.config')]
    params["session"] = None
    params["api_id"] = None
    params["api_hash"] = None
    params["device_model"] = None
    params["app_version"] = None
    params["system_lang_code"] = None
    if not writed:
        writed = [file for file in os.listdir() if file.endswith('.json')]
        if writed:
            writed = writed[0]
            params["session"] = writed[:-5]
            with open(writed, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            if "api_id" in json_data:
                utils.setSetting(params["session"], "API_ID", json_data["api_id"])
            elif "app_id" in json_data:
                utils.setSetting(params["session"], "API_ID", json_data["app_id"])

            if "api_hash" in json_data:
                utils.setSetting(params["session"], "API_HASH", json_data["api_hash"])
            elif "app_hash" in json_data:
                utils.setSetting(params["session"], "API_HASH", json_data["app_hash"])
            
            if "device_model" in json_data:
                utils.setSetting(params["session"], "DEVICE_MODEL", json_data["device_model"])
            elif "device" in json_data:
                utils.setSetting(params["session"], "DEVICE_MODEL", json_data["device"])

            if "app_version" in json_data:
                utils.setSetting(params["session"], "APP_VERSION", json_data["app_version"])

            if "system_lang_code" in json_data:
                utils.setSetting(params["session"], "SYSTEM_LANG_CODE", json_data["system_lang_code"])
            elif "lang_pack" in json_data:
                utils.setSetting(params["session"], "SYSTEM_LANG_CODE", json_data["lang_pack"])
    else:
        writed = writed[0]
        params["session"] = writed[:-7]

    if not params["session"]:
        writed = [file for file in os.listdir() if file.endswith('.session')]
        if writed:
            writed = writed[0]
            params["session"] = writed[:-8]
        else:
            params["session"] = input("   Введите номер телефона: ")
    with open(f"{params['session']}.config", 'a', encoding='utf-8') as config:
        config.close()

    params["api_id"] = utils.getSetting(params["session"], "API_ID")
    params["api_hash"] = utils.getSetting(params["session"], "API_HASH")
    params["device_model"] = utils.getSetting(params["session"], "DEVICE_MODEL")
    params["app_version"] = utils.getSetting(params["session"], "APP_VERSION")
    params["system_lang_code"] = utils.getSetting(params["session"], "SYSTEM_LANG_CODE")

    while True:
        try:
            if not params["api_id"]:
                writed = input("Введите api_id сессии (Enter - по умолчанию): ")
                if writed:
                    params["api_id"] = int(writed)
                else:
                    params["api_id"] = 16623
                utils.setSetting(params["session"], "API_ID", params["api_id"])
            else:
                params["api_id"] = int(params["api_id"])
            if not params["api_hash"]:
                writed = input("Введите api_hash сессии (Enter - по умолчанию): ")
                if writed:
                    params["api_hash"] = writed
                else:
                    params["api_hash"] = "8c9dbfe58437d1739540f5d53c72ae4b"
                utils.setSetting(params["session"], "API_HASH", params["api_hash"])
            if not params["device_model"]:
                params["device_model"] = "Waffentrager"
                utils.setSetting(params["session"], "DEVICE_MODEL", params["device_model"])
            if not params["app_version"]:
                params["app_version"] = "v.2.4"
                utils.setSetting(params["session"], "APP_VERSION", params["app_version"])
            if not params["system_lang_code"]:
                params["system_lang_code"] = "ru-RU"
                utils.setSetting(params["session"], "SYSTEM_LANG_CODE", params["system_lang_code"])

            break
        except Exception as e:
            utils.logger(f"[MAIN] [ERROR] {repr(e)}", "error")

    writed = utils.getSetting(params["session"], "PROXY")
    if not writed:
        writed = input("Введите прокси (IP:PORT:LOGIN:PASSWORD) или нажмите Enter для пропуска: ")
        if writed:
            params["proxy"] = writed
            utils.setSetting(params["session"], "PROXY", params["proxy"])
    else:
        utils.logger(f"[MAIN] Рабочий прокси {writed}", "warn")
        writed = input("Введите свое значение или Enter чтоб продолжить: ")
    
    params["proxy"] = None
    if writed:
        writed = writed.split(':')
        if len(writed) == 4:
            params["proxy"] = {
                'proxy_type': python_socks.ProxyType.HTTP,
                'addr': writed[0],
                'port': int(writed[1]),
                'username': writed[2],
                'password': writed[3]
            }

    client = TelegramClient(
        params["session"], params["api_id"], params["api_hash"], 
        proxy = params["proxy"], 
        device_model = params["device_model"], 
        app_version = params["app_version"], 
        system_lang_code  = params["system_lang_code"], 
        timeout = 20, request_retries = 100, connection_retries = 100, retry_delay = 5
    )
    while True:
        await client.connect()
        if not await client.is_user_authorized():
            utils.logger(f"[MAIN] Формирую сессию", "silly")
            await client.send_code_request(params["session"])
            while True:
                try:
                    while True:
                        try:
                            await client.sign_in(params["session"], code = input('   Введите код: '))
                            break
                        except errors.SessionPasswordNeededError:
                            while True:
                                try:
                                    password = input("Введите пароль: ")
                                    await client.sign_in(password = password)
                                    break
                                except Exception as e:
                                    if "The password (and thus its hash value) you entered is invalid" in repr(e):
                                        utils.logger(f"[AUTHORAZ] [ERROR] Неправильный пароль", "error")
                                        continue
                                    utils.logger(f"[AUTHORAZ] [ERROR] {repr(e)}", "error")
                                    input()
                                    continue
                        break
                except Exception as e:
                    if "The phone code entered was invalid" in repr(e):
                        utils.logger(f"[AUTHORAZ] [ERROR] Неверный код", "error")
                        continue
                    if "wait" in repr(e):
                        utils.logger(f"[AUTHORAZ] [ERROR] Флуд на попытки подключиться", "error")
                        continue
                    utils.logger(f"[AUTHORAZ] [ERROR] {repr(e)}", "error")
                    input()
                    continue
                break
        else:
            break

    while True:
        try:
            clear()
            print("")
            print("")
            print(" 1 - Заполнение аккаунта")
            print(" 2 - Заполнение чатами")
            print(" 3 - Чистка аккаунта")
            print(" 4 - Спам по чатам")
            print(" 5 - Спам по каналам")
            print(" 6 - Парс участников чатов")
            print("- - - - - -")
            mode = input("  Выберите режим работы: ")

            if mode == "1":
                await accounter(client, params["session"])
            if mode == "2":
                await chater(client, params["session"])
            if mode == "3":
                await cleaner(client, params["session"])
            if mode == "4":
                await spamer(client, params)
            if mode == "5":
                await channel(client, params["session"])
            if mode == "6":
                await pars_people(client, params)

        except Exception as e:
            utils.logger(f"[MAIN] [ERROR] {repr(e)}", "error")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())