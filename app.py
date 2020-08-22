import os
# * These are environment variables that you set
# * when running this application LOCALLY.
# ! You do not need this when the application is deployed.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

from credentials import client_id, client_secret

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YerSecretKey'

# Check documentation for possible parameters
# ! By default, 'offline' should be False.

# * Get client_id and client_secret from the Google APIs developer console.
# * https://console.developers.google.com
# Create a project, then create an OAuth consent screen and lastly, create a credential for your Web Application.
# ! The client_id and client_secret are from the credentials.py file, which is a file that is not included in the Git repository.
blueprint = make_google_blueprint(client_id=client_id,
                                    client_secret=client_secret, 
                                    offline=True,
                                    scope=['profile', 'email'])

app.register_blueprint(blueprint, url_prefix='/login')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
def welcome():
    # ! Returns an internal server error when not logged in.

    # This picks up the user information (resp = response)
    # ! Check with documentation if the string is still the same, as it can change.
    resp = google.get('/oauth2/v2/userinfo')
    
    # Checks if there's a response and records it.
    assert resp.ok, resp.text

    # This sets the data that can be collected from the user
    # The Google log-in page also adds the fields specified here
    # if the user will consent on the access.
    email = resp.json()['email']

    return render_template('welcome.html', email=email)

@app.route('/login/google')
def loginOAuthGoogle():

    # Checks if the user is already logged in through Google
    if not google.authorized:
        # Automatically redirects user to the Google Login page.
        return render_template(url_for('google.login'))

    # This picks up the user information (resp = response)
    # ! Check with documentation if the string is still the same, as it can change.
    resp = google.get('/oauth2/v2/userinfo')
    
    # Checks if there's a response and records it.
    assert resp.ok, resp.text

    # This sets the data that can be collected from the user
    # The Google log-in page also adds the fields specified here
    # if the user will consent on the access.
    email = resp.json()['email']

    # Automatically redirects user to Welcome
    return render_template('welcome.html', email=email)

if __name__ == "__main__":
    app.run()
