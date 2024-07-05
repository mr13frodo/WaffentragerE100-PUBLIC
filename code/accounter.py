import os
import utils
import random
from telethon.tl import functions, types
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


async def accounter(client, session):
    clear()
    utils.logger(f"[ACCOUNT] Запускаюсь...", "silly")

    while True:
        try:
            input("Убедитесь в наличии аваторок в папке avatar внутри base")
            AVATARS = []
            try:
                for item in os.listdir("./base/avatar"):
                    AVATARS.append(item)
                if len(AVATARS) == 0:
                    utils.logger(f"[ACCOUNT] [{session}] Аватаров нет, пропускаю...", "warn")
                    AVATARS = None
            except Exception as e:
                AVATARS = None
                utils.logger(f"[ACCOUNT] [{session}] Аватаров нет, пропускаю...", "warn")

            input("Убедитесь в наличии имен в файле first_name.txt внутри base")
            try:
                with open('./base/first_name.txt', 'r', encoding='utf-8') as file:
                    FIRST_NAMES = list(filter(None, file.read().split('\n')))
                    file.close()
                if len(FIRST_NAMES) == 0:
                    utils.logger(f"[ACCOUNT] [{session}] Имен нет, пропускаю...", "warn")
                    FIRST_NAMES = None
            except Exception as e:
                FIRST_NAMES = None
                utils.logger(f"[ACCOUNT] [{session}] Имен нет, пропускаю...", "warn")

            input("Убедитесь в наличии фамилий в файле last_name.txt внутри base")
            try:
                with open('./base/last_name.txt', 'r', encoding='utf-8') as file:
                    LAST_NAMES = list(filter(None, file.read().split('\n')))
                    file.close()
                if len(LAST_NAMES) == 0:
                    utils.logger(f"[ACCOUNT] [{session}] Фамилий нет, пропускаю...", "warn")
                    LAST_NAMES = None
            except Exception as e:
                LAST_NAMES = None
                utils.logger(f"[ACCOUNT] [{session}] Фамилий нет, пропускаю...", "warn")

            try:
                input("Убедитесь в наличии био в файле status.txt внутри base")
                with open('./base/status.txt', 'r', encoding='utf-8') as file:
                    STATUSES = list(filter(None, file.read().split('\n')))
                    file.close()
                if len(STATUSES) == 0:
                    utils.logger(f"[ACCOUNT] [{session}] Био нет, пропускаю...", "warn")
                    STATUSES = None
            except Exception as e:
                STATUSES = None
                utils.logger(f"[ACCOUNT] [{session}] Био нет, пропускаю...", "warn")

            break

        except Exception as e:
            utils.logger(f"[ACCOUNT] [{session}] [ERROR] {repr(e)}", "error")

    try:
        utils.logger(f"[ACCOUNT] [{session}] Меняю информацию...", "silly")

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
            utils.logger(f"[ACCOUNT] [{session}] Гружу аватар...", "silly")
            avatar = f"./base/avatar/{AVATARS[random.randint(0, len(AVATARS) - 1)]}"
            await client(functions.photos.UploadProfilePhotoRequest(
                file = await client.upload_file(avatar)
            ))

        utils.logger(f"[ACCOUNT] [{session}] Запрещаю пересылать сообщения...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyForwards(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        utils.logger(f"[ACCOUNT] [{session}] Запрещаю звонить...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneCall(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        utils.logger(f"[ACCOUNT] [{session}] Запрещаю добавлять в чаты...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyChatInvite(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        utils.logger(f"[ACCOUNT] [{session}] Скрываю номер...", "silly")
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneNumber(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))

        utils.logger(f"[ACCOUNT] [{session}] Создаю папки...", "silly")
        try:
            await client(functions.messages.UpdateDialogFilterRequest(
                id = 11,
                filter=types.DialogFilter(
                    id = 12,
                    title = "Люди",
                    pinned_peers = [],
                    include_peers = [],
                    exclude_peers = [],
                    contacts = True,
                    non_contacts = True
                )
            ))
        except Exception as e:
            pass

        try:
            await client(functions.messages.UpdateDialogFilterRequest(
                id = 12,
                filter=types.DialogFilter(
                    id = 12,
                    title = "Группы",
                    pinned_peers = [],
                    include_peers = [],
                    exclude_peers = [],
                    groups=True
                )
            ))
        except Exception as e:
            pass

        try:
            await client(functions.messages.UpdateDialogFilterRequest(
                id = 13,
                filter=types.DialogFilter(
                    id = 13,
                    title = "Каналы",
                    pinned_peers = [],
                    include_peers = [],
                    exclude_peers = [],
                    broadcasts=True
                )
            ))
        except Exception as e:
            pass

    except Exception as e:
        utils.logger(f"[ACCOUNT] [{session}] [ERROR] {repr(e)}", "error")

    input("Чтобы выйти нажмите Enter...")