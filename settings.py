import rpc
import pathlib
import shutil
from functions import *
#from daemon import


if getConfig("use_colors"):
    from colors import *
    appendLog('Colors imported')
else:
    RESET = ''
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    BBLACK = BRED = BGREEN = BYELLOW = BBLUE = BMAGENTA = BCYAN = BWHITE = ''
    ULINE = REVERSE = ''
    appendLog('Loading without colors')


sysname = getOS()


if sysname == "windows":
    from swinlnk.swinlnk import SWinLnk

    swl = SWinLnk()


def settings():
    appendLog('Settings page 1 opened')
    global sysname

    try:
        while True:
            
            setTitle("AutoZoom (Настройки)", sysname)
            clear()
            
            if getConfig("debug"):
                debug_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("debug"):
                debug_val = f'{BRED}Выкл.{RESET}'
            else:
                debug_val = f'{BRED}ERROR{RESET}'

            if getConfig("run_fullscreen"):
                fullscreen_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("run_fullscreen"):
                fullscreen_val = f'{BRED}Выкл.{RESET}'
            else:
                fullscreen_val = f'{BRED}ERROR{RESET}'

            if getConfig("sounds"):
                sounds_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("sounds"):
                sounds_val = f'{BRED}Выкл.{RESET}'
            else:
                sounds_val = f'{BRED}ERROR{RESET}'

            if getConfig("obs_exe") and getConfig("obs_core") not in [None, 'Disabled']:
                obs_val = f'{BGREEN}Вкл.{RESET}'
            else:
                obs_val = f'{BRED}Выкл.{RESET}'
                
            if getConfig("use_colors"):
                color_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("use_colors"):
                color_val = f'{BRED}Выкл.{RESET}'
            else:
                color_val = f'{BRED}ERROR{RESET}'
                
            if getConfig("shutdown_enabled"):
                shutdown_en_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("shutdown_enabled"):
                shutdown_en_val = f'{BRED}Выкл.{RESET}'
            else:
                shutdown_en_val = f'{BRED}ERROR{RESET}'
             
            shutdown_time_val = getConfig("shutdown_timeout")
            start_val = getConfig("start")
            stop_val = getConfig("stop")
            
            print(f'{RESET}{BBLACK}»{RESET} Настройки (1 стр.)\n')

            print(f'  {BRED}1.{RESET} Режим отладки ({debug_val})')
            print(f'     {BBLACK}Не рекомендуем включать его без необходимости\n')

            print(f'  {BRED}2.{RESET} Цветной вывод ({color_val})')
            print(f'     {BBLACK}Отображение цветных текстов в меню и выводе (нужен перезапуск)\n')

            print(f'  {BRED}3.{RESET} Полный экран ({fullscreen_val})')
            print(f'     {BBLACK}{winOnly(BRED, BBLACK, sysname, end=" ")}Эмулировать вызов полного экрана при запуске (окно должно быть в фокусе)\n')

            print(f'  {BRED}4.{RESET} Звуковые сигналы ({sounds_val})')
            print(f'     {BBLACK}Воспроизводить звуки при начале/конце конференций и записи видео\n')
            
            print(f'  {BRED}5.{RESET} Запись через OBS ({obs_val})')
            print(f'     {BBLACK}{winOnly(BRED, BBLACK, sysname, end=" ")}Возможность записи конференций через OBS\n')

            print(f'  {BRED}6.{RESET} Автовыключение ({shutdown_en_val})')
            print(f'     {BBLACK}Когда конференции закончатся компьютер выключится\n')

            print(f'  {BRED}7.{RESET} Следующая страница')
            print(f'     {BBLACK}Перейти на вторую страницу настроек\n')

            print(f'  {BRED}8.{RESET} В главное меню')
            print(f'     {BBLACK}Вернуться в основное меню{RESET}\n')

            print(f' {BBLACK}Для переключения параметров Вкл/Выкл просто введите номер{RESET}') #\n Если окно приложения слишком мелкое - увеличьте его или листайте это меню{RESET}')

            settings_choose = input(f'\n > {BRED}')

            if settings_choose == '1':
                setConfig("debug", not getConfig("debug"))
                appendLog(f'Changed option "debug" to {getConfig("debug")}')
                
                clear()
                continue

            elif settings_choose == '2':
                setConfig("use_colors", not getConfig("use_colors"))
                appendLog(f'Changed option "use_colors" to {getConfig("use_colors")}')
                
                clear()
                continue

            elif settings_choose == '3':
                if sysname == 'windows':
                    setConfig("run_fullscreen", not getConfig("run_fullscreen"))
                    appendLog(f'Changed option "run_fullscreen" to {getConfig("run_fullscreen")}')
                
                clear()
                continue

            elif settings_choose == '4':
                setConfig("sounds", not getConfig("sounds"))
                appendLog(f'Changed option "sounds" to {getConfig("sounds")}')
                
                clear()
                continue
                
            elif settings_choose == '5':

                if sysname == 'windows':
                    if getConfig("obs_core") and getConfig("obs_exe") not in [None, 'Disabled']:
                        setConfig("obs_core", "Disabled")
                        setConfig("obs_exe", "Disabled")
                        
                    else:
                        clear()
                        obs_choice = input(f'{RESET}Хотите использовать запись через OBS? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET}): ')
                        
                        if obs_choice.lower() in yes_list:
                            while True:
                                try:
                                    filename = easygui.fileopenbox('Выберите путь до obs32.exe или obs64.exe')
                                    if filename.find("obs64.exe") != -1:
                                        setConfig("obs_exe", filename)
                                        setConfig("obs_core", filename[:-9])
                                        print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-9]}{RESET}')
                                        time.sleep(3)
                                        break
                                    elif filename.find("obs32.exe") != -1:
                                        setConfig("obs_exe", filename)
                                        setConfig("obs_core", filename[:-9])
                                        print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-9]}{RESET}')
                                        time.sleep(3)
                                        break
                                    elif filename.find("obs.exe") != -1:
                                        setConfig("obs_exe", filename)
                                        setConfig("obs_core", filename[:-7])
                                        print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-7]}{RESET}')
                                        time.sleep(3)
                                        break
                                    else:
                                        easygui.msgbox("Неверный путь")
                                    break
                                except Exception as exp:
                                    appendLog(f'Could not select OBS path: {exp}')
                                    none = input('Вы не выбрали верный путь для OBS.\n\n > ')
                                    clear()
                                    break
                                        
                        appendLog(f'Changed option "obs_exe" to {getConfig("obs_exe")}')
                        appendLog(f'Changed option "obs_core" to {getConfig("obs_core")}')
                
                clear()
                continue

            elif settings_choose == '6':
                setConfig("shutdown_enabled", not getConfig("shutdown_enabled"))
                appendLog(f'Changed option "shutdown_enabled" to {getConfig("shutdown_enabled")}')
                
                clear()
                continue

            elif settings_choose == '7':
                clear()
                settings2()
                
            elif settings_choose == '8':
                rpc.inMenu()
                clear()
                setTitle("AutoZoom (Главная)", sysname)
                return
                
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return


