# Reflex Dynamic Form App

This project demonstrates a simple Reflex application that loads form templates from JSON files and stores completed forms in SQLite.

## Folder Structure
- `forms/` – JSON templates.
- `database/` – SQLite database file `forms.db`.
- `scripts/` – Tools such as the Excel VBA macro.
- `tests/` – Unit tests.

## Running the App
Install dependencies and run the app:
```bash
pip install -r requirements.txt
python app.py
```

## Excel Template Export
A VBA module is provided in `scripts/excel_to_json.bas` that exports the active worksheet to a JSON file with the same name as the worksheet. Column A contains field labels. Column B contains either a data type (e.g., `text`, `number`) or a semicolon-separated list for dropdown choices.

## Tests
Run `pytest` to execute the unit tests.
