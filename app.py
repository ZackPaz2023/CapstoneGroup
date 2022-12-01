import os
import time
import pathlib
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, jsonify
from flask import render_template
from DB_Connection import *
from DummyInfo import monthLengths
from ValidateNewData import valid_new_user_input, valid_new_donation_input, valid_new_fundraiser_input

app = Flask(__name__, static_url_path='/static')
app.config['UPLOADED_FILES'] = "static/"


class User:
    emailPK = ""
    name = ""
    username = ""

    def __init__(self):
        self.isGuest = True
        self.name = "Guest"


currentUser = User()
newUserFlags = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
newFundraiserFlags = [0, 0]
newDonationFlags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
inputData = []
loginFlag = 0


@app.route('/')
def home_page():  # create landing page later
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    global newUserFlags, newDonationFlags, newFundraiserFlags, inputData
    newUserFlags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    newDonationFlags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    newFundraiserFlags = [0, 0]
    inputData = []
    cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name, Email FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID")
    homePageFundraiserData = cursor.fetchall()

    if not currentUser.isGuest:
        userOwnedFundraiser = []
        for fund in homePageFundraiserData:
            if fund[8] == currentUser.emailPK:
                userOwnedFundraiser.append(fund)
                homePageFundraiserData.remove(fund)
        cursor.execute(
            "SELECT Title, DonationsToFund, FundNo FROM DONATES INNER JOIN FUNDRAISER ON FundNo = FundID WHERE EmailAddress = '%s'" % currentUser.emailPK)
        userDonationsTable = cursor.fetchall()
        return render_template('dashboard.html', name=currentUser.name, userOwnedFund=userOwnedFundraiser,
                               fundraiserTable=homePageFundraiserData, userDonorTable=userDonationsTable,
                               isGuest=currentUser.isGuest)

    return render_template('dashboard.html', name=currentUser.name, fundraiserTable=homePageFundraiserData,
                           isGuest=currentUser.isGuest)


@app.route('/tagSort/')
@app.route('/tagSort/<tag>')
def fundTagSort(tag=None):
    if tag == None or tag == "All":
        cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID AND Email != '%s'" % currentUser.emailPK)
        homePageFundraiserData = cursor.fetchall()
    else:
        cursor.execute(
            "SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID AND FUNDRAISER.Tag = '%s' " % tag)
        homePageFundraiserData = cursor.fetchall()
    return render_template('fundraiserSortedByTagsGenerator.html', fundraiserTable=homePageFundraiserData)


@app.route('/login', methods=['POST', 'GET'])
def login():
    cursor.execute("SELECT Username FROM USER")
    DB_Usernames = list(cursor)
    # DB_Usernames usernames returned in ("string",) format. Usernames were reformatted below for comparison operations.
    DB_UsernamesReformatted = []
    global loginFlag
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
                # incorrect password
                loginFlag = 1
                return redirect(url_for('login'))
        else:
            # inccorrect Username
            loginFlag = 1
            return redirect(url_for('login'))
    else:
        return render_template("login.html", flag=loginFlag)


@app.route("/log-out")
def loggingOut():
    currentUser.emailPK = ""
    currentUser.name = "Guest"
    currentUser.username = ""
    currentUser.isGuest = True
    return redirect(url_for('dashboard'))


@app.route('/settings')
def profile_page(name=None, email=None):
    cursor.execute("SELECT Username, Password, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country, CardNumber, ExpirationDate, RouteNo, AccountNo FROM USER WHERE Email = '%s'" % currentUser.emailPK)
    userInfo = cursor.fetchall()
    userInfoList = []
    for userItem in userInfo:
        for item in userItem:
            userInfoList.append(item)

    isUsingCreditCard = False
    if str(userInfoList[11]) == "None":
        isUsingCreditCard = True
    return render_template('settings.html', isUsingCreditCard=isUsingCreditCard, flag=newUserFlags, inputData=inputData, name=userInfoList[2], username= userInfoList[0], password=userInfoList[1], phonenumber=userInfoList[3], zipcode=userInfoList[4], streetaddress=userInfoList[5], state=userInfoList[6], city=userInfoList[7], country=userInfoList[8], cardnumber=userInfoList[9], month=str(userInfoList[10])[5:7], year = str(userInfoList[10])[0:5] , routeno=userInfoList[11], accountno=userInfoList[12])

