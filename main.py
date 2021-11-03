# -*- coding: utf-8 -*-

import sys
import pip
import webbrowser
import os
import time
import platform
import subprocess
from pathlib import Path

import libinstaller

from functions import *

appendLog('main.py start initialized', startup=True)

setTitle("", getOS())

from daemon import main
import settings
import editor
import rpc

if getConfig("use_colors"):
    from colors import *
else:
    RESET = ''
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    BBLACK = BRED = BGREEN = BYELLOW = BBLUE = BMAGENTA = BCYAN = BWHITE = ''
    ULINE = REVERSE = ''

import wget
import requests
import keyboard
import getpass
from zipfile import ZipFile

version = 2.4
path = Path(__file__).resolve().parent

def mainMenu():
    try:
        setTitle("AutoZoom (Главная)", getOS())
    
        global version
        global path
        
        appendLog('Main menu opened')
        rpc.inMenu()
        
        while True:
            if getConfig("update_check"):
                print(f'{RESET}Загрузка данных о последней версии...')
                
                try:
                    setTitle("Загрузка данных...", getOS())
                    serv_ver = requests.get("https://www.end-play.xyz/AutoZoomVersion.txt").text
                    setTitle("AutoZoom (Главная)", getOS())
                    ignore = False
                    clear()
                    
                except Exception as exp:
                    appendLog(f'Version number load failed {exp}')
                    setTitle("Ошибка загрузки данных", getOS())
                    print(f'Не удалось загрузить данные о последней версии.\nПроверьте подключение к сети и повторите попытку.\n\nСтатус сервера центра обновлений:\n{BRED}https://stats.uptimerobot.com/OqwR9iAqBg{RESET}')

                    todo = input(f'\nВведите {BRED}ignore {RESET}чтобы выключить проверку обновлений и продолжить\nлибо введите что угодно иное чтобы закрыть программу.\n\n > {BRED}')

                    if todo.lower() == 'ignore':
                        setConfig("update_check", False)
                        serv_ver = ''
                        appendLog('Skipping update check')
                        setTitle("AutoZoom (Главная)", getOS())
                        ignore = True
                        clear()
                    else:
                        rpc.disconnect()
                        sys.exit()
                    
                if ignore == False and float(serv_ver) > float(version):
                    show_version = f' ({BRED}!{RESET})'
                else:
                    show_version = ''
                    
            else:
                show_version = f' ({BRED}!{RESET})'
                setTitle("AutoZoom (Главная)", getOS())
                serv_ver = 'disabled'
                appendLog('Skipping update check')
                clear()
            
            print(f'{BBLACK}»{RESET} Главное меню\n')
            print(f' {BRED}1.{RESET} Запуск')
            print(f' {BRED}2.{RESET} Редактор')
            print(f' {BRED}3.{RESET} Настройки')
            print(f' {BRED}4.{RESET} Обновление{show_version}')
            print(f' {BRED}5.{RESET} Помощь и связь')
            print(f' {BRED}6.{RESET} Закрыть приложение')
            
            if getConfig("debug"):
                print(f' {BRED}10.{RESET} Меню разработчика')
            
            menu_choose = input(f'\n {RESET}> {BRED}')
            print(RESET)
            
            if menu_choose == '1':
                appendLog('Went to daemon')
                main('menu')
            elif menu_choose == '2':
                appendLog('Went to editor')
                rpc.inEditor()
                editor.editor()
            elif menu_choose == '3':
                appendLog('Went to settings')
                rpc.inSettings()
                settings.settings()
            elif menu_choose == '4':
                appendLog('Went to updater')
                rpc.inUpdater()
                updater(serv_ver, version)
            elif menu_choose == '5':
                appendLog('Went to help')
                rpc.inHelp()
                helpMenu()
            elif menu_choose == '6':
                appendLog('Exited AutoZoom from main menu', shutdown=True)
                rpc.disconnect()
                clear()
                sys.exit()
            elif menu_choose == '10':
                if getConfig("debug"):
                    appendLog('Went to help')
                    rpc.inDebug()
                    devMenu()
                else:
                    clear()
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
            setTitle("AutoZoom (Помощь)", getOS())
            appendLog('Help menu opened')
            clear()
            global version
            global path
            
            print(f'{BBLACK}»{RESET} Меню помощи\n')
            print(f' {BRED}1.{RESET} Документация')
            print(f' {BRED}2.{RESET} Сайт проекта')
            print(f' {BRED}3.{RESET} Центр поддержки')
            print(f' {BRED}4.{RESET} Telegram проекта')
            print(f' {BRED}5.{RESET} Связаться с автором')
            print(f' {BRED}6.{RESET} Поддержать проект')
            print(f' {BRED}7.{RESET} Список поддержавших')
            print(f' {BRED}8.{RESET} Сводка информации')
            print(f' {BRED}9.{RESET} В главное меню')
            
            help_choose = input(f'\n > {BRED}')
            
            if help_choose == '1':
                try:
                    clear()
                    appendLog('Opened AutoZoom wiki')
                    webbrowser.open("https://github.com/profitrollgame/autozoom/wiki")
                except Exception as exp:
                    clear()
                    appendLog(f'Failed to open AutoZoom wiki: {exp}')
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://github.com/profitrollgame/autozoom/wiki{RESET}\n\n > ')
                clear()
            elif help_choose == '2':
                try:
                    clear()
                    appendLog('Opened AutoZoom website')
                    webbrowser.open("https://www.end-play.xyz/autozoom")
                except Exception as exp:
                    clear()
                    appendLog(f'Failed to open AutoZoom website: {exp}')
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://www.end-play.xyz/autozoom{RESET}\n\n > ')
                clear()
            elif help_choose == '3':
                try:
                    clear()
                    appendLog('Opened AutoZoom support center')
                    webbrowser.open("https://www.tidio.com/talk/ydqcvfvgkud3jjk2482uaesvjpeohlh3")
                except Exception as exp:
                    clear()
                    appendLog(f'Failed to open AutoZoom support center: {exp}')
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://www.tidio.com/talk/ydqcvfvgkud3jjk2482uaesvjpeohlh3{RESET}\n\n > ')
                clear()
            elif help_choose == '4':
                try:
                    clear()
                    appendLog('Opened AutoZoom Telegram group')
                    webbrowser.open("https://t.me/auto_zoom")
                except Exception as exp:
                    clear()
                    appendLog(f'Failed to open AutoZoom Telegram group: {exp}')
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://t.me/auto_zoom{RESET}\n\n > ')
                clear()
            elif help_choose == '5':
                try:
                    clear()
                    appendLog('Opened AutoZoom\'s developer Telegram')
                    webbrowser.open("https://t.me/profitroll")
                except Exception as exp:
                    clear()
                    appendLog(f'Failed to open AutoZoom\'s developer Telegram: {exp}')
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://t.me/profitroll{RESET}\n\n > ')
                clear()
            elif help_choose == '6':
                try:
                    clear()
                    appendLog('Opened AutoZoom\'s donation page')
                    webbrowser.open("https://www.end-play.xyz/autozoom/donate")
                except Exception as exp:
                    clear()
                    appendLog(f'Failed to open AutoZoom\'s donation page: {exp}')
                    none = input(f'{RESET}Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: {BRED}https://www.end-play.xyz/autozoom/donate{RESET}\n\n > ')
                clear()
            elif help_choose == '7':
                try:
                    clear()
                    print(f'{BBLACK}»{RESET} Список поддержавших проект:\n\n{(requests.get("https://www.end-play.xyz/AutoZoomDonors.txt").text).replace("-", RESET+" •"+BRED)}{RESET}')
                except Exception as exp:
                    clear()
                    appendLog(f'Failed to load donation list {exp}')
                    print(f'{RESET}Не удалось загрузить данные о списке поддержавших проект.\nВы можете посмотреть его самостоятельно: {BRED}https://www.end-play.xyz/AutoZoomDonors.txt')
                none = input('\n > ')
                clear()
            if help_choose == '8':
                clear()
                
                if getState("RBTray.exe"):
                    rbtray = f'{BGREEN}Активен{RESET}'
                else:
                    rbtray = f'{BRED}Неактивен{RESET}'
                    
                if rpc.connected:
                    dsrpc = f'{BGREEN}Активен{RESET}'
                else:
                    dsrpc = f'{BRED}Неактивен{RESET}'
                    
                appendLog(f'Showing system information:\n=============================================\nHelpful data for fault search:\n\nOS: {platform.system()}\nRelease: {platform.release()}\nArch: {os_arch()}\nPy Ver: {platform.python_version()}\nPIP Ver: {pip.__version__}\nImpl: {platform.python_implementation()}\nRev: {platform.python_revision()}\nPy Path: {sys.path[4]}\nAZ Ver: {version}\nAZ User: {getpass.getuser()}\nAZ User Home: {Path.home()}\nAZ Path: {path}\nRBTray: {str(getState("RBTray.exe"))}\nRPC: {str(rpc.connected)}\n=============================================')
                print(f'{BBLACK}»{RESET} Информация о системе\n')
                print(' Система:')
                print(f'  {BBLACK}•{RESET} ОС: {YELLOW}{platform.system()}{RESET}')
                print(f'  {BBLACK}•{RESET} Релиз: {YELLOW}{platform.release()}{RESET}')
                print(f'  {BBLACK}•{RESET} Разрядность: {YELLOW}{os_arch()}{RESET}')
                print('\n Python:')
                print(f'  {BBLACK}•{RESET} Версия: {YELLOW}{platform.python_version()}{RESET}')
                print(f'  {BBLACK}•{RESET} Версия PIP: {YELLOW}{pip.__version__}{RESET}')
                print(f'  {BBLACK}•{RESET} Вариант: {YELLOW}{platform.python_implementation()}{RESET}')
                print(f'  {BBLACK}•{RESET} Ревизия: {YELLOW}{platform.python_revision()}{RESET}')
                print(f'  {BBLACK}•{RESET} Расположение: {BRED}{sys.path[4]}{RESET}')
                print('\n AutoZoom:')
                print(f'  {BBLACK}•{RESET} Версия: {YELLOW}{version}{RESET}')
                print(f'  {BBLACK}•{RESET} Пользователь: {YELLOW}{getpass.getuser()}{RESET}')
                print(f'  {BBLACK}•{RESET} Папка пользователя: {BRED}{Path.home()}{RESET}')
                print(f'  {BBLACK}•{RESET} Расположение: {BRED}{path}{RESET}')
                print('\n Интеграции:')
                print(f'  {BBLACK}•{RESET} RBTray: {rbtray}')
                print(f'  {BBLACK}•{RESET} Discord RPC: {dsrpc}')
                none = input('\n > ')
                clear()
            elif help_choose == '9':
                rpc.inMenu()
                clear()
                setTitle("AutoZoom (Главная)", getOS())
                return
            else:
                clear()
                continue
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return

def devMenu():
    try:
        while True:
            setTitle("AutoZoom (Отладка)", getOS())
            appendLog('Help menu opened')
            
            clear()
            
            print(f'{BBLACK}»{RESET} Меню отладки\n')
            print(f' {BRED}1.{RESET} PlaySound test')
            print(f' {BRED}2.{RESET} WinSound test')
            print(f' {BRED}3.{RESET} Play-audio test')
            print(f' {BRED}4.{RESET} playSound function test')
            print(f' {BRED}5.{RESET} OS check test')
            print(f' {BRED}6.{RESET} Telegram test')
            print(f' {BRED}7.{RESET} Zoom meeting test')
            print(f' {BRED}8.{RESET} Color test')
            print(f' {BRED}9.{RESET} Exit to menu')
            
            choose = input(f'\n > {BRED}')
            
            if choose == '1':
                from playsound import playsound
                playsound(sounds_folder+"debug.wav")
                continue
            
            elif choose == '2':
                import winsound
                winsound.PlaySound(sounds_folder+"debug.wav", winsound.SND_FILENAME)
                continue
                
            elif choose == '3':
                os.system(f'play-audio {sounds_folder}debug.wav')
                continue
                
            elif choose == '4':
                playSound("debug")
                continue
                
            elif choose == '5':
                clear()
                none = input(f'{RESET}{getOS()}\n\n > ')
                continue
                
            elif choose == '6':
                clear()
                import telegram_send
                telegram_send.send(messages=["Telegram message test"], parse_mode="markdown", conf=files_folder+"telegram.conf")
                continue
                
            elif choose == '7':
                clear()
                print(editor.debugLesson())
                none = input(f'{RESET}\n > ')
                continue
                
            elif choose == '8':
                clear()
                print(f'{BLACK}███{RED}███{GREEN}███{YELLOW}███{BLUE}███{MAGENTA}███{CYAN}███{WHITE}███')
                print(f'{BBLACK}███{BRED}███{BGREEN}███{BYELLOW}███{BBLUE}███{BMAGENTA}███{BCYAN}███{BWHITE}███')
                print(f'{RESET}RESET')
                print(f'{REVERSE}REVERSE{RESET}')
                print(f'{ULINE}UNDERLINE{RESET}')
                none = input(RESET+'\n > ')
                continue
                
            elif choose == '9':
                rpc.inMenu()
                clear()
                setTitle("AutoZoom (Главная)", getOS())
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
            setTitle("AutoZoom (Обновления)", getOS())
            appendLog('Updater menu opened')
            clear()
            
            if getConfig("update_check") and float(serv_ver) > float(version):
                show_version = f' ({BRED}!{RESET})'
                serv_ver = serv_ver.rstrip('\n')
                show_action = f'Обновить до {BGREEN}{serv_ver}{RESET}'
                changelog_text = f'Изменения в версии {BGREEN}{serv_ver}{RESET}:'
                changelog_footer = '\nОбновитесь чтобы вышеуказанное работало.'
            elif serv_ver == 'disabled':
                show_version = ''
                show_action = f'Переустановить'
                changelog_text = f'Изменения в вашей версии:'
                changelog_footer = ''
            else:
                show_version = ''
                show_action = f'Переустановить'
                changelog_text = f'Изменения в вашей версии:'
                changelog_footer = ''
        
        
            print(f'{BBLACK}»{RESET} Меню обновлений\n')
            print(f' {BRED}1.{RESET} {show_action}')
            print(f' {BRED}2.{RESET} Список изменений')
            print(f' {BRED}3.{RESET} В главное меню')
            if not getConfig("update_check"):
                print(f'\n{BRED}Внимание!{RESET} У вас выключена проверка обновлений.\nЕсли это было сделанно временно - включите её в настройках.')
            updater_choose = input(f'\n > {BRED}')
            
            if updater_choose == '1':
                appendLog('Choosed to update')
                
                while True:
                    clear()
                    print(f'{RESET}Подтвердите действие:\n')
                    print(f' {BRED}1.{RESET} Установить')
                    print(f' {BRED}2.{RESET} Отменить')
                    updater_decide = input(f'\n > {BRED}')
                    print(RESET)
                    
                    if updater_decide == '1':
                        appendLog('Trying to update AutoZoom')
                        clear()
                        
                        try:
                            wget.download('https://www.end-play.xyz/AutoZoomLatest.zip', out='AutoZoomLatest.zip')
                            appendLog('Latest zip downloaded')
                        except Exception as exp:
                            print(f'{RESET}Не удалось загрузить архив с последней версией.\nПроверьте подключение к сети и повторите попытку.\n\nСтатус сервера центра обновлений:\n{BRED}https://status.end-play.xyz/786373747{RESET}')
                            appendLog(f'Failed to download zip: {exp}')
                            none = input(f'\n > {BRED}')
                            continue

                        with ZipFile('AutoZoomLatest.zip', 'r') as zipObj:
                            zipObj.extractall()
                            print(f'{RESET}Все файлы были успешно загружены')
                            appendLog('Latest zip extracted')
                        
                        if os.path.exists("AutoZoomLatest.zip"):
                            os.remove("AutoZoomLatest.zip")
                            appendLog('Latest used zip deleted')
                        
                        clear()
                        none = input(f'{RESET}Обновление завершено, перезапустите AutoZoom.\n\n > ')
                        rpc.disconnect()
                        clear()
                        print(f'{RESET}Закрываем приложение {BGREEN}AutoZoom{RESET}...')
                        appendLog('Exiting AutoZoom after an update')
                        sys.exit()
                    elif updater_decide == '2':
                        clear()
                        appendLog('Aborted update')
                        break
                    else:
                        continue
                        
            elif updater_choose == '2':
                appendLog('Choosed to check changelog')
                try:
                    changelog = requests.get("https://www.end-play.xyz/AutoZoomChangelog.txt")
                    changelog.encoding = None
                    appendLog('Changelog loaded')
                    clear()
                    print(f'{RESET}{changelog_text}\n')
                    print(changelog.text)
                    print(changelog_footer)
                    none = input('\n > ')
                    continue
                except Exception as exp:
                    clear()
                    print(f'{RESET}Не удалось загрузить чейнджлог.\nПроверьте подключение к сети и повторите попытку.\n\nСтатус сервера центра обновлений:\n{BRED}https://status.end-play.xyz/786373747{RESET}')
                    appendLog(f'Failed to check changelog: {exp}')
                    none = input('\n > ')
                    continue
                    
            elif updater_choose == '3':
                rpc.inMenu()
                clear()
                appendLog('Returning to main menu')
                setTitle("AutoZoom (Главная)", getOS())
                return
                
            else:
                continue
                
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return

if __name__ == '__main__':
    from functions import getConfig
    from daemon import clear, getOS, setTitle
    import time
    setTitle("Загрузка main...", getOS())
    clear()
    
    if getConfig("run_fullscreen"):
        keyboard.press('alt, enter')
        time.sleep(.25)
        keyboard.release('alt, enter')
        
    setTitle("AutoZoom (Главная)", getOS())
    mainMenu()
    sys.exit()
