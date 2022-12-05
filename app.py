import datetime
import os
import time
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, jsonify
from flask import render_template
from DB_Connection import *
from DummyInfo import monthLengths
from RecoveryEmailHandler import *
from ValidateNewData import valid_new_user_input, valid_new_donation_input, valid_new_fundraiser_input, valid_email, valid_password
from PasswordHasher import hash_password, verify_password, check_for_rehash

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
newUserFlags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
newFundraiserFlags = [0, 0]
newDonationFlags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
inputData = []
loginFlag = 0
accountRecoveryFlag = 0
tagValues = ["Other", "Animals", "Business", "Community", "Creative", "Education", "Emergencies", "Environment", "Event", "Faith", "Family", "Funeral and Memorial", "Medical", "Monthly Bills", "Newlyweds", "Sports", "Travel", "Volunteer", "Wishes"]
accountRecoveryEmail = ""

@app.route('/')
def home_page():  # create landing page later
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    global newUserFlags, newDonationFlags, newFundraiserFlags, inputData, loginFlag
    newUserFlags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    newDonationFlags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    newFundraiserFlags = [0, 0]
    loginFlag = 0
    inputData = []
    cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name, Email, Timeframe FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID")
    homePageFundraiserData = cursor.fetchall()
    generalFundPopulation = []
    for fund in homePageFundraiserData:
        if datetime.datetime.now() < fund[9]:
            generalFundPopulation.append(fund)

    if not currentUser.isGuest:
        userOwnedFundraiser = []
        restOfFundraisers = []
        for fund in homePageFundraiserData:
            if fund[8] == currentUser.emailPK:
                userOwnedFundraiser.append(fund)
            else:
                restOfFundraisers.append(fund)
        cursor.execute(
            "SELECT FundID, EmailAddress FROM DONATES INNER JOIN FUNDRAISER ON FundNo = FundID WHERE EmailAddress = '%s'" % currentUser.emailPK)
        fundraisersThisUserDonatedToo = cursor.fetchall()
        restRestOfFundraiser = []
        userDonationsTable = []
        for fund in restOfFundraisers:
            for fundDonatedToo in fundraisersThisUserDonatedToo:
                if fund[2] == fundDonatedToo[0] and datetime.datetime.now() < fund[9]:
                    userDonationsTable.append(fund)
            else:
                if fund not in userDonationsTable and datetime.datetime.now() < fund[9]:
                    restRestOfFundraiser.append(fund)
        return render_template('dashboard.html', name=currentUser.name, userOwnedFund=userOwnedFundraiser,
                               fundraiserTable=restRestOfFundraiser, userDonorTable=userDonationsTable,
                               isGuest=currentUser.isGuest)

    return render_template('dashboard.html', name=currentUser.name, fundraiserTable=generalFundPopulation,
                           isGuest=currentUser.isGuest)