@app.route("/recordingNewUserSettings")
def updatingUserSettings():
    userName = request.form["UserName"]
    password = request.form["Password"]
    name = request.form["Name"]
    phoneNumber = request.form["PhoneNumber"]
    zipCode = request.form["ZipCode"]
    streetAddress = request.form["StreetAddress"]
    state = request.form["State"]
    city = request.form["City"]
    country = request.form["Country"]
    radioToggled = request.form['paymentOptionToggle']
    if radioToggled == "creditCard":
        cardNumber = request.form["CardNumber"]
        expirationDate = request.form["Year"] + "-" + request.form["Month"] + "-" + str(monthLengths(int(request.form["Month"]), int(request.form["Year"])))
        if (valid_new_user_input(request.form, radioToggled)[0]):
            cursor.execute("UPDATE USER SET Username = '%s', Password = '%s', Name = '%s', PhoneNumber = '%s', ZipCode = '%s', StreetAddress = '%s', State = '%s', City = '%s', Country = '%s', CardNumber = '%s', ExpirationDate = '%s'" % (userName, password, name, phoneNumber, zipCode, streetAddress, state, city, country, cardNumber, expirationDate))
            db.commit()
    elif radioToggled == "bankInfo":
        routingNumber = request.form["RoutingNumber"]
        accountNumber = request.form["AccountNumber"]
        if (valid_new_user_input(request.form, radioToggled)[0]):
            cursor.execute("UPDATE USER SET Username = '%s', Password = '%s', Name = '%s', PhoneNumber = '%s', ZipCode = '%s', StreetAddress = '%s', State = '%s', City = '%s', Country = '%s', RouteNo = '%s', AccountNo = '%s'" % (userName, password, name, phoneNumber, zipCode, streetAddress, state, city, country, routingNumber, accountNumber))
            db.commit()
    return redirect(url_for('dashboard'))


@app.route('/donation-form/<fund_ID>')
def donation_form_page(fund_ID=None):
    paymentOptionIsCreditCard = True
    cursor.execute("SELECT Title FROM FUNDRAISER WHERE FundID = '%s'" % fund_ID)
    fundraiserInfo = cursor.fetchall()
    fundraiserInfoList = []
    for line in fundraiserInfo:
        for item in line:
            fundraiserInfoList.append(item)

    if not currentUser.isGuest:
        cursor.execute(
            "SELECT StreetAddress, City, State, ZipCode, Country, CardNumber, ExpirationDate, RouteNo, AccountNo  FROM USER WHERE Email = '%s'" % currentUser.emailPK)
        userInfo = cursor.fetchall()
        userInfoList = []
        for row in userInfo:
            for attribute in row:
                userInfoList.append(attribute)
        restOfAddress = userInfoList[1] + " " + userInfoList[2] + " " + str(userInfoList[3]) + " " + userInfoList[4]
        if str(userInfoList[7]) == "None":
            return render_template('new-donation.html', isGuest=currentUser.isGuest, fundraiser_ID=fund_ID,
                                   fundraiser_name=fundraiserInfoList[0], name=currentUser.name,
                                   email=currentUser.emailPK, streetAddress=userInfoList[0],
                                   restOfAddress=restOfAddress, cardNum=str(userInfoList[5]),
                                   expirationDate=str(userInfoList[6]), creditCardOption=paymentOptionIsCreditCard,
                                   flag=newDonationFlags, inputData=inputData)
        else:
            paymentOptionIsCreditCard = False
            return render_template('new-donation.html', isGuest=currentUser.isGuest, fundraiser_ID=fund_ID,
                                   fundraiser_name=fundraiserInfoList[0], name=currentUser.name,
                                   email=currentUser.emailPK, streetAddress=userInfoList[0],
                                   restOfAddress=restOfAddress, routingNum=str(userInfoList[7]),
                                   accountNum=str(userInfoList[8]), creditCardOption=paymentOptionIsCreditCard,
                                   flag=newDonationFlags, inputData=inputData)
    else:
        return render_template('new-donation.html', isGuest=currentUser.isGuest, fundraiser_ID=fund_ID,
                               fundraiser_name=fundraiserInfoList[0], name=currentUser.name,
                               flag=newDonationFlags, inputData=inputData)


