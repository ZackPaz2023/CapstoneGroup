from flask import Flask, request, redirect, url_for
from flask import render_template
from DB_Connection import *
from DummyInfo import monthLengths

app = Flask(__name__)

class User:
    emailPK = ""
    name = ""
    username = ""
    def __init__(self):
        self.isGuest = True
        self.name = "Guest"

currentUser = User()

@app.route('/')
def home_page(): #create landing page later
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT Title, Description, Goal, Balance, FundID FROM FUNDRAISER")
    homePageFundraiserData = cursor.fetchmany(20)  # size restricted to prevent overloading front page
    return render_template('dashboard.html', name=currentUser.name, table=homePageFundraiserData)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    cursor.execute("SELECT Username FROM USER")
    DB_Usernames = list(cursor)
    #DB_Usernames usernames returned in ("string",) format. Usernames were reformatted below for comparison operations.
    DB_UsernamesReformatted = []
    for name in DB_Usernames:
        DB_UsernamesReformatted.append(name[0])

    if request.method == 'POST':
        userName = request.form["username"]
        password = request.form["password"]

        if userName in DB_UsernamesReformatted:
            cursor.execute("SELECT Password FROM USER WHERE Username = '%s'" % userName)
            DB_Password = cursor.fetchone()[0]
            if password == DB_Password:
                currentUser.isGuest = False
                cursor.execute("SELECT Name, Email, Username FROM USER WHERE UserName = '%s'" % userName)
                nameAndEmail = cursor.fetchmany(2)
                currentUser.name = nameAndEmail[0][0]
                currentUser.emailPK = nameAndEmail[0][1]
                currentUser.username = userName
                return redirect(url_for('dashboard'))
            else:
                #incorrect password
                return redirect(url_for('login'))
        else:
            #inccorrect Username
            return redirect(url_for('login'))
    else:
        return render_template("login.html")

@app.route('/profile')
def profile_page(name=None, email=None):
    return render_template('profile.html', name=name, email=email)

@app.route('/donation-form')
def donation_form_page(name=None):
    cursor.execute("SELECT StreetAddress, City, State, ZipCode, Country, CardNumber, ExpirationDate, RouteNo, AccountNo  FROM USER WHERE Email = '%s'" % currentUser.emailPK)
    userInfo = cursor.fetchall()
    userInfoList = []
    for info in userInfo:
        for item in info:
            userInfoList.append(item)
    restOfAddress = userInfoList[1] + " " + userInfoList[2] + " " + str(userInfoList[3]) + " " + userInfoList[4]
    return render_template('new-donation.html', name=currentUser.name, email=currentUser.emailPK, streetAddress=userInfoList[0], restOfAddress=restOfAddress, cardNum=str(userInfoList[5]), expirationDate=str(userInfoList[6]), routeNo=str(userInfoList[7]), accountNo=str(userInfoList[8]))

@app.route('/fundraiser/<fundraiser_ID>')
def fundraiser_page(fundraiser_ID=None):
    cursor.execute("SELECT Title, Description, Goal, Balance, CreationDate, Timeframe FROM FUNDRAISER WHERE FundID = '%s'" % fundraiser_ID)
    fundraiserInfo = []
    for line in list(cursor):
        for item in line:
            fundraiserInfo.append(item)

    return render_template('fundraiser.html', fund_name=fundraiserInfo[0], fund_desc = fundraiserInfo[1], fund_goal = fundraiserInfo[2], fund_balance = fundraiserInfo[3], fund_creationdate = fundraiserInfo[4], fund_timeline = fundraiserInfo[5])

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
    expirationDate = request.form["Year"] + "-" + request.form["Month"] + "-" + str(monthLengths(int(request.form["Month"]), int(request.form["Year"])))
    print(expirationDate)
    routingNumber = request.form["RoutingNumber"]
    accountNumber = request.form["AccountNumber"]

    cursor.execute("INSERT INTO USER (Username, Password, Email, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country, CardNumber, ExpirationDate, RouteNo, AccountNo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (userName, password, email, name, phoneNumber, zipCode, streetAddress, state, city, country, cardNumber, expirationDate, routingNumber, accountNumber))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/settings')
def settings_page():
    return 'This is the settings page.'

if __name__ == '__main__':
    app.run()