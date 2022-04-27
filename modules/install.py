# -*- coding: utf-8 -*-

import os
from modules.functions import getOS, appendLog

libs = ["keyboard", "ast", "inputimeout", "telegram_send", "wget", "requests", "zipfile", "asyncio", "getpass", "pypresence"]

if getOS() == "windows":
    libs.append("easygui")
    libs.append("tkinter")
    libs.append("swinlnk")

if getOS() != "android":
    libs.append("playsound")
else:
    try:
        if not "play-audio" in os.popen('pkg list-all').read():
            os.system('pkg install play-audio')
    except:
        appendLog("Could not install play-audio")

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.writelines('\n'.join(libs))