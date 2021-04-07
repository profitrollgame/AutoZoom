# -*- coding: utf-8 -*-

import sys
import webbrowser
import os
import time
import platform
import subprocess
from pathlib import Path

from functions import *

os.system("title")

from daemon import main, editor, settings, clear
import rpc

if getConfig("use_colors"):
    from colors import *
else:
    RESET = ''
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    BBLACK = BRED = BGREEN = BYELLOW = BBLUE = BMAGENTA = BCYAN = BWHITE = ''
    ULINE = REVERSE = ''

import libinstaller

import wget
import requests
import keyboard
from zipfile import ZipFile

version = 1.8
path = Path(__file__).resolve().parent

def mainMenu():
    try:
        os.system("title AutoZoom (Главная)")
    
        global version
        global path
        
        rpc.inMenu()
        
        while True:
            print(f'{RESET}Загрузка данных о последней версии...')
            try:
                os.system("title Загрузка данных...")
                serv_ver = requests.get("https://www.end-play.xyz/AutoZoomVersion.txt").text
                os.system("title AutoZoom (Главная)")
                clear()
            except:
                os.system("title Ошибка загрузки данных")
                print(f'Не удалось загрузить данные о последней версии.\nПроверьте подключение к сети и повторите попытку.\n\nСтатус сервера центра обновлений:\n{BRED}https://status.end-play.xyz/786373747{RESET}')
                none = input('\n > ')
                rpc.disconnect()
                sys.exit()
            if float(serv_ver) > float(version):
                show_version = f' ({BRED}!{RESET})'
            else:
                show_version = ''
                
            print(f'{BBLACK}»{RESET} Главное меню\n')
            print(f' {BRED}1.{RESET} Запуск')
            print(f' {BRED}2.{RESET} Редактор')
            print(f' {BRED}3.{RESET} Настройки')
            print(f' {BRED}4.{RESET} Обновление{show_version}')
            print(f' {BRED}5.{RESET} Помощь и связь')
            print(f' {BRED}6.{RESET} Закрыть приложение')
            menu_choose = input(f'\n > {BRED}')
            print(RESET)
            
            if menu_choose == '1':
                main('menu')
            elif menu_choose == '2':
                rpc.inEditor()
                editor()
            elif menu_choose == '3':
                rpc.inSettings()
                settings()
            elif menu_choose == '4':
                rpc.inUpdater()
                updater(serv_ver, version)
            elif menu_choose == '5':
                rpc.inHelp()
                helpMenu()
            elif menu_choose == '6':
                rpc.disconnect()
                clear()
                sys.exit()
            else:
                clear()
                continue
    except KeyboardInterrupt:
        rpc.disconnect()
        clear()
        print(f'Закрываем приложение {BGREEN}AutoZoom{RESET}...')
        sys.exit()

def os_arch():
    is_64bits = sys.maxsize > 2**32
    
    if is_64bits:
        return '64bit'
    else:
        return '32bit'

def helpMenu():
    try:
        while True:
            os.system("title AutoZoom (Помощь)")
            clear()
            global version
            global path
            
            print(f'{BBLACK}»{RESET} Меню помощи\n')
            print(f' {BRED}1.{RESET} Документация')
            print(f' {BRED}2.{RESET} Telegram проекта')
            print(f' {BRED}3.{RESET} Связаться с автором')
            print(f' {BRED}4.{RESET} Сводка информации')
            print(f' {BRED}5.{RESET} В главное меню')
            help_choose = input(f'\n > {BRED}')
            
            if help_choose == '1':
                try:
                    clear()
                    webbrowser.open("https://github.com/profitrollgame/autozoom/wiki")
                except:
                    clear()
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://github.com/profitrollgame/autozoom/wiki{RESET}\n\n > ')
                clear()
            elif help_choose == '2':
                try:
                    clear()
                    webbrowser.open("https://t.me/auto_zoom")
                except:
                    clear()
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://t.me/auto_zoom{RESET}\n\n > ')
                clear()
            elif help_choose == '3':
                try:
                    clear()
                    webbrowser.open("https://t.me/profitroll")
                except:
                    clear()
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://t.me/profitroll{RESET}\n\n > ')
                clear()
            if help_choose == '4':
                clear()
                print(f'{BBLACK}»{RESET} Информация о системе\n')
                print(' Система:')
                print(f'  {BBLACK}•{RESET} ОС: {YELLOW}{platform.system()}{RESET}')
                print(f'  {BBLACK}•{RESET} Релиз: {YELLOW}{platform.release()}{RESET}')
                print(f'  {BBLACK}•{RESET} Разрядность: {YELLOW}{os_arch()}{RESET}')
                print('\n Python:')
                print(f'  {BBLACK}•{RESET} Версия: {YELLOW}{platform.python_version()}{RESET}')
                print(f'  {BBLACK}•{RESET} Вариант: {YELLOW}{platform.python_implementation()}{RESET}')
                print(f'  {BBLACK}•{RESET} Ревизия: {YELLOW}{platform.python_revision()}{RESET}')
                print(f'  {BBLACK}•{RESET} Расположение: {BRED}{sys.path[4]}{RESET}')
                print('\n AutoZoom:')
                print(f'  {BBLACK}•{RESET} Версия: {YELLOW}{version}{RESET}')
                print(f'  {BBLACK}•{RESET} Расположение: {BRED}{path}{RESET}')
                none = input('\n > ')
                clear()
            elif help_choose == '5':
                rpc.inMenu()
                clear()
                os.system("title AutoZoom (Главная)")
                return
            else:
                clear()
                continue
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return

