## Day 1: Project setup and home page

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

---------------------------------------------------------------------------------

## Day 2: Service detail page and 404 handling

I built the service detail page today, the lookup, and 404 error handling.
Initially I faced some confusion understanding the generator expression syntax:

(s for s in services if s['id'] == service_id)

I thought the first `s` was redundant and we could achieve the purpose without
it, but when I tried that it gave an "Invalid Syntax Error." When I explored it,
I learned that the leading expression tells Python what to produce for each
match, not just which items to visit.

Then I tested it by visiting a service that doesn't exist yet, like /service/99,
to check if the program handles that gracefully. It correctly showed the 404
page.

---------------------------------------------------------------------------------

## Day 3: Service request form

I added a request form to each service using Flask-WTF. `RequestForm` in
`forms.py` uses `DataRequired` and `Length` validators, and I moved the
"find the service or abort(404)" lookup into a helper, `get_service_or_404`,
since two routes needed it.

My first empty-form test only showed "Please fill out this field". That is the
browser's own check, so it never reached Flask and proved nothing about my
validation. I added `novalidate` to the form tag to switch it off, and then
WTForms returned "This field is required." and the `Length` error for a short
message, which confirmed the server-side validation works. The fields I had
already filled stayed in place after an error because the form object holds the
submitted data. I removed `novalidate` afterwards, so users still get the
browser check, but the server check is the one that protects the app.

After a valid submit the route redirects to the detail page (Post/Redirect/Get)
and shows a flash message, so refreshing the page can't save the request twice.
Requests are stored in an in-memory list, so they disappear whenever the app
restarts. That is the reason I will be adding a database later.