# -*- coding: utf-8 -*-

import pip
import time
import json
import os
import shutil
import gzip
import getpass
from datetime import datetime
from pathlib import Path
from subprocess import check_output

path = Path(__file__).resolve().parent
sounds_folder = str(Path(str(path)+"/sounds/")) + os.sep
files_folder = str(Path(str(path)+"/files/")) + os.sep
logs_folder = str(Path(str(path)+"/logs/")) + os.sep

yes_list = ['y', 'yes', 'д', 'да']
no_list = ['n', 'no', 'н', 'нет']

default_config = {
            "firstboot": True,
            "debug": False,
            "shutdown_timeout": 30,
            "shutdown_enabled": False,
            "start": "shift+f7",
            "stop": "shift+f8",
            "telegram_enabled": False,
            "use_colors": True,
            "run_fullscreen": False,
            "use_rpc": True,
            "sounds": True,
            "end_mode": "shutdown",
            "obs_exe": None,
            "obs_core": None,
            "update_check": True,
            "write_logs": True,
            "log_size": 512
    }


# Функция возвращающая надпись Windows Only
def winOnly(color, reset, system, start='', end=''):

    if system != 'windows':
        return f"{start}{color}Только для Windows!{reset}{end}"
        
    else:
        return ""


# Функция возвращающая тип ОС
def getOS():

    if os.name == 'nt':
        return "windows"
        
    elif 'android' in str(check_output('uname -a', shell=True).lower()):
        return "android"
        
    else:
        return "unix"


# Функция отвечает за очищение командной строки
if getOS() == "windows":
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')


# Установка заголовка окна cmd.exe
def setTitle(title, system):
    if system == "windows":
        try:
            os.system(f"title {title}")
        except:
            pass


# Получить номер дня недели
def getDayNum(day):
    output = datetime.strptime(day, "%d.%m.%Y").isoweekday()
    return output


