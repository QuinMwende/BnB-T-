# AiryB Django Project

This workspace contains the active Django project under `bnb_system/`.

## Project layout

- `bnb_system/` - main Django project package
- `bnb_system/manage.py` - project entry point
- `bnb_system/templates/` - HTML templates
- `bnb_system/static/` - static assets
- `bookings/`, `hotel/`, `payments/`, `properties/`, `reviews/`, `users/` - Django apps
- `.venv/` - Python virtual environment

## Run locally

1. Activate the virtual environment:
   - PowerShell: `\.venv\Scripts\Activate.ps1`
   - Command Prompt: `\.venv\Scripts\activate.bat`

2. Start the server from the workspace root:
   ```powershell
   python manage.py runserver
   ```

## Dependencies

See `requirements.txt`.
