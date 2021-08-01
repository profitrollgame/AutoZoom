import rpc
from functions import *
from datetime import datetime, date, timedelta
from daemon import getLessons, getConfig

if getConfig("use_colors"):
    from colors import *
    appendLog('Colors imported')
else:
    RESET = ''
    BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    BBLACK = BRED = BGREEN = BYELLOW = BBLUE = BMAGENTA = BCYAN = BWHITE = ''
    ULINE = REVERSE = ''
    appendLog('Loading without colors')


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
    if getConfig("debug"):
        print(dictionary)
    
    dictionary.sort(key = lambda x: datetime.strptime(x["time"], '%H:%M'))
    dictionary.sort(key = lambda x: datetime.strptime(x["date"], '%d.%m.%Y')) 
    appendLog('Lessons dictionary sorted')


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
        lessname = strCleaner(lessname)
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
                abort = "skip"
                conflict = False
                conflictles = ''
                confstr = 'конференцией'
                
                try:
                
                    for lesson in lessons_got:
                    
                        if lesson["date"] == finallessdate and lesson["time"] == lesstime:
                            conflict = True
                            
                            if conflictles == '':
                                conflictles = f'{CYAN}{lesson["name"]}{RESET}'
                                confstr = 'конференцией'
                                
                            else:
                                conflictles += f', {CYAN}{lesson["name"]}{RESET}'
                                confstr = 'конференциями'
                    
                    if conflict:
                        while True:
                            clear()
                            choice = input(f'{RESET}Время и дата конференции совпадают с {confstr} {conflictles}.\nДобавить ещё одну конференцию на то же время? ({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n\n > ')

                            if choice.lower() in yes_list:
                                abort = "bypass"
                                break
                                
                            elif choice.lower() in no_list:
                                abort = "restart"
                                break
                                
                            else:
                                continue
                            
                    if abort == "restart":
                        continue
                    else:
                        break                        
                    
                except Exception as exp:
                    none = input(exp)
                    pass
                
                break
            except:
                continue
        
        clear()
        lesslink = input(f'{RESET}Введите ссылку на конференцию:\n{BBLACK}Формат: {BRED}https://us01web.zoom.us/j/ИДЕНТИФИКАТОР?pwd=ПАРОЛЬ{RESET}\n{BBLACK}Либо введите {YELLOW}1 {BBLACK}для добавления по номеру и паролю{RESET}\n\n > {BRED}').replace(" ", "")
        lesslink = strCleaner(lesslink)

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
            
            if repeat.lower() in yes_list:
                finalrepeat = True
                finalrepeatday = getDayNum(finallessdate)
                local_lessons.update({"repeat": finalrepeat})
                local_lessons.update({"repeat_day": finalrepeatday})
                break
            elif repeat.lower() in no_list:
                finalrepeat = False
                finalrepeatday = None
                local_lessons.update({"repeat": finalrepeat})
                local_lessons.update({"repeat_day": finalrepeatday})
                break
            else:
                continue
        
        while True:
            if getOS() == "windows":
                clear()
                lessrecord = input(f'Записать эту конференцию? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n\n > ')
                
                if lessrecord.lower() in yes_list:
                    finallessrecord = True
                    local_lessons.update({"record": finallessrecord})
                    break
                elif lessrecord.lower() in no_list:
                    finallessrecord = False
                    local_lessons.update({"record": finallessrecord})
                    break
                else:
                    continue
            else:
                finallessrecord = False
                local_lessons.update({"record": finallessrecord})
                break
            
        
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
        lessname = strCleaner(lessname)
        
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
                    
                    local_lessons.update({"time": lesstime})
                    
                else:
                    try:
                        finallesstime = (datetime.strptime(lesstime, "%H:%M"))
                        finallesstime = lesstime
                        
                        local_lessons.update({"time": lesstime})
                        
                        abort = "skip"
                        conflict = False
                        conflictles = ''
                        confstr = 'конференцией'
                        
                        try:
                        
                            for lesson in lessons_got:
                            
                                if lesson["date"] == finallessdate and lesson["time"] == lesstime:
                                    conflict = True
                                    
                                    if conflictles == '':
                                        conflictles = f'{CYAN}{lesson["name"]}{RESET}'
                                        confstr = 'конференцией'
                                        
                                    else:
                                        conflictles += f', {CYAN}{lesson["name"]}{RESET}'
                                        confstr = 'конференциями'
                            
                            if conflict:
                                while True:
                                    clear()
                                    choice = input(f'{RESET}Время и дата конференции совпадают с {confstr} {conflictles}.\nДобавить ещё одну конференцию на то же время? ({BGREEN}Да{RESET}/{BRED}Нет{RESET})\n\n > ')

                                    if choice.lower() in yes_list:
                                        abort = "bypass"
                                        break
                                        
                                    elif choice.lower() in no_list:
                                        abort = "restart"
                                        break
                                        
                                    else:
                                        continue
                                            
                            if abort == "restart":
                                continue
                                
                            else:
                                break                        
                            
                        except Exception as exp:
                            none = input(exp)
                            pass
                    except:
                        continue
                
                break
            except:
                continue
        
        clear()
        lesslink = input(f'{RESET}Введите ссылку на конференцию:\n{BBLACK}Формат: {BRED}https://us01web.zoom.us/j/ИДЕНТИФИКАТОР?pwd=ПАРОЛЬ{RESET}\n{BBLACK}Либо введите {YELLOW}1 {BBLACK}для добавления по номеру и паролю{RESET}\n\n > {BRED}').replace(" ", "")
        lesslink = strCleaner(lesslink)

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
            
            if repeat.lower() in yes_list:
                finalrepeat = True
                finalrepeatday = getDayNum(finallessdate)
                local_lessons.update({"repeat": finalrepeat})
                local_lessons.update({"repeat_day": finalrepeatday})
                break
            elif repeat.lower() in no_list:
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
            if getOS() == "windows":
                clear()
                print(f'Записать эту конференцию? {RESET}({BGREEN}Да{RESET}/{BRED}Нет{RESET})')
                print(f'\nОригинальное значение: {BRED}{lessons_got[edi]["record"]}{RESET}')
                lessrecord = input('\n > ')
                
                if lessrecord.lower() in yes_list:
                    finallessrecord = True
                    local_lessons.update({"record": finallessrecord})
                    break
                elif lessrecord.lower() in no_list:
                    finallessrecord = False
                    local_lessons.update({"record": finallessrecord})
                    break
                elif lessrecord == '':
                    finallessrecord = lessons_got[edi]["record"]
                    local_lessons.update({"record": finallessrecord})
                    break
                else:
                    continue
            else:
                finallessrecord = False
                local_lessons.update({"record": finallessrecord})
                break
            
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
            
            if removeall.lower() in yes_list:
                with open(files_folder+'lessons.json', 'w', encoding="utf-8") as f:
                    f.write("[]")
                    f.close()
                
                appendLog('All lessons removed')
                clear()
                none = input('Все конференции были удалены.\n\n > ')
                clear()
                break
            elif removeall.lower() in no_list:
                appendLog('All lessons removal aborted')
                clear()
                break
            else:
                continue
                
    except KeyboardInterrupt:
        appendLog('All lessons removal aborted')
        
        clear()
        return


