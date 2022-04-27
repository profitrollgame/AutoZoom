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

from modules.functions import *

if getConfig("use_colors"):
    from modules.colors import *
    appendLog('Colors imported')
else:
    RESET = ''
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    BBLACK = BRED = BGREEN = BYELLOW = BBLUE = BMAGENTA = BCYAN = BWHITE = ''
    ULINE = REVERSE = ''
    appendLog('Loading without colors')

sysname = getOS()

clear()
setTitle("Загрузка daemon...", sysname)
appendLog('daemon.py start initialized', startup=True)

import modules.rpc as rpc

if sysname == "windows":
    import easygui
    import tkinter

import keyboard
import ast
import inputimeout
import telegram_send

menu_choose = None

try:
    from inputimeout import inputimeout, TimeoutOccurred
    appendLog('inputimeout imported')
except Exception as exp:
    appendLog(f'Failed to import inputimeout: {exp}')
    print(f'[{YELLOW}WARN{RESET}] Не удалось импортировать классы "inputimeout" и "TimeoutOccurred" из модуля "inputimeout"')

def nowtime(seconds=True, noice=True, color=True):
    now = datetime.now()
    if seconds:
        justnow = now.strftime("%H:%M:%S")
    else:
        justnow = now.strftime("%H:%M")
    
    if noice:
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


def tgsend(enabled, message, video=None):
    if enabled:
        if os.path.exists(files_folder+'telegram.conf'):
            tg_file = open(files_folder+'telegram.conf', 'r', encoding="utf-8")
            tg_text = tg_file.read()
            
            if tg_text != 'Not Configured':
            
                try:
                    if video is not None:
                        telegram_send.send(messages=[f"{message}"], videos=[f"{video}"], parse_mode="markdown", conf=files_folder+"telegram.conf")
                    else:
                        telegram_send.send(messages=[f"{message}"], parse_mode="markdown", conf=files_folder+"telegram.conf")
                    
                except Exception as excep:
                    appendLog(f'Failed to send TG message "{message}": {exp}')
                    playSound(getConfig("sound_warning"), nowtime())
                    print(f'{nowtime()} Не удалось отправить Telegram сообщение "{message}" (Ошибка: {exp})')


async def tgsendVideo(msg, video, video_new):
    print(f"{nowtime()} Отправка записи конференции {CYAN}{msg}{RESET}.")
    try:
        tgsend(getConfig("telegram_enabled"), msg, video=video)
        os.rename(video, video_new)
    except Exception as exp:
        tgsend(getConfig("telegram_enabled"), f"⚠ Отправка видео `{video}` прошла с ошибкой `{exp}`")

