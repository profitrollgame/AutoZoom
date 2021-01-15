# -*- coding: utf-8 -*-

import subprocess
import time
import datetime
import os
import pip
import pathlib
import json
import getopt
import sys
import winsound
from random import randint
from pathlib import Path
from datetime import datetime, date, timedelta

path = Path(__file__).resolve().parent
sounds_folder = str(Path(str(path)+"/sounds/")) + os.sep
files_folder = str(Path(str(path)+"/files/")) + os.sep

def saveJson(filename, value):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(value, f, indent=4, ensure_ascii=False)

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
            saveJson(files_folder+'config.json', temp_config_list)
        else:
            try:
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    return config_list[some_var]
            except:
                return "Error"
    else:
        os.mkdir(files_folder)

def install(package, first_class=None, second_class=None):
    try:
        from config import debug
    except:
        debug = False

    try:
        exec(f"{package} = __import__('{package}')")
        globals()[package] = __import__(package)
        if getConfig("debug"):
            print(f'[OK] Импортирован модуль "{package}"')
    except:
        print(f'Trying to import package {package}')
        if hasattr(pip, 'main'): 
            pip.main(['install', package])
            print(f'[OK] Установлен модуль "{package}"')
            try:
                exec(f"{package} = __import__('{package}')")
                globals()[package] = __import__(package)
            except ModuleNotFoundError:
                none = input('Упс, модуль ещё не готов...')
                print('Упс, модуль ещё не готов...')
            if getConfig("debug"):
                print(f'[OK] Импортирован модуль "{package}"')
        else: 
            pip._internal.main(['install', package])
            print(f'[OK] Установлен модуль "{package}"')
            exec(f"{package} = __import__('{package}')")
            globals()[package] = __import__(package)
            if getConfig("debug"):
                print(f'[OK] Импортирован модуль "{package}"')

install('easygui')
install('tkinter')
install('keyboard')
install('ast')
install('telegram_send')
install('inputimeout')

#telegram_send.send(messages=[f"I'm alive"], parse_mode="markdown")#, conf=f"{files_folder}telegram.conf")

menu_choose = None

try:
    from inputimeout import inputimeout, TimeoutOccurred
except:
    print(f'[WARN] Не удалось импортировать классы "inputimeout" и "TimeoutOccurred" из модуля "inputimeout"')

if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

def nowtime(seconds=True, noice=True):
    now = datetime.now()
    if seconds == True:
        justnow = now.strftime("%H:%M:%S")
    else:
        justnow = now.strftime("%H:%M")
    
    if noice == True:
        beautiful = f'[{justnow}]'
    else:
        beautiful = justnow
        
    return beautiful

def act(x):
    return x+10

def waitStart(runTime, action):
    from datetime import datetime, time
    from time import sleep

    startTime = time(*(map(int, runTime.split(':'))))
    while startTime > datetime.today().time():
        sleep(2)
    return action

def getPair(line):
    key, sep, value = line.strip().partition(" ")
    return int(key), value

def getLessons():
    if not os.path.exists(files_folder+'lessons.json'):
        with open(files_folder+'lessons.json', 'w', encoding="utf-8") as f:
            f.write("[]")
            lessons_list = []
    else:
        with open(files_folder+'lessons.json', encoding="utf-8") as json_file:
            lessons_list = json.load(json_file)
            
    return lessons_list

def getState():
    output = os.popen('wmic process get description, processid').read()
    if "CptHost.exe" in output:
        return True
    else:
        return False

def listLessons(from_where='remove'):
    try:
        if from_where == 'editor':
            print('Полный список запланированных конференций:\n')

        print('================================================')
        for les in enumerate(getLessons()):
        
            if les[1]["repeat"]:
                repeat = 'Вкл.'
            else:
                repeat = 'Выкл.'
                
            if les[1]["record"]:
                record = 'Вкл.'
            else:
                record = 'Выкл.'
        
            try:
                repeat_day = getDay(les[1]["repeat_day"])
            except:
                repeat_day = 'Не повторяется'
                
            length = len(str(les[0]))
            
            spacer_all = 6 * ' ' #(4+length) * ' '
            spacer_ind = (5 - length) * ' ' #(len(str(les[0]))-1)*' '
            
            # print(5 - length)
            # print(f'length = "{length}"')
            # print(f'spacer_all = "{spacer_all}"')
            # print(f'spacer_ind = "{spacer_ind}"')
        
            print(f'{spacer_all}Имя:    {les[1]["name"]}\n{spacer_all}Дата:   {les[1]["date"]}\n{spacer_all}Время:  {les[1]["time"]}\n {les[0]}{spacer_ind}Ссылка: {les[1]["link"]}\n{spacer_all}Повтор: {repeat}\n{spacer_all}День:   {repeat_day}\n{spacer_all}Запись: {record}\n================================================')

        if from_where == 'editor':
            none = input('\n\n > ')
    except KeyboardInterrupt:
        clear()
        return

