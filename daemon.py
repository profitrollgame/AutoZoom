# -*- coding: utf-8 -*-

import subprocess
import contextlib
import importlib
import time
import datetime
import os
import pathlib
import json
import getopt
import sys
from random import randint
from pathlib import Path
from datetime import datetime, date, timedelta

from functions import *

if getConfig("use_colors"):
    from colors import *
    appendLog('Colors imported')
else:
    RESET = ''
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    BBLACK = BRED = BGREEN = BYELLOW = BBLUE = BMAGENTA = BCYAN = BWHITE = ''
    ULINE = REVERSE = ''
    appendLog('Loading without colors')

if os.name == 'nt':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

if os.name == 'nt':
    import winsound
else:
    import playsound

clear()
os.system("title Загрузка daemon...")
appendLog('Loading daemon')

import libinstaller

import easygui
import tkinter
import keyboard
import ast
import inputimeout
import telegram_send
import getpass


menu_choose = None

try:
    from inputimeout import inputimeout, TimeoutOccurred
    appendLog('inputimeout imported')
except Exception as exp:
    appendLog(f'Failed to import inputimeout: {exp}')
    print(f'[{YELLOW}WARN{RESET}] Не удалось импортировать классы "inputimeout" и "TimeoutOccurred" из модуля "inputimeout"')

def nowtime(seconds=True, noice=True, color=True):
    now = datetime.now()
    if seconds == True:
        justnow = now.strftime("%H:%M:%S")
    else:
        justnow = now.strftime("%H:%M")
    
    if noice == True:
        if not color:
            beautiful = f'[{justnow}]'
        else:
            beautiful = f'[{CYAN}{justnow}{RESET}]'
    else:
        if not color:
            beautiful = f'{justnow}'
        else:
            beautiful = f'{CYAN}{justnow}{RESET}'
        
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
        appendLog('File lessons.json does not exist')
        with open(files_folder+'lessons.json', 'w', encoding="utf-8") as f:
            f.write("[]")
            f.close()
            lessons_list = []
            
        appendLog(f'Created lessons.json')
    else:
        with open(files_folder+'lessons.json', encoding="utf-8") as json_file:
            lessons_list = json.load(json_file)
            json_file.close()
            
        appendLog('File lessons.json loaded')
            
    return lessons_list

def getState():

    if os.name == 'nt':
    
        try:
            output = os.popen(f'tasklist /fi "IMAGENAME eq CptHost.exe" /fi "USERNAME ne NT AUTHORITY\{getpass.getuser()}"').read()
            
            if "CptHost.exe" in output:
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

def listLessons(from_where='remove'):

    try:
    
        appendLog('Showing list of everything planned')
    
        if from_where == 'editor':
            print(f'{RESET}Полный список запланированных конференций:\n')

        print(f'{BBLACK}================================================{RESET}')
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
            
            spacer_all = 6 * ' '
            spacer_ind = (5 - length) * ' '
            
        
            print(f'{spacer_all}Имя:    {YELLOW}{les[1]["name"]}{RESET}')
            print(f'{spacer_all}Дата:   {YELLOW}{les[1]["date"]}{RESET}')
            print(f'{spacer_all}Время:  {YELLOW}{les[1]["time"]}{RESET}')
            print(f' {GREEN}{les[0]}{RESET}{spacer_ind}Ссылка: {YELLOW}{les[1]["link"]}{RESET}')
            print(f'{spacer_all}Повтор: {YELLOW}{repeat}{RESET}')
            print(f'{spacer_all}День:   {YELLOW}{repeat_day}{RESET}')
            print(f'{spacer_all}Запись: {YELLOW}{record}{RESET}')
            print(f'{BBLACK}================================================{RESET}')

        if from_where == 'editor':
            none = input('\n\n > ')
            
    except KeyboardInterrupt:
        clear()
        return

def sortLessons(dictionary):
    dictionary.sort(key = lambda x: datetime.strptime(x['time'], '%H:%M'))
    dictionary.sort(key = lambda x: datetime.strptime(x['date'], '%d.%m.%Y')) 
    appendLog('Lessons dictionary sorted')
    
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

