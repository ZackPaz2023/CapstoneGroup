from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('hello.html', name="Tricia", price="3")

@app.route('/login')
@app.route('/login/<name>')
def login_page(name=None):
    return render_template('hello.html', name=name)

@app.route('/profile')
def profile_page():
    return 'This is the profile page.'

@app.route('/donation-form')
def donation_form_page():
    return 'This is the donation form page.'

@app.route('/fundraiser/<fundraiser_name>')
def fundraiser_page(fundraiser_name=None):
    return render_template('fundraiser.html', fundraiser_name=fundraiser_name)

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