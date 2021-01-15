## Добро пожаловать в AutoZoom!

В этом файле описаны все шаги которые нужно выполнить для работы с программой.

### Содержание
1. Описание и информация
2. Инструкция по установке
3. Инструкция по использованию
4. Благодарности и помощь

* GitHub вики проекта: https://github.com/profitrollgame/autozoom/wiki
* Обратная связь и предложения: https://t.me/profitroll
* Сообщить об ошибке/баге: https://github.com/profitrollgame/autozoom/issues

### 1. Информация и описание программы

AutoZoom создан для автоматизации присоединения к
всевозможным Zoom конференциями. С помощью этой утилиты
можно запланировать присоединение к желаемой конференции
в удобное время и удобный день. Также может быть
полезно школьникам/студентам, которые желают побывать
на уроке/паре, но при этом находиться не у компьютера.
Софт может спасти вас в случае если нужно куда-то уходить,
а пропустить конференцию принципиально нельзя.

Я не писал эту программу чтобы вредить знаниям учеников,
мешать им учиться или что-то подобное. Сделано это лишь
для удобства, интереса ради или даже в шутку.


### 2.1. Инструкция по установке

1. Пришло время найти место для нашей программы. Скопируйте папку из этого
архива в любое удобное место на компьютере (если ещё этого не сделали).