def main(source='deamon'):

    global sysname

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
        
        setTitle("AutoZoom (Демон)", sysname)
        appendLog('Main daemon opened')

        import webbrowser
        
        if (getConfig("obs_core") or getConfig("obs_exe")) == None:
            clear()
            while True:
                obs_choice = input(f'{RESET}Хотите использовать запись через OBS? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET}): ')
                if obs_choice.lower() in yes_list:
                    with open(f"{files_folder}config.json", encoding="utf-8") as json_file:
                        config_list = json.load(json_file)
                        json_file.close()
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
                                none = input('Вы не выбрали верный путь для OBS.\n\n > ')
                                setConfig("obs_exe", "Disabled")
                                setConfig("obs_core", "Disabled")
                                appendLog(f'Could not select path to OBS: {exp}')
                                
                                clear()
                                break
                    break
                    
                elif obs_choice.lower() in no_list:
                    setConfig("obs_exe", "Disabled")
                    setConfig("obs_core", "Disabled")
                    
                    clear()
                    break
                    
                else:
                    clear()
                    continue
        
        if not os.path.exists(files_folder+'telegram.conf'):
            clear()
            tg_choice = input(f'{RESET}Хотите использовать Telegram бота? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET}): ')
            if tg_choice.lower() in yes_list:
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
                
            elif tg_choice.lower() in no_list:
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
                
                diff = ((datetime.strptime(today, "%d.%m.%Y") - datetime.strptime(lesson_date, "%d.%m.%Y")).days)
                
                if getConfig("debug"):
                    print(f'{nowtime()} Конференция {CYAN}{lesson_name}{RESET}: Разница дней {BRED}{diff}{RESET}, Повторение {BRED}{lesson_repeat}{RESET}.')
                
                if diff > 0 and not lesson_repeat:
                
                    if getConfig("remove_old"):
                    
                        del lessons_list[lessons_list.index(les)]
                        
                        saveJson(files_folder+'lessons.json', lessons_list)
                        appendLog(f'Old lesson named {lesson_name} removed')
                            
                        if getConfig("debug"):
                            print(f'{nowtime()} Старая конференция {CYAN}{lesson_name}{RESET} за {CYAN}{lesson_date} {RESET}в {BRED}{lesson_time}{RESET} удалена.')
                        
                        lessons_list = getLessons()
                
                elif (today == lesson_date) or (getDayNum(today) == lesson_repeat_day):
                    print(f'{BBLACK}================================================{RESET}\n')
                
                    print(f'{nowtime()} Найдена конференция {CYAN}{lesson_name}{RESET} в {BRED}{lesson_time}{RESET}. Ждём начала...')
                    
                    setTitle(f'Ждём начала "{lesson_name}"', sysname)
                    
                    waiting_time_unix = int(time.time())
                    rpc.waitLesson(lesson_name, waiting_time_unix)
                    
                    waitStart(lesson_time, lambda: act(100))
                    
                    try:
                        if sysname == 'windows':
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
                            
                            appendLog(f'Replaced link {lesson_url_original} with {lesson_url}')
                            
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
                            
                            appendLog(f'Replaced link {lesson_url_original} with {lesson_url}')
                            
                            if sysname == "android":
                                os.system(f'xdg-open "{lesson_url_original}"')
                            else:
                                os.system(f'xdg-open "{lesson_url}"')
                            
                    except Exception as exep:
                        appendLog(f'Failed to open lesson {lesson_name} in Zoom: {exep}')
                        
                        try:
                            webbrowser.open(lesson_url_original)
                            
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
                    
                    if sysname == "windows":
                    
                        while not getState():
                            setTitle(f'Конференция "{lesson_name}" задерживается', sysname)
                            
                            if getConfig("debug"):
                                print(f'{nowtime()} Конференция задерживается, ждём... ({getState()})')
                            
                            if retries == 1:
                                appendLog('Lesson delay found')
                            
                            time.sleep(5)
                            retries += 1
                            
                            if getConfig("debug"):
                                if retries == 2:
                                    playSound(getConfig("sound_warning"), nowtime())
                                    tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* обнаружена {profilename}")
                            
                            if retries == 36:
                                playSound(getConfig("sound_warning"), nowtime())
                                tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 3 минуты {profilename}")
                                print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}3{RESET} минуты')
                                appendLog(f'Lesson delay exceeded: {retries} retries')
                            
                            if retries == 120:
                                playSound(getConfig("sound_warning"), nowtime())
                                tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 10 минут {profilename}")
                                print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}10{RESET} минут')
                                appendLog(f'Lesson delay exceeded: {retries} retries')
                            
                            if retries == 360:
                            
                                if getConfig("debug"):
                                    playSound(getConfig("sound_warning"), nowtime())
                                    tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 30 минут, конференция сбошена {profilename}")
                                    print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}30{RESET} минут, конференция сброшена')
                                else:
                                    playSound(getConfig("sound_warning"), nowtime())
                                    tgsend(getConfig("telegram_enabled"), f"⚠ Задержка конференции *{lesson_name}* превысила 30 минут, конференция сбошена {profilename}")
                                    print(f'{nowtime()} Задержка конференции {CYAN}{lesson_name}{RESET} превысила {BRED}30{RESET} минут, конференция сброшена')
                                
                                appendLog(f'Lesson delay exceeded: {retries} retries')
                                
                                playSound(getConfig("sound_ended"), nowtime())
                                
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
                                        
                                        setTitle(f'Идёт конференция "{lesson_name}"', sysname)
                                        
                                        playSound(getConfig("sound_started"), nowtime())
                                        tgsend(getConfig("telegram_enabled"), f"▶ Зашёл на конференцию *{lesson_name}* в *{nowtime(False, False, False)}* {profilename}")
                                        
                                        appendLog(f'Joined lesson {lesson_name} at {nowtime(False, False, False)}')
                                        
                                        rpc.onLesson(lesson_name, start_time_unix)
                                        
                                        if lesson_obs:
                                            try:
                                                obs_process = subprocess.Popen(getConfig("obs_exe"), cwd=getConfig("obs_core"))
                                                appendLog(f'Sent instruction to open OBS')
                                                time.sleep(getConfig("obs_delay"))
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
                                            playSound(getConfig("sound_recordstart"), nowtime())
                                    
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
                            
                            setTitle(f'Конференция "{lesson_name}" завершилась', sysname)
                            
                            if getConfig("debug"):
                                tgsend(getConfig("telegram_enabled"), f"◀ Конференция *{lesson_name}* длилась *{str(round(lesson_duration/60, 2))}* мин.")
                                print(f'{nowtime()} Конференция длилась {BGREEN}{str(lesson_duration)} сек{RESET}. ({BGREEN}{str(round(lesson_duration/60, 2))} мин{RESET}.)')
                                fire_and_forget(tgsendVideo(f"{lesson_name}", "C:\\Users\\PC-Admin\\AutoZoom\\lessons\\meeting.mp4", f'C:\\Users\\PC-Admin\\AutoZoom\\lessons\\meeting_{datetime.now().strftime("%d.%m.%Y_%H-%M-%S")}.mp4'))
                            else:
                                tgsend(getConfig("telegram_enabled"), f"◀ Конференция *{lesson_name}* длилась *{str(int(lesson_duration/60))}* мин.")
                                print(f'{nowtime()} Конференция длилась {BGREEN}{str(lesson_duration)} сек{RESET}. ({BGREEN}{str(int(lesson_duration/60))} мин{RESET}.)')
                            
                            appendLog(f'Lesson {lesson_name} duration was {str(int(lesson_duration/60))} m. ({str(lesson_duration)} s.)')
                            
                            playSound(getConfig("sound_ended"), nowtime())
                            
                            if lesson_obs:
                                keyboard.press(stop)
                                time.sleep(.25)
                                keyboard.release(stop)
                                print(f'{nowtime()} Сигнал остановки записи через OBS отправлен.') 
                                playSound(getConfig("sound_recordstop"), nowtime())
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
                        
                    else:
                        playSound(getConfig("sound_started"), nowtime())
                        tgsend(getConfig("telegram_enabled"), f"▶ Присоединился к конференции *{lesson_name}* в *{nowtime(False, False, False)}* {profilename}")
                        
                        appendLog(f'Joined lesson {lesson_name} at {nowtime(False, False, False)}')
                        
                        if not lesson_repeat:
                            del lessons_list[lessons_list.index(les)]
                            
                            saveJson(files_folder+'lessons.json', lessons_list)
                            appendLog(f'Lesson named {lesson_name} removed')
                            
                            if getConfig("debug"):
                                print(f'{nowtime()} Конференция {CYAN}{lesson_name}{RESET} в {BRED}{lesson_time}{RESET} удалена.')
                        
                        lessons_list = getLessons()
                
            except KeyboardInterrupt:
                appendLog('Lessons waiting reset')
                
                setTitle("Ожидание конференции сбошено", sysname)
                
                if getConfig("debug"):
                    print(f'{nowtime()} Ожидание конференции сброшено.')
                else:
                    print('')
                
                time.sleep(1)
                pass

        time.sleep(3)
        appendLog('Could not find any more lessons today')
        print(f'{nowtime()} Конференций нет или же все в списке закончились.')
        setTitle('Конференции закончились, режим ожидания', sysname)
        
        if lessons_count > 0:
            if getConfig("shutdown_enabled"):
                if getConfig("end_mode") == 'shutdown':
                    try:
                        tgsend(getConfig("telegram_enabled"), f"⚠ Конференции кончились, автовыключение {profilename}через {str(getConfig('shutdown_timeout'))} мин...")
                        print(f'{nowtime()} Ваш ПК автоматически выключится через {BRED}{str(getConfig("shutdown_timeout"))} мин{RESET}.')
                        
                        appendLog(f'Shutting PC down in {str(getConfig("shutdown_timeout"))}')
                        
                        playSound(getConfig("sound_shutdown"), nowtime())
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
                elif getConfig("end_mode") == 'sleep':
                    try:
                        tgsend(getConfig("telegram_enabled"), f"⚠ Конференции кончились, отправление в сон {profilename}через {str(getConfig('shutdown_timeout'))} мин...")
                        print(f'{nowtime()} Ваш ПК автоматически заснёт через {BRED}{str(getConfig("shutdown_timeout"))} мин{RESET}.')
                        
                        appendLog(f'Falling asleep in {str(getConfig("shutdown_timeout"))}')
                        
                        playSound(getConfig("sound_shutdown"), nowtime())
                        end_unix = int(time.time())+getConfig("shutdown_timeout")*60
                        rpc.sleepmode(end_unix)
                        shutdown = inputimeout(prompt=f'{nowtime()} Нажмите {CYAN}Enter{RESET} чтобы предотвратить засыпание ПК...', timeout=getConfig("shutdown_timeout")*60)
                        
                        appendLog('Sleep mode aborted')
                        clear()
                    except TimeoutOccurred:
                        clear()
                        print(f'{nowtime()} Время вышло, уводим ваш ПК в спящий режим...')
                        time.sleep(3)
                        tgsend(getConfig("telegram_enabled"), f"⚠ Время таймаута исткело, переводим ПК в спящий режим...")
                        time.sleep(5)
                        appendLog('Activating PC sleep mode')
                        os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep")
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
            setTitle("AutoZoom (Главная)", sysname)
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
    from modules.functions import getOS, setTitle
    setTitle("AutoZoom (Демон)", getOS())
    import sys
    clear()
    
    main()
