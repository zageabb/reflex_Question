import json
from pathlib import Path

TEMPLATE_DIR = Path('forms')


def load_templates():
    templates = {}
    for path in TEMPLATE_DIR.glob('*.json'):
        with open(path, 'r') as f:
            data = json.load(f)
            templates[data['name']] = data
    return templates
