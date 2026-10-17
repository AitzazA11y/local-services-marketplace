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

---------------------------------------------------------------------------------

## Day 4: Requests page and the in-memory problem

I added a /requests page that loops over the submitted requests and shows each
one with its service title. Each request only stores a service_id, and the view
looks up the title from the services list, the same way a foreign key works in
a database. With nothing submitted the page shows "No requests yet", and after
two submissions both were listed.

Then I stopped and restarted the app and the page was empty again, because the
requests live in a plain Python list in memory. Every restart wipes them, which
is why I will be adding a database later.

One thing I noticed is that anyone can open /requests and read every client's
name and contact. Clients should only see their own requests, providers only
the ones for their services, and the admin everything, which needs user accounts
and roles first.

---------------------------------------------------------------------------------

## Day 5: Moving to a database

This time, I replaced the in-memory data with a real database. I wrote models.py
with Service and ServiceRequest using Flask-SQLAlchemy and SQLite. A request
links to its service through a foreign key and a relationship, so
request.service gives me the whole service object. I also added seed.py to put
the three starting services into the database. It checks the row count first,
so running it twice doesn't create duplicates.

Then I tested saving a request for service 99, which doesn't exist. I expected
an error, but it saved. SQLite doesn't enforce foreign keys unless you turn them
on for each connection, so I ended up with an orphaned row pointing at a
service that isn't there. I deleted that row and enabled enforcement with
PRAGMA foreign_keys=ON. When I repeated the test it failed with an IntegrityError (FOREIGN KEY
constraint failed), which is the behavior I expected the first time and is the standard behavior that databases like PostgreSQL and MySQL have by default.

In the app itself, the route's 404 check catches a missing service first, and
the database constraint is the safety net behind it.

---------------------------------------------------------------------------------

## Day 6: Routes now use the database

I switched the app from the in-memory lists to the database. The home page and
the detail page now read services with Service.query.all() and
db.get_or_404(), which replaced my generator-expression lookup. The templates
didn't need any change, because Jinja's service.title works on a model object
the same way it did on a dictionary. The one place it broke was in Python code:
service['provider'] had to become service.provider, since a model object isn't
subscriptable.

The request form now saves a ServiceRequest to the database. I wrapped the
commit in a try/except that calls db.session.rollback() on failure, because a
failed commit leaves the session unusable, and the user gets a friendly message
instead of a crash page. The /requests page reads from the database too, newest
first, and uses the relationship (entry.service.title) instead of my old
manual title lookup.

To test it I submitted two requests, restarted the app, and both were still
there, which was the problem the in-memory list couldn't solve. After that I
deleted the old services and requests_list from app.py, since nothing used
them any more.

---------------------------------------------------------------------------------

## Day 7: User accounts and registration

I started on authentication on a new branch, add-authentication, after merging
the database work into main through a pull request. I added a User model with a
name, a unique email, a password hash and a role that defaults to client. The
table is named users on purpose, since "user" is a reserved word in PostgreSQL
and I plan to move to it later.

Passwords are never stored as typed. set_password() hashes them with Werkzeug,
and the database only holds the hash. I first called this "encrypted", but that
is wrong: encryption can be reversed with a key, while a hash is one-way. At
login the app will hash what the user types and compare the two hashes.

For registration I wrote a RegisterForm with Email(), a minimum password length
and EqualTo for the confirm field. I used PasswordField, not TextAreaField, so
the characters show as dots and the password isn't put back in the page when
the form comes back with errors. I tested the validators from the terminal with
bad data and got errors for the email format, the short password and the
mismatch, which is what I expected.

An email that is already taken is checked in two places. The form's
validate_email gives the user a clear message, and unique=True on the column is
the safety net in case two people register the same email at the same moment.
Emails are lowercased before saving so the same address in different capitals
counts as one account. The role is not a form field, so nobody can choose their
own role at signup.

---------------------------------------------------------------------------------

## Day 8: Login, logout and protecting the request form

I added login and logout with Flask-Login. After a correct login, login_user()
stores the user's id in the session cookie, and a user_loader function loads
the matching user on every later request. The navbar now checks current_user.is_authenticated.
If I'm logged in it shows the user's name and a Logout link, and if not it shows Login and Register links.

I put @login_required on the request form. When I visited it logged out, I was sent to the
login page with a message instead of seeing the form. I also tried a wrong password and a 
wrong email, and both gave the same message, "Invalid email or password." For security reasons,
I used the same message for both cases to prevent user enumeration. If the messages were different, anyone could use the login form to find out which emails have accounts, which leaks users' private information and makes them easier to target with guessed passwords or phishing.

After registering, I landed on the home page with "Account created" but I was
not logged in, which was confusing. I changed it so registration redirects to
the login page with "Account created. Please log in."

I decided to keep browsing public, so the home page and service pages are
visible to anyone, as on other marketplaces. Only actions and personal data
need a login.

Still open: /requests is visible to everyone and lists every client's name and
contact. @login_required alone won't fix it, because any logged-in user would
still see all requests. Each request has to be linked to the user who sent it,
which needs a new column and Flask-Migrate.