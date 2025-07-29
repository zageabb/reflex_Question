# Development Tasks for Dynamic Reflex Form App

This document outlines steps to build an application using Python and [Reflex](https://reflex.dev) for managing dynamic forms. The app will load form templates from JSON files, display them in the UI, store completed forms in SQLite, and provide a VBA tool to convert Excel worksheets into template JSON files.

## 1. Project Setup
- Initialize a new Python project and install Reflex.
- Configure SQLite only for the `completed_forms` table used to store submitted forms.
- Create folder structure:
  - `forms/` for JSON templates.
  - `database/` for the SQLite file.
  - `scripts/` for helper tools (e.g., Excel conversion).

## 2. Excel to JSON Conversion Tool
- Write a VBA macro that reads the active worksheet and outputs a JSON file.
- The worksheet name becomes the template name.
- Row 1 is the template description.
- Column A lists field names; column B lists either drop-down choices or a data type for entry (text, number, date, etc.).
- Export possible selections and data types so the Python app can build the form dynamically.

## 3. Form Template Loader
- Implement a Python utility to read template JSON files directly from `forms/` when the app starts or when templates change (without inserting them into a database).
- Ensure each template JSON file includes a unique identifier and description.

## 4. Reflex Application
1. Build a home page showing a list of completed forms with a brief summary (e.g., template name and timestamp).
2. Add an "Add Form" button that opens a page with a dropdown listing available templates from the file system (`forms/` directory).
3. When a template is selected, generate the form dynamically based on the template JSON:
   - Text fields for free input.
   - Dropdowns for predefined choices.
   - Basic data validation using the specified data types.
4. On submission, store the filled-in data as JSON in the `completed_forms` table with a unique description (timestamp-based).
5. Provide a page to view or download previously completed forms.

## 5. Database Schema
- `completed_forms` table: `id`, `template_name`, `timestamp`, `form_json`. Templates are stored as JSON files, so no `templates` table is required.

## 6. Retrieval and Display
- Implement endpoints in Reflex to fetch completed form data for display or editing.
- Show stored forms on the main page with options to view the details.

## 7. Testing
- Create unit tests for the template loader (which reads JSON files), form submission logic, and database interactions.
- Manually verify the VBA export by generating a sample template and importing it into the app.

## 8. Future Enhancements
- User authentication for form access.
- Better input validation and custom form widgets.

