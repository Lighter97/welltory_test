# welltory_test
Этот скрипт позволяет проверить JSON-файлы на соответствие определённым схемам (стандарт JSON Schema).
В репозитории есть тестовые файлы: папка "event" с JSON-файлами и папка "schema" с файлами схем.

## Зависимости
 - fastjsonschema==2.14.5
 - Jinja2==2.11.2
 - MarkupSafe==1.1.1

## Установка зависимостей
``python -m pip install -r requirements.txt``

## Запуск скрипта
PowerShell:
``
python.exe .\validate.py
``  
bash:
``
python validate.py
``

## Настройка скрипта
В файле `config.py` можно прописать пути, по которым расположены соответствующие папки и файл шаблона:  
 - `EVENT_PATH` - путь к папке с JSON-файлами  
 - `SCHEMA_PATH` - путь к папке с файлами схем  
 - `TEMPLATE_FILE` - путь к файлу шаблона для генерации отчёта
 
После запуска скрипта он сгенерирует отчёт вида `report_DD-MM-YY_HH-mm.html`, где:
 - DD - день
 - MM - месяц
 - YY - год
 - HH - часы
 - mm - минуты
 
# Примерный отчёт

# Отчёт от 03-12-20 | 22-45

## Файл 1eba2aa1-2acf-460d-91e6-55a8c3e3b7a3

*   В поле ['data'] отсутствуют поля ['id', 'labels', 'rr_id', 'timestamp', 'unique_id', 'user', 'user_id']

## Файл 297e4dc6-07d1-420d-a5ae-e4aff3aedc19

*   В поле ['data'] отсутствуют поля ['source', 'timestamp', 'finish_time', 'activity_type', 'time_start', 'unique_id']

## Файл 29f0bfa7-bd51-4d45-93be-f6ead1ae0b96

*   Файл пуст

## Файл 2e8ffd3c-dbda-42df-9901-b7a30869511a

*   Не найдена схема meditation_created

## Файл 3ade063d-d1b9-453f-85b4-dda7bfda4711

*   Не найдена схема cmarker_calculated

## Файл 3b4088ef-7521-4114-ac56-57c68632d431

*   В поле ['data'] отсутствуют поля ['cmarkers', 'datetime', 'user_id']

### Проверено 10 JSON файлов.
