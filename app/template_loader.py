"""Utility for loading form templates from JSON files."""

import json
from pathlib import Path

# Locate the ``forms`` directory relative to this file so the app can be
# executed from any working directory.
TEMPLATE_DIR = Path(__file__).parent / "forms"


def load_templates():
    templates = {}
    for path in TEMPLATE_DIR.glob('*.json'):
        with open(path, 'r') as f:
            data = json.load(f)
            templates[data['name']] = data
    return templates
