# Добро пожаловать!

Contact me [directly](https://t.me/profitroll) or via [Support Center](https://www.tidio.com/talk/ydqcvfvgkud3jjk2482uaesvjpeohlh3) if you need English translation.\
В этом файле описаны все шаги которые нужно выполнить для работы с программой.

## Содержание

1. [Описание и информация](https://github.com/profitrollgame/autozoom#1-%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D1%8F-%D0%B8-%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B)
2. [Инструкция по установке](https://github.com/profitrollgame/autozoom#21-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B5)
3. [Инструкция по использованию](https://github.com/profitrollgame/autozoom#3-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E)
4. [Благодарности и помощь](https://github.com/profitrollgame/autozoom#4-%D0%B7%D0%B0%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0)

## Полезные ссылки

* [GitHub вики проекта](https://github.com/profitrollgame/autozoom/wiki)
* [Обратная связь и предложения](https://t.me/profitroll)
* [Сообщить об ошибке/баге](https://github.com/profitrollgame/autozoom/issues)
* [Центр поддержки](https://www.tidio.com/talk/ydqcvfvgkud3jjk2482uaesvjpeohlh3)



## 2.2. Запись конференций



## 2.3. Telegram бот

Если же вам нужно получать уведомления от бота через Telegram - такая опция тоже есть. Для этого нужно создать бота через BotFather ([@BotFather](https://t.me/botfather)) командой `/newbot`. Затем вводим имя нашему боту, по сути любое которое нужно. Затем id бота чтобы оно заканчивалось на `bot` или `_bot`.

После этого мы получаем HTTP API (токен бота) который вводим во время запуска AutoZoom или же перейдя в пункт настроек. После ввода туда токена нужно написать нашему только что созданному боту через его имя (то, что на "bot" кончается) номер который выдаст AutoZoom.

По желанию можно введя команду `/setuserpic` и выбрав вашего бота ещё и сменить его аватар. Теперь каждый раз когда AutoZoom будет начинать работу или заходить/покидать конференцию вы сразу же получите сообщение в вашу личку Telegram.

## 3. Инструкция по использованию

У нас есть рабочая и настроенная программа, но как же этим чудом теперь пользоваться? Всё очень просто. Для начала открываем наш `start.bat` и тыкаем в пункт "Редактор". Там жмём "Добавить урок" и следуем шагам в приложении. Чтобы удалить конференцию в меню редактора можно нажать "Удалить урок" и выбрать индекс (число слева посередине каждого урока). Также, если вдруг что-то перенеслось, можно изменить конференции. нажав в редакторе "Изменить урок".

Если нужно записать программу в автозапуск - сделать это легко. Для этого создайте ярлык для `daemon.bat` или `start.bat`, вырежьте его и вставьте по пути автозапуска (обычно это `C:\Users\ПОЛЬЗОВАТЕЛЬ\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`). Готово! Теперь при запуске компьютера через некоторое время после входа в пользователя у вас запустится AutoZoom сам. Это может быть полезно если хочется полностью автоматизировать присоединение к конференциям.

Также если что-то пошло не так - можно в меню настроек сбросить все параметры до "По умолчанию".

## 4. Заключительные слова

На этом полная установка подходит к концу. Если же вы нашли ошибки – оставляйте свои репорты на [GitHub](https://github.com/profitrollgame/autozoom/issues) или пишите мне в [Telegram](https://t.me/profitroll).

Приятного использования!

P.S.: Отдельное спасибо Kusyaka за помощь в создании сего творения. Без тебя, если честно, у меня бы ничего не вышло, дружище <3
