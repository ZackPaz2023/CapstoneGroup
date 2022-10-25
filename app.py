import time
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
    cursor.execute("SELECT Title, Description, FundID FROM FUNDRAISER")
    homePageFundraiserData = cursor.fetchall()
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

@app.route('/donation-form/<fund_ID>')
def donation_form_page(fund_ID=None):
    cursor.execute("SELECT StreetAddress, City, State, ZipCode, Country, CardNumber, ExpirationDate, RouteNo, AccountNo  FROM USER WHERE Email = '%s'" % currentUser.emailPK)
    userInfo = cursor.fetchall()
    userInfoList = []
    for row in userInfo:
        for attribute in row:
            userInfoList.append(attribute)
    restOfAddress = userInfoList[1] + " " + userInfoList[2] + " " + str(userInfoList[3]) + " " + userInfoList[4]

    cursor.execute("SELECT * FROM FUNDRAISER WHERE FundID = '%s'" % fund_ID)
    fundraiserInfo = cursor.fetchall()
    fundraiserInfoList = []
    for line in fundraiserInfo:
        for item in line:
            fundraiserInfoList.append(item)
    return render_template('new-donation.html', fundraiser_ID=fund_ID ,fundraiser_name = fundraiserInfoList[0], name=currentUser.name, email=currentUser.emailPK, streetAddress=userInfoList[0], restOfAddress=restOfAddress, cardNum=str(userInfoList[5]), expirationDate=str(userInfoList[6]), routeNo=str(userInfoList[7]), accountNo=str(userInfoList[8]))


@app.route('/submittingDonation', methods=["POST"])
def recordingDonation():
    amount = request.form["amount"]
    email = request.form["email"]
    fund_id = request.form["fund_id"]

    # inserting new record into DONATES table
    cursor.execute("SELECT EmailAddress, FundNo FROM DONATES WHERE EXISTS (SELECT 1 FROM DONATES WHERE EmailAddress = %s AND FundNo = %s)" , (email, fund_id))
    doesExistInDB = cursor.fetchall()
    if not doesExistInDB:
        cursor.execute("INSERT INTO DONATES (EmailAddress, FundNo, DonationsToFund) VALUES (%s,%s,%s)", (email, fund_id, amount))
    else:
        cursor.execute("UPDATE DONATES SET DonationsToFund = DonationsToFund + %s WHERE (EmailAddress = %s AND FundNo = %s)", (int(amount), email, fund_id))

    #Inserting new record into DONATION table
    cursor.execute("INSERT INTO DONATION (DonationAmount, TransactionDate) VALUES (%s, %s)", (amount, time.strftime('%Y-%m-%d %H:%M:%S')))

    #inserting new record into GIVES table
    cursor.execute("SELECT LAST_INSERT_ID()")
    transactionID = cursor.fetchone()[0]
    cursor.execute("INSERT INTO GIVES (EmailAddress, TransactionNo) VALUES (%s, %s)", (email, transactionID))

    #Inserting new record into FUNDS table
    cursor.execute("INSERT INTO FUNDS (TransactionNo, FundNo) VALUES (%s,%s)", (transactionID, fund_id))
    db.commit()
    return redirect(url_for('dashboard'))


@app.route('/fundraiser/<fundraiser_ID>')
def fundraiser_page(fundraiser_ID=None):
    cursor.execute("SELECT Title, Description, Goal, Balance, CreationDate, Timeframe FROM FUNDRAISER WHERE FundID = '%s'" % fundraiser_ID)
    fundraiserInfo = []
    for line in list(cursor):
        for item in line:
            fundraiserInfo.append(item)

    #Reformatting time constraints to be more user friendly
    fundraiserCreationDate = str(fundraiserInfo[4])[0:10]
    fundraiserCreationDate = fundraiserCreationDate[5:8] + fundraiserCreationDate[8:10] + "-" + fundraiserCreationDate[0:4]
    fundraiserTimeline = str(fundraiserInfo[5])[0:10]
    fundraiserTimeline = fundraiserTimeline[5:8] + fundraiserTimeline[8:10] + "-" + fundraiserTimeline[0:4]

    cursor.execute("SELECT Name, DonationsToFund FROM USER INNER JOIN DONATES ON Email = EmailAddress WHERE fundNo = %s" % fundraiser_ID)
    donationTable = cursor.fetchall()
    balance = 0.00
    for donation in donationTable:
        balance += float(donation[1])

    return render_template('fundraiser.html', fund_ID = fundraiser_ID, fund_name=fundraiserInfo[0], fund_desc = fundraiserInfo[1], fund_goal = fundraiserInfo[2], fund_balance = balance, fund_creationdate = fundraiserCreationDate, fund_timeline = fundraiserTimeline, table = donationTable)

@app.route('/new-fundraiser')
def fundraiser_form_page():
    return render_template('new-fundraiser-form.html')

@app.route('/fillingNewFundraiserForm', methods=["POST"])
def recordNewFundraiserrForm():
    title = request.form["title"]
    description = request.form["description"]
    goal = request.form["goal"]
    day = request.form["day"]
    if int(day) < 10:
        day = "0%s" % day
    timeline = request.form["Year"] + '-' + request.form["Month"] + '-' + day
    creation = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO FUNDRAISER (Title, Description, Goal, CreationDate, Timeframe) VALUES (%s,%s,%s,%s,%s)", (title, description, goal, creation, timeline))
    cursor.execute("SELECT LAST_INSERT_ID()")
    FundID = cursor.fetchone()[0]
    cursor.execute("INSERT INTO OWNS (EmailAddress, FundNo) VALUES (%s, %s)", (currentUser.emailPK, FundID))
    db.commit()

    return redirect(url_for('dashboard'))

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