# Функция проверки размера файла
def checkSize():
    global logs_folder
    
    i = 0

    while i < 2:
        try:
            log = os.stat(logs_folder + 'latest.log')

            if (log.st_size / 1024) > getConfig("log_size"):
                with open(logs_folder + 'latest.log', 'rb') as f_in:
                    with gzip.open(f'{logs_folder}{datetime.now().strftime("%d.%m.%Y_%H:%M:%S")}.zip', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                        
                        if getConfig("debug"):
                            print(f'Copied {logs_folder}{datetime.now().strftime("%d.%m.%Y_%H:%M:%S")}.zip')
                            
                open(logs_folder + 'latest.log', 'w').close()
                
            i = 2

        except FileNotFoundError:
            if getConfig("debug"):
                print('Log file not found')
                time.sleep(2)
            
            try:
                log = open(logs_folder + 'latest.log', 'a')
                open(logs_folder + 'latest.log', 'a').close()
            except:
                try:
                    os.mkdir(logs_folder)
                    log = open(logs_folder + 'latest.log', 'a')
                    open(logs_folder + 'latest.log', 'a').close()
                except:
                    if getConfig("debug"):
                        time.sleep(2)
                        print('Log file could not be created')
            
            i += 1


# Функция добавления в лог
def appendLog(message, startup=False, shutdown=False):

    if getConfig("write_logs"):
    
        global logs_folder

        checkSize()

        try:
            log = open(logs_folder + 'latest.log', 'a')
            open(logs_folder + 'latest.log', 'a').close()
        except:
            try:
                os.mkdir(logs_folder)
                log = open(logs_folder + 'latest.log', 'a')
                open(logs_folder + 'latest.log', 'a').close()
            except:
                time.sleep(2)
                print('Log file could not be created')
                
        if startup:
            log.write(f'[{datetime.now().strftime("%H:%M:%S | %d.%m.%Y")}] [STARTUP] {message}\n')
        elif shutdown:
            log.write(f'[{datetime.now().strftime("%H:%M:%S | %d.%m.%Y")}] [SHUTDOWN] {message}\n')
        else:
            log.write(f'[{datetime.now().strftime("%H:%M:%S | %d.%m.%Y")}] {message}\n')
            
        log.close()


# Функция проигрывания звука
def playSound(soundname, timing=''):

    global sysname

    if getConfig("sounds"):
    
        if getOS() == "windows":
        
            try:
                winsound.PlaySound(sounds_folder+soundname+".wav", winsound.SND_FILENAME)
                
            except Exception as exp:
                appendLog(f'Could not play winsound: {exp}')
                
                if getConfig("debug"):
                    print(f'{timing} Не удалось проиграть winsound звук "{soundname}" (Ошибка: {exp})')
                
                try:
                    playsound(sounds_folder+soundname+".wav")
                    
                except Exception as exp:
                    appendLog(f'Could not play playsound: {exp}')
                    
                    if getConfig("debug"):
                        print(f'{timing} Не удалось проиграть playsound звук "{soundname}" (Ошибка: {exp})')
                        
        elif getOS() == "android":
        
            try:
                os.system(f'play-audio {sounds_folder}{soundname}.wav')
                
            except Exception as exp:
                appendLog(f'Could not play play-audio: {exp}')
                    
        else:
        
            try:
                playsound(sounds_folder+soundname+".wav")
                
            except Exception as exp:
                appendLog(f'Could not play playsound: {exp}')
                
                if getConfig("debug"):
                    print(f'{timing} Не удалось проиграть playsound звук "{soundname}" (Ошибка: {exp})')


# Функция добавления переменных, если их нет
def repairConfig(some_dic):

    global files_folder
    global default_config
    
    for key in default_config:
    
        try:
            some_dic[key]
            
        except KeyError:
            some_dic[key] = default_config[key]
            saveJson(files_folder+'config.json', some_dic)


# Функция изменения переменной конфигурации
def setConfig(some_var, some_val):

    global files_folder
    global default_config

    if os.path.exists(files_folder):
    
        if not os.path.exists(files_folder+'config.json'):
        
            temp_config_list = default_config
            temp_config_list[some_var] = some_val
            
            saveJson(files_folder+'config.json', temp_config_list)
            
        else:
        
            try:
            
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                
                    config_list = json.load(json_file)
                    json_file.close()
                    
                    try:
                        config_list[some_var] = some_val
                        saveJson(files_folder+'config.json', config_list)
                        appendLog(f'Changed variable "{somevar}" to {some_val}')
                        
                    except:
                    
                        try:
                            repairConfig(config_list)
                            config_list = json.load(json_file)
                            json_file.close()
                            config_list[some_var] = some_val
                            saveJson(files_folder+'config.json', config_list)
                            appendLog(f'Changed variable "{somevar}" to {some_val}')
                            
                        except:
                            pass
            except:
            
                return "Error"
    else:
        os.mkdir(files_folder)
        
        if not os.path.exists(files_folder+'config.json'):
        
            temp_config_list = default_config
            temp_config_list[some_var] = some_val
            
            saveJson(files_folder+'config.json', temp_config_list)
            
        else:
        
            try:
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                
                    config_list = json.load(json_file)
                    json_file.close()
                    
                    try:
                        config_list[some_var] = some_val
                        saveJson(files_folder+'config.json', config_list)
                        
                    except:
                    
                        try:
                            repairConfig(config_list)
                            config_list = json.load(json_file)
                            json_file.close()
                            config_list[some_var] = some_val
                            saveJson(files_folder+'config.json', config_list)
                            appendLog(f'Changed variable "{somevar}" to {some_val}')
                            
                        except:
                            config_list[some_var] = some_val
                            saveJson(files_folder+'config.json', config_list)
                            appendLog(f'Changed variable "{somevar}" to {some_val}')
                            
            except:
                return "Error"


# Функция получения переменной конфигурации
def getConfig(some_var):

    global files_folder
    global default_config

    if os.path.exists(files_folder):
    
        if not os.path.exists(files_folder+'config.json'):
            temp_config_list = default_config
            
            saveJson(files_folder+'config.json', temp_config_list)
            return temp_config_list[some_var]
            
        else:
            try:
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                
                    config_list = json.load(json_file)
                    json_file.close()
                    
                    try:
                        return config_list[some_var]
                        
                    except:
                        try:
                            repairConfig(config_list)
                            config_list = json.load(json_file)
                            json_file.close()
                            return config_list[some_var]
                        except:
                            return default_config[some_var]
            except:
                return "Error"
    else:
        os.mkdir(files_folder)
        if not os.path.exists(files_folder+'config.json'):
            temp_config_list = default_config
            
            saveJson(files_folder+'config.json', temp_config_list)
            return temp_config_list[some_var]
        else:
        
            try:
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                    
                    try:
                        return config_list[some_var]
                        
                    except:
                        try:
                            repairConfig(config_list)
                            config_list = json.load(json_file)
                            json_file.close()
                            return config_list[some_var]
                            
                        except:
                            return default_config[some_var]   
            except:
                return "Error"


# Получить статус процесса
def getState(process="CptHost.exe"):

    if getOS() == 'windows':
    
        try:
            output = os.popen(f'tasklist /fi "IMAGENAME eq {process}" /fi "USERNAME ne NT AUTHORITY\{getpass.getuser()}"').read()
            
            if process in output:
                return True
            else:
                return False
                    
        except Exception as exp:
            appendLog(f'Failed to get state using tasklist: {exp}')
            
            output = os.popen('wmic process get description, processid').read()
            
            if "CptHost.exe" in output:
                return True
            else:
                return False


# Функция сохранения информации в json файл
def saveJson(filename, value):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(value, f, indent=4, ensure_ascii=False)
        f.close()