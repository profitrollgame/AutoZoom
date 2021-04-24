# -*- coding: utf-8 -*-

import os, sys
from colors import *
from functions import getConfig
from functions import appendLog

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
    appendLog("No module easygui")
    libs.append("easygui")
###################################
try:
    import tkinter
except ModuleNotFoundError:
    appendLog("No module tkinter")
    libs.append("tkinter")
###################################
try:
    import keyboard
except ModuleNotFoundError:
    appendLog("No module keyboard")
    libs.append("keyboard")
###################################
try:
    import ast
except ModuleNotFoundError:
    appendLog("No module ast")
    libs.append("ast")
###################################
try:
    import inputimeout
except ModuleNotFoundError:
    appendLog("No module inputimeout")
    libs.append("inputimeout")
###################################
try:
    import telegram_send
except ModuleNotFoundError:
    appendLog("No module telegram_send")
    libs.append("telegram_send")
###################################
try:
    import wget
except ModuleNotFoundError:
    appendLog("No module wget")
    libs.append("wget")
###################################
try:
    import requests
except ModuleNotFoundError:
    appendLog("No module requests")
    libs.append("requests")
###################################
try:
    import playsound
except ModuleNotFoundError:
    appendLog("No module playsound")
    libs.append("playsound")
###################################
try:
    from zipfile import ZipFile
except ModuleNotFoundError:
    appendLog("No module zipfile")
    libs.append("zipfile")
###################################
try:
    import asyncio
except ModuleNotFoundError:
    appendLog("No module asyncio")
    libs.append("asyncio")
###################################
try:
    import getpass
except ModuleNotFoundError:
    appendLog("No module getpass")
    libs.append("getpass")
###################################
try:
    from pypresence import Presence
except ModuleNotFoundError:
    appendLog("No module pypresence")
    libs.append("pypresence")
###################################
if len(libs) > 0:
    print("Не хватает нужных модулей, пробуем установить...\nЭто может занять некоторое время. Пожалуйста, не закрывайте программу.")
    appendLog('Missing some modules, trying to install them')
    
    for each in libs:
        try:
            if getConfig("debug"):
                response = os.system('"{}" -m pip install -U '.format(sys.executable) + each)
            else:
                response = os.system('"{}" -m pip install -U '.format(sys.executable) + each + " -q --no-warn-script-location")
        except:
            response = os.system('"{}" -m pip install -U '.format(sys.executable) + each + " -q --no-warn-script-location")

        print(f"{RESET}[{BGREEN}OK{RESET}] Установлен модуль {YELLOW}{each}{RESET}.")
        
        appendLog(f'Module {each} installed')
        
        if response != 0:
            appendLog(f'Failed to install {each}')
            sys.exit(f"{RESET}[{BRED}ERR{RESET}] Установка {YELLOW}{each} {RESET}провалилась.")
            
    appendLog('Everything seems to be installed')
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
        import getpass
        from zipfile import ZipFile
        from pypresence import Presence
    except ModuleNotFoundError:
        sys.exit(f"\n#############################################################################\n{BGREEN} Пожалуйста, перезапустите программу для продолжения!{RESET}\n Если это сообщение видно не впервые - напишите {BRED}@profitroll {RESET}в {CYAN}Telegram {RESET}или\n включите {BRED}debug {RESET}в {BRED}files/config.json {RESET}и решите проблему самостоятельно.\n#############################################################################")
#########################################################