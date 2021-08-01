# -*- coding: utf-8 -*-

import time
import os
import sys
from colors import *
from functions import *

version = '2.3'

import libinstaller
from pypresence import Presence

client_id = '800049969960058882'

RPC = Presence(client_id,pipe=0)

connected = False

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



def waitLesson(lesson, start):
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_waiting', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Ожидание', state=f'Ждём начала «{lesson}»', details='Конференция не началась', start=start)
        appendLog(f'Discord RPC changed to waitLesson (Lesson: {lesson}, Start: {start})')
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

def onLesson(lesson, start):
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_lesson', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Конференция', state=f'Слушаем «{lesson}»', details='Идёт конференция', start=start)
        appendLog(f'Discord RPC changed to onLesson (Lesson: {lesson}, Start: {start})')
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

def inMenu(): 
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_menu', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Главное меню', state='Открыт список опций', details='В главном меню')
        appendLog('Discord RPC changed to inMenu')
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

def shutdown(end):
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_shutdown', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Выключение', state='Отсчёт до авто-выключения', details='Выключение ПК', end=end)
        appendLog(f'Discord RPC changed to shutdown (End: {end})')
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

def inSettings():
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_settings', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Настройки', state='Открыты настройки', details='В главном меню')
        appendLog('Discord RPC changed to inSettings')
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

def inDebug():
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_debug', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Отладка', state='Открыто меню отладки', details='В меню разработчика')
        appendLog('Discord RPC changed to inDebug')
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

def inEditor():
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_editing', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Редактор', state='Открыт редактор', details='В главном меню')
        appendLog('Discord RPC changed to inEditor')
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

def inUpdater():
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_updating', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Обновление', state='Открыт центр обновлений', details='В главном меню')
        appendLog('Discord RPC changed to inUpdater')
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

def inHelp():
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_support', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Помощь', state='Открыта помощь', details='В главном меню')
        appendLog('Discord RPC changed to inHelp')
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

def lessonEnded():
    try:
        if getConfig("use_rpc") and getOS != "android":
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_waiting', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Ожидание', state=f'Ждём указаний', details='Все конференции закончились')
        appendLog('Discord RPC changed to lessonEnded')
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


if __name__ == "__main__":
    try:
        RPC.connect()
        RPC.update(large_image='1024_cover', small_image='status_settings', large_text=f'AutoZoom • v{str(version)}\nhttp://bit.ly/auto_zoom', small_text='Отладка', state='Модуль Discord RPC запущен в режиме тестирования', details='Режим отладки')
        appendLog('Discord RPC changed to debug')
    except AttributeError:
        appendLog('Discord RPC failed to change status')
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