def sortLessons(dictionary):
    dictionary.sort(key = lambda x: datetime.strptime(x['time'], '%H:%M'))
    dictionary.sort(key = lambda x: datetime.strptime(x['date'], '%d.%m.%Y')) 

def getDayNum(day):
    output = datetime.strptime(day, "%d.%m.%Y").isoweekday()
    return output

def getDay(number):
    if number == 1:
        return 'Понедельник'
    if number == 2:
        return 'Вторник'
    if number == 3:
        return 'Среда'
    if number == 4:
        return 'Четверг'
    if number == 5:
        return 'Пятница'
    if number == 6:
        return 'Суббота'
    if number == 7:
        return 'Воскресенье'

# def repeatLesson():

def addLesson():
    try:
        local_lessons = {}
        lessons_got = getLessons()

        lessname = input('Введите (своё) имя конференции:\n\n > ')
        local_lessons.update({"name": lessname})
        
        while True:
            clear()
            today = date.today()
            today_1 = date.today() + timedelta(days=1)
            today_2 = date.today() + timedelta(days=2)
            today_3 = date.today() + timedelta(days=3)
            today_4 = date.today() + timedelta(days=4)
            today_5 = date.today() + timedelta(days=5)
            today_6 = date.today() + timedelta(days=6)
            
            print(f'Введите дату конференции (дд.мм.гггг)\nили же просто номер для дней ниже:\n')
            print(f'1. {today.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'2. {today_1.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_1.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'3. {today_2.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_2.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'4. {today_3.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_3.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'5. {today_4.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_4.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'6. {today_5.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_5.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'7. {today_6.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_6.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            
            try:
                lessdate = input('\n > ')
                if lessdate == '':
                    finallessdate = lessons_got[edi]["date"]
                elif lessdate == '1':
                    finallessdate = today.strftime("%d.%m.%Y")
                elif lessdate == '2':
                    finallessdate = today_1.strftime("%d.%m.%Y")
                elif lessdate == '3':
                    finallessdate = today_2.strftime("%d.%m.%Y")
                elif lessdate == '4':
                    finallessdate = today_3.strftime("%d.%m.%Y")
                elif lessdate == '5':
                    finallessdate = today_4.strftime("%d.%m.%Y")
                elif lessdate == '6':
                    finallessdate = today_5.strftime("%d.%m.%Y")
                elif lessdate == '7':
                    finallessdate = today_6.strftime("%d.%m.%Y")
                else:
                    try:
                        test = (datetime.strptime(lessdate, "%d.%m.%Y"))
                        finallessdate = lessdate
                    except:
                        continue
                    
                local_lessons.update({"date": finallessdate})
                    
                break
            except:
                continue
         
        while True:
            clear()
            try:
                lesstime = input('Введите время конференции (чч:мм):\n\n > ')
                finallesstime = (datetime.strptime(lesstime, "%H:%M"))
                local_lessons.update({"time": lesstime})
                break
            except:
                continue
        
        clear()
        lesslink = input('Введите ссылку на конференцию:\n\n > ')
        local_lessons.update({"link": lesslink})
        
        while True:
            clear()
            repeat = input(f'Повторять эту конференцию ({getDay(getDayNum(finallessdate))})? (Да/Нет)\n\n > ')
            
            if repeat.lower() in ['y', 'yes', 'д', 'да']:
                finalrepeat = True
                finalrepeatday = getDayNum(finallessdate)
                local_lessons.update({"repeat": finalrepeat})
                local_lessons.update({"repeat_day": finalrepeatday})
                break
            elif repeat.lower() in ['n', 'no', 'н', 'нет']:
                finalrepeat = False
                finalrepeatday = None
                local_lessons.update({"repeat": finalrepeat})
                local_lessons.update({"repeat_day": finalrepeatday})
                break
            else:
                continue
        
        while True:
            clear()
            lessrecord = input('Записать эту конференцию? (Да/Нет)\n\n > ')
            
            if lessrecord.lower() in ['y', 'yes', 'д', 'да']:
                finallessrecord = True
                local_lessons.update({"record": finallessrecord})
                break
            elif lessrecord.lower() in ['n', 'no', 'н', 'нет']:
                finallessrecord = False
                local_lessons.update({"record": finallessrecord})
                break
            else:
                continue
                
        
        lessons_got.append(dict(local_lessons))
        sortLessons(lessons_got)
        saveJson(files_folder+'lessons.json', lessons_got)
        
        clear()
        print(f'Добавлен урок "{local_lessons["name"]}" за {local_lessons["date"]} на время {local_lessons["time"]}.')
        none = input('\n > ')
    except KeyboardInterrupt:
        clear()
        return
    

def editLesson():
    try:
        local_lessons = {}
        lessons_got = getLessons()
        
        while True:
            print('Выберите номер (индекс) для изменения:\n')
            listLessons()
            lessons_got = getLessons()
            
            print('Для отмены операции введите "c" или "cancel"')
            
            edi = input('\n > ')
            
            if not isinstance(edi, int):
                if edi.lower() == 'c' or edi.lower() == 'cancel':
                    clear()
                    return
                try:
                    edi = int(edi)
                except:
                    clear()
                    continue
                
            try:
                probe = lessons_got[edi]["name"]
                break
            except:
                clear()
                print('Выберите правильный индекс (номер) для изменения.')
                time.sleep(3)
                clear()
                continue
                
            break

        clear()
        lessname = input(f'Введите (своё) имя конференции:\n(Оригинальное имя: "{lessons_got[edi]["name"]}")\n\n > ')
        if lessname == '':
            lessname = lessons_got[edi]["name"]
        local_lessons.update({"name": lessname})
        
        while True:
            clear()
            today = date.today()
            today_1 = date.today() + timedelta(days=1)
            today_2 = date.today() + timedelta(days=2)
            today_3 = date.today() + timedelta(days=3)
            today_4 = date.today() + timedelta(days=4)
            today_5 = date.today() + timedelta(days=5)
            today_6 = date.today() + timedelta(days=6)
            
            print(f'Введите дату конференции (дд.мм.гггг)\nили же просто номер для дней ниже:\n(Оригинальная дата: "{lessons_got[edi]["date"]}")\n')
            print(f'1. {today.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'2. {today_1.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_1.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'3. {today_2.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_2.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'4. {today_3.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_3.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'5. {today_4.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_4.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'6. {today_5.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_5.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            print(f'7. {today_6.strftime("%d.%m.%Y")} ({getDay(datetime.strptime(today_6.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())})')
            
            try:
                lessdate = input('\n > ')
                if lessdate == '':
                    finallessdate = lessons_got[edi]["date"]
                elif lessdate == '1':
                    finallessdate = today.strftime("%d.%m.%Y")
                elif lessdate == '2':
                    finallessdate = today_1.strftime("%d.%m.%Y")
                elif lessdate == '3':
                    finallessdate = today_2.strftime("%d.%m.%Y")
                elif lessdate == '4':
                    finallessdate = today_3.strftime("%d.%m.%Y")
                elif lessdate == '5':
                    finallessdate = today_4.strftime("%d.%m.%Y")
                elif lessdate == '6':
                    finallessdate = today_5.strftime("%d.%m.%Y")
                elif lessdate == '7':
                    finallessdate = today_6.strftime("%d.%m.%Y")
                else:
                    try:
                        test = (datetime.strptime(lessdate, "%d.%m.%Y"))
                        finallessdate = lessdate
                    except:
                        continue
                    
                local_lessons.update({"date": finallessdate})
                    
                break
            except:
                continue
         
        while True:
            clear()
            try:
                lesstime = input(f'Введите время конференции (чч:мм):\n(Оригинальное время: "{lessons_got[edi]["time"]}")\n\n > ')
                
                if lesstime == '':
                    finallesstime = lessons_got[edi]["time"]
                    lesstime = lessons_got[edi]["time"]
                else:
                    try:
                        finallesstime = (datetime.strptime(lesstime, "%H:%M"))
                    except:
                        continue
                
                local_lessons.update({"time": lesstime})
                break
            except:
                continue
        
        clear()
        lesslink = input(f'Введите ссылку на конференцию\n(Оригинальная ссылка: "{lessons_got[edi]["link"]}")\n\n > ')
        
        if lesslink == '':
            lesslink = lessons_got[edi]["link"]
        local_lessons.update({"link": lesslink})
        
        while True:
            clear()
            repeat = input(f'Повторять эту конференцию ({getDay(getDayNum(finallessdate))})? (Да/Нет)\n(Оригинальное значение: "{getDay(lessons_got[edi]["repeat_day"])}")\n\n > ')
            
            if repeat.lower() in ['y', 'yes', 'д', 'да']:
                finalrepeat = True
                finalrepeatday = getDayNum(finallessdate)
                local_lessons.update({"repeat": finalrepeat})
                local_lessons.update({"repeat_day": finalrepeatday})
                break
            elif repeat.lower() in ['n', 'no', 'н', 'нет']:
                finalrepeat = False
                local_lessons.update({"repeat": finalrepeat})
                break
            elif repeat == '':
                finalrepeat = lessons_got[edi]["repeat"]
                local_lessons.update({"repeat": finalrepeat})
                try:
                    finalrepeatday = lessons_got[edi]["repeat_day"]
                    local_lessons.update({"repeat_day": finalrepeatday})
                except:
                    pass
                break
            else:
                continue
        
        while True:
            clear()
            lessrecord = input(f'Записать эту конференцию? (Да/Нет)\n(Оригинальное значение: "{lessons_got[edi]["record"]}")\n\n > ')
            
            if lessrecord.lower() in ['y', 'yes', 'д', 'да']:
                finallessrecord = True
                local_lessons.update({"record": finallessrecord})
                break
            elif lessrecord.lower() in ['n', 'no', 'н', 'нет']:
                finallessrecord = False
                local_lessons.update({"record": finallessrecord})
                break
            elif lessrecord == '':
                finallessrecord = lessons_got[edi]["record"]
                local_lessons.update({"record": finallessrecord})
                break
            else:
                continue
                
        del lessons_got[edi]
        lessons_got.append(dict(local_lessons))
        sortLessons(lessons_got)
        saveJson(files_folder+'lessons.json', lessons_got)
        clear()
        print(f'Изменён урок "{lessname}" за {finallessdate} на время {finallesstime}.')
        none = input('\n > ')
    except KeyboardInterrupt:
        clear()
        return
    

def removeLesson():
    try:
        while True:
            print('Выберите номер (индекс) для удаления:\n')
            listLessons()
            lessons_local = getLessons()
            print('Для отмены операции введите "c" или "cancel"')
            
            rem = input('\n > ')
            
            if rem.lower() == 'c' or rem.lower() == 'cancel':
                clear()
                break
            else:
                try:
                    rem = int(rem)
                except:
                    clear()
                    continue
                
            try:
                del_name = lessons_local[rem]["name"]
                del_date = lessons_local[rem]["date"]
                del_time = lessons_local[rem]["time"]
                del lessons_local[rem]
            except:
                clear()
                print('Выберите правильный индекс (номер) для удаления.')
                time.sleep(3)
                clear()
                continue
                
            sortLessons(lessons_local)
            saveJson(files_folder+'lessons.json', lessons_local)
            clear()
            print(f'Удалён урок "{del_name}" за {del_date} на время {del_time}.')
            none = input('\n > ')
            break
    except KeyboardInterrupt:
        clear()
        return

def removeAllLessons():
    try:
        while True:
            clear()
            removeall = input(f'Вы уверены что хотите удалить все конференции? (Да/Нет)\nВнимание! Это действие нельзя обратить!\nВаши настройки затронуты НЕ будут.\n\n > ')
            
            if removeall.lower() in ['y', 'yes', 'д', 'да']:
                with open(files_folder+'lessons.json', 'w', encoding="utf-8") as f:
                    f.write("[]")
                clear()
                none = input('Все уроки были удалены.\n\n > ')
                clear()
                break
            elif removeall.lower() in ['n', 'no', 'н', 'нет']:
                clear()
                break
            else:
                continue
    except KeyboardInterrupt:
        clear()
        return

def editor():
    try:
        from main import mainMenu
        while True:
            clear()
            editor_choose = input('» Меню редактора\n\n1. Добавить урок\n2. Изменить урок\n3. Удалить урок\n4. Посмотреть уроки\n5. Удалить все уроки\n6. В главное меню\n\n > ')
            if editor_choose == '1':
                clear()
                addLesson()
            elif editor_choose == '2':
                clear()
                editLesson()
            elif editor_choose == '3':
                clear()
                removeLesson()
            elif editor_choose == '4':
                clear()
                listLessons(from_where = 'editor')
            elif editor_choose == '5':
                clear()
                removeAllLessons()
            elif editor_choose == '6':
                clear()
                mainMenu()
            else:
                continue
    except KeyboardInterrupt:
        clear()
        return

def tgsend(enabled, message):
    if enabled:
        telegram_send.send(messages=[f"{message}"], parse_mode="markdown", conf=files_folder+"telegram.conf")

def settings():
    try:
        while True:
            clear()
            
            if getConfig("debug"):
                debug_val = 'Вкл.'
            elif not getConfig("debug"):
                debug_val = 'Выкл.'
            else:
                debug_val = 'ERROR'
                
            if getConfig("shutdown_enabled"):
                shutdown_en_val = 'Вкл.'
            elif not getConfig("shutdown_enabled"):
                shutdown_en_val = 'Выкл.'
            else:
                shutdown_en_val = 'ERROR'
                
            if os.path.exists(files_folder+'telegram.conf'):
                tg_var = 'Настроен'
            else:
                tg_var = 'Не настроен'
                
            if getConfig("telegram_enabled"):
                telegram_en_val = 'Вкл.'
            elif not getConfig("debug"):
                telegram_en_val = 'Выкл.'
            else:
                telegram_en_val = 'ERROR'
             
            shutdown_time_val = getConfig("shutdown_timeout")
            start_val = getConfig("start")
            stop_val = getConfig("stop")
            settings_choose = input(f'» Настройки\n\n1. Режим отладки ({debug_val})\n2. Авто выключение ПК ({shutdown_en_val})\n3. Таймаут выключения ПК ({shutdown_time_val} мин.)\n4. Комбинация начала записи OBS ({start_val})\n5. Комбинация остановки записи OBS ({stop_val})\n6. Telegram бот ({telegram_en_val})\n7. Настроить Telegram бота ({tg_var})\n8. Сбросить все настройки\n9. В главное меню\n\n > ')

            if settings_choose == '1':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    
                config_list["debug"] = not getConfig("debug")
                saveJson(files_folder+'config.json', config_list)
                clear()
                continue
            elif settings_choose == '2':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    
                config_list["shutdown_enabled"] = not getConfig("shutdown_enabled")
                saveJson(files_folder+'config.json', config_list)
                clear()
                continue
            elif settings_choose == '3':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                
                try:
                    clear()
                    config_list["shutdown_timeout"] = int(input('Введите через сколько минут после конференции выключать ПК:\n\n > '))
                    saveJson(files_folder+'config.json', config_list)
                    continue
                except:
                    clear()
                    print('Нужно использовать целое число.')
                    time.sleep(2)
                    continue
                continue
            elif settings_choose == '4':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                
                try:
                    clear()
                    config_list["start"] = input('Введите комбинацию клавиш для начала записи OBS:\nЭта комбинация должна быть идентична оной в самом OBS!\n\n > ')
                    saveJson(files_folder+'config.json', config_list)
                    continue
                except:
                    clear()
                    print('Нужно использовать комбинацию клавиш в виде текста.')
                    time.sleep(2)
                    continue
                continue
            elif settings_choose == '5':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                
                try:
                    clear()
                    config_list["stop"] = input('Введите комбинацию клавиш для остановки записи OBS:\nЭта комбинация должна быть идентична оной в самом OBS!\n\n > ')
                    saveJson(files_folder+'config.json', config_list)
                    continue
                except:
                    clear()
                    print('Нужно использовать комбинацию клавиш в виде текста.')
                    time.sleep(2)
                    continue
                continue
            elif settings_choose == '6':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    
                config_list["telegram_enabled"] = not getConfig("telegram_enabled")
                saveJson(files_folder+'config.json', config_list)
                clear()
                continue
            elif settings_choose == '7':
                clear()
                none = input('Пожалуйста, прочтите инструкцию по установке Telegram бота в README.TXT\nчтобы хорошо понимать что сейчас от вас нужно.\n\n > ')
                
                while True:
                    clear()
                    try:
                        telegram_send.configure(files_folder+'telegram.conf', channel=False, group=False, fm_integration=False)
                        break
                    except:
                        clear()
                        continue
                    telegram_send.send(messages=[f"🎊 Конфигурация правильна, всё работает!"], parse_mode="markdown", conf=f"{files_folder}telegram.conf")
                    clear()
                continue
            elif settings_choose == '8':
                while True:
                    clear()
                    reset_decision = input('Вы уверены что хотите сбросить настройки? (Да/Нет)\n\nВнимание! Это действие нельзя обратить!\nВаш список конференций затронут НЕ будет.\n\n > ')
                    if reset_decision.lower() in ['y', 'yes', 'д', 'да']:
                        temp_config_list = {}
                        temp_config_list["debug"] = False
                        temp_config_list["shutdown_timeout"] = 30
                        temp_config_list["shutdown_enabled"] = True
                        temp_config_list["start"] = "shift+f7"
                        temp_config_list["stop"] = "shift+f8"
                        temp_config_list["telegram_enabled"] = False
                        saveJson(files_folder+'config.json', temp_config_list)
                        if os.path.exists(files_folder+"obscorepath.txt"):
                                os.remove(files_folder+"obscorepath.txt")
                        if os.path.exists(files_folder+"obspath.txt"):
                                os.remove(files_folder+"obspath.txt")
                        if os.path.exists(files_folder+"telegram.conf"):
                                os.remove(files_folder+"telegram.conf")
                        clear()
                        none = input('Все настройки были сброшены до стандартных.\n\n > ')
                        clear()
                        break
                    elif reset_decision.lower() in ['n', 'no', 'н', 'нет']:
                        clear()
                        break
                    else:
                        clear()
                        continue
                    continue
                clear()
                continue
            elif settings_choose == '9':
                clear()
                return
    except KeyboardInterrupt:
        clear()
        return

def main(source='deamon'):
    try:
        from main import mainMenu
        clear()

        import webbrowser
            #lessons_list = open('lessons.json', 'r')
            
        try:
            with open(files_folder+'obspath.txt', 'r', encoding="utf-8") as f:
                current_obs_path = f.read()
        except:
            current_obs_path = ''
        
        if not os.path.exists(files_folder+'obspath.txt') or current_obs_path == '':
            obs_choice = input('Хотите использовать запись через OBS? (Д/Н): ')
            if obs_choice.lower() == 'д' or obs_choice.lower() == 'y':
                with open(files_folder+'obspath.txt', 'w', encoding="utf-8") as f:
                    while True:
                        try:
                            filename = easygui.fileopenbox('Выберите путь до obs32.exe или obs64.exe')
                            if filename.find("obs64.exe") != -1:
                                f.write(filename)
                                with open(files_folder+'obscorepath.txt', 'w', encoding="utf-8") as f:
                                    f.write(filename[:-9])
                                print(f'Сохранены пути для OBS:\nПриложение: {filename}\nКорневая папка: {filename[:-9]}')
                                time.sleep(3)
                                break
                            elif filename.find("obs32.exe") != -1:
                                f.write(filename)
                                with open(files_folder+'obscorepath.txt', 'w', encoding="utf-8") as f:
                                    f.write(filename[:-9])
                                print(f'Сохранены пути для OBS:\nПриложение: {filename}\nКорневая папка: {filename[:-9]}')
                                time.sleep(3)
                                break
                            elif filename.find("obs.exe") != -1:
                                f.write(filename)
                                with open(files_folder+'obscorepath.txt', 'w', encoding="utf-8") as f:
                                    f.write(filename[:-7])
                                print(f'Сохранены пути для OBS:\nПриложение: {filename}\nКорневая папка: {filename[:-7]}')
                                time.sleep(3)
                                break
                            else:
                                easygui.msgbox("Неверный путь")
                            break
                        except:
                            none = input('Вы не выбрали верный путь для OBS.\n\n > ')
                            if os.path.exists(files_folder+"obscorepath.txt"):
                                os.remove(files_folder+"obscorepath.txt")
                            if os.path.exists(files_folder+"obspath.txt"):
                                os.remove(files_folder+"obspath.txt")
                            clear()
                            break
                                
        if not os.path.exists(files_folder+'telegram.conf'):
            tg_choice = input('Хотите использовать Telegram бота? (Д/Н): ')
            if tg_choice.lower() == 'д' or tg_choice.lower() == 'y':
                # with open(files_folder+'telegram.conf', 'w', encoding="utf-8") as f:
                clear()
                none = input('Пожалуйста, прочтите инструкцию по установке Telegram бота в README.TXT\nчтобы хорошо понимать что сейчас от вас нужно.\n')
                clear()
                            
                telegram_send.configure(files_folder+'telegram.conf', channel=False, group=False, fm_integration=False)
                telegram_send.send(messages=[f"🎊 Конфигурация правильна, всё работает!"], parse_mode="markdown", conf=f"{files_folder}telegram.conf")
                clear()
        
        lessons_count = 0
        
        try:
            if getConfig("debug"):
                print(f'{nowtime()} Конфигурация импортирована')
        except:
            print(f'{nowtime()} Конфигурация отсутсвует, выключаем отладку')

        
        for les in getLessons():
            lessons_list = getLessons()
        
            lesson_name = les["name"]
            lesson_date = les["date"]
            lesson_time = les["time"]
            lesson_url = les["link"]
            lesson_obs = les["record"]
            lesson_repeat = les["repeat"]
            lesson_repeat_day = les["repeat_day"]
            
            today = date.today().strftime("%d.%m.%Y")
            
            if getDayNum(today) == lesson_repeat_day: #lesson_date == today: # or getDayNum(today) == lesson_repeat_day:
                print('================================================\n')
            
                print(f'{nowtime()} Найден урок "{lesson_name}" в {lesson_time}. Ждём начала...')
                waitStart(lesson_time, lambda: act(100))
                webbrowser.open(lesson_url)
                easteregg_number = randint(1, 100000)
                if easteregg_number == 69420:
                    webbrowser.open('https://www.pornhub.com/view_video.php?viewkey=ph5f3eb1e206aa8')
                print(f'{nowtime()} Ждём 10 секунд до отслеживания Zoom...')
                time.sleep(10)
                
                while not getState():
                    if getConfig("debug"):
                        print(f'{nowtime()} Урок задерживается, ждём...')
                    time.sleep(5)
                    continue
                
                record_now = False 
                lesson_duration = 0
                firstshow = True
                
                if lesson_obs:
                    try:
                        if getConfig("debug"):
                            print(f'{nowtime()} Импортированы клавиши старта и остановки записи ({getConfig("start")} и {getConfig("stop")}).')
                            
                        start = getConfig("start")
                        stop = getConfig("stop")
                    except:
                        start = 'shift+f7'
                        stop = 'shift+f8'
                        if getConfig("debug"):
                            print(f'{nowtime()} Используем стандартные клавиши старта и остановки записи ({start} и {stop}).')
                    
                while True:
                    if getState():
                            if firstshow:
                                print(f'{nowtime()} Захвачен текущий урок в Zoom.')
                                winsound.PlaySound(sounds_folder+"started.wav", winsound.SND_FILENAME)
                                tgsend(getConfig("telegram_enabled"), f"▶ Зашёл на урок *{lesson_name}* в *{nowtime(False, False)}*")
                                if lesson_obs:
                                    try:
                                        obs_path_file = open(files_folder+'obspath.txt', 'r', encoding="utf-8")
                                        obs_path_file_text = obs_path_file.read()
                                        
                                        obs_core_path_file = open(files_folder+'obscorepath.txt', 'r', encoding="utf-8")
                                        obs_core_path_file_text = obs_core_path_file.read()
                                        
                                        obs_process = subprocess.Popen(obs_path_file_text, cwd=obs_core_path_file_text)
                                        time.sleep(5)
                                    except:
                                        print(f'{nowtime()} Не удалось открыть OBS для записи.')
                                else:
                                    if getConfig("debug"):
                                        print(f'{nowtime()} Не включаем OBS для записи.')
                                firstshow = False
                            
                            if lesson_obs:
                                if not record_now:
                                    keyboard.press(start)
                                    time.sleep(.25)
                                    keyboard.release(start)
                                    record_now = True
                                    print(f'{nowtime()} Сигнал записи OBS отправлен.') 
                                    # ({start})')
                                    
                            lesson_duration = lesson_duration + 10
                                
                            if getConfig("debug"):
                                print(f'{nowtime()} Zoom подключён. Урок идёт уже {str(lesson_duration)} сек. ({str(round(lesson_duration/60, 2))} мин.)')
                                
                            time.sleep(10)
                            continue
                    else:
                        if getConfig("debug"):
                            print(f'{nowtime()} Zoom отключился. Процесс CptHost.exe более не существует.')
                            
                        tgsend(getConfig("telegram_enabled"), f"◀ Урок *{lesson_name}* длился *{str(round(lesson_duration/60, 2))}* мин.")
                        print(f'{nowtime()} Урок длился {str(lesson_duration)} сек. ({str(round(lesson_duration/60, 2))} мин.)')
                        winsound.PlaySound(sounds_folder+"ended.wav", winsound.SND_FILENAME)
                        
                        if lesson_obs:
                            keyboard.press(stop)
                            time.sleep(.25)
                            keyboard.release(stop)
                            print(f'{nowtime()} Сигнал остановки записи через OBS отправлен.') 
                            # ({stop})')
                            record_now = False
                            time.sleep(3)
                            try:
                                obs_process.terminate()
                            except:
                                if getConfig("debug"):
                                    print(f'{nowtime()} Не удалось остановить процесс OBS.')
                            
                        if not lesson_repeat:
                            del lessons_list[i]
                                
                            saveJson(files_folder+'lessons.json', lessons_list)
                                
                            print(f'{nowtime()} Урок "{lesson_name}" в {lesson_time} удалён.')
                        
                        print('\n================================================\n\n')
                            
                        firstshow = True
                        
                        lessons_count = lessons_count+1
                            
                        break
            record_now = False
            lessons_list = getLessons()


        time.sleep(3)
        print(f'{nowtime()} Уроков нет или же все в списке закончились.')
        
        if lessons_count > 0:
            if getConfig("shutdown_enabled"):
                try:
                    print(f'{nowtime()} Ваш ПК автоматически выключится через {str(getConfig("shutdown_timeout"))} мин.')
                    winsound.PlaySound(sounds_folder+"shutdown.wav", winsound.SND_FILENAME)
                    shutdown = inputimeout(prompt=f'{nowtime()} Нажмите Enter чтобы предотвратить выключение ПК...', timeout=getConfig("shutdown_timeout")*60)
                except TimeoutOccurred:
                    print(f'{nowtime()} Время вышло, выключаем ваш ПК...')
                    time.sleep(3)
                    tgsend(getConfig("telegram_enabled"), f"⚠ Уроков больше нет, выключаем ваш ПК...")
                    time.sleep(5)
                    os.system("shutdown /s /t 1")
        
        if source == 'deamon':
            exit = input(f'{nowtime()} Программа завершена! Нажмите Enter чтобы выйти...')
            clear()
            sys.exit()
        elif source == 'menu':
            exit = input(f'{nowtime()} Программа завершена! Нажмите Enter чтобы вернуться в меню...')
            clear()
            return
    except KeyboardInterrupt:
        if source == 'deamon':
            exit = input(f'{nowtime()} Программа остановлена! Нажмите Enter чтобы выйти...')
            clear()
            sys.exit()
        elif source == 'menu':
            exit = input(f'{nowtime()} Программа остановлена! Нажмите Enter чтобы вернуться в меню...')
            clear()
            return

if __name__ == '__main__':
    import sys
    clear()
    
    main()