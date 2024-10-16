# ДЗ #9
1. Написать 10-20 автотестов на API Niffler


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
Так мы попадем в папку проекта тестов, где тесты лежат
```bash
python -m pytest tests/authorization/main/profile/test_profile.py tests/authorization/main/tests_main.py tests/authorization/test_authorization.py tests/registration/test_registration.py tests/test_presentation.py -v --alluredir=allure-result --clean-alluredir --allure-no-capture
```
```bash
python -m pytest tests_api -v --alluredir=allure-result --clean-alluredir --allure-no-capture
```
и сама команда для тестов(тут у нас также сгенерируется allure отчет)
```bash
allure serve .\allure-result\
```
Так запускаем allure отчет, чтобы на него посмотреть


----
команды, для обычного запуска автотестов(без allure)
```bash
python -m pytest tests_ui/presentation/test_presentation.py tests_ui/presentation/registration/test_registration.py tests_ui/presentation/authorization/test_authorization.py tests_ui/presentation/authorization/main/tests_main.py tests_ui/presentation/authorization/main/profile/test_profile.py -v  --env=.env
```
```bash
python -m pytest tests_api -v --env=.env
```
env необязательно указывать, он дефолтный env возьмет
```bash
python -m pytest tests_api -v
```
