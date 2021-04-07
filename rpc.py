# -*- coding: utf-8 -*-

import time
import os
import sys
from colors import *
from functions import *

version = '1.8'

import libinstaller
from pypresence import Presence

client_id = '800049969960058882'

RPC = Presence(client_id,pipe=0)

connected = False

if getConfig("use_rpc"):
    try:
        RPC.connect()
        connected = True
    except:
        pass
else:
    connected = False

def disconnect():
    global connected
    
    if getConfig("use_rpc"):
        try:
            RPC.close()
            connected = False
        except:
            pass

def connect():
    global connected
    
    try:
        RPC.connect()
        connected = True
    except:
        pass

def reset():
    if getConfig("use_rpc"):
        RPC.clear()



def waitLesson(lesson, start):
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_waiting', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Ожидание', state=f'Ждём начала «{lesson}»', details='Урок не начался', start=start)
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)

def onLesson(lesson, start):
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_lesson', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Урок', state=f'Слушаем «{lesson}»', details='Идёт урок', start=start)
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)

def inMenu(): 
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_menu', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Главное меню', state='Открыт список опций', details='В главном меню')
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)

def shutdown(end):
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_shutdown', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Выключение', state='Отсчёт до авто-выключения', details='Выключение ПК', end=end)
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)

def inSettings():
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_settings', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Настройки', state='Открыты настройки', details='В главном меню')
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)

def inEditor():
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_editing', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Редактор', state='Открыт редактор', details='В главном меню')
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)

def inUpdater():
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_updating', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Обновление', state='Открыт центр обновлений', details='В главном меню')
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)

def inHelp():
    try:
        if getConfig("use_rpc"):
            if connected == False:
                connect()
            RPC.update(large_image='1024_cover', small_image='status_support', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Помощь', state='Открыта помощь', details='В главном меню')
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)
    except AssertionError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)



if __name__ == "__main__":
    try:
        RPC.connect()
        RPC.update(large_image='1024_cover', small_image='status_settings', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Отладка', state='Модуль Discord RPC запущен в режиме тестирования', details='Режим отладки')
    except AttributeError:
        if getConfig("debug"):
            print(f'{RESET}Модуль {BRED}Discord RPC {RESET}не смог подключиться.\nВозможно, ваш {CYAN}Discord {RESET}не открыт.')
            time.sleep(1)


################################################################################
# Неудачная попытка работы с discord_rpc. Потом, быть может, попробую ещё раз. #
################################################################################

# import discord_rpc
# import time

# if __name__ == "__main__":
    # def readyCallback(current_user):
        # print('Our user: {}'.format(current_user))

    # def disconnectedCallback(codeno, codemsg):
        # print('Disconnected from Discord rich presence RPC. Code {}: {}'.format(
            # codeno, codemsg
        # ))

    # def errorCallback(errno, errmsg):
        # print('An error occurred! Error {}: {}'.format(
            # errno, errmsg
        # ))

# # Note: 'event_name': callback
    # callbacks = {
        # 'ready': readyCallback,
        # 'disconnected': disconnectedCallback,
        # 'error': errorCallback,
    # }

# # if __name__ != "__main__":
    # discord_rpc.initialize('800049969960058882', callbacks=callbacks, log=False)
    # none = input('init')
    
    # i = 0
    
    # while i < 10:
        # discord_rpc.update_presence(
            # **{
                # 'state': f'Загрузка...',
                # 'details': 'Загрузка...',
                # #'start_timestamp': start,
                # 'large_image_key': '1024_cover',
                # 'small_image_key': 'status_waiting',
                # 'large_image_text': f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom',
                # 'small_image_text': 'Ожидание',
            # }
        # )
        # discord_rpc.update_connection()
        # time.sleep(3)
        # discord_rpc.run_callbacks()
        # i += 1

    # i = 0
    # start = time.time()
    # while i < 10:
        # i += 1

    #large_image='1024_cover', small_image='status_waiting', large_text=f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom', small_text='Ожидание', state=f'Ждём начала «{lesson}»', details='Урок не начался', start=start

        # discord_rpc.update_presence(
            # **{
                # 'state': f'Ждём начала «lesson»',
                # 'details': 'Урок не начался',
                # 'start_timestamp': start,
                # 'large_image_key': '1024_cover',
                # 'small_image_key': 'status_waiting',
                # 'large_image_text': f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom',
                # 'small_image_text': 'Ожидание',
            # }
        # )

        # discord_rpc.update_connection()
        # time.sleep(1)
        # discord_rpc.run_callbacks()

    # discord_rpc.shutdown()


    # def disconnect():
        # if getConfig("use_rpc"):
            # discord_rpc.shutdown()


    # def inMenu():
        # if getConfig("use_rpc"):
            # discord_rpc.update_presence(
                # **{
                    # 'state': f'Ждём начала «lesson»',
                    # 'details': 'Урок не начался',
                    # #'start_timestamp': start,
                    # 'large_image_key': '1024_cover',
                    # 'small_image_key': 'status_waiting',
                    # 'large_image_text': f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom',
                    # 'small_image_text': 'Ожидание',
                # }
            # )
            # discord_rpc.update_connection()

# def waitLesson(lesson, start):
    # if getConfig("use_rpc"):
        # discord_rpc.update_presence(
            # **{
                # 'state': f'Ждём начала «lesson»',
                # 'details': 'Урок не начался',
                # 'start_timestamp': start,
                # 'large_image_key': '1024_cover',
                # 'small_image_key': 'status_waiting',
                # 'large_image_text': f'AutoZoom • v{version}\nhttp://bit.ly/auto_zoom',
                # 'small_image_text': 'Ожидание',
            # }
        # )
