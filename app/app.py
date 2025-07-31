import reflex as rx
from datetime import datetime
from typing import ClassVar

from app.template_loader import load_templates
from app.db import save_form, list_forms

class FormState(rx.State):
    templates: ClassVar[dict] = load_templates()
    selected_template: str = ""
    form_data: dict[str, str] = {}

    def select_template(self, template_name: str) -> None:
        """Choose a template and initialize blank form data."""
        self.selected_template = template_name
        self.form_data = {
            field["label"]: "" for field in self.templates[template_name]["fields"]
        }

    def update_field(self, field_name: str, value: str) -> None:
        """Update a single field in the form data."""
        self.form_data[field_name] = value

    def submit(self) -> None:
        """Save the current form to the database and reset."""
        timestamp = datetime.now().isoformat()
        save_form(self.selected_template, timestamp, self.form_data)
        self.reset_state()

    def reset_state(self) -> None:
        """Clear the currently selected template and reload templates."""
        self.selected_template = ""
        self.form_data = {}
        FormState.templates = load_templates()


def form_fields():
    tmpl = FormState.templates.get(FormState.selected_template)
    if not tmpl:
        return rx.fragment()
    controls = []
    for field in tmpl["fields"]:
        label = field["label"]
        if field["type"] == "dropdown":
            control = rx.select(
                field["choices"],
                on_change=lambda v, lbl=label: FormState.update_field(lbl, v),
            )
        else:
            control = rx.input(
                on_change=lambda v, lbl=label: FormState.update_field(lbl, v)
            )
        controls.append(rx.vstack(rx.text(label), control))
    return rx.vstack(*controls, rx.button('Submit', on_click=FormState.submit))


def index() -> rx.Component:
    forms = list_forms()
    items = [
        rx.hstack(rx.text(f"{fid}. {name} @ {ts}")) for fid, name, ts in forms
    ]
    add_button = rx.button('Add Form', on_click=lambda: rx.redirect('/add'))
    return rx.vstack(rx.heading('Completed Forms'), *items, add_button)


def add_form() -> rx.Component:
    dropdown = rx.select(FormState.templates.keys(), on_change=FormState.select_template)
    return rx.vstack(dropdown, form_fields())

app = rx.App()
app.add_page(index, route='/')
app.add_page(add_form, route='/add')

if __name__ == '__main__':
    app.run()