def updater(serv_ver, version):
    try:
        while True:
            os.system("title AutoZoom (Обновления)")
            clear()
            if float(serv_ver) > float(version):
                show_version = f' ({BRED}!{RESET})'
                serv_ver = serv_ver.rstrip('\n')
                show_action = f'Обновить до {BGREEN}{serv_ver}{RESET}'
                changelog_text = f'Изменения в версии {BGREEN}{serv_ver}{RESET}:'
                changelog_footer = '\nОбновитесь чтобы вышеуказанное работало.'
            else:
                show_version = ''
                show_action = f'Переустановить'
                changelog_text = f'Изменения в вашей версии:'
                changelog_footer = ''
        
        
            print(f'{BBLACK}»{RESET} Меню обновлений\n')
            print(f' {BRED}1.{RESET} {show_action}')
            print(f' {BRED}2.{RESET} Список изменений')
            print(f' {BRED}3.{RESET} В главное меню')
            updater_choose = input(f'\n > {BRED}')
            if updater_choose == '1':
                while True:
                    clear()
                    print(f'{RESET}Подтвердите действие:\n')
                    print(f' {BRED}1.{RESET} Установить')
                    print(f' {BRED}2.{RESET} Отменить')
                    updater_decide = input('\n > ')
                    
                    if updater_decide == '1':
                        clear()
                        
                        try:
                            wget.download('https://www.end-play.xyz/AutoZoomLatest.zip', out='AutoZoomLatest.zip')
                        except:
                            print(f'Не удалось загрузить архив с последней версией.\nПроверьте подключение к сети и повторите попытку.\n\nСтатус сервера центра обновлений:\n{BRED}https://status.end-play.xyz/786373747{RESET}')
                            none = input('\n > ')
                            continue

                        with ZipFile('AutoZoomLatest.zip', 'r') as zipObj:
                            zipObj.extractall()
                            print('Все файлы были успешно загружены') 
                        
                        if os.path.exists("AutoZoomLatest.zip"):
                                os.remove("AutoZoomLatest.zip")
                        
                        clear()
                        none = input('Обновление завершено, перезапустите AutoZoom.\n\n > ')
                        rpc.disconnect()
                        clear()
                        print(f'Закрываем приложение {BGREEN}AutoZoom{RESET}...')
                        sys.exit()
                    elif updater_decide == '2':
                        clear()
                        break
                    else:
                        continue
            elif updater_choose == '2':
                try:
                    changelog = requests.get("https://www.end-play.xyz/AutoZoomChangelog.txt")
                    changelog.encoding = None
                    clear()
                    print(f'{RESET}{changelog_text}\n')
                    print(changelog.text)
                    print(changelog_footer)
                    none = input('\n > ')
                    continue
                except:
                    print(f'{RESET}Не удалось загрузить чейнджлог.\nПроверьте подключение к сети и повторите попытку.\n\nСтатус сервера центра обновлений:\n{BRED}https://status.end-play.xyz/786373747{RESET}')
                    none = input('\n > ')
                    continue
            elif updater_choose == '3':
                rpc.inMenu()
                clear()
                os.system("title AutoZoom (Главная)")
                return
            else:
                continue
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return

if __name__ == '__main__':
    os.system("title Загрузка main...")
    from functions import getConfig
    from daemon import clear
    import time
    clear()
    
    if getConfig("run_fullscreen"):
        keyboard.press('alt, enter')
        time.sleep(.25)
        keyboard.release('alt, enter')
    os.system("title AutoZoom (Главная)")
    mainMenu()
    sys.exit()