def settings2():
    appendLog('Settings page 2 opened')
    global sysname

    try:
        while True:
            
            setTitle("AutoZoom (Настройки)", sysname)
            clear()
                
            if getConfig("use_colors"):
                color_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("use_colors"):
                color_val = f'{BRED}Выкл.{RESET}'
            else:
                color_val = f'{BRED}ERROR{RESET}'
            
            if os.path.exists(files_folder+'telegram.conf'):
                tg_file = open(files_folder+'telegram.conf', 'r', encoding="utf-8")
                tg_text = tg_file.read()
                if tg_text != 'Not Configured':
                    tg_var = f'{BGREEN}Настроен{RESET}'
                else:
                    tg_var = f'{BRED}Не настроен{RESET}'
            else:
                tg_var = f'{BRED}Не настроен{RESET}'
                
            if getConfig("telegram_enabled"):
                telegram_en_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("telegram_enabled"):
                telegram_en_val = f'{BRED}Выкл.{RESET}'
            else:
                telegram_en_val = f'{BRED}ERROR{RESET}'
                
            if getConfig("update_check"):
                update_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("update_check"):
                update_val = f'{BRED}Выкл.{RESET}'
            else:
                update_val = f'{BRED}ERROR{RESET}'
             
            shutdown_time_val = getConfig("shutdown_timeout")
            start_val = getConfig("start")
            stop_val = getConfig("stop")
            
            print(f'{RESET}{BBLACK}»{RESET} Настройки (2 стр.)\n')

            print(f'  {BRED}1.{RESET} Таймаут выключения ({YELLOW}{shutdown_time_val} мин.{RESET})')
            print(f'     {BBLACK}Время в минутах после которого ПК будет выключен\n')

            print(f'  {BRED}2.{RESET} Начать запись ({YELLOW}{start_val}{RESET})')
            print(f'     {BBLACK}{winOnly(BRED, BBLACK, sysname, end=" ")}Комбинация клавиш для начала записи через OBS (см. документацию)\n')

            print(f'  {BRED}3.{RESET} Остановить запись ({YELLOW}{stop_val}{RESET})')
            print(f'     {BBLACK}{winOnly(BRED, BBLACK, sysname, end=" ")}Комбинация клавиш для остановки записи через OBS (см. документацию)\n')

            print(f'  {BRED}4.{RESET} Отправлять уведомления ({telegram_en_val})')
            print(f'     {BBLACK}Ваш бот отправит сообщениия о начале/конце конференции и выключении ПК\n')

            print(f'  {BRED}5.{RESET} Настроить Telegram бота ({tg_var})')
            print(f'     {BBLACK}Настроить на вашем ПК бота для ЛС (см. документацию)\n')
            
            print(f'  {BRED}6.{RESET} Проверка обновлений ({update_val})')
            print(f'     {BBLACK}Ускоряет загрузку меню, но не рекомендуем выключать без необходимости\n')
            
            print(f'  {BRED}7.{RESET} Следующая страница')
            print(f'     {BBLACK}Перейти на третью страницу настроек\n')

            print(f'  {BRED}8.{RESET} Назад')
            print(f'     {BBLACK}Вернуться на предыдущую страницу{RESET}\n')

            print(f' {BBLACK}Для переключения параметров Вкл/Выкл просто введите номер{RESET}') #\n Если окно приложения слишком мелкое - увеличьте его или листайте это меню{RESET}')

            settings_choose = input(f'\n > {BRED}')

            if settings_choose == '1':
                
                try:
                    clear()
                    shutdown_timeout_val = int(input(f'{RESET}Введите через сколько минут после конференции выключать ПК:\n\n > {BRED}'))
                    setConfig("shutdown_timeout", shutdown_timeout_val)
                    appendLog(f'Changed option "shutdown_timeout" to {getConfig("shutdown_timeout")}')
                    continue
                    
                except:
                    clear()
                    print(f'{RESET}Нужно использовать целое число.')
                    time.sleep(2)
                    continue
                    
                continue

            elif settings_choose == '2':
                
                if sysname == 'windows':
                
                    try:
                        clear()
                        start_value = input(f'{RESET}Введите комбинацию клавиш для начала записи OBS:\nЭта комбинация должна быть идентична оной в самом OBS!\n\n > {YELLOW}')
                        setConfig("start", start_value)
                        appendLog(f'Changed option "start" to {getConfig("start")}')
                        continue
                        
                    except:
                        clear()
                        print(f'{RESET}Нужно использовать комбинацию клавиш в виде текста.')
                        time.sleep(2)
                        continue
                    
                clear()
                continue

            elif settings_choose == '3':
                
                if sysname == 'windows':
                
                    try:
                        clear()
                        stop_value = input(f'{RESET}Введите комбинацию клавиш для остановки записи OBS:\nЭта комбинация должна быть идентична оной в самом OBS!\n\n > {YELLOW}')
                        setConfig("stop", stop_value)
                        appendLog(f'Changed option "stop" to {getConfig("stop")}')
                        continue
                        
                    except:
                        clear()
                        print(f'{RESET}Нужно использовать комбинацию клавиш в виде текста.')
                        time.sleep(2)
                        continue
                        
                clear()
                continue

            elif settings_choose == '4':
                    
                setConfig("telegram_enabled", not getConfig("telegram_enabled"))
                appendLog(f'Changed option "telegram_enabled" to {getConfig("telegram_enabled")}')
                
                clear()
                continue

            elif settings_choose == '5':
            
                clear()
                print(f'{RESET}Пожалуйста, прочтите инструкцию по установке Telegram бота в {BRED}README.txt{RESET}')
                print(f'или в документации/инструкции что в разделе {CYAN}Помощь{RESET} главного меню')
                print(f'чтобы хорошо понимать что сейчас от вас нужно.')
                none = input('\n > ')
                
                while True:
                    clear()
                    
                    try:
                        telegram_send.configure(files_folder+'telegram.conf', channel=False, group=False, fm_integration=False)
                        break
                        
                    except:
                        clear()
                        continue
                        
                    telegram_send.send(messages=[f"🎊 Конфигурация правильна, всё работает!"], parse_mode="markdown", conf=f"{files_folder}telegram.conf")
                    appendLog('Telegram Send successfully configured')
                    clear()
                    
                continue

            elif settings_choose == '6':
                setConfig("update_check", not getConfig("update_check"))
                appendLog(f'Changed option "update_check" to {getConfig("update_check")}')
                
                clear()
                continue

            elif settings_choose == '7':
                appendLog('Going to settings page 3')
                clear()
                settings3()

            elif settings_choose == '8':
                appendLog('Returned to settings page 1')
                clear()
                return
                
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return


