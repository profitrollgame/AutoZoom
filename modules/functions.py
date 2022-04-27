# -*- coding: utf-8 -*-

from socket import send_fds
import time
import json
import os
import shutil
import gzip
import getpass
import keyboard
from modules.telegram import telegramSendText
from datetime import datetime
from pathlib import Path
import asyncio, threading
from subprocess import check_output

path = Path(__file__).resolve().parent
sounds_folder = str(Path(str(path)+"/sounds/")) + os.sep
files_folder = str(Path(str(path)+"/files/")) + os.sep
logs_folder = str(Path(str(path)+"/logs/")) + os.sep

yes_list = ['y', 'yes', 'т', 'так', 'j', 'ja']
no_list = ['n', 'no', 'н', 'ні', 'nein']

default_config = {
    "firstrun": True,
    "debug": False,
    "update_check": True,
    "logging": {
        "enabled": True,
        "rotate_size": 512
    },
    "meetings": {
        "remove_old": True
    },
    "meeting_end": {
        "mode": "shutdown",
        "shutdown": {
            "timeout": 30
        }
    },
    "obs": {
        "enabled": False,
        "path_bin": None,
        "path_core": None,
        "delay": 10,
        "video": {
            "send": False,
            "path": None,
            "filename": None
        },
        "keybinds": {
            "record_start": "shift+f7",
            "record_stop": "shift+f8"
        }
    },
    "telegram": {
        "enabled": False,
        "token": None,
        "user_id": None
    },
    "appearance": {
        "theme": "dark",
        "colors": True,
        "fullscreen": False
    },
    "rpc": {
        "enabled": True,
        "app_id": "800049969960058882"
    },
    "sounds": {
        "enabled": True,
        "sounds": {
            "meeting_ended": "ended",
            "record_start": "recordstart",
            "record_stop": "recordstop",
            "shutdown": "shutdown",
            "meeting_started": "started",
            "meeting_warning": "warning"
        }
    },
    "binds": {
        "app_start": {
            "commands": [],
            "keymaps": [],
            "messages": []
        },
        "app_end": {
            "commands": [],
            "keymaps": [],
            "messages": []
        },
        "queue_start": {
            "commands": [],
            "keymaps": [],
            "messages": []
        },
        "queue_end": {
            "commands": [],
            "keymaps": [],
            "messages": []
        },
        "meeting_start": {
            "commands": [],
            "keymaps": [],
            "messages": []
        },
        "meeting_end": {
            "commands": [],
            "keymaps": [],
            "messages": []
        }
    }
    # "start": "shift+f7",
    # "stop": "shift+f8",
    # "telegram_enabled": False,
    # "use_colors": True,
    # "run_fullscreen": False,
    # "rpc_use": True,
    # "rpc_id": "800049969960058882",
    # "sounds": True,
    # "end_mode": "shutdown",
    # "obs_exe": None,
    # "obs_core": None,
    # "obs_delay": 10,
    # "write_logs": True,
    # "log_size": 512,
    # "sound_ended": "ended",
    # "sound_recordstart": "recordstart",
    # "sound_recordstop": "recordstop",
    # "sound_shutdown": "shutdown",
    # "sound_started": "started",
    # "sound_warning": "warning"
    # "shutdown_timeout": 30,
    # "shutdown_enabled": False,
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


# Импортирование игралки звуков
try:
    if getOS() == "windows":
        import winsound
        from playsound import playsound
    elif getOS() == "unix":
        from playsound import playsound
except:
    pass


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
                with open(logs_folder + 'latest.log', 'rb', encoding='utf-8') as f_in:
                    with gzip.open(f'{logs_folder}{datetime.now().strftime("%d.%m.%Y_%H:%M:%S")}.zip', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                        
                        if getConfig("debug"):
                            print(f'Copied {logs_folder}{datetime.now().strftime("%d.%m.%Y_%H:%M:%S")}.zip')
                
                open(logs_folder + 'latest.log', 'w', encoding='utf-8').close()
            
            i = 2

        except FileNotFoundError:
            if getConfig("debug"):
                print('Log file not found')
                time.sleep(2)
            
            try:
                log = open(logs_folder + 'latest.log', 'a', encoding='utf-8')
                open(logs_folder + 'latest.log', 'a', encoding='utf-8').close()
            except:
                try:
                    os.mkdir(logs_folder)
                    log = open(logs_folder + 'latest.log', 'a', encoding='utf-8')
                    open(logs_folder + 'latest.log', 'a', encoding='utf-8').close()
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
            log = open(logs_folder + 'latest.log', 'a', encoding='utf-8')
            open(logs_folder + 'latest.log', 'a', encoding='utf-8').close()
        except:
            try:
                os.mkdir(logs_folder)
                log = open(logs_folder + 'latest.log', 'a', encoding='utf-8')
                open(logs_folder + 'latest.log', 'a', encoding='utf-8').close()
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


# Функция удаления ненужного мусора из строки
def strCleaner(string):
    
    output = string.replace('"', '\"').replace('\n', '')
    
    appendLog(f"String cleaned: {output}")
    
    return output


# Load json to dict
def jsonLoad(filename):
    """Loads arg1 as json and returns its contents"""
    with open(filename, "r", encoding='utf8') as file:
        output = json.load(file)
        file.close()
    return output

# Save json dict to filename
def jsonSave(contents, filename):
    """Dumps dict/list arg1 to file arg2"""
    with open(filename, "w", encoding='utf8') as file:
        json.dump(contents, file, ensure_ascii=False, indent=4)
        file.close()
    return


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
                        appendLog(f'Changed variable "{some_var}" to {some_val}')
                        
                    except:
                    
                        try:
                            repairConfig(config_list)
                            config_list = json.load(json_file)
                            json_file.close()
                            config_list[some_var] = some_val
                            saveJson(files_folder+'config.json', config_list)
                            appendLog(f'Changed variable "{some_var}" to {some_val}')
                            
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
                            appendLog(f'Changed variable "{some_var}" to {some_val}')
                            
                        except:
                            config_list[some_var] = some_val
                            saveJson(files_folder+'config.json', config_list)
                            appendLog(f'Changed variable "{some_var}" to {some_val}')
                
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
                            try:
                                setConfig(some_var, default_config[some_var])
                                return default_config[some_var]
                            except:
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

# Fire some function
_loop = None
def fire_and_forget(coro):
    global _loop
    if _loop is None:
        _loop = asyncio.new_event_loop()
        threading.Thread(target=_loop.run_forever, daemon=True).start()
    _loop.call_soon_threadsafe(asyncio.create_task, coro)


def configSet(key: str, value, *args: str):
    """Set key to a value

    Args:
        * key (str): The last key of the keys path.
        * value (str/int/float/list/dict/None): Some needed value.
        * *args (str): Path to key like: dict[args][key].
    """    
    this_dict = jsonLoad(f"{files_folder}config.json")
    string = "this_dict"

    for arg in args:
        string += f'["{arg}"]'

    if type(value) in [str]:
        string += f'["{key}"] = "{value}"'
    else:
        string += f'["{key}"] = {value}'

    exec(string)
    jsonSave(this_dict, f"{files_folder}config.json")
    return

def configGet(key: str, *args: str):
    """Get value of the config key

    Args:
        * key (str): The last key of the keys path.
        * *args (str): Path to key like: dict[args][key].

    Returns:
        * any: Value of provided key
    """    
    this_dict = jsonLoad(f"{files_folder}config.json")
    this_key = this_dict
    for dict_key in args:
        this_key = this_key[dict_key]
    return this_key[key]

async def execBind(action: str, kind="command"):
    """Execute binded action

    Args:
        * action (str): Bind, command or message.
        * kind (str, optional): "keybind", "command" or "message". Defaults to "command".
    """
    if kind == "message":
        telegramSendText(message=action)
    elif kind == "keybind":
        keyboard.press_and_release(action)
    else:
        os.system(action)
    return