@app.route('/tagSort/')
@app.route('/tagSort/<tag>')
def fundTagSort(tag=None):
    if tag == None or tag == "All":
        if not currentUser.isGuest:
            cursor.execute("SELECT FundID, EmailAddress FROM DONATES INNER JOIN FUNDRAISER ON FundNo = FundID WHERE EmailAddress = '%s'" % currentUser.emailPK)
            fundsDonatedToo = cursor.fetchall()
            cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name, Timeframe FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID AND Email != '%s'" % currentUser.emailPK)
            homePageFundraiserData = cursor.fetchall()
            restRestOfFundraiser = []
            userDonationsTable = []
            for fund in homePageFundraiserData:
                for fundDonatedToo in fundsDonatedToo:
                    if fund[2] == fundDonatedToo[0] and datetime.datetime.now() < fund[8]:
                        userDonationsTable.append(fund)
                else:
                    if fund not in userDonationsTable and datetime.datetime.now() < fund[8]:
                        restRestOfFundraiser.append(fund)
        else:
            cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID")
            restRestOfFundraiser = cursor.fetchall()
            cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name, Timeframe FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID")
            homePageFundraiserData = cursor.fetchall()
            restRestOfFundraiser = []
            for fund in homePageFundraiserData:
                if datetime.datetime.now() < fund[8]:
                    restRestOfFundraiser.append(fund)
    else:
        if not currentUser.isGuest:
            cursor.execute("SELECT FundID, EmailAddress FROM DONATES INNER JOIN FUNDRAISER ON FundNo = FundID WHERE EmailAddress = '%s'" % currentUser.emailPK)
            fundsDonatedToo = cursor.fetchall()
            cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name, Timeframe FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID AND FUNDRAISER.Tag = '%s' AND Email != '%s'" % (tag, currentUser.emailPK))
            homePageFundraiserData = cursor.fetchall()
            restRestOfFundraiser = []
            userDonationsTable = []
            for fund in homePageFundraiserData:
                for fundDonatedToo in fundsDonatedToo:
                    if fund[2] == fundDonatedToo[0] and datetime.datetime.now() < fund[8]:
                        userDonationsTable.append(fund)
                else:
                    if fund not in userDonationsTable and datetime.datetime.now() < fund[8]:
                        restRestOfFundraiser.append(fund)
        else:
            cursor.execute("SELECT Title, Description, FundID, ImagePath, Goal, Balance, ROUND((Balance / Goal) * 100, 1) AS PercentLeft, Name, Timeframe FROM FUNDRAISER INNER JOIN OWNS INNER JOIN USER ON OWNS.EmailAddress = USER.Email WHERE OWNS.FundNo = FUNDRAISER.FundID AND FUNDRAISER.Tag = '%s' " % tag)
            homePageFundraiserData = cursor.fetchall()
            restRestOfFundraiser = []
            for fund in homePageFundraiserData:
                if datetime.datetime.now() < fund[8]:
                    restRestOfFundraiser.append(fund)

    return render_template('fundraiserSortedByTagsGenerator.html', fundraiserTable=restRestOfFundraiser)

@app.route('/login', methods=['POST', 'GET'])
def login():
    global accountRecoveryFlag, accountRecoveryEmail
    accountRecoveryEmail = ""
    accountRecoveryFlag = 0
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
            cursor.execute("SELECT Password FROM USER WHERE Username = %(username)s", {'username': userName})
            DB_Password = cursor.fetchone()[0]
            if verify_password(password, DB_Password):
                currentUser.isGuest = False
                cursor.execute("SELECT Name, Email, Username FROM USER WHERE UserName = %(username)s", {'username': userName})
                nameAndEmail = cursor.fetchmany(2)
                currentUser.name = nameAndEmail[0][0]
                currentUser.emailPK = nameAndEmail[0][1]
                currentUser.username = userName
                if check_for_rehash(DB_Password):
                    cursor.execute("""UPDATE USER
                                      SET Password = %(password)s
                                      WHERE Email = %(email)s""",
                                   {'password': hash_password(password), 'email': nameAndEmail[0][1]})
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

@app.route("/recover-username")
def recover_username():
    return render_template("user-recovery.html", recovery="username", flag=accountRecoveryFlag)

@app.route("/recoverUsername", methods=["POST"])
def send_username_email():
    print(request.form)
    global accountRecoveryFlag
    accountRecoveryFlag = 0
    email = request.form['email']
    if valid_email(email):
        cursor.execute("""SELECT * 
                          FROM USER 
                          WHERE Email = %(email)s""",
                       {'email': email})
        dataRecovered = cursor.fetchone()
        print(dataRecovered)
        if dataRecovered != None:
            send_email(RecoveryType.USERNAME, dataRecovered[0], email)
            print("Email sent")
        else:
            accountRecoveryFlag = 1
            print("No email found")
    else:
        accountRecoveryFlag = 1

    return redirect(url_for('recover_username'))

@app.route("/recover-password")
def recover_password():
    return render_template("user-recovery.html", recovery="password", flag=accountRecoveryFlag)

