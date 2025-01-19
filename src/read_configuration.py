import yaml


def read_configuration(*args):
    with open('config/config.yaml', 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    result = []
    for arg in args:
        result.append(data[arg])
    return result
