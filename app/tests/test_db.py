import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
from db import save_form, list_forms, get_form, update_form, DB_PATH


def test_db_operations(tmp_path, monkeypatch):
    test_db = tmp_path / 'test.db'
    monkeypatch.setattr('db.DB_PATH', test_db)

    save_form('TestTemplate', '2023', {'a': 1})
    forms = list_forms()
    assert len(forms) == 1
    form_id, name, ts = forms[0]
    assert name == 'TestTemplate'

    form = get_form(form_id)
    assert form['data'] == {'a': 1}

def test_update_form(tmp_path, monkeypatch):
    test_db = tmp_path / 'test.db'
    monkeypatch.setattr('db.DB_PATH', test_db)

    save_form('Temp', '2023', {'a': 1})
    form_id = list_forms()[0][0]
    update_form(form_id, 'Temp', '2024', {'a': 2})
    form = get_form(form_id)
    assert form['data'] == {'a': 2}
    assert form['timestamp'] == '2024'
