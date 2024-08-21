



# ДЗ #4
1) Запустить локально niffler и убедиться, что регистрация / логин работают. Без локально работающего niffler дальнейшее обучение будет невозможно, по всем проблемам пишите в чат 1-го потока. В случае вечного loader на логине - пробуем incognito window или почистить руками cookies, session storage, local storage.

2) Написать 10 UI тестов. Использовать можно selenium, selene, playwright

Рекомендуется шаги, такие как логин (если это не тест логина), добавление сущностей которые необходимы в тесте, возможно удаление сущностей после теста, реализовать через АПИ с помощью библиотеки requests



Формат сдачи ДЗ: домашнее задание должно включать в себя PR в ВАШ ФОРК репозитория https://github.com/qa-guru/niffler-st5


**Установка**

Клонируйте репозиторий:
```bash
git clone <URL этого репозитория>
```

Перейдите в директорию проекта:
```bash
cd <имя директории куда скачали репозиторий>
cd .\niffler_e_2_e_tests_python\
```

Установите необходимые зависимости:
```bash
pip install -r requirements.txt
playwright install
cd ..
```


**Запуск**

Поднимаем Приложение в контейнере, выполните команду:
README."Минимальные предусловия для работы с проектом Niffler" выполнить шаги 1,2,7,8
README."Запуск Niffler в докере" Выполнить 4 и 6 шаг(в 6-ом выполняем там где REST указан)

Запуск проверялся только на windows 10, работало
если вдруг не заработает, то у меня база данных падала, проверьте, что postgres/init-database.sh , в самом файле символы окончания строки стоит LF и только это(можно через Notepad++ посмотреть)

**Тестирование**

Для запуска тестов используйте:
Перед тем как запустить тесты откройте новую console, чтобы там ввести эту команду

```bash
cd .\niffler_e_2_e_tests_python\
```
Так мы попадем в папку, где тесты лежат
```bash
pytest .\ -v
```
и сама команда для тестов


pytest niffler_e_2_e_tests_python/presentation/authorization/main/profile/test_profile.py niffler_e_2_e_tests_python/presentation/authorization/mai
n/tests_main.py niffler_e_2_e_tests_python/presentation/authorization/test_authorization.py niffler_e_2_e_tests_python/presentation/registration/test_registration.py niffler_e_2_e_test
s_python/presentation/test_presentation.py -v