def settings3():
    appendLog('Settings page 3 opened')
    
    try:
        while True:
            
            setTitle("AutoZoom (Настройки)", sysname)
            clear()
                
            if getConfig("write_logs"):
                logs_val = f'{BGREEN}Вкл.{RESET}'
            elif not getConfig("write_logs"):
                logs_val = f'{BRED}Выкл.{RESET}'
            else:
                logs_val = f'{BRED}ERROR{RESET}'
             
            shutdown_time_val = getConfig("shutdown_timeout")
            start_val = getConfig("start")
            stop_val = getConfig("stop")
            
            print(f'{RESET}{BBLACK}»{RESET} Настройки (3 стр.)\n')

            print(f'  {BRED}1.{RESET} Запись действий в лог ({logs_val})')
            print(f'     {BBLACK}Запись каждого действия в файл для отладки (не выключайте без причин)\n')

            print(f'  {BRED}2.{RESET} Размер лога действий ({YELLOW}{str(getConfig("log_size"))} Кб{RESET})')
            print(f'     {BBLACK}Размер файла лога превышая который он будет упакован в архив\n')

            print(f'  {BRED}3.{RESET} Добавить в автозапуск')
            print(f'     {BBLACK}{winOnly(BRED, BBLACK, sysname, end=" ")}Автоматически запускать демона при входе в систему\n')

            print(f'  {BRED}4.{RESET} Сбросить все настройки')
            print(f'     {BBLACK}Восстановить настройки по умолчанию\n')

            print(f'  {BRED}5.{RESET} Назад')
            print(f'     {BBLACK}Вернуться на предыдущую страницу{RESET}\n')

            print(f' {BBLACK}Для переключения параметров Вкл/Выкл просто введите номер{RESET}') #\n Если окно приложения слишком мелкое - увеличьте его или листайте это меню{RESET}')
            settings_choose = input(f'\n > {BRED}')

            if settings_choose == '1':
                setConfig("write_logs", not getConfig("write_logs"))
                appendLog(f'Changed option "write_logs" to {getConfig("write_logs")}')

            if settings_choose == '2':
                
                try:
                    clear()
                    log_size_value = int(input(f'{RESET}Введите после скольки килобайт архивировать лог:\n\n > {BRED}'))
                    setConfig("log_size", log_size_value)
                    continue
                except:
                    clear()
                    print(f'{RESET}Нужно использовать целое число.')
                    time.sleep(2)
                    continue
                    
                appendLog(f'Changed option "log_size" to {getConfig["log_size"]}')
                continue

            if settings_choose == '3':
            
                if sysname == "windows":
                
                    global swl 
                    
                    try:
                        clear()
                        
                        shutil.copyfile('daemon.bat', 'startdaemon.bat')
                        
                        with open('startdaemon.bat', 'r') as f :
                            filedata = f.read()
                            filedata = filedata.replace('python daemon.py', f'python {path}\\daemon.py')
                        
                        with open('startdaemon.bat', 'w') as f:
                            f.write(filedata)
                            f.close()

                        swl.create_lnk(f'{path}\\startdaemon.bat', f'{pathlib.Path.home()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\AutoZoomDaemon.lnk')
                        appendLog('Autorun script added')
                        
                        none = input(f'Демон AutoZoom был добавлен в автозапуск.\nПуть: {BRED}{pathlib.Path.home()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\AutoZoomDaemon.lnk{RESET}\n\n > ')
                        continue
                        
                    except Exception as exp:
                        clear()
                        none = input(f'Не удалось добавить в автозапуск:\n{BRED}{exp}{RESET}\n\n > ')
                        appendLog(f'Could not add autorun: {exp}')
                        continue
                        
                    continue
                    
                else:
                    continue

            elif settings_choose == '4':
                appendLog('Resetting configuration')
            
                while True:
                    clear()
                    reset_decision = input(f'{RESET}Вы уверены что хотите сбросить настройки? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n\n{BRED}Внимание!{RESET} Это действие нельзя обратить!\nВаш список конференций затронут НЕ будет.\n\n > ')

                    if reset_decision.lower() in yes_list:
                    
                        from functions import default_config
                        
                        saveJson(files_folder+'config.json', default_config)
                        appendLog('Configuration dropped to default')
                        clear()
                        
                        none = input(f'{RESET}Все настройки были сброшены до стандартных.\n\n > ')
                        
                        clear()
                        break
                        
                    elif reset_decision.lower() in no_list:
                        appendLog('Configuration reset aborted')
                        clear()
                        break
                        
                    else:
                        clear()
                        continue
                        
                    continue
                    
                clear()
                continue

            elif settings_choose == '5':
                appendLog('Returned to settings page 2')
                clear()
                return
                
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return