@app.route("/recoverPassword", methods=["POST"])
def send_password_email():
    global accountRecoveryFlag, accountRecoveryEmail
    accountRecoveryFlag = 0
    email = request.form['email']
    username = request.form['username']
    if valid_email(email):
        cursor.execute("""SELECT * 
                          FROM USER 
                          WHERE Email = %(email)s AND Username = %(username)s""",
                       {'email': email, 'username': username})
        dataRecovered = cursor.fetchone()
        if dataRecovered != None:
            send_email(RecoveryType.PASSWORD, "", email)
            print("Email sent")
            accountRecoveryEmail = email
        else:
            accountRecoveryFlag = 1
            print("No email found")
    else:
        accountRecoveryFlag = 1

    return redirect(url_for('recover_password'))

@app.route("/new-password")
def new_password():
    return render_template("user-recovery.html", recovery="new-password", flag=accountRecoveryFlag)

@app.route("/submittingNewPassword", methods=["POST"])
def submitting_new_password():
    global accountRecoveryFlag
    password = request.form['password']
    confirmPassword = request.form['confirm-password']

    if valid_password(password) and password == confirmPassword:
        cursor.execute("""UPDATE USER
                          SET Password = %(password)s
                          WHERE Email = %(email)s""",
                       {'email': accountRecoveryEmail, 'password': hash_password(password)})
        return redirect(url_for('login'))
    else:
        accountRecoveryFlag = 1
        return redirect(url_for('new_password'))


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
        cursor.execute("UPDATE FUNDRAISER SET Balance = Balance + %s WHERE FundID = %d" % (amount, int(fund_id)))

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


@app.route('/new-fundraiser')
def fundraiser_form_page():
    return render_template('new-fundraiser-form.html', flag=newFundraiserFlags, inputData=inputData)


@app.route('/fillingNewFundraiserForm', methods=["POST", "GET"])
def recordNewFundraiserForm():
    global newFundraiserFlags, inputData
    inputData = []
    for values in request.form.values():
        inputData.append(values)
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

@app.route('/fundraiser/<fundraiser_ID>')
def fundraiser_page(fundraiser_ID=None):
    cursor.execute(
        "SELECT Title, Description, Goal, Balance, CreationDate, Timeframe, Tag, ImagePath, ROUND((Balance / Goal) * 100, 1) AS PercentLeft FROM FUNDRAISER WHERE FundID = '%s'" % fundraiser_ID)
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

    # Five most recent donations
    cursor.execute(
        "SELECT Name, DonationAmount, TransactionDate FROM USER RIGHT JOIN (SELECT EmailAddress, DonationAmount, TransactionDate FROM GIVES RIGHT JOIN (SELECT DonationAmount, TransactionID, TransactionDate FROM DONATION INNER JOIN FUNDS ON TransactionID = FUNDS.TransactionNo AND FundNo = %s) AS R ON GIVES.TransactionNo = TransactionID) as B ON Email = EmailAddress ORDER BY TransactionDate DESC limit 5" % fundraiser_ID)
    fiveMostRecentDonationsTable = cursor.fetchall()
    padding = 5 - len(fiveMostRecentDonationsTable)
    if padding != 5:
        for num in range(padding):
            fiveMostRecentDonationsTable.append(("", "", ""))

    # top 5 donations
    cursor.execute(
        "SELECT Name, DonationAmount, TransactionDate FROM USER RIGHT JOIN (SELECT EmailAddress, DonationAmount, TransactionDate FROM GIVES RIGHT JOIN (SELECT DonationAmount, TransactionID, TransactionDate FROM DONATION INNER JOIN FUNDS ON TransactionID = FUNDS.TransactionNo AND FundNo = %s) AS R ON GIVES.TransactionNo = TransactionID) as B ON Email = EmailAddress ORDER BY DonationAmount DESC limit 5" % fundraiser_ID)
    topFiveDonationsTable = cursor.fetchall()
    paddingMax = 5 - len(topFiveDonationsTable)
    if paddingMax != 5:
        for num in range(paddingMax):
            topFiveDonationsTable.append(("", "", ""))

    #does this user own this fundraiser
    listOfUserOwnedFundraiser = []
    cursor.execute("SELECT FundNo FROM OWNS WHERE EmailAddress = '%s'" % currentUser.emailPK)
    for item in list(cursor):
        listOfUserOwnedFundraiser.append(item[0])
    doesThisUserOwnThisFundraiser = False
    for fund in listOfUserOwnedFundraiser:
        if str(fund) == str(fundraiser_ID):
            doesThisUserOwnThisFundraiser = True
            break

    return render_template('fundraiser.html', fund_ID=fundraiser_ID, fund_name=fundraiserInfo[0],
                           fund_desc=fundraiserInfo[1], fund_goal=fundraiserInfo[2], fund_tag=fundraiserInfo[6],
                           fund_balance=fundraiserInfo[3], fund_creationdate=fundraiserCreationDate,
                           fund_timeline=fundraiserTimeline, isOwner = doesThisUserOwnThisFundraiser, image=fundraiserInfo[7], percentage=fundraiserInfo[8], recentDonortable = fiveMostRecentDonationsTable, topFiveDonations = topFiveDonationsTable)

