



# ДЗ #5
1. Провести рефакторинг готовых тестов из предыдущего задания - выделить подготовительные шаги, данные и шаги после теста в фикстуры, можно  реализовать через хелперы фикстур
2. Расширить тестовое покрытие добавив еще 10 тестов с учетом полученных знаний о фикстурах

# ДЗ #6
1. Добавить тесты с бд:

- через UI или API добавляем, изменяем, удаляем сущность
- проверяем в БД корректность данных

2. Добавить/доработать сценарии, где без запроса в БД невозможно реализовать (по примеру с удалением категории)


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
cd ..
```
Так мы попадем в корень проекта, где тесты лежат
```bash
pytest niffler_e_2_e_tests_python/presentation/authorization/main/profile/test_profile.py niffler_e_2_e_tests_python/presentation/authorization/main/tests_main.py niffler_e_2_e_tests_python/presentation/authorization/test_authorization.py niffler_e_2_e_tests_python/presentation/registration/test_registration.py niffler_e_2_e_tests_python/presentation/test_presentation.py -v --alluredir=allure-result --clean-alluredir
```
и сама команда для тестов
```bash
allure serve
```