def debugLesson():
    try:
        from profile import debuglink, name
        appendLog('Debug link added to the list')
        
        local_lessons = {}
        lessons_got = getLessons()
        
        local_lessons.update({"name": "Debug Lesson"})
        local_lessons.update({"date": date.today().strftime("%d.%m.%Y")})
        local_lessons.update({"time": "00:00"})
        local_lessons.update({"link": debuglink})
        local_lessons.update({"repeat": False})
        local_lessons.update({"repeat_day": None})
        local_lessons.update({"record": True})
        
        lessons_got.append(dict(local_lessons))
        sortLessons(lessons_got)
        saveJson(files_folder+'lessons.json', lessons_got)
        
        return f"{RESET}Конференция для отладки профиля {CYAN}{name} {RESET}была добавлена."
        
    except:
        return f"{RESET}Для отладки нужен профиль {BRED}profile.py {RESET}со ссылкой на конференцию {BRED}debuglink {RESET}и именем {BRED}name{RESET}."


def editor():
    try:
        setTitle("AutoZoom (Редактор)", getOS())
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
                setTitle("AutoZoom (Главная)", getOS())
                mainMenu()
            else:
                continue
            
    except KeyboardInterrupt:
        appendLog('Exiting back to main menu')
        rpc.inMenu()
        clear()
        return