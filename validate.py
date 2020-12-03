# -*- coding: utf-8 -*-
import codecs
import datetime
import json
from pathlib import Path

from fastjsonschema import JsonSchemaException, compile
from jinja2 import Template

from config import EVENT_PATH, SCHEMA_PATH, TEMPLATE_FILE, REPORTS_PATH


def read_schemas(schemas_path):
    """
    Read all schemas
    Returns the list with schema files' paths
    """

    # Generate list of all schema files in directory
    p = Path(schemas_path).glob("*.schema")
    # Check if each item in list is not directory
    schemas_list = [x for x in p if x.is_file()]
    return schemas_list


def compile_schemas(schemas):
    """
    Compile all schemas
    Returns the dict where:
    key     - schema name
    value   - compiled validation function
    """

    schema_dict = {}
    for path in schemas:
        with open(path, "r") as schema_file:
            schema_dict[path.stem] = compile(json.loads(schema_file.read()))
    return schema_dict


def read_files(events_path):
    """
    Read all the event files
    Returns the list with event files' paths
    """

    # Generate list of all event files in directory
    p = Path(events_path).glob("*.json")
    # Check if each item in list is not directory
    events_list = [x for x in p if x.is_file()]
    return events_list


# Process all files
schemas = read_schemas(SCHEMA_PATH)
compiled_schemas = compile_schemas(schemas)
events = read_files(EVENT_PATH)

# Info for future report generation
file_reports = {}

for path in events:
    with open(path, "r") as event_file:
        # Extract filename
        file_name = path.stem
        # Process json to python dict
        file_dict = json.loads(event_file.read())
        # Add entry to report dictionary
        file_reports[file_name] = []

        # Check if file is empty
        if not file_dict:
            file_reports[file_name].append("Файл пуст")
            continue

        # Check if file has 'event' field
        if "event" not in file_dict:
            file_reports[file_name].append('Не найдено поле "event"')
            continue

        # Check if necessary schema is exist
        if file_dict["event"] not in compiled_schemas:
            file_reports[file_name].append(
                f'Не найдена схема {file_dict["event"]}'
            )
            continue

        try:
            # Validation function is in the compile_schemas() dict
            compiled_schemas[file_dict["event"]](file_dict)
        except JsonSchemaException as e:
            file_reports[file_name].append(
                f'В поле {e.path} отсутствуют поля {e.rule_definition}'
            )
        else:
            file_reports[file_name].append('Файл валиден')

""" Generate the report """
template = Template(open(TEMPLATE_FILE, 'r', encoding='utf-8').read())
now = datetime.datetime.now()

report_date = now.strftime('%d-%m-%y')
report_time = now.strftime('%H-%M')
report_filename = REPORTS_PATH / f'report_{report_date}_{report_time}.html'
# Create reports directory if not exists
Path(REPORTS_PATH).mkdir(exist_ok=True)

result_html = template.render(
    report_date=report_date,
    report_time=report_time,
    json_count=len(events),
    file_reports=file_reports,
)

with open(report_filename, 'w+', encoding='utf-8') as report_file:
    report_file.write(result_html)
