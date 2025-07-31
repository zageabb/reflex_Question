import reflex as rx
from datetime import datetime

from app.template_loader import load_templates
from app.db import save_form, list_forms

class FormState(rx.State):
    templates = load_templates()
    selected_template: str = ''
    form_data: dict = {}

    def select_template(self, template_name: str):
        self.selected_template = template_name
        self.form_data = {field['label']: '' for field in self.templates[template_name]['fields']}

    def submit(self):
        timestamp = datetime.now().isoformat()
        save_form(self.selected_template, timestamp, self.form_data)
        self.reset_state()

    def reset_state(self):
        """Clear the currently selected template and reload templates."""
        self.selected_template = ''
        self.form_data = {}
        FormState.templates = load_templates()


def form_fields():
    tmpl = FormState.templates.get(FormState.selected_template)
    if not tmpl:
        return rx.fragment()
    controls = []
    for field in tmpl['fields']:
        label = field['label']
        if field['type'] == 'dropdown':
            control = rx.select(field['choices'], on_change=FormState.form_data[label].set)
        else:
            control = rx.input(on_change=FormState.form_data[label].set)
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
    options = list(FormState.templates.keys())
    dropdown = rx.select(options, on_change=FormState.select_template)
    return rx.vstack(dropdown, form_fields())

app = rx.App()
app.add_page(index, path='/')
app.add_page(add_form, path='/add')

if __name__ == '__main__':
    app.run()