@app.route('/submittingDonation', methods=["POST"])
def recordingDonation():
    print(request.form)
    valid_input = valid_new_donation_input(request.form, currentUser.isGuest, request.form["paymentOptionToggle"])[0]
    global newDonationFlags, inputData
    newDonationFlags = valid_new_donation_input(request.form, currentUser.isGuest, request.form["paymentOptionToggle"])[1]

    inputData = []
    for values in request.form.values():
        inputData.append(values)

    print(inputData)

    if valid_input:
        amount = request.form["amount"]
        fund_id = request.form["fund_id"]
        # updating balance in Fundraiser
        cursor.execute("UPDATE FUNDRAISER SET Balance = Balance + %d WHERE FundID = %d" % (int(amount), int(fund_id)))

        if not currentUser.isGuest:
            email = request.form["email"]

            # inserting new record into DONATES table
            cursor.execute(
                "SELECT EmailAddress, FundNo FROM DONATES WHERE EXISTS (SELECT 1 FROM DONATES WHERE EmailAddress = %s AND FundNo = %s)",
                (email, fund_id))
            doesExistInDB = cursor.fetchall()
            if not doesExistInDB:
                cursor.execute("INSERT INTO DONATES (EmailAddress, FundNo, DonationsToFund) VALUES (%s,%s,%s)",
                               (email, fund_id, amount))
            else:
                cursor.execute(
                    "UPDATE DONATES SET DonationsToFund = DonationsToFund + %s WHERE (EmailAddress = %s AND FundNo = %s)",
                    (int(amount), email, fund_id))

            # Inserting new record into DONATION table
            cursor.execute("INSERT INTO DONATION (DonationAmount, TransactionDate) VALUES (%s, %s)",
                           (amount, time.strftime('%Y-%m-%d %H:%M:%S')))

            # inserting new record into GIVES table
            cursor.execute("SELECT LAST_INSERT_ID()")
            transactionID = cursor.fetchone()[0]
            cursor.execute("INSERT INTO GIVES (EmailAddress, TransactionNo) VALUES (%s, %s)", (email, transactionID))

            # Inserting new record into FUNDS table
            cursor.execute("INSERT INTO FUNDS (TransactionNo, FundNo) VALUES (%s,%s)", (transactionID, fund_id))
            db.commit()
            return redirect(url_for('dashboard'))
        else:
            # Inserting new record into DONATION table
            cursor.execute("INSERT INTO DONATION (DonationAmount, TransactionDate) VALUES (%s, %s)",
                           (amount, time.strftime('%Y-%m-%d %H:%M:%S')))

            cursor.execute("SELECT LAST_INSERT_ID()")
            transactionID = cursor.fetchone()[0]

            # Inserting new record into FUNDS table
            cursor.execute("INSERT INTO FUNDS (TransactionNo, FundNo) VALUES (%s,%s)", (transactionID, fund_id))
            db.commit()

    if valid_input:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('donation_form_page', fund_ID=request.form["fund_id"]))


@app.route('/fundraiser/<fundraiser_ID>')
def fundraiser_page(fundraiser_ID=None):
    cursor.execute(
        "SELECT Title, Description, Goal, Balance, CreationDate, Timeframe, Tag FROM FUNDRAISER WHERE FundID = '%s'" % fundraiser_ID)
    fundraiserInfo = []
    for line in list(cursor):
        for item in line:
            fundraiserInfo.append(item)

    # Reformatting time constraints to be more user friendly
    fundraiserCreationDate = str(fundraiserInfo[4])[0:10]
    fundraiserCreationDate = fundraiserCreationDate[5:8] + fundraiserCreationDate[8:10] + "-" + fundraiserCreationDate[
                                                                                                0:4]
    fundraiserTimeline = str(fundraiserInfo[5])[0:10]
    fundraiserTimeline = fundraiserTimeline[5:8] + fundraiserTimeline[8:10] + "-" + fundraiserTimeline[0:4]

    # getting donations from registered users
    cursor.execute(
        "SELECT Name, DonationsToFund FROM USER INNER JOIN DONATES ON Email = EmailAddress WHERE fundNo = %s" % fundraiser_ID)
    donationTable = cursor.fetchall()

    # Getting guest donations
    cursor.execute(
        "SELECT 'Guest Donor' as Name, DonationAmount FROM (SELECT TransactionNo, DonationAmount, FundNo FROM FUNDS INNER JOIN DONATION ON FUNDS.TransactionNo = DONATION.TransactionID WHERE FundNo = %s) as R WHERE TransactionNo NOT IN (SELECT TransactionNo FROM GIVES)" % fundraiser_ID)
    guestTable = cursor.fetchall()

    donationTable += guestTable

    balance = 0.00
    for donation in donationTable:
        balance += float(donation[1])

    return render_template('fundraiser.html', fund_ID=fundraiser_ID, fund_name=fundraiserInfo[0],
                           fund_desc=fundraiserInfo[1], fund_goal=fundraiserInfo[2], fund_tag=fundraiserInfo[6],
                           fund_balance=fundraiserInfo[3], fund_creationdate=fundraiserCreationDate,
                           fund_timeline=fundraiserTimeline, table=donationTable)


@app.route('/new-fundraiser')
def fundraiser_form_page():
    return render_template('new-fundraiser-form.html', flag=newFundraiserFlags, inputData=inputData)


