from flask import Flask, request, redirect, url_for
from flask import render_template
from DB_Connection import *

app = Flask(__name__)

class User:
    emailPK = ""
    name = "Guest"
    def __init__(self):
        self.isGuest = True

currentUser = User()

@app.route('/')
def home_page(): #create landing page later
    return render_template('login.html')

@app.route('/dashboard/<username>') # <username> be used to get username-info from MySQL database
def dashboard(username):
    cursor.execute("SELECT Title, Description, Goal, Balance FROM FUNDRAISER")
    homePageFundraiserData = cursor.fetchmany(20)  # size restricted to prevent overloading front page
    # **** dashboard expects USERNAME as a route parameter. use USERNAME to locate user records ****
    return render_template('hello.html', name=username, table=homePageFundraiserData)


@app.route('/login', methods = ['POST', 'GET']) #hardcoded database *currently*
def login():
    database = {"gib": "123", "scott": "111", "slow": "069"}  # replace with MySQL database

    if request.method == 'POST':
       name1 = request.form["username"]
       pwd = request.form["password"]

       if name1 in database and database[name1] == pwd: #if username is in database and if it matches
           return redirect(url_for('dashboard', username=name1))
       else:
           return redirect(url_for('login'))
    else:
       return render_template("login.html")

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