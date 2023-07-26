import json

from json import JSONDecodeError


def parse_json(line):
    try:
        return json.loads(line)
    except JSONDecodeError:
        return None


def parse_messages(lines):
    collect = []
    for line in lines.splitlines():
        parsed_line = parse_json(line)
        if parsed_line:
            collect.append(parsed_line)
    return collect


def pp_json(json_object):
    print(json.dumps(json_object, indent=2))
