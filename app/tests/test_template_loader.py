import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from template_loader import load_templates

def test_load_templates(tmp_path, monkeypatch):
    # create sample template
    sample = tmp_path / "sample.json"
    sample.write_text('{"name": "Test", "description": "test", "fields": []}')
    monkeypatch.setattr('template_loader.TEMPLATE_DIR', tmp_path)
    templates = load_templates()
    assert 'Test' in templates
    assert templates['Test']['description'] == 'test'
