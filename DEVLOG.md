Day 1: Project setup and home page

I created the project folder in VS Code, made a virtual environment with
`python -m venv venv`, and tried to activate it. PowerShell blocked it with an
execution policy error, because Windows doesn't allow scripts to run by default.
I then opened a new terminal with the + button, and VS Code activated the venv
on its own using a session-only policy, so `(venv)` appeared in the prompt
without me changing any system settings.

After that I installed Flask and Flask-WTF, set up Git with a .gitignore before
my first commit so venv/ wouldn't get tracked, and pushed to GitHub. Then I built
the home page: a hardcoded list of services shown through base.html and home.html.
I changed the list to empty to test it, and the page showed "No services available"
instead of a blank screen, which is what I predicted.