@app.route('/fillingNewFundraiserForm', methods=["POST", "GET"])
def recordNewFundraiserForm():
    global newFundraiserFlags, inputData
    inputData = []
    for values in request.form.values():
        inputData.append(values)
    print(request.form)
    print(inputData)
    newFundraiserFlags = valid_new_fundraiser_input(request.form)[1]
    valid_fundraiser = valid_new_fundraiser_input(request.form)[0]
    title = request.form["title"]
    description = request.form["description"]
    tag = request.form["tag"]
    goal = request.form["goal"]
    day = request.form["day"]
    if int(day) < 10:
        day = "0%s" % day
    timeline = request.form["Year"] + '-' + request.form["Month"] + '-' + day
    creation = time.strftime('%Y-%m-%d %H:%M:%S')

    images = os.listdir('static')

    if valid_fundraiser:
        return render_template('new-fundraiser-second-page.html', title=title, description=description, tag=tag, goal=goal,
                               timeline=timeline, creation=creation, imageList=images)
    else:
        return redirect(url_for('fundraiser_form_page'))


@app.route("/select", methods=["GET", "POST"])
def selectImage():
    title = request.form["title"]
    description = request.form["description"]
    tag = request.form["tag"]
    goal = request.form["goal"]
    timeline = request.form["timeline"]
    creation = request.form["creation"]
    image = request.form["imageSelect"]

    cursor.execute(
        "INSERT INTO FUNDRAISER (Title, Description, Tag, ImagePath, Goal, CreationDate, Timeframe) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (title, description, tag, image, goal, creation, timeline))
    cursor.execute("SELECT LAST_INSERT_ID()")
    FundID = cursor.fetchone()[0]
    cursor.execute("INSERT INTO OWNS (EmailAddress, FundNo) VALUES (%s, %s)", (currentUser.emailPK, FundID))
    db.commit()

    return redirect(url_for('dashboard'))


@app.route('/uploader', methods=["GET", "POST"])
def upload_file():
    title = request.form["title"]
    description = request.form["description"]
    tag = request.form["tag"]
    goal = request.form["goal"]
    timeline = request.form["timeline"]
    creation = request.form["creation"]
    image = request.files['file']
    image.save(os.path.join(app.config['UPLOADED_FILES'], secure_filename(image.filename)))
    cursor.execute(
        "INSERT INTO FUNDRAISER (Title, Description, Tag, ImagePath, Goal, CreationDate, Timeframe) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (title, description, tag, image.filename, goal, creation, timeline))
    cursor.execute("SELECT LAST_INSERT_ID()")
    FundID = cursor.fetchone()[0]
    cursor.execute("INSERT INTO OWNS (EmailAddress, FundNo) VALUES (%s, %s)", (currentUser.emailPK, FundID))
    db.commit()

    return redirect(url_for('dashboard'))


@app.route('/new-user-form')
def new_user_form_page():
    return render_template("new-user-form.html", flag=newUserFlags, inputData=inputData)


@app.route('/fillingNewUserForm', methods=["POST"])
def recordNewUserForm():
    global inputData
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
    radioToggled = request.form['paymentOptionToggle']
    if radioToggled == "creditCard":
        cardNumber = request.form["CardNumber"]
        expirationDate = request.form["Year"] + "-" + request.form["Month"] + "-" + str(
            monthLengths(int(request.form["Month"]), int(request.form["Year"])))
        if valid_new_user_input(request.form, radioToggled)[0]:
            cursor.execute(
                "INSERT INTO USER (Username, Password, Email, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country, CardNumber, ExpirationDate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (userName, password, email, name, phoneNumber, zipCode, streetAddress, state, city, country, cardNumber,
                 expirationDate))
            db.commit()
    elif radioToggled == "bankInfo":
        routingNumber = request.form["RoutingNumber"]
        accountNumber = request.form["AccountNumber"]
        if valid_new_user_input(request.form, radioToggled)[0]:
            cursor.execute(
                "INSERT INTO USER (Username, Password, Email, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country, RouteNo, AccountNo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (userName, password, email, name, phoneNumber, zipCode, streetAddress, state, city, country,
                 routingNumber, accountNumber))
            db.commit()

    inputData = []
    for values in request.form.values():
        inputData.append(values)

    global newUserFlags
    newUserFlags = valid_new_user_input(request.form, radioToggled)[1]
    if valid_new_user_input(request.form, radioToggled)[0]:
        currentUser.isGuest = False
        currentUser.name = name
        currentUser.emailPK = email
        currentUser.username = userName
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('new_user_form_page'))


if __name__ == '__main__':
    app.run(debug=True)