2. Попробуйте запустить ваш `start.bat` в папке `AutoZoom`. Возможно, он сам отправит вас на страницу загрузки Python.
Если же этого не произошло - сделать это можно вручную с официального сайта или из магазина приложений
Microsoft Store (https://www.microsoft.com/ru-ru/p/python-37/9nj46sx7x90p?activetab=pivot:overviewtab&source=lp).

3. Дважды нажмите на `start.bat` и выберите пункт "Редактор" чтобы редактировать ваши уроки на любой
удобный день. Введите все нужные данные. Название конференции, дату, время, ссылку на приглашение.

4. Теперь самая важная часть. Установите Zoom (https://zoom.us/download) на свой ПК.
Запустите его и зарегистрируйтесь/войдите в аккаунт. При входе ОБЯЗАТЕЛЬНО
нужно нажать на галочку о сохранении аккаунта "Не выполнять выход".

5. Нажмите на шестерёнку под вашим аватаром (правый верхний угол) и зайдите
в пункт "Видеоизображение". В этом пункте найдите галочку "Выключать мое видео
при входе в конференцию" и активируйте её. Затем уберите галочку с "Всегда показывать диалоговое
окно предварительного просмотра видео при подключении к видеоконференции". Замечательно,
теперь отправляемся во вкладку "Звук" где внизу проверяем чтобы была галочка возле "Автоматически
подключать звук с компьютера" и "Отключить звук моего микрофона при подключении к конференции". Также
можно убрать галочку с "Нажмите и удерживайте клавишу пробел, чтобы временно включить свой звук", если нужно.
Почти закончили. Теперь перейдите в пункт "Сочетания клавиш" и выключите всё вам не нужное дабы случайно
не помешать процессу автоматизации. Некоторые сочетания нужно удалить. Например, `Alt+A` лучше удалить нажав
сначала на неё, а потом на Backspace. Желательно убрать все ненужные сочетания сразу.

6. Вроде как всё настроено, пришло время открыть в папке приложения файл `start.bat` двойным нажатием и всё готово.
После вопроса про OBS можно перейти к опциональным шагам ниже для записи конференций или же просто нажать
"Н" на клавиатуре и перейти сразу к делу.


### 2.2. Запись конференций

С [официального сайта](https://obsproject.com/download) скачайте и установите OBS Studio для записи всех конференций.
После стандартного процесса установки откройте только что установленный OBS. В вопросах мастера настойки укажите,
что вас интересует запись. Разрешение укажите нужное вам.

Пройдя всё банальное и объяснённое в установщике отправляемся в настройки. Сразу же находим пункт "Вывод" в боковой
панели и меняем формат записи на `mp4`, если нужно будет потом редактировать видео. Если же нет – не трогаем.
Потом двигаемся к пункту "Горячие клавиши" и находим "Начать запись" и "Остановить запись". Тыкаем на поле мышкой, а
затем прожимаем необходимую комбинацию клавиш. Рекомендую устанавливать на старт `Shift+F7`, а на остановку `Shift+F8`,
однако можете поставить всё что вам удобно.

Чтобы наша запись работала правильно необходимо открыть в боковой панели "Общие" и в подразделе "Системный трей" поставить
галочку в пункте "Скрывать окно в системный трей при запуске". Запомните это, ведь если нужно будет открыть OBS вручную
для настройки - нужно на панели задач с правой стороны найти стрелочку вверх и там нажать на иконку OBS. Во время записи
там будет показан красный кружок для более удобной индикации. По желанию можно вывести иконку на панель задач просто перетащив
её своей мышкой под окошко трея.

Класс, теперь тут всё настроено. Тыкаем "Применить" и "ОК" внизу окна. Теперь мы в главном меню. Если ещё нет никаких
источников и в микшере пусто – не беда. Тыкаем + внизу окна источников и нажимаем "Захват экрана".
Выбираем нужный нам экран и жмакаем "ОК".

Если в микшере таки пусто – тыкаем тот же + и нажимаем "Захват выходного аудиопотока" для записи вашего устройства
воспроизведения (колонки, наушники, не важно). Выбираем нужное устройство из списка и тыкаем "ОК".
Если нужно ещё и записать ваш голос с микрофона – снова жмём + добавляя устройство ВХОДНОГО аудиопотока,
выбираем нужный микрофон и дальше снова "ОК". Замечательно, в OBS всё настроено. Двигаем в AutoZoom.

В случае если вы ставили свои комбинации клавиш (вместо рекомендуемых), то сейчас нужно открыть `start.bat` в папке
AutoZoom и выбрать пункт "Настройки". Затем выберите пункт "Начать запись" и введите желаемую комбинацию
клавиш (например, `Shift+F7`), нажмите `Enter`. Теперь выберите пункт "Остановить запись" и снова введите комбинацию клавиш.
Желательно, чтобы комбинации были разными, дабы точно избежать сбоев, однако это не по принципиально. Чудесно, жмакаем
последний пункт здесь и в меню редактора. Движемся дальше к run.bat.

Открывая AutoZoom можно обнаружить, что он спрашивает хотим ли мы использовать OBS. Пишем `Y` или `Д` и жмём `Enter`.
В появившемся окне выбираем .exe файл нашего OBS. Обычно он лежит в `C:/Program Files/obs-studio/bin/64bit/obs64.exe`,
но у вас может быть вместо `64bit` папка `32bit`, а файл `obs32.exe`. В случае с выбранным вами другим путём при
установке – ищите файл там, куда кинули.

После выбора `.exe` файла вам должно в консоль AutoZoom написать пути ядра и приложения OBS.
Они также будут храниться в файлах AutoZoom, если вдруг понадобится их изменить.


### 2.3. Telegram бот
Если же вам нужно получать уведомления от бота через Telegram - такая опция тоже есть.
Для этого нужно создать бота через BotFather ([@BotFather](https://t.me/botfather)) командой `/newbot`.
Затем вводим имя нашему боту, по сути любое которое нужно. Затем id бота чтобы оно заканчивалось на `bot` или `_bot`.

После этого мы получаем HTTP API (токен бота) который вводим во время запуска AutoZoom или же перейдя в пункт
настроек. После ввода туда токена нужно написать нашему только что созданному боту через его имя (то, что на "bot" кончается)
номер который выдаст AutoZoom.

По желанию можно введя команду `/setuserpic` и выбрав вашего бота ещё и сменить его аватар.
Теперь каждый раз когда AutoZoom будет начинать работу или заходить/покидать конференцию вы сразу же получите
сообщение в вашу личку Telegram.


### 3. Инструкция по использованию -----------

У нас есть рабочая и настроенная программа, но как же этим чудом теперь пользоваться? Всё очень просто.
Для начала открываем наш `start.bat` и тыкаем в пункт "Редактор". Там жмём "Добавить урок" и следуем шагам в приложении.
Чтобы удалить конференцию в меню редактора можно нажать "Удалить урок" и выбрать индекс (число слева посередине каждого урока).
Также, если вдруг что-то перенеслось, можно изменить конференции. нажав в редакторе "Изменить урок".

Если нужно записать программу в автозапуск - сделать это легко.
Для этого создайте ярлык для `daemon.bat` или `start.bat`, вырежьте его и вставьте по пути автозапуска
(обычно это `C:\Users\ПОЛЬЗОВАТЕЛЬ\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`).
Готово! Теперь при запуске компьютера через некоторое время после входа в пользователя у вас запустится AutoZoom сам. Это
может быть полезно если хочется полностью автоматизировать присоединение к конференциям.

Также если что-то пошло не так - можно в меню настроек сбросить все параметры до "По умолчанию".


### 4. Заключительные слова ---------------

На этом полная установка подходит к концу.
Если же вы нашли ошибки – оставляйте свои репорты на [GitHub](https://github.com/profitrollgame/autozoom/issues) или пишите мне в [Telegram](https://t.me/profitroll).

Приятного использования!

P.S.: Отдельное спасибо Kusyaka за помощь в создании сего творения.
Без тебя, если честно, у меня бы ничего не вышло, дружище <3
