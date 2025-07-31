import reflex as rx
from datetime import datetime
from typing import ClassVar

from app.template_loader import load_templates
from app.db import save_form, list_forms, get_form, update_form

class FormState(rx.State):
    templates: ClassVar[dict] = load_templates()
    selected_template: str = ""
    form_data: dict[str, str] = {}
    editing_id: int | None = None

    def start_new_form(self, template_name: str):
        """Begin a new form based on the given template."""
        self.selected_template = template_name
        self.editing_id = None
        self.form_data = {
            field["label"]: "" for field in self.templates[template_name]["fields"]
        }
        return rx.redirect("/fill")

    def load_form(self, form_id: int):
        """Load an existing form for editing."""
        form = get_form(form_id)
        if not form:
            return
        self.selected_template = form["template_name"]
        self.editing_id = form_id
        tmpl_fields = self.templates[self.selected_template]["fields"]
        self.form_data = {
            f["label"]: form["data"].get(f["label"], "") for f in tmpl_fields
        }
        return rx.redirect("/fill")

    def update_field(self, field_name: str, value: str) -> None:
        """Update a single field in the form data."""
        self.form_data[field_name] = value

    def submit(self) -> None:
        """Save or update the current form in the database and reset."""
        timestamp = datetime.now().isoformat()
        if self.editing_id is None:
            save_form(self.selected_template, timestamp, self.form_data)
        else:
            update_form(self.editing_id, self.selected_template, timestamp, self.form_data)
        self.reset_state()
        return rx.redirect("/")

    def reset_state(self) -> None:
        """Clear the currently selected template and reload templates."""
        self.selected_template = ""
        self.form_data = {}
        self.editing_id = None
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


def layout(*content: rx.Component) -> rx.Component:
    """Base layout with header and navigation buttons."""
    header = rx.hstack(
        rx.heading("Dynamic Form App"),
        rx.spacer(),
        rx.button("Home", on_click=lambda _: rx.redirect("/")),
        rx.button("Add Form", on_click=lambda _: rx.redirect("/add")),
        padding="1em",
    )
    body = rx.box(*content, padding="1em")
    return rx.vstack(header, rx.divider(), body)


def index() -> rx.Component:
    forms = list_forms()
    items = []
    for fid, name, ts in forms:
        edit_btn = rx.button(
            "Edit",
            # Reflex on_click handlers do not receive any arguments, so we wrap
            # the form ID using a default parameter.
            on_click=lambda _, f=fid: FormState.load_form(f),
        )
        items.append(rx.hstack(rx.text(f"{fid}. {name} @ {ts}"), edit_btn))
    add_button = rx.button('Add Form', on_click=lambda _: rx.redirect('/add'))
    content = rx.vstack(rx.heading('Completed Forms'), *items, add_button)
    return layout(content)


def add_form() -> rx.Component:
    """Page for selecting a template and displaying its form."""
    template_rows = []
    for name in FormState.templates.keys():
        template_rows.append(
            rx.hstack(
                rx.text(name),
                rx.button(
                    "Use this",
                    # The on_click event provides no arguments; capture the name
                    # with a default parameter instead of expecting a parameter.
                    on_click=lambda _, n=name: FormState.start_new_form(n),
                ),
            )
        )
    content = rx.vstack(*template_rows, form_fields())
    return layout(content)

def fill_form() -> rx.Component:
    """Page for filling out the currently selected template."""
    content = rx.vstack(
        rx.heading(
            rx.cond(
                FormState.selected_template != "",
                FormState.selected_template,
                "Fill Form",
            )
        ),
        form_fields(),
    )
    return layout(content)


app = rx.App()
app.add_page(index, route='/')
app.add_page(add_form, route='/add')
app.add_page(fill_form, route='/fill')

if __name__ == '__main__':
    app.run()
