# -*- coding: utf-8 -*-

import time
import os
import sys
from colors import *
from functions import *

version = '2.5'

import libinstaller
from pypresence import Presence

client_id = '800049969960058882'

RPC = Presence(client_id,pipe=0)

connected = False

rpc_dict = {
    "large_image": "1024_cover",
    "small_image": {
        "waiting": "status_waiting",
        "conference": "status_lesson",
        "menu": "status_menu",
        "shutdown": "status_shutdown",
        "settings": "status_settings",
        "debug": "status_debug",
        "editor": "status_editing",
        "updating": "status_updating",
        "support": "status_support"
    },
    "large_text": "AutoZoom • v%version%\nhttp://bit.ly/auto_zoom"
}

if getConfig("use_rpc") and getOS != "android":
    try:
        RPC.connect()
        connected = True
    except:
        pass
else:
    connected = False

def disconnect():
    global connected
    
    if getConfig("use_rpc") and getOS != "android":
        try:
            RPC.close()
            connected = False
            appendLog('Discord RPC disconnected')
        except:
            appendLog('Discord RPC failed to disconnect')

def connect():
    global connected
    
    try:
        RPC.connect()
        connected = True
        appendLog('Discord RPC connected')
    except:
        appendLog('Discord RPC failed to connect')

def reset():
    if getConfig("use_rpc") and getOS != "android":
        RPC.clear()
        appendLog('Discord RPC status cleared')


def changePresence(sml_img, sml_txt, stt, dtls, start=None, end=None):
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(
                large_image=rpc_dict["large_image"],
                small_image=rpc_dict["small_image"][sml_img],
                large_text=rpc_dict["large_text"].replace("%version%", str(version)),
                small_text=sml_txt,
                state=stt,
                details=dtls,
                start=start,
                end=end
            )
        appendLog(f'Discord RPC changed: (Small image: {sml_img}, Small text: {sml_txt}, State: {stt}, Details: {dtls}, Start: {str(start)}, End: {str(end)})')
    except AttributeError:
        appendLog('Discord RPC failed to change status')
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        appendLog('Discord RPC failed to change status')
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except Exception as exp:
        appendLog(f'Discord RPC failed to change status due to {exp}')
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.\nОшибка: {BRED}{exp}{RESET}')
            time.sleep(1)


def waitLesson(conference, start):
    changePresence("waiting", "Ожидание", f"Ждём начала «{conference}»", "Конференция не началась", start=start)

def onLesson(conference, start):
    changePresence("conference", "Конференция", f"Слушаем «{conference}»", "Идёт конференция", start=start)

def inMenu(): 
    changePresence("menu", "Главное меню", "Открыт список опций", "В главном меню")

def shutdown(end):
    changePresence("shutdown", "Выключение", "Отсчёт до авто-выключения", "Выключение ПК", end=end)

def inSettings():
    changePresence("settings", "Настройки", "Открыты настройки", "В главном меню")

def inDebug():
    changePresence("debug", "Отладка", "Открыто меню отладки", "В меню разработчика")

def inEditor():
    changePresence("editor", "Редактор", "Открыт редактор", "В главном меню")

def inUpdater():
    changePresence("updating", "Обновление", "Открыт центр обновлений", "В главном меню")

def inHelp():
    changePresence("support", "Помощь", "Открыта помощь", "В главном меню")

def lessonEnded():
    changePresence("waiting", "Ожидание", "Ждём указаний", "Все конференции закончились")


if __name__ == "__main__":
    changePresence("settings", "Отладка", "Модуль Discord RPC запущен в режиме тестирования", "Режим отладки")