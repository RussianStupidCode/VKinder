# [VKinder](https://github.com/netology-code/py-advanced-diplom) - Tinder для бедных

## Приложение подбирает подходящих пользователей по устанавливаемым критериям

# Вход в приложение 
При запуске приложени вам будет предложен ввод токена пользователя от вконтакте 
```
Введите токен:
```
Вы можете ввести свой или стандартный
```
958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008
```
При успешном вводе выведется 
```
Токен сохранен успешно
```

Иначе дальше пройти не получится. Наличие токена обязательное условие.

# Список команд
Приглашение для ввода команд
```
Введите команду:
```

чтобы узнать список команд достаточно ввеси команду ```help```

Результат команды ```help```
```
Список команд:
        gsu - получить подходящих пользователей по критериям
        gcl - получить список установленных критериев
        exit - выход
        help - справка
        sc - установить (изменить) критерии
        afu - добавить пользователя в избранное
        gfu - получить список избранных пользователей
        cu - сменить пользователя
```

* ### ```gsu``` - получение списка подходящих пользователей
    Спустя примерно 3 секунды веведется список подходящих пользователей
    ```
    {'url': 'https://vk.com/id9814282', 'photo': ['https://sun9-80.userapi.com/c9628/u9814282/-6/x_552f0481.jpg']}
    {'url': 'https://vk.com/id304374583', 'photo': ['https://sun9-5.userapi.com/impf/c637928/v637928344/57338/eZw4d5xrGrU.jpg?size=743x1080&quality=96&sign=f543e53d13f02bd23079c1bfb78e8985&c_uniq_tag=Ney4D6R62tPDVIzFOodvR7p29jJ1O1mQDbR3dk54IiU&type=album', 'https://sun9-42.userapi.com/impf/c638627/v638627583/1696d/Ycah51wagMA.jpg?size=810x1080&quality=96&sign=308c3ad8d4e56787e0613f6cbbb6a539&c_uniq_tag=7XE1ZK9ftoLmTkLnxL48vRruD0ZqDWM7UEeHW-t4BVE&type=album', 'https://sun9-42.userapi.com/impf/c624625/v624625583/323f7/VF5juF18pz0.jpg?size=870x652&quality=96&sign=43ea4c7f0c36c60f8b1dbaf0bd46a150&c_uniq_tag=CsKXbuAUKgXIT7teJqPFW3QXJmzSgCAZCm-D6YIAJDY&type=album']}
    {'url': 'https://vk.com/id196517166', 'photo': ['https://sun9-53.userapi.com/impf/dgDkYB2zzZ_3yUi5YN3ORKcwi-gKeFlrEfDoHg/00zEkSyM-d0.jpg?size=250x375&quality=96&sign=5f4a5d465fade7c620c80ef43ce95301&c_uniq_tag=2XHhL7au1Yewvi32FT0xiTlp6wq-_9OcBiELRXKMqPw&type=album', 'https://sun9-62.userapi.com/impf/c630827/v630827166/a3a6/bKawi383duU.jpg?size=338x700&quality=96&sign=56936ba469fc17d199f14f38886724fb&c_uniq_tag=KiYkmbqHd_2X2JgZne7uSxXXGkyoKs3mRKl1D7hxkUY&type=album', 'https://sun9-18.userapi.com/impf/c622228/v622228166/433a1/wv-4ft4X-Bk.jpg?size=442x1080&quality=96&sign=a50d9db1314a47e65f5d0d2ae9730263&c_uniq_tag=Cjrf1R1zvKhp1ET8v9zHfMebrn7YWDQpn4o5Yp3i0mQ&type=album']}
    ```
    При повторном запросе в рамках одного запуска пользователи не повторяются.  
    Дополнительно из списка выдачи исключаются пользователи добавленные в избранное  
    
    Когда пользователи по подходящим критериям исчерпаются при вводе команды выведется
    ```
  Не найдено подходящих пользователей. Измените критерии поиска
    ```