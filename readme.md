# VK-Hater-Bot
Бот, который гневно комментирует сообщения людей из хейт листа в беседах и лс. Размещение - группа/страница.
## Команды
+хейт - добавляет пользователя из пересланного сообщения в хейт лист

-хейт - убирает пользователя из пересланного сообщения из хейт листа

!кд <секунды> - задержка перед отправкой сообщения
## Настройка бота для страницы
Заполняем поля файла config.py:
```
u_admins = [] - айди страниц, которые смогут отдавать команды боту
bot_id = - айди страницы бота
u_token = '' - токен страницы бота
```
Токен получаем [здесь](https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1)

## Настройка бота для группы
Заполняем поля файла config.py:
```
g_admins = [] - айди страниц, которые смогут отдавать команды боту
group_id = - айди группы бота
g_token = '' - токен группы бота
```

Для получения айди группы переходим в нужную группу:
```
Управление -> Настройки -> Адрес сообщества -> Номер сообщества -> club*цифры* -> Копируем только цифры
```
Для получения токена группы переходим в нужную группу:
```
Управление -> Настройки -> Работа с API -> Создать ключ -> Выставляем галочки и создаем
```
Также нужно настроить Long Poll API для бота:
```
Управление -> Настройки -> Работа с API -> Long Poll API -> Long Poll API: Включено + Версия API: 5.92 -> Типы событий -> Выставляем галочки
```
И последний шаг:
```
Управление -> Сообщения -> Сообщения сообщества: Включены -> Настройки для бота -> Возможности ботов: Включены -> Разрешать добавлять сообщество в беседы - ставим галочку
```
