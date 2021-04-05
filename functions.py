# -*- coding: utf-8 -*-

import pip
import json
import os
from pathlib import Path

path = Path(__file__).resolve().parent
sounds_folder = str(Path(str(path)+"/sounds/")) + os.sep
files_folder = str(Path(str(path)+"/files/")) + os.sep

def getConfig(some_var):
    global files_folder

    if os.path.exists(files_folder):
        if not os.path.exists(files_folder+'config.json'):
            temp_config_list = {}
            temp_config_list["debug"] = False
            temp_config_list["shutdown_timeout"] = 30
            temp_config_list["shutdown_enabled"] = True
            temp_config_list["start"] = "shift+f7"
            temp_config_list["stop"] = "shift+f8"
            temp_config_list["telegram_enabled"] = False
            temp_config_list["use_colors"] = True
            temp_config_list["run_fullscreen"] = False
            temp_config_list["use_rpc"] = True
            temp_config_list["sounds"] = True
            temp_config_list["end_mode"] = "shutdown"
            temp_config_list["obs_exe"] = None
            temp_config_list["obs_core"] = None
            saveJson(files_folder+'config.json', temp_config_list)
            return temp_config_list[some_var]
        else:
            try:
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                    return config_list[some_var]
            except:
                return "Error"
    else:
        os.mkdir(files_folder)
        if not os.path.exists(files_folder+'config.json'):
            temp_config_list = {}
            temp_config_list["debug"] = False
            temp_config_list["shutdown_timeout"] = 30
            temp_config_list["shutdown_enabled"] = True
            temp_config_list["start"] = "shift+f7"
            temp_config_list["stop"] = "shift+f8"
            temp_config_list["telegram_enabled"] = False
            temp_config_list["use_colors"] = True
            temp_config_list["run_fullscreen"] = False
            temp_config_list["use_rpc"] = True
            temp_config_list["sounds"] = True
            temp_config_list["end_mode"] = "shutdown"
            temp_config_list["obs_exe"] = None
            temp_config_list["obs_core"] = None
            saveJson(files_folder+'config.json', temp_config_list)
            return temp_config_list[some_var]
        else:
            try:
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                    return config_list[some_var]
            except:
                return "Error"



def saveJson(filename, value):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(value, f, indent=4, ensure_ascii=False)
        f.close()