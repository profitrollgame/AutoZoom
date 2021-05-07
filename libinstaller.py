# -*- coding: utf-8 -*-

import os, sys
from colors import *
from functions import getConfig, setConfig, getOS, yes_list, no_list
from functions import appendLog
from subprocess import check_output

if getConfig("firstboot"):

    if getOS() == "android":
        while True:
            os.system('clear')
            confirmation = input(f'{BRED}Внимание! {RESET}AutoZoom практически не оптимизирован под {CYAN}Android{RESET}.\nПродолжая использовать программу на ОС кроме {CYAN}Windows {RESET}вы действуете на свой страх и риск.\nПолноценная поддержка операционной системы Android не планируется.\nДля хоть какой-то работы нужно установить Zoom\nи заранее его настроить.\n\nВведите {BGREEN}Да {RESET}если вас не пугает указанное выше.\nВведите {BRED}Нет {RESET}если вас это не устраивает, программа сама закроется.\n\n > ')

            if confirmation.lower() in yes_list:
                setConfig("firstboot", False)
                setConfig("obs_core", "Disabled")
                setConfig("obs_exe", "Disabled")
                setConfig("use_rpc", False)
                break
                
            elif confirmation.lower() in no_list:
                setConfig("firstboot", True)
                sys.exit()
                break
                
            else:
                continue
                
    elif getOS() == "unix":
        while True:
            os.system('clear')
            confirmation = input(f'{BRED}Внимание! {RESET}AutoZoom плохо оптимизирован под {CYAN}Linux {RESET}и {CYAN}MacOS{RESET}.\nПродолжая использовать программу на ОС кроме {CYAN}Windows {RESET}вы действуете на свой страх и риск.\nПолноценная поддержка UNIX систем реализована не будет.\nДля хоть какой-то работы нужно установить Zoom\nи заранее его настроить.\n\nВведите {BGREEN}Да {RESET}если вас не пугает указанное выше.\nВведите {BRED}Нет {RESET}если вас это не устраивает, программа сама закроется.\n\n > ')

            if confirmation.lower() in yes_list:
                setConfig("firstboot", False)
                setConfig("obs_core", "Disabled")
                setConfig("obs_exe", "Disabled")
                break
                
            elif confirmation.lower() in no_list:
                setConfig("firstboot", True)
                sys.exit()
                break
                
            else:
                continue
                
    elif getOS() == "windows":
        setConfig("firstboot", False)

#########################################################
libs = []
###################################
if getOS() == "windows":
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
        from swinlnk.swinlnk import SWinLnk
    except ModuleNotFoundError:
        appendLog("No module swinlnk")
        libs.append("swinlnk")
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
if getOS() != "android":
    try:
        from playsound import playsound
    except ModuleNotFoundError:
        appendLog("No module playsound")
        libs.append("playsound")
else:
    try:
        if not "play-audio" in os.popen('pkg list-all').read():
            os.system('pkg install play-audio')
    except:
        appendLog("Could not install play-audio")
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
        if getOS() == "windows":
            import easygui
            import tkinter
            from swinlnk.swinlnk import SWinLnk
            
        import keyboard
        import ast
        import inputimeout
        import telegram_send
        import wget
        import requests
        import asyncio
        import getpass
        
        if getOS() != "android":
            from playsound import playsound
            
        from zipfile import ZipFile
        from pypresence import Presence
        
    except ModuleNotFoundError:
        sys.exit(f"\n#############################################################################\n{BGREEN} Пожалуйста, перезапустите программу для продолжения!{RESET}\n Если это сообщение видно не впервые - напишите {BRED}@profitroll {RESET}в {CYAN}Telegram {RESET}или\n включите {BRED}debug {RESET}в {BRED}files/config.json {RESET}и решите проблему самостоятельно.\n#############################################################################")
#########################################################