@app.route('/fundraiser-edit-settings/<fundID>')
def editingFundraiserFirstPage(fundID=None):
    cursor.execute("SELECT Title, Description, Goal, Tag, Timeframe, ImagePath FROM FUNDRAISER WHERE FundID = '%s'" % fundID)
    fundItems = []
    for line in list(cursor):
        for item in line:
            fundItems.append(item)

    return render_template("editFundraiser.html", image = fundItems[5], fundID= fundID, title = fundItems[0], description=fundItems[1], goal = fundItems[2], tagsList = tagValues, thisTag= fundItems[3], timeframeMonth = int(str(fundItems[4])[5:7]), timeframeYear = int(str(fundItems[4])[0:4]), timeframeDay = int(str(fundItems[4])[8:10]), flag=newFundraiserFlags, inputData=inputData)

@app.route('/submittingEditForFundraiserFirstPage/<fundID>', methods=["GET", "POST"])
def editingFundraiserSecondPage(fundID=None):
    global newFundraiserFlags
    newFundraiserFlags = valid_new_fundraiser_input(request.form)[1]
    valid_fundraiser = valid_new_fundraiser_input(request.form)[0]
    title = request.form['title']
    description = request.form['description']
    goal = request.form['goal']
    tag = request.form['tag']
    day = request.form['day']
    if int(day) < 10:
        day = "0%s" % day
    timeline = request.form["Year"] + '-' + request.form["Month"] + '-' + day
    images = os.listdir('static')
    thisImage = request.form['image']

    if valid_fundraiser:
        return render_template('edit-fundraiser-second-page.html', fundID= fundID, title=title, description=description, tag=tag, goal=goal,
                               timeline=timeline, imageList=images, thisImage = thisImage)
    else:
        return redirect(url_for('editingFundraiserFirstPage', fundID=fundID))

@app.route("/editingSelect", methods=["GET", "POST"])
def editingSelectImage():
    title = request.form["title"]
    description = request.form["description"]
    tag = request.form["tag"]
    goal = request.form["goal"]
    timeline = request.form["timeline"]
    image = request.form["imageSelect"]
    fundID = request.form["fundID"]

    cursor.execute("""UPDATE FUNDRAISER 
                      SET Title = %(title)s, Description = %(description)s, Tag = %(tag)s, 
                      ImagePath = %(image)s, Goal = %(goal)s, Timeframe = %(timeline)s 
                      WHERE FundID = %(fundID)s """,
                   {'title': title, 'description': description, 'tag': tag, 'image': image,
                    'goal': goal, 'timeline': timeline, 'fundID': fundID})
    db.commit()

    return redirect(url_for('dashboard'))

