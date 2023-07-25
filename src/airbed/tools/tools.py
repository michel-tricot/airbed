import json

from json import JSONDecodeError



def parse_messages(lines):
    collect = []
    for line in lines.splitlines():
        try:
            collect.append(json.loads(line))
        except JSONDecodeError:
            pass
    return collect


def pp_json(json_object):
    print(json.dumps(json_object, indent=2))
