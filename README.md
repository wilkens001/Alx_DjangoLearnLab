# Django LibraryProject

This is a Django project created as part of the ALX Django Learning Lab exercises.

## Project Structure

The project follows the standard Django project structure:

- `manage.py`: A command-line utility that lets you interact with this Django project in various ways.
- `LibraryProject/`
  - `__init__.py`: An empty file that tells Python that this directory should be considered a Python package.
  - `settings.py`: Settings/configuration for this Django project.
  - `urls.py`: The URL declarations for this Django project; a "table of contents" of your Django-powered site.
  - `asgi.py`: An entry-point for ASGI-compatible web servers to serve your project.
  - `wsgi.py`: An entry-point for WSGI-compatible web servers to serve your project.

## Project Components

### settings.py
The settings file contains all the configuration of your Django installation, including:
- Database configuration
- Installed applications
- Middleware setup
- Static files handling

### urls.py
The URL declarations for this Django project - effectively the "table of contents" of your Django-powered site.

### manage.py
A command-line utility that lets you interact with this Django project in various ways:
- Running the development server
- Creating database tables
- Creating new applications

## Development Server

To start the development server:
```bash
python manage.py runserver
```

Then visit http://127.0.0.1:8000/ to see the default Django welcome page.