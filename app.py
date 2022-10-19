from flask import Flask, request, redirect, url_for
from flask import render_template
from DB_Connection import *

app = Flask(__name__)

@app.route('/')
def home_page(name=None, price=None):
    return render_template('hello.html', name=name, price=price)

@app.route('/login')
@app.route('/login/')
def login_page(username=None, password=None):
    return render_template('loginForm.html', username=username, password=password)

@app.route('/profile')
def profile_page(name=None, email=None):
    return render_template('profile.html', name=name, email=email)

@app.route('/donation-form')
def donation_form_page(name=None):
    return render_template('new-donation.html', name="tricia")

@app.route('/fundraiser/<fundraiser_name>')
def fundraiser_page(fundraiser_name=None):
    return render_template('fundraiser.html', fundraiser_name=fundraiser_name)

@app.route('/new-fundraiser-form')
def fundraiser_form_page():
    return 'This is the new fundraiser form page.'

@app.route('/new-user-form')
def new_user_form_page():
   return render_template("new-user-form.html")

@app.route('/fillingNewUserForm', methods=["POST"])
def recordNewUserForm():
    userName = request.form["UserName"]
    password = request.form["Password"]
    email = request.form["Email"]
    name = request.form["Name"]
    phoneNumber = request.form["PhoneNumber"]
    zipCode = request.form["ZipCode"]
    streetAddress = request.form["StreetAddress"]
    state = request.form["State"]
    city = request.form["City"]
    country = request.form["Country"]
    cardNumber = request.form["CardNumber"]
    #expirationDate = request.form["ExpirationDate"]
    expirationDate = "2022-10-10"
    routingNumber = request.form["RoutingNumber"]
    accountNumber = request.form["AccountNumber"]

    cursor.execute("INSERT INTO USER (Username, Password, Email, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country, CardNumber, ExpirationDate, RouteNo, AccountNo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (userName, password, email, name, phoneNumber, zipCode, streetAddress, state, city, country, cardNumber, expirationDate, routingNumber, accountNumber))
    db.commit()
    return redirect(url_for('home_page'))

@app.route('/settings')
def settings_page():
    return 'This is the settings page.'

if __name__ == '__main__':
    app.run()