@app.route('/editingUploader', methods=["GET", "POST"])
def editing_upload_file():
    title = request.form["title"]
    description = request.form["description"]
    tag = request.form["tag"]
    goal = request.form["goal"]
    timeline = request.form["timeline"]
    image = request.files['file']
    fundID = request.form["fundID"]

    image.save(os.path.join(app.config['UPLOADED_FILES'], secure_filename(image.filename)))
    cursor.execute("""UPDATE FUNDRAISER 
                      SET Title = %(title)s, Description = %(description)s, Tag = %(tag)s, 
                      ImagePath = %(image)s, Goal = %(goal)s, Timeframe = %(timeline)s 
                      WHERE FundID = %(fundID)s """,
                   {'title': title, 'description': description, 'tag': tag, 'image': image.filename,
                    'goal': goal, 'timeline': timeline, 'fundID': fundID})
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
                (userName, hash_password(password), email, name, phoneNumber, zipCode, streetAddress, state, city, country, cardNumber,
                 expirationDate))
            db.commit()
    elif radioToggled == "bankInfo":
        routingNumber = request.form["RoutingNumber"]
        accountNumber = request.form["AccountNumber"]
        if valid_new_user_input(request.form, radioToggled)[0]:
            cursor.execute(
                "INSERT INTO USER (Username, Password, Email, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country, RouteNo, AccountNo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (userName, hash_password(password), email, name, phoneNumber, zipCode, streetAddress, state, city, country,
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
    return render_template('UserSettings.html', isUsingCreditCard=isUsingCreditCard, flag=newUserFlags, inputData=inputData, name=userInfoList[2], username= userInfoList[0], password=userInfoList[1], phonenumber=userInfoList[3], zipcode=userInfoList[4], streetaddress=userInfoList[5], state=userInfoList[6], city=userInfoList[7], country=userInfoList[8], cardnumber=userInfoList[9], month=str(userInfoList[10])[5:7], year = str(userInfoList[10])[0:4] , routeno=userInfoList[11], accountno=userInfoList[12])

@app.route("/recordingNewUserSettings", methods=['POST', 'GET'])
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
        if valid_new_user_input(request.form, radioToggled, True)[0]:
            cursor.execute("""UPDATE USER 
                              SET Username = %(username)s, Password = %(password)s, Name = %(name)s, 
                              PhoneNumber = %(phoneNumber)s, ZipCode = %(zipCode)s, StreetAddress = %(streetAddress)s, 
                              State = %(state)s, City = %(city)s, Country = %(country)s, CardNumber = %(cardNumber)s, 
                              ExpirationDate = %(expirationDate)s, RouteNo = NULL, AccountNo = NULL 
                              WHERE Email = %(email)s""",
                           {'username': userName, 'password': hash_password(password), 'name': name, 'phoneNumber': phoneNumber,
                            'zipCode': zipCode, 'streetAddress': streetAddress, 'state': state, 'city': city, 'country': country,
                            'cardNumber': cardNumber, 'expirationDate': expirationDate, 'email': currentUser.emailPK})
            db.commit()
    elif radioToggled == "bankInfo":
        routingNumber = request.form["RoutingNumber"]
        accountNumber = request.form["AccountNumber"]
        if valid_new_user_input(request.form, radioToggled, True)[0]:
            cursor.execute("""UPDATE USER 
                                      SET Username = %(username)s, Password = %(password)s, Name = %(name)s, 
                                      PhoneNumber = %(phoneNumber)s, ZipCode = %(zipCode)s, StreetAddress = %(streetAddress)s, 
                                      State = %(state)s, City = %(city)s, Country = %(country)s, CardNumber = NULL, 
                                      ExpirationDate = NULL, RouteNo = %(routeNo)s, AccountNo = %(accountNo)s 
                                      WHERE Email = %(email)s""",
                           {'username': userName, 'password': hash_password(password), 'name': name, 'phoneNumber': phoneNumber,
                            'zipCode': zipCode, 'streetAddress': streetAddress, 'state': state, 'city': city,
                            'country': country, 'routeNo': routingNumber, 'accountNo': accountNumber, 'email': currentUser.emailPK})
            db.commit()

    global newUserFlags
    newUserFlags = valid_new_user_input(request.form, radioToggled, True)[1]
    if valid_new_user_input(request.form, radioToggled, True)[0]:
        currentUser.name = name
        currentUser.username = userName
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('profile_page'))

if __name__ == '__main__':
    app.run(debug=True)
