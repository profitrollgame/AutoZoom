# -*- coding: utf-8 -*-

import os, sys
from colors import *
from functions import getConfig

# Работает не очень стабильно при отсутствии интернета
# try:
    # if getConfig("debug"):
        # updatepip = os.system('"{}" -m pip install -U '.format(sys.executable) + '--upgrade pip')
        # print(f"{RESET}[{BGREEN}OK{RESET}] Обновлён {YELLOW}PIP{RESET}.")
    # else:
        # updatepip = os.system('"{}" -m pip install -U '.format(sys.executable) + '--upgrade pip' + " -q --no-warn-script-location")
        # print(f"{RESET}[{BGREEN}OK{RESET}] Обновлён {YELLOW}PIP{RESET}.")
# except:
    # updatepip = os.system('"{}" -m pip install -U '.format(sys.executable) + '--upgrade pip' + " -q --no-warn-script-location")
    
# if updatepip != 0:
    # sys.exit(f"{RESET}[{BRED}ERR{RESET}] Обновление {YELLOW}PIP {RESET}провалилось.")

#########################################################
libs = []
###################################
try:
    import easygui
except ModuleNotFoundError:
    libs.append("easygui")
###################################
try:
    import tkinter
except ModuleNotFoundError:
    libs.append("tkinter")
###################################
try:
    import keyboard
except ModuleNotFoundError:
    libs.append("keyboard")
###################################
try:
    import ast
except ModuleNotFoundError:
    libs.append("ast")
###################################
try:
    import inputimeout
except ModuleNotFoundError:
    libs.append("inputimeout")
###################################
try:
    import telegram_send
except ModuleNotFoundError:
    libs.append("telegram_send")
###################################
try:
    import wget
except ModuleNotFoundError:
    libs.append("wget")
###################################
try:
    import requests
except ModuleNotFoundError:
    libs.append("requests")
###################################
try:
    import playsound
except ModuleNotFoundError:
    libs.append("playsound")
###################################
try:
    from zipfile import ZipFile
except ModuleNotFoundError:
    libs.append("zipfile")
###################################
try:
    import asyncio
except ModuleNotFoundError:
    libs.append("asyncio")
###################################
try:
    from pypresence import Presence
except ModuleNotFoundError:
    libs.append("pypresence")
###################################
if len(libs) > 0:
    print("Не хватает нужных модулей, пробуем установить...")
    
    for each in libs:
        try:
            if getConfig("debug"):
                response = os.system('"{}" -m pip install -U '.format(sys.executable) + each)
            else:
                response = os.system('"{}" -m pip install -U '.format(sys.executable) + each + " -q --no-warn-script-location")
        except:
            response = os.system('"{}" -m pip install -U '.format(sys.executable) + each + " -q --no-warn-script-location")

        print(f"{RESET}[{BGREEN}OK{RESET}] Установлен модуль {YELLOW}{each}{RESET}.")
        if response != 0:
            sys.exit(f"{RESET}[{BRED}ERR{RESET}] Установка {YELLOW}{each} {RESET}провалилась.")
    print(f"{RESET}[{BGREEN}OK{RESET}] Все модули были успешно установлены.")
    
    try:
        import easygui
        import tkinter
        import keyboard
        import ast
        import inputimeout
        import telegram_send
        import wget
        import requests
        import playsound
        import asyncio
        from zipfile import ZipFile
        from pypresence import Presence
    except ModuleNotFoundError:
        sys.exit(f"\n#############################################################################\n{BGREEN} Пожалуйста, перезапустите программу для продолжения!{RESET}\n Если это сообщение видно не впервые - напишите {BRED}@profitroll {RESET}в {CYAN}Telegram {RESET}или\n включите {BRED}debug {RESET}в {BRED}files/config.json {RESET}и решите проблему самостоятельно.\n#############################################################################")
#########################################################