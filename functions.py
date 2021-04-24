# -*- coding: utf-8 -*-

import pip
import time
import json
import os
import shutil
import gzip
from datetime import datetime
from pathlib import Path

path = Path(__file__).resolve().parent
sounds_folder = str(Path(str(path)+"/sounds/")) + os.sep
files_folder = str(Path(str(path)+"/files/")) + os.sep
logs_folder = str(Path(str(path)+"/logs/")) + os.sep


default_config = {
            "debug": False,
            "shutdown_timeout": 30,
            "shutdown_enabled": True,
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
def appendLog(message):

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
                
        log.write(f'[{datetime.now().strftime("%H:%M:%S | %d.%m.%Y")}] {message}\n')
        log.close()


# Функция добавления переменных, если их нет
def repairConfig(some_dic):
    global files_folder
    global default_config
    
    for key in some_dic:
        try:
            some_dic[key]
        except NameError:
            some_dic[key] = default_config[key]
            
            saveJson(files_folder+'config.json', some_dic)
   

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


def saveJson(filename, value):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(value, f, indent=4, ensure_ascii=False)
        f.close()