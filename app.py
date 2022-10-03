from flask import Flask
app = Flask(__name__)

@app.route('/')
def home_page():
    return '<p>This is the home page. <a href="/donation-form">Click here</a> to go to the donation page</p>'

@app.route('/login')
def login_page():
    return 'This is the login page.'

@app.route('/profile')
def profile_page():
    return 'This is the profile page.'

@app.route('/donation-form')
def donation_form_page():
    return 'This is the donation form page.'

@app.route('/fundraiser')
def fundraiser_page():
    return 'This is the fundraiser page.'

@app.route('/new-fundraiser-form')
def fundraiser_form_page():
    return 'This is the new fundraiser form page.'

@app.route('/new-user-form')
def new_user_form_page():
    return 'This is the New User form page.'

@app.route('/settings')
def settings_page():
    return 'This is the settings page.'

if __name__ == '__main__':
    app.run()