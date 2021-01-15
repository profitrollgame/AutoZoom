import sys
import webbrowser
import os
import platform
import subprocess
from daemon import install
from pathlib import Path

install('wget')
install('zipfile')
install('requests')
import wget
import requests
from zipfile import ZipFile
from daemon import main, editor, settings, clear

version = 1.4
path = Path(__file__).resolve().parent

def mainMenu():
    try:
        global version
        global path
        
        while True:
            serv_ver = requests.get("https://www.end-play.xyz/AutoZoomVersion.txt").text
            if float(serv_ver) > float(version):
                show_version = ' (!)'
            else:
                show_version = ''
        
            #clear()
            menu_choose = input(f'» Главное меню\n\n1. Запуск\n2. Редактор\n3. Настройки\n4. Обновление{show_version}\n5. Помощь и связь\n6. Закрыть приложение\n\n > ')
            
            if menu_choose == '1':
                main('menu')
            elif menu_choose == '2':
                editor()
            elif menu_choose == '3':
                settings()
            elif menu_choose == '4':
                updater(serv_ver, version)
            elif menu_choose == '5':
                helpMenu()
            elif menu_choose == '6':
                clear()
                sys.exit()
            else:
                clear()
                continue
    except:
        clear()

def os_arch():
    is_64bits = sys.maxsize > 2**32
    
    if is_64bits:
        return '64bit'
    else:
        return '32bit'

def helpMenu():
    try:
        while True:
            clear()
            global version
            global path
            help_choose = input(f'» Меню помощи\n\n1. Документация\n2. Telegram проекта\n3. Связаться с автором\n4. Сводка информации\n5. В главное меню\n\n > ')
            if help_choose == '1':
                try:
                    clear()
                    webbrowser.open("https://github.com/profitrollgame/autozoom/wiki")
                except:
                    clear()
                    none = input('Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: https://github.com/profitrollgame/autozoom/wiki\n\n > ')
                clear()
            elif help_choose == '2':
                try:
                    clear()
                    webbrowser.open("https://t.me/auto_zoom")
                except:
                    clear()
                    none = input('Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: https://t.me/auto_zoom\n\n > ')
                clear()
            elif help_choose == '3':
                try:
                    clear()
                    webbrowser.open("https://t.me/profitroll")
                except:
                    clear()
                    none = input('Не удалось открыть страницу вашего браузера.\nВы можете открыть адрес самостоятельно: https://t.me/profitroll\n\n > ')
                clear()
            if help_choose == '4':
                clear()
                print('» Информация о системе\n')
                print('Система:')
                print(f'• ОС: {platform.system()}')
                print(f'• Релиз: {platform.release()}')
                print(f'• Разрядность: {os_arch()}')
                print('\nPython:')
                print(f'• Версия: {platform.python_version()}')
                print(f'• Вариант: {platform.python_implementation()}')
                print(f'• Ревизия: {platform.python_revision()}')
                print(f'• Расположение: {sys.path[4]}')
                print('\nAutoZoom:')
                print(f'• Версия: {version}')
                print(f'• Расположение: {path}')
                none = input('\n > ')
                clear()
            elif help_choose == '5':
                clear()
                return
            else:
                clear()
                continue
    except KeyboardInterrupt:
        clear()
        return

def updater(serv_ver, version):
    try:
        while True:
            clear()
            if float(serv_ver) > float(version):
                show_version = ' (!)'
                serv_ver = serv_ver.rstrip('\n')
                show_action = f'Обновить до {serv_ver}'
                changelog_text = f'Изменения в версии {serv_ver}:'
                changelog_footer = '\nОбновитесь чтобы вышеуказанное работало.'
            else:
                show_version = ''
                show_action = f'Переустановить'
                changelog_text = f'Изменения в вашей версии:'
                changelog_footer = ''
        
        
            updater_choose = input(f'» Меню обновлений\n\n1. {show_action}\n2. Список изменений\n3. В главное меню\n\n > ')
            if updater_choose == '1':
                while True:
                    clear()
                    updater_decide = input(f'1. Установить\n2. Отменить\n\n > ')
                    
                    if updater_decide == '1':
                        clear()
                
                        wget.download('https://www.end-play.xyz/AutoZoomLatest.zip', out='AutoZoomLatest.zip')
                        with ZipFile('AutoZoomLatest.zip', 'r') as zipObj:
                            zipObj.extractall()
                            print('Все файлы были успешно загружены') 
                        
                        if os.path.exists("AutoZoomLatest.zip"):
                                os.remove("AutoZoomLatest.zip")
                        
                        clear()
                        none = input('Обновление завершено, перезапустите AutoZoom.\n\n > ')
                        sys.exit()
                    elif updater_decide == '2':
                        clear()
                        break
                    else:
                        continue
            elif updater_choose == '2':
                changelog = requests.get("https://www.end-play.xyz/AutoZoomChangelog.txt")
                changelog.encoding = None
                clear()
                print(f'{changelog_text}\n')
                print(changelog.text)
                print(changelog_footer)
                
                none = input('\n > ')
                continue
            elif updater_choose == '3':
                clear()
                return
            else:
                continue
    except:
        clear()
        return

if __name__ == '__main__':
    from daemon import clear
    clear()
    
    mainMenu()