def addLesson():
    appendLog('Adding new lesson')
    
    try:
        local_lessons = {}
        lessons_got = getLessons()

        lessname = input(f'{RESET}Введите (своё) имя конференции:\n{BBLACK}Нужно лишь для отображения в Discord и самом AutoZoom{RESET}\n\n > {CYAN}')
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
            
            print(f'{RESET}Введите дату конференции или номер дня ({BRED}ДД.ММ.ГГГГ{RESET}):\n')
            print(f' {BRED}1.{RESET} {today.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}2.{RESET} {today_1.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_1.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}3.{RESET} {today_2.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_2.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}4.{RESET} {today_3.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_3.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}5.{RESET} {today_4.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_4.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}6.{RESET} {today_5.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_5.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}7.{RESET} {today_6.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_6.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            
            try:
                lessdate = input(f'\n > {BRED}')
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
                lesstime = input(f'{RESET}Введите время конференции ({BRED}ЧЧ:ММ{RESET}):\n\n > {BRED}')
                finallesstime = (datetime.strptime(lesstime, "%H:%M"))
                local_lessons.update({"time": lesstime})
                break
            except:
                continue
        
        clear()
        lesslink = input(f'{RESET}Введите ссылку на конференцию:\n{BBLACK}Формат: {BRED}https://us01web.zoom.us/j/ИДЕНТИФИКАТОР?pwd=ПАРОЛЬ{RESET}\n{BBLACK}Либо введите {YELLOW}1 {BBLACK}для добавления по номеру и паролю{RESET}\n\n > {BRED}').replace(" ", "")

        if lesslink.replace(' ', '') == '1':
            clear()
            lessid = input(f'{RESET}Введите идентификатор конференции:\n{BBLACK}Формат: {BRED}012 3456 7890 {BBLACK} либо {BRED}01234567890{RESET}\n\n > {BRED}')
            clear()
            lesspasswd = input(f'{RESET}Введите код доступа (пароль) конференции:\n\n > {BRED}')
            lesslink = f'https://us01web.zoom.us/j/{lessid.replace(" ", "")}?pwd={lesspasswd.replace(" ", "")}'

        local_lessons.update({"link": lesslink})
        
        while True:
            clear()
            repeat = input(f'{RESET}Повторять эту конференцию ({getDay(getDayNum(finallessdate))})? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n\n > ')
            
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
            lessrecord = input(f'Записать эту конференцию? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n\n > ')
            
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
        print(f'Добавлена конференция {CYAN}{local_lessons["name"]}{RESET} за {BRED}{local_lessons["date"]}{RESET} на время {BRED}{local_lessons["time"]}{RESET}.')
        appendLog(f'Added lesson {local_lessons["name"]} (Date: {local_lessons["date"]}, Time: {local_lessons["time"]}, Link: {local_lessons["link"]})')
        none = input('\n > ')
        
    except KeyboardInterrupt:
        appendLog('Lesson adding aborted')
        clear()
        return
    

def editLesson():
    appendLog(f'Editing existing lesson')
    
    try:
        local_lessons = {}
        lessons_got = getLessons()
        
        while True:
            print(f'{RESET}Выберите номер (индекс) для изменения:\n')
            listLessons()
            lessons_got = getLessons()
            
            print(f'\nДля отмены операции введите {BRED}c{RESET} или {BRED}cancel{RESET}')
            
            edi = input(f'\n > {BGREEN}')
            
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
                print(f'{RESET}Выберите {ULINE}правильный{RESET} индекс (номер) для изменения.')
                time.sleep(3)
                clear()
                continue
                
            break

        clear()
        lessname = input(f'{RESET}Введите (своё) имя конференции:\n{BBLACK}Нужно лишь для отображения в Discord и самом AutoZoom{RESET}\n\nОригинальное имя: {CYAN}{lessons_got[edi]["name"]}{RESET}\n\n > {CYAN}')
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
            
            print(f'{RESET}Введите дату конференции или номер дня ({BRED}ДД.ММ.ГГГГ{RESET}):\n')
            print(f' {BRED}1.{RESET} {today.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}2.{RESET} {today_1.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_1.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}3.{RESET} {today_2.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_2.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}4.{RESET} {today_3.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_3.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}5.{RESET} {today_4.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_4.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}6.{RESET} {today_5.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_5.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f' {BRED}7.{RESET} {today_6.strftime("%d.%m.%Y")} ({BGREEN}{getDay(datetime.strptime(today_6.strftime("%d.%m.%Y"), "%d.%m.%Y").isoweekday())}{RESET})')
            print(f'\nОригинальная дата: {BRED}{lessons_got[edi]["date"]}{RESET}')
            
            try:
                lessdate = input(f'\n > {BRED}')
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
                lesstime = input(f'{RESET}Введите время конференции ({BRED}ЧЧ:ММ{RESET}):\n\nОригинальное время: {BRED}{lessons_got[edi]["time"]}{RESET}\n\n > {BRED}')
                
                if lesstime == '':
                    finallesstime = lessons_got[edi]["time"]
                    lesstime = lessons_got[edi]["time"]
                else:
                    try:
                        finallesstime = (datetime.strptime(lesstime, "%H:%M"))
                        finallesstime = lesstime
                    except:
                        continue
                
                local_lessons.update({"time": lesstime})
                break
            except:
                continue
        
        clear()
        lesslink = input(f'{RESET}Введите ссылку на конференцию:\n{BBLACK}Формат: {BRED}https://us01web.zoom.us/j/ИДЕНТИФИКАТОР?pwd=ПАРОЛЬ{RESET}\n{BBLACK}Либо введите {YELLOW}1 {BBLACK}для добавления по номеру и паролю{RESET}\n\n > {BRED}').replace(" ", "")

        if lesslink.replace(' ', '') == '1':
            clear()
            lessid = input(f'{RESET}Введите идентификатор конференции:\n{BBLACK}Формат: {BRED}012 3456 7890 {BBLACK} либо {BRED}01234567890{RESET}\n\n > {BRED}')
            clear()
            lesspasswd = input(f'{RESET}Введите код доступа (пароль) конференции:\n\n > {BRED}')
            lesslink = f'https://us01web.zoom.us/j/{lessid.replace(" ", "")}?pwd={lesspasswd.replace(" ", "")}'
            
        if lesslink == '':
            lesslink = lessons_got[edi]["link"]
            
        local_lessons.update({"link": lesslink})
        
        while True:
            clear()
            try:
                lessrepeatday = getDay(lessons_got[edi]["repeat_day"])
            except:
                lessrepeatday = 'Не повторяется'
            
            print(f'{RESET}Повторять эту конференцию ({YELLOW}{getDay(getDayNum(finallessdate))}{RESET})? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})')
            print(f'\nОригинальное значение: {BRED}{lessrepeatday}{RESET}')
            repeat = input('\n > ')
            
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
            print(f'Записать эту конференцию? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})')
            print(f'\nОригинальное значение: {BRED}{lessons_got[edi]["record"]}{RESET}')
            lessrecord = input('\n > ')
            
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
        print(f'Изменена конференция {CYAN}{lessname}{RESET} за {BRED}{finallessdate}{RESET} на время {BRED}{finallesstime}{RESET}.')
        appendLog(f'Edited lesson {lessname} (Date: {finallessdate}, Time: {finallesstime}, Link: {local_lessons["link"]})')
        none = input('\n > ')
        
    except KeyboardInterrupt:
        appendLog('Editing existing lesson aborted')
        clear()
        return
    

def removeLesson():
    appendLog(f'Removing existing lesson')
    
    try:
        while True:
            print(f'{RESET}Выберите номер (индекс) для удаления:\n')
            listLessons()
            lessons_local = getLessons()
            print(f'\n{BBLACK}Для отмены операции введите {BRED}c{BBLACK} или {BRED}cancel{RESET}')
            
            rem = input(f'\n > {BRED}')
            
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
                print(f'{RESET}Выберите {ULINE}правильный{RESET} индекс (номер) для удаления.')
                time.sleep(3)
                clear()
                continue
                
            sortLessons(lessons_local)
            saveJson(files_folder+'lessons.json', lessons_local)
            clear()
            print(f'{RESET}Удалена конференция {CYAN}{del_name}{RESET} за {BRED}{del_date}{RESET} на время {BRED}{del_time}{RESET}.')
            appendLog(f'Removed lesson {del_name} (Date: {del_date}, Time: {del_time})')
            none = input('\n > ')
            break
    except KeyboardInterrupt:
        appendLog('Lesson removal aborted')
        clear()
        return

def removeAllLessons():
    appendLog('Removing all lessons')
    
    try:
        while True:
            clear()
            removeall = input(f'{RESET}Вы уверены что хотите удалить все конференции? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n{BRED}Внимание!{RESET} Это действие нельзя обратить!\nВаши настройки затронуты НЕ будут.\n\n > ')
            
            if removeall.lower() in ['y', 'yes', 'д', 'да']:
                with open(files_folder+'lessons.json', 'w', encoding="utf-8") as f:
                    f.write("[]")
                    f.close()
                    
                appendLog('All lessons removed')
                clear()
                none = input('Все конференции были удалены.\n\n > ')
                clear()
                break
            elif removeall.lower() in ['n', 'no', 'н', 'нет']:
                appendLog('All lessons removal aborted')
                clear()
                break
            else:
                continue
                
    except KeyboardInterrupt:
        appendLog('All lessons removal aborted')
        
        clear()
        return

import rpc

def editor():
    try:
        os.system("title AutoZoom (Редактор)")
        appendLog('Editor menu opened')
        
        from main import mainMenu
        
        while True:
            clear()
            
            print(f'{BBLACK}»{RESET} Меню редактора\n')
            print(f' {BRED}1.{RESET} Добавить конференцию')
            print(f' {BRED}2.{RESET} Изменить конференцию')
            print(f' {BRED}3.{RESET} Удалить конференцию')
            print(f' {BRED}4.{RESET} Посмотреть конференции')
            print(f' {BRED}5.{RESET} Удалить все конференции')
            print(f' {BRED}6.{RESET} В главное меню')
            editor_choose = input(f'\n > {BRED}')
            
            if editor_choose == '1':
                appendLog('Went to lesson adding')
                clear()
                addLesson()
            elif editor_choose == '2':
                appendLog('Went to lesson editing')
                clear()
                editLesson()
            elif editor_choose == '3':
                appendLog('Went to lesson removal')
                clear()
                removeLesson()
            elif editor_choose == '4':
                appendLog('Went to lesson lising')
                clear()
                listLessons(from_where = 'editor')
            elif editor_choose == '5':
                appendLog('Went to all lessons removal')
                clear()
                removeAllLessons()
            elif editor_choose == '6':
                appendLog('Exiting back to main menu')
                rpc.inMenu()
                clear()
                os.system("title AutoZoom (Главная)")
                mainMenu()
            else:
                continue
                
    except KeyboardInterrupt:
        appendLog('Exiting back to main menu')
        rpc.inMenu()
        clear()
        return

def tgsend(enabled, message):
    if enabled:
        if os.path.exists(files_folder+'telegram.conf'):
            tg_file = open(files_folder+'telegram.conf', 'r', encoding="utf-8")
            tg_text = tg_file.read()
            
            if tg_text != 'Not Configured':
                try:
                    telegram_send.send(messages=[f"{message}"], parse_mode="markdown", conf=files_folder+"telegram.conf")
                except Exception as excep:
                    appendLog(f'Failed to send TG message "{message}": {exp}')
                    print(f'{nowtime()} Не удалось отправить Telegram сообщение "{message}" (Ошибка: {exp})')

def playSound(soundname):

    if getConfig("sounds"):
    
        if os.name == 'nt':
            winsound.PlaySound(sounds_folder+soundname+".wav", winsound.SND_FILENAME)
        else:
            playsound.playsound(sounds_folder+soundname+".wav")

def settings():
    appendLog('Settings page 1 opened')

    try:
        while True:
            
            os.system("title AutoZoom (Настройки)")
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
            elif not getConfig("debug"):
                telegram_en_val = f'{BRED}Выкл.{RESET}'
            else:
                telegram_en_val = f'{BRED}ERROR{RESET}'
             
            shutdown_time_val = getConfig("shutdown_timeout")
            start_val = getConfig("start")
            stop_val = getConfig("stop")
            
            print(f'{RESET}{BBLACK}»{RESET} Настройки (1 стр.)\n')

            print(f'  {BRED}1.{RESET} Режим отладки ({debug_val})')
            print(f'     {BBLACK}Не рекомендуем включать его без необходимости\n')

            print(f'  {BRED}2.{RESET} Цветной вывод ({color_val})')
            print(f'     {BBLACK}Отображение цветных текстов в меню и выводе (нужен перезапуск)\n')

            print(f'  {BRED}3.{RESET} Полный экран ({fullscreen_val})')
            print(f'     {BBLACK}Эмулировать вызов полного экрана при запуске (окно должно быть в фокусе)\n')

            print(f'  {BRED}4.{RESET} Звуковые сигналы ({sounds_val})')
            print(f'     {BBLACK}Воспроизводить звуки при начале/конце конференций и записи видео\n')
            
            
            print(f'  {BRED}5.{RESET} Запись через OBS ({obs_val})')
            print(f'     {BBLACK}Возможность записи конференций через OBS\n')

            print(f'  {BRED}6.{RESET} Автовыключение ({shutdown_en_val})')
            print(f'     {BBLACK}Когда конференции закончатся компьютер выключится\n')

            print(f'  {BRED}7.{RESET} Следующая страница')
            print(f'     {BBLACK}Перейти на вторую страницу настроек\n')

            print(f'  {BRED}8.{RESET} В главное меню')
            print(f'     {BBLACK}Вернуться в основное меню{RESET}\n')

            print(f' {BBLACK}Для переключения параметров Вкл/Выкл просто введите номер{RESET}') #\n Если окно приложения слишком мелкое - увеличьте его или листайте это меню{RESET}')
            settings_choose = input(f'\n > {BRED}')

            if settings_choose == '1':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                    
                config_list["debug"] = not getConfig("debug")
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "debug" to {getConfig("debug")}')
                
                clear()
                continue

            elif settings_choose == '2':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                    
                config_list["use_colors"] = not getConfig("use_colors")
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "use_colors" to {getConfig("use_colors")}')
                
                clear()
                continue

            elif settings_choose == '3':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                config_list["run_fullscreen"] = not getConfig("run_fullscreen")
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "run_fullscreen" to {getConfig("run_fullscreen")}')
                
                clear()
                continue

            elif settings_choose == '4':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                config_list["sounds"] = not getConfig("sounds")
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "sounds" to {getConfig("sounds")}')
                
                clear()
                continue
                
            elif settings_choose == '5':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                if getConfig("obs_core") and getConfig("obs_exe") not in [None, 'Disabled']:
                    config_list["obs_core"] = 'Disabled'
                    config_list["obs_exe"] = 'Disabled'
                else:
                    clear()
                    obs_choice = input(f'{RESET}Хотите использовать запись через OBS? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET}): ')
                    if obs_choice.lower() in ['y', 'yes', 'д', 'да']:
                        while True:
                            try:
                                filename = easygui.fileopenbox('Выберите путь до obs32.exe или obs64.exe')
                                if filename.find("obs64.exe") != -1:
                                    config_list["obs_exe"] = filename
                                    config_list["obs_core"] = filename[:-9]
                                    print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-9]}{RESET}')
                                    time.sleep(3)
                                    break
                                elif filename.find("obs32.exe") != -1:
                                    config_list["obs_exe"] = filename
                                    config_list["obs_core"] = filename[:-9]
                                    print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-9]}{RESET}')
                                    time.sleep(3)
                                    break
                                elif filename.find("obs.exe") != -1:
                                    f.write(filename)
                                    config_list["obs_exe"] = filename
                                    config_list["obs_core"] = filename[:-7]
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
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "obs_exe" to {getConfig("obs_exe")}')
                appendLog(f'Changed option "obs_core" to {getConfig("obs_core")}')
                
                clear()
                continue

            elif settings_choose == '6':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                    
                config_list["shutdown_enabled"] = not getConfig("shutdown_enabled")
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "shutdown_enabled" to {getConfig("shutdown_enabled")}')
                
                clear()
                continue

            elif settings_choose == '7':
                clear()
                settings2()
                
            elif settings_choose == '8':
                rpc.inMenu()
                clear()
                os.system("title AutoZoom (Главная)")
                return
                
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return

def settings2():
    appendLog('Settings page 2 opened')

    try:
        while True:
            
            os.system("title AutoZoom (Настройки)")
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
            elif not getConfig("debug"):
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
            print(f'     {BBLACK}Комбинация клавиш для начала записи через OBS (см. документацию)\n')

            print(f'  {BRED}3.{RESET} Остановить запись ({YELLOW}{stop_val}{RESET})')
            print(f'     {BBLACK}Комбинация клавиш для остановки записи через OBS (см. документацию)\n')

            print(f'  {BRED}4.{RESET} Отправлять уведомления ({telegram_en_val})')
            print(f'     {BBLACK}Ваш бот отправит сообщениия о начале/конце конференции и выключении ПК\n')

            print(f'  {BRED}5.{RESET} Настроить Telegram бота ({tg_var})')
            print(f'     {BBLACK}Настроить на вашем ПК бота для ЛС (см. документацию)\n')
            
            print(f'  {BRED}6.{RESET} Проверка обновлений ({update_val})')
            print(f'     {BBLACK}Не рекомендуем выключать без необходимости\n')
            
            print(f'  {BRED}7.{RESET} Следующая страница')
            print(f'     {BBLACK}Перейти на третью страницу настроек\n')

            print(f'  {BRED}8.{RESET} Назад')
            print(f'     {BBLACK}Вернуться на предыдущую страницу{RESET}\n')

            print(f' {BBLACK}Для переключения параметров Вкл/Выкл просто введите номер{RESET}') #\n Если окно приложения слишком мелкое - увеличьте его или листайте это меню{RESET}')
            settings_choose = input(f'\n > {BRED}')

            if settings_choose == '1':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                try:
                    clear()
                    config_list["shutdown_timeout"] = int(input(f'{RESET}Введите через сколько минут после конференции выключать ПК:\n\n > {BRED}'))
                    saveJson(files_folder+'config.json', config_list)
                    appendLog(f'Changed option "shutdown_timeout" to {getConfig("shutdown_timeout")}')
                    continue
                except:
                    clear()
                    print(f'{RESET}Нужно использовать целое число.')
                    time.sleep(2)
                    continue
                continue

            elif settings_choose == '2':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                try:
                    clear()
                    config_list["start"] = input(f'{RESET}Введите комбинацию клавиш для начала записи OBS:\nЭта комбинация должна быть идентична оной в самом OBS!\n\n > {YELLOW}')
                    saveJson(files_folder+'config.json', config_list)
                    appendLog(f'Changed option "start" to {getConfig("start")}')
                    continue
                except:
                    clear()
                    print(f'{RESET}Нужно использовать комбинацию клавиш в виде текста.')
                    time.sleep(2)
                    continue
                continue

            elif settings_choose == '3':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                try:
                    clear()
                    config_list["stop"] = input(f'{RESET}Введите комбинацию клавиш для остановки записи OBS:\nЭта комбинация должна быть идентична оной в самом OBS!\n\n > {YELLOW}')
                    saveJson(files_folder+'config.json', config_list)
                    appendLog(f'Changed option "stop" to {getConfig("stop")}')
                    continue
                except:
                    clear()
                    print(f'{RESET}Нужно использовать комбинацию клавиш в виде текста.')
                    time.sleep(2)
                    continue
                continue

            elif settings_choose == '4':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                    
                config_list["telegram_enabled"] = not getConfig("telegram_enabled")
                saveJson(files_folder+'config.json', config_list)
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
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                config_list["update_check"] = not getConfig("update_check")
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "update_check" to {getConfig("update_check")}')
                
                clear()
                continue

            elif settings_choose == '7':
                appendLog('Going to settings page 3')
                clear()
                settings3()

            elif settings_choose == '8':
                appendLog('Returning to settings page 1')
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
            
            os.system("title AutoZoom (Настройки)")
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

            print(f'  {BRED}3.{RESET} Сбросить все настройки')
            print(f'     {BBLACK}Восстановить настройки по умолчанию\n')

            print(f'  {BRED}4.{RESET} Назад')
            print(f'     {BBLACK}Вернуться на предыдущую страницу{RESET}\n')

            print(f' {BBLACK}Для переключения параметров Вкл/Выкл просто введите номер{RESET}') #\n Если окно приложения слишком мелкое - увеличьте его или листайте это меню{RESET}')
            settings_choose = input(f'\n > {BRED}')

            if settings_choose == '1':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                config_list["write_logs"] = not getConfig("write_logs")
                saveJson(files_folder+'config.json', config_list)
                appendLog(f'Changed option "write_logs" to {getConfig("write_logs")}')

            if settings_choose == '2':
                with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                    config_list = json.load(json_file)
                    json_file.close()
                
                try:
                    clear()
                    config_list["log_size"] = int(input(f'{RESET}Введите после скольки килобайт архивировать лог:\n\n > {BRED}'))
                    saveJson(files_folder+'config.json', config_list)
                    continue
                except:
                    clear()
                    print(f'{RESET}Нужно использовать целое число.')
                    time.sleep(2)
                    continue
                    
                appendLog(f'Changed option "log_size" to {getConfig["log_size"]}')
                continue

            elif settings_choose == '3':
                appendLog('Resetting configuration')
            
                while True:
                    clear()
                    reset_decision = input(f'{RESET}Вы уверены что хотите сбросить настройки? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n\n{BRED}Внимание!{RESET} Это действие нельзя обратить!\nВаш список конференций затронут НЕ будет.\n\n > ')

                    if reset_decision.lower() in ['y', 'yes', 'д', 'да']:
                    
                        from functions import default_config
                        
                        saveJson(files_folder+'config.json', default_config)
                        appendLog('Configuration dropped to default')
                        clear()
                        none = input(f'{RESET}Все настройки были сброшены до стандартных.\n\n > ')
                        clear()
                        break
                        
                    elif reset_decision.lower() in ['n', 'no', 'н', 'нет']:
                        appendLog('Configuration reset aborted')
                        clear()
                        break
                        
                    else:
                        clear()
                        continue
                        
                    continue
                    
                clear()
                continue

            elif settings_choose == '4':
                appendLog('Returning to settings page 2')
                clear()
                return
                
    except KeyboardInterrupt:
        rpc.inMenu()
        clear()
        return

def main(source='deamon'):

    ##########################################

    # Возможность профилей сделана для себя
    # и не планируется как фича, однако
    # вы можете присобачить сюда что хотите.
    
    try:
        from profile import profilename
    except:
        profilename = ''
        pass
        
    ##########################################

    try:
        import time
        from main import mainMenu
        clear()
        
        os.system("title AutoZoom (Демон)")
        appendLog('Main daemon opened')

        import webbrowser
        
        if (getConfig("obs_core") or getConfig("obs_exe")) == None:
            clear()
            while True:
                obs_choice = input(f'{RESET}Хотите использовать запись через OBS? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET}): ')
                if obs_choice.lower() in ['y', 'yes', 'д', 'да']:
                    with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                        config_list = json.load(json_file)
                        json_file.close()
                        while True:
                            try:
                                filename = easygui.fileopenbox('Выберите путь до obs32.exe или obs64.exe')
                                if filename.find("obs64.exe") != -1:
                                    config_list["obs_exe"] = filename
                                    config_list["obs_core"] = filename[:-9]
                                    saveJson(files_folder+'config.json', config_list)
                                    print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-9]}{RESET}')
                                    time.sleep(3)
                                    break
                                elif filename.find("obs32.exe") != -1:
                                    config_list["obs_exe"] = filename
                                    config_list["obs_core"] = filename[:-9]
                                    saveJson(files_folder+'config.json', config_list)
                                    print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-9]}{RESET}')
                                    time.sleep(3)
                                    break
                                elif filename.find("obs.exe") != -1:
                                    config_list["obs_exe"] = filename
                                    config_list["obs_core"] = filename[:-7]
                                    saveJson(files_folder+'config.json', config_list)
                                    print(f'Сохранены пути для OBS:\nПриложение: {BRED}{filename}{RESET}\nКорневая папка: {BRED}{filename[:-7]}{RESET}')
                                    time.sleep(3)
                                    break
                                else:
                                    easygui.msgbox("Неверный путь")
                                    continue
                                break
                            except Exception as exp:
                                none = input('Вы не выбрали верный путь для OBS.\n\n > ')
                                config_list["obs_exe"] = 'Disabled'
                                config_list["obs_core"] = 'Disabled'
                                saveJson(files_folder+'config.json', config_list)
                                appendLog(f'Could not select path to OBS: {exp}')
                                
                                clear()
                                break
                    break
                elif obs_choice.lower() in ['n', 'no', 'н', 'нет']:
                    with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                        config_list = json.load(json_file)
                        config_list["obs_exe"] = 'Disabled'
                        config_list["obs_core"] = 'Disabled'
                        saveJson(files_folder+'config.json', config_list)
                        json_file.close()
                        
                    clear()
                    break
                else:
                    clear()
                    continue
                                
        if not os.path.exists(files_folder+'telegram.conf'):
            clear()
            tg_choice = input(f'{RESET}Хотите использовать Telegram бота? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET}): ')
            if tg_choice.lower() in ['y', 'yes', 'д', 'да']:
                clear()
                print(f'Пожалуйста, прочтите инструкцию по установке Telegram бота в {BRED}README.txt{RESET}')
                print(f'или в документации/инструкции что в разделе {CYAN}Помощь{RESET} главного меню')
                print(f'чтобы хорошо понимать что сейчас от вас нужно.')
                none = input('\n > ')
                clear()
                            
                while True:
                    clear()
                    
                    try:
                        telegram_send.configure(files_folder+'telegram.conf', channel=False, group=False, fm_integration=False)
                        break
                    except Exception as exp:
                        appendLog(f'Failed to configure Telegram Send: {exp}')
                        clear()
                        continue
                        
                    telegram_send.send(messages=[f"🎊 Конфигурация правильна, всё работает!"], parse_mode="markdown", conf=f"{files_folder}telegram.conf")
                    appendLog('Telegram Send successfully configured')
                    clear()
                    
            elif tg_choice.lower() in ['n', 'no', 'н', 'нет']:
                with open(files_folder+'telegram.conf', 'w', encoding="utf-8") as f:
                    f.write('Not Configured')
                    f.close()
                    
        lessons_count = 0
        
        try:
            if getConfig("debug"):
                print(f'{nowtime()} Конфигурация импортирована\n')
        except:
            print(f'{nowtime()} Конфигурация {BRED}отсутсвует{RESET}, выключаем отладку\n')

        
        for les in getLessons():
            try:
                lessons_list = getLessons()
            
                lesson_name = les["name"]
                lesson_date = les["date"]
                lesson_time = les["time"]
                lesson_url = les["link"]
                lesson_url_original = les["link"]
                lesson_obs = les["record"]
                lesson_repeat = les["repeat"]
                
                try:
                    lesson_repeat_day = les["repeat_day"]
                except:
                    lesson_repeat_day = 'Не повторяется'
                
                today = date.today().strftime("%d.%m.%Y")
                
                if (today == lesson_date) or (getDayNum(today) == lesson_repeat_day):
                    print(f'{BBLACK}================================================{RESET}\n')
                
                    print(f'{nowtime()} Найдена конференция {CYAN}{lesson_name}{RESET} в {BRED}{lesson_time}{RESET}. Ждём начала...')
                    
                    waiting_time_unix = int(time.time())
                    rpc.waitLesson(lesson_name, waiting_time_unix)
                    
                    waitStart(lesson_time, lambda: act(100))
                    
                    try:
                        if os.name == 'nt':
                            i = 0
                            
                            if i == 0:
                                lesson_url = lesson_url.replace(f"https://zoom.us/j/", "zoommtg://zoom.us/join?action=join&confno=")
                            
                            while i < 10:
                                lesson_url = lesson_url.replace(f"https://us0{i}web.zoom.us/j/", "zoommtg://zoom.us/join?action=join&confno=")
                                i += 1
                                
                            lesson_url = lesson_url.replace("&", "^&")
                            lesson_url = lesson_url.replace("?pwd", "^&pwd")
                            
                            if getConfig("debug"):
                                print(f'{nowtime()} Ориг. ссылка: {BRED}{lesson_url_original}{RESET}')
                                print(f'{nowtime()} Измен. ссылка: {BRED}{lesson_url}{RESET}')
                                
                            appendLog(f'Replacing link {lesson_url_original} with {lesson_url}')
                            
                            os.system(f'start {lesson_url}')
                        else:
                            i = 0
                            
                            if i == 0:
                                lesson_url = lesson_url.replace(f"https://zoom.us/j/", "zoommtg://zoom.us/join?action=join&confno=")
                                
                            while i < 10:
                                lesson_url = lesson_url.replace(f"https://us0{i}web.zoom.us/j/", "zoommtg://zoom.us/join?action=join&confno=")
                                i += 1
                            
                            lesson_url = lesson_url.replace("?pwd=", "&pwd=")
                            
                            if getConfig("debug"):
                                print(f'{nowtime()} Ориг. ссылка: {BRED}{lesson_url_original}{RESET}')
                                print(f'{nowtime()} Измен. ссылка: {BRED}{lesson_url}{RESET}')
                                
                            appendLog(f'Replacing link {lesson_url_original} with {lesson_url}')
                                
                            os.system(f'xdg-open "{lesson_url}"')
                    except Exception as exep:
                        appendLog(f'Failed to open lesson {lesson_name} in Zoom: {exep}')
                        
                        try:
                            webbrowser.open(lesson_url)
                        except Exception as exp:
                            print(f'{nowtime()} Открыть конференцию {CYAN}{lesson_name}{RESET} не удалось ни напрямую, ни в браузере.')
                            appendLog(f'Failed to open lesson {lesson_name} in both browser and Zoom: {exp}')
                    
                    easteregg_number = randint(1, 100000)
                    
                    if easteregg_number == 69420:
                        appendLog('Easteregg summoned')
                        webbrowser.open('https://www.pornhub.com/view_video.php?viewkey=ph5f3eb1e206aa8')
                        
                    print(f'{nowtime()} Ждём {BRED}10 секунд{RESET} до отслеживания Zoom...')
                    time.sleep(10)
                    
                    retries = 0
                    destroy = False
                    
                    while not getState():
                        if getConfig("debug"):
                            print(f'{nowtime()} Конференция задерживается, ждём... ({getState()})')
                        
                        appendLog('Lesson delay found')
                            
                        time.sleep(5)
                        retries += 1
                        
                        if retries == 36:
                            tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 3 минуты {profilename}")
                            print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}3{RESET} минуты')
                            appendLog(f'Lesson delay exceeded: {retries} retries')
                            
                        if retries == 120:
                            tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 10 минут {profilename}")
                            print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}10{RESET} минут')
                            appendLog(f'Lesson delay exceeded: {retries} retries')
                        
                        if retries == 360:
                        
                            if getConfig("debug"):
                                tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 30 минут, конференция сбошена {profilename}")
                                print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}30{RESET} минут, конференция сброшена')
                            else:
                                tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 30 минут, конференция сбошена {profilename}")
                                print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}30{RESET} минут, конференция сброшена')
                                
                            appendLog(f'Lesson delay exceeded: {retries} retries')
                            
                            playSound("ended")
                            
                            if lesson_obs:
                            
                                record_now = False
                                
                                time.sleep(3)
                                
                                try:
                                    obs_process.terminate()
                                except Exception as exp:
                                    appendLog(f'Failed to stop OBS process: {exp}')
                                    
                                    if getConfig("debug"):
                                        print(f'{nowtime()} Не удалось остановить процесс OBS.')
                                
                            if not lesson_repeat:
                                del lessons_list[lessons_list.index(les)]
                                    
                                saveJson(files_folder+'lessons.json', lessons_list)
                                    
                                if getConfig("debug"):
                                    print(f'{nowtime()} Конференция {CYAN}{lesson_name}{RESET} в {BRED}{lesson_time}{RESET} удалена.')
                            
                            print(f'\n{BBLACK}================================================{RESET}\n\n')
                                
                            firstshow = True
                            
                            lessons_count = lessons_count+1
                            destroy = True
                            break
                        
                        continue
                    
                    record_now = False 
                    lesson_duration = 0
                    firstshow = True
                    
                    if lesson_obs and not destroy:
                        try:
                            if getConfig("debug"):
                                print(f'{nowtime()} Импортированы клавиши старта и остановки записи ({YELLOW}{getConfig("start")}{RESET} и {YELLOW}{getConfig("stop")}{RESET}).')
                                
                            start = getConfig("start")
                            stop = getConfig("stop")
                        except:
                            start = 'shift+f7'
                            stop = 'shift+f8'
                            if getConfig("debug"):
                                print(f'{nowtime()} Используем стандартные клавиши старта и остановки записи ({YELLOW}{start}{RESET} и {YELLOW}{stop}{RESET}).')
                        
                    i = 0
                    
                    while True and not destroy:
                        while i < 3:
                            if getState():
                                if firstshow:
                                    try:
                                        start_time_unix = int(time.time())
                                        lesson_start = datetime.now()
                                    except:
                                        pass
                                    
                                    print(f'{nowtime()} Захвачена текущая конференция в Zoom.')
                                    
                                    playSound("started")
                                    tgsend(getConfig("telegram_enabled"), f"▶ Зашёл на конференцию *{lesson_name}* в *{nowtime(False, False, False)}* {profilename}")
                                    
                                    appendLog(f'joined lesson {lesson_name} at {nowtime(False, False, False)}')
                                    
                                    rpc.onLesson(lesson_name, start_time_unix)
                                    
                                    if lesson_obs:
                                        try:
                                            obs_process = subprocess.Popen(getConfig("obs_exe"), cwd=getConfig("obs_core"))
                                            appendLog(f'Sent instruction to open OBS')
                                            time.sleep(5)
                                        except Exception as exp:
                                            appendLog(f'Failed to open OBS: {exp}')
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
                                        playSound("recordstart")
                                        
                                lesson_duration = (datetime.now() - lesson_start).total_seconds()
                                    
                                if getConfig("debug"):
                                    print(f'{nowtime()} Zoom подключён. Конференция идёт уже {BGREEN}{str(lesson_duration)} сек{RESET}. ({BGREEN}{str(round(lesson_duration/60, 2))} мин{RESET}.)')
                                    
                                time.sleep(5)
                                continue
                            else:
                                i += 1
                                appendLog(f'CptHost.exe not found, trying again in 10 seconds')
                                
                                if getConfig("debug"):
                                    print(f'{nowtime()} {BRED}Конференция не обнаружена! {RESET}Повторная проверка через {BRED}10 {RESET}секунд...')
                                    
                                time.sleep(10)
                                continue
                                
                        if getConfig("debug"):
                            print(f'{nowtime()} Zoom отключился. Процесс {BRED}CptHost.exe{RESET} более не существует.')
                            
                        appendLog(f'CptHost.exe not found, Zoom disconnected')
                            
                        if getConfig("debug"):
                            tgsend(getConfig("telegram_enabled"), f"◀ Конференция *{lesson_name}* длилась *{str(round(lesson_duration/60, 2))}* мин.")
                            print(f'{nowtime()} Конференция длилась {BGREEN}{str(lesson_duration)} сек{RESET}. ({BGREEN}{str(round(lesson_duration/60, 2))} мин{RESET}.)')
                        else:
                            tgsend(getConfig("telegram_enabled"), f"◀ Конференция *{lesson_name}* длилась *{str(int(lesson_duration/60))}* мин.")
                            print(f'{nowtime()} Конференция длилась {BGREEN}{str(lesson_duration)} сек{RESET}. ({BGREEN}{str(int(lesson_duration/60))} мин{RESET}.)')
                            
                        appendLog(f'Lesson {lesson_name} duration was {str(int(lesson_duration/60))} m. ({str(lesson_duration)} s.)')
                            
                        playSound("ended")
                        
                        if lesson_obs:
                            keyboard.press(stop)
                            time.sleep(.25)
                            keyboard.release(stop)
                            print(f'{nowtime()} Сигнал остановки записи через OBS отправлен.') 
                            playSound("recordstop")
                            record_now = False
                            time.sleep(3)
                            
                            try:
                                obs_process.terminate()
                            except Exception as exp:
                                appendLog(f'Failed to stop OBS process: {exp}')
                                
                                if getConfig("debug"):
                                    print(f'{nowtime()} Не удалось остановить процесс OBS.')
                            
                        if not lesson_repeat:
                            del lessons_list[lessons_list.index(les)]
                                
                            saveJson(files_folder+'lessons.json', lessons_list)
                            appendLog(f'Lesson named {lesson_name} removed')
                                
                            if getConfig("debug"):
                                print(f'{nowtime()} Конференция {CYAN}{lesson_name}{RESET} в {BRED}{lesson_time}{RESET} удалена.')
                        
                        print(f'\n{BBLACK}================================================{RESET}\n\n')
                            
                        firstshow = True
                        
                        lessons_count = lessons_count+1
                        break
                        
                record_now = False
                retries = 0
                destroy = False
                lessons_list = getLessons()
                
            except KeyboardInterrupt:
                appendLog('Lessons waiting reset')
                
                if getConfig("debug"):
                    print(f'{nowtime()} Ожидание конференции сброшено.')
                else:
                    print('')
                    
                time.sleep(1)
                pass

        time.sleep(3)
        appendLog('Could not find any more lessons today')
        print(f'{nowtime()} Конференций нет или же все в списке закончились.')
        
        if lessons_count > 0:
            if getConfig("shutdown_enabled"):
                if getConfig("end_mode") == 'shutdown':
                    try:
                        tgsend(getConfig("telegram_enabled"), f"⚠ Конференции кончились, автовыключение {profilename}через {str(getConfig('shutdown_timeout'))} мин...")
                        print(f'{nowtime()} Ваш ПК автоматически выключится через {BRED}{str(getConfig("shutdown_timeout"))} мин{RESET}.')
                        
                        appendLog(f'Shutting PC down in {str(getConfig("shutdown_timeout"))}')
                        
                        playSound("shutdown")
                        end_unix = int(time.time())+getConfig("shutdown_timeout")*60
                        rpc.shutdown(end_unix)
                        shutdown = inputimeout(prompt=f'{nowtime()} Нажмите {CYAN}Enter{RESET} чтобы предотвратить выключение ПК...', timeout=getConfig("shutdown_timeout")*60)
                        
                        appendLog('Shutdown aborted')
                        clear()
                    except TimeoutOccurred:
                        clear()
                        print(f'{nowtime()} Время вышло, выключаем ваш ПК...')
                        time.sleep(3)
                        tgsend(getConfig("telegram_enabled"), f"⚠ Время таймаута исткело, выключаем ваш ПК...")
                        time.sleep(5)
                        appendLog('Shutting PC down')
                        os.system("shutdown /s /t 1")
                # elif getConfig("end_mode") == 'restart':
                    # from datetime import datetime, time
                    # from time import sleep

                    # runTime = "00:00"
                    # startTime = time(*(map(int, runTime.split(':'))))
                    # tomorrow = date.today()+timedelta(days=1)
                    # timestamp = (tomorrow - date(1970, 1, 1)).total_seconds()
                    # while startTime.total_seconds() > timestamp: #(date.today() + timedelta(days=1)).time():
                        # sleep(2)
        
        if source == 'deamon':
            appendLog(f'Waiting for any input')
            
            rpc.lessonEnded()
            exit = input(f'{nowtime()} Программа завершена! Нажмите {CYAN}Enter{RESET} чтобы выйти...')
            rpc.disconnect()
            clear()
            sys.exit()
        elif source == 'menu':
            appendLog(f'Waiting for any input')
            
            rpc.lessonEnded()
            exit = input(f'{nowtime()} Программа завершена! Нажмите {CYAN}Enter{RESET} чтобы вернуться в меню...')
            rpc.inMenu()
            clear()
            os.system("title AutoZoom (Главная)")
            return
    except KeyboardInterrupt:
        if source == 'deamon':
            appendLog(f'Deamon stopped, waiting for any input')
            
            rpc.lessonEnded()
            exit = input(f'{nowtime()} Программа остановлена! Нажмите {CYAN}Enter{RESET} чтобы выйти...')
            rpc.disconnect()
            clear()
            sys.exit()
        elif source == 'menu':
            appendLog(f'Deamon stopped, waiting for any input')
            
            rpc.lessonEnded()
            exit = input(f'{nowtime()} Программа остановлена! Нажмите {CYAN}Enter{RESET} чтобы вернуться в меню...')
            rpc.inMenu()
            clear()
            return

if __name__ == '__main__':
    os.system("title AutoZoom (Демон)")
    import sys
    clear()
    
    main()
