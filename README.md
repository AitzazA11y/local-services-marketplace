# Local Services Marketplace

A Flask web app where people can browse local service providers (plumbers,
electricians, tutors) and send a request to one of them.

## Current status

Early development. Data is hardcoded and held in memory, so submitted requests
are lost when the app restarts. A database, user accounts and role-based access
are planned next.

## Features so far

- Browse services and view a detail page for each
- Request a service through a validated form (Flask-WTF, CSRF protection)
- Custom 404 page for services that don't exist
- Requests page listing submitted requests

## Run locally

    git clone https://github.com/AitzazA11y/local-services-marketplace.git
    cd local-services-marketplace
    python -m venv venv

Activate the virtual environment:

- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

Then install the packages and start the app:

    pip install -r requirements.txt
    python app.py

Then open the address shown in the terminal (usually http://127.0.0.1:5000)

## Project log

See DEVLOG.md for what I built, what broke, and how I fixed it.