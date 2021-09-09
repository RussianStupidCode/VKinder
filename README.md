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
    Спустя примерно 3 секунды выведется список подходящих пользователей
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
* ### ```gcl``` - получение списка установленных критериев
  Команда отображает список критериев для поиска  
  Критерии автоматически устанавливаются в зависимости от введенного токена пользователя
  
  Определяется город и противоположный пол (если указаны у пользователя токена)
  ```
  Список критериев:
    Возраст: от 0 до 9999 | необязательный | вес 1.0
    Пол: женщина | обяательный | вес 1.0
    Город: Оренбург | обяательный | вес 1.0
    Статус отношений: в активном поиске | обяательный  | вес 1.0

  ```
  Параметры имеют флажок (обязательный\необязательный) это эквиваентно включению или отключению критерия
  
  Результаты сортируются исходя из суммы весов совпадения по критериям
  
* ### ```sc``` - установка параметров поиска
  При вводе команды будет выведен список критериев которые можно изменять
  ```
  Список критериев: ['пол', 'возраст', 'город', 'статус']
  ```
  Для изменения необходимого критерия надо ввести его название
  ```
  Введите название критерия: пол
  ```
 
* ### ```afu``` - добавить пользователя в избранное по id
  добавить можно только пользователя, который выводился в качестве подходящий.
  
  при неуспешном добавлении будет ошибка
  ```
  Пользователь с таким id вам не показывался
  ```

* ### ```gfu``` - получить список избранных пользователей

  Пример вывода результатов при запросе команды
  ```
  {'url': 'https://vk.com/id9814282', 'photo': ['https://sun9-80.userapi.com/c9628/u9814282/-6/x_552f0481.jpg']}
  {'url': 'https://vk.com/id170210230', 'photo': ['https://sun9-40.userapi.com/impf/c307804/v307804230/3bf/y4kTYaa8B0M.jpg?size=226x604&quality=96&sign=4f67f77cc9f2cfaa5c310afbab396e56&c_uniq_tag=We6n6jy4ueB5NYTTV5lRVo1bS0-VEaB6XCBF0Aydhro&type=album', 'https://sun9-19.userapi.com/impf/c9270/v9270230/1cbb/zBL-oxt3i64.jpg?size=231x604&quality=96&sign=dec66c5703f6c39df8d39eff90df3269&c_uniq_tag=zF-pUUa20yulw97r0qURFLC_8Y1dCRjZg5dPokQAUS8&type=album', 'https://sun9-3.userapi.com/c5193/u170210230/-6/x_e85c993c.jpg']}
  {'url': 'https://vk.com/id401731991', 'photo': ['https://sun9-33.userapi.com/impg/1Pj8ZLhdUmHkTF4J03HVtZdlmHPdt3dwbsXIJg/e1ONv2A5vuk.jpg?size=864x1080&quality=96&sign=b86037ed449b276ac19354f5be960f0d&c_uniq_tag=jxiDB8evVgRX-iu5-nWmRgFvUF5Qboau6n-Cfs9AVMw&type=album', 'https://sun9-17.userapi.com/impg/q_fFnMGCX2nq_Ql5nfosySfGTP5v5_mucu-pEA/YXWAChMFoHI.jpg?size=510x608&quality=95&sign=b37edf713c789511665dba73c689c73c&c_uniq_tag=c4UmmQkaFgLjlG4QalqLmTrkuZOZTmnnW-gfkgX32Ss&type=album', 'https://sun9-67.userapi.com/impg/yd7rL31rVOdPlKTlYKEi6Vsl51Vkh_NdpEWM-Q/GC_jyslIgy8.jpg?size=540x544&quality=96&sign=a9e5b4176cdf14d49ec1ee60d8d0e3a1&c_uniq_tag=xCgIvBrjIh4S8mbc4Nr-vVh7fFedAkQTvcSyrEWMZdA&type=album']}
  ```

* ### ```cu``` - установить пользователя для которого будет осуществляться поиск
  Пользователь устанавливается по id
  После смены пользователя отобразится список автоматически установленных критериев
  ```
  Введите команду: cu
  Введите id пользователя: 1
  Список критериев:
    Возраст: от 0 до 9999 | необязательный | вес 1.0
    Пол: женщина | обяательный | вес 1.0
    Город: Санкт-Петербург | обяательный | вес 1.0
    Статус отношений: в активном поиске | обяательный  | вес 1.0
  ```
  Список избранных пользователей у каждого свой