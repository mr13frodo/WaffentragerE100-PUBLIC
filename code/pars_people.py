import os
import utils
from telethon.tl import functions, types
from datetime import datetime
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')


async def pars_people(client, params):
    clear()
    dialogs = await client.get_dialogs()
    groups = []
    for dialog in dialogs:
        if dialog.is_group:
            groups.append(dialog)

        
    for group in groups:
        try:
            utils.logger(f"Парщу  участников с {group.title}...", "silly")
            try:
                if group.entity.deactivated:
                    continue
            except Exception as e:
                    pass
            
            admin_usernames = []
            async for admin in client.iter_participants(group.id, filter = types.ChannelParticipantsAdmins):
                try:
                    if admin.username:
                        admin_usernames.append(admin.username)
                except Exception as e:
                    utils.logger(f"[USERPARS] [ERROR] {repr(e)}", "error")
            user_list = await client.get_participants(entity = group.entity)
            utils.logger(f"Спарсил {len(user_list)}...", "silly")

            utils.logger(f"Перебираю список участников...", "silly")
            for user in user_list:
                if user.username:
                    if user.bot:
                        utils.logger(f"{user.username} оказался ботом...", "warn")
                        continue
                    if user.username in admin_usernames:
                        utils.logger(f"{user.username} админ чата...", "warn")
                        continue
                    if user.premium:
                        utils.logger(f"{user.username} потенциально кадровик...", "warn")
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
                                utils.logger(f"{user.username} давно не в сети...", "warn")
                                continue
                        else:
                            if status.split("(")[0] != "UserStatusRecently" and status.split("(")[0] != "UserStatusOnline":
                                utils.logger(f"{user.username} давно не в сети...", "warn")
                                continue

                    with open('./users.txt', 'a', encoding='utf-8') as f:
                        f.write(f"@{user.username}" + '\n')
            print("")
        except Exception as e:
            utils.logger(f"[USERPARS] [ERROR] {repr(e)}", "error")