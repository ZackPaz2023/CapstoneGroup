import datetime
import mysql.connector

def monthLengths(month, year):
    lengths = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if (month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
        return 29
    else:
        return lengths[month - 1]

def main():
    dbConnection = mysql.connector.connect(host = "localhost",
                                           user = "root",
                                           password = "password",
                                           database = "test")

    dbCursor = dbConnection.cursor()

    #User Info: Username, Password, Email, Name, Phone Number, Zip, Street Address, City, State, Country, Card Number, Exp Date, Routing Number, Account Number
    userInfo = [("fqrqwqy", "0verth3rqinb0w", "kansasgirl@gmail.com", "Dorothy Gale", "202-918-2132", 40293, "4042 Nowear Lane", "Fields", "KS", "United States", 3589481030276534, "2024-12-" + str(monthLengths(12, 2024)), None , None),
                ("clownschool", "DrunkenClown", "clownin@yahoo.com", "Honk McWaxxer", "320-577-7956", 23464, "1111 State Street", "Blowhorn", "AK", "United States",None , None, 670826054, 71523538),
                ("HomewardBound", "RADIO", "DenverNotColorodo@gmail.com", "John Denver", "582-482-0588", 48104, "1971 Country Road", "Mountain Mama", "WV", "United States", 4572307398817873, "2023-06-" + str(monthLengths(6, 2023)),None ,None ),
                ("Lutece1879", "FreeBird", "2ofakind@gmail.com", "Lutece", "582-203-0838", 10902, "552 Upward Lane", "Columbia", "VA", "United States", None, None, 534369903, 93525636),
                ("Kira1966", "BitesTheDust", "kirayoshikage@aol.com", "Kira Yoshikage", "318-659-6412", 77200, "4156 Villa Road", "Morioh", "", "Japan", 341179894763895, "2025-02-" + str(monthLengths(2, 2025)), None, None),
                ("NotAScammer", "businessmogel", "workingfromhome@gmail.com", "Bernie Madoff", "309-611-6048", 82985, "12345 Main Street", "New York City", "NY", "United States",None , None, 358769721, 51162661),
                ("BigSturdy", "Doctor's Office", "personalcomputer@outlook.com", "William Doors", "203-952-2952", 52185, "645 Silicon Alley", "San Jose", "CA", "United States", 4848900679160589, "2024-08-" + str(monthLengths(8, 2024)),None ,None ),
                ("Murphy's Law", "OCPStandardPassword", "Tinman@gmail.com", "Alex Murphy", "301-387-4911", 63453, "50399 Justice Road", "Detroit", "MI", "United States", None, None, 270393550, 46045801),
                ("FirstConsul", "AverageHeightForTheTime", "nbonaparte@yahoo.com", "Napoleon Bonaparte", "582-333-0707", 85947, "4154 Fraternity Street", "Paris", "", "France", 6011352349624030, "2026-01-" + str(monthLengths(1, 2026)),None ,None ),
                ("clopez", "asdfasdf", "lopez@gmail.com", "Carlos Lopez", "121-123-1234", 64123, "This is the St.", "Kansas City", "MO", "US", None, None, 123456789, 12345678),
                ("kwhite", "asdfasdf", "white@gmail.com", "Katie White", "456-567-7890", 64123, "this is the St.", "Kansas City", "MO", "US", 1111222233334444, "2025-03-" + str(monthLengths(3, 2025)), None,None ),
                ("JackMan", "asdfasdf", "Jlopez@gmail.com", "Jack Lopez", "736-204-7295", 64123, "This is the St.", "Kansas City", "MO", "US", None , None, 183609257, 16849206),
                ("LastConsul", "AcrosstheRhine", "venividivici@outlook.com", "Julius Caesar", "213-708-6937", 61422, "415 SPQR Street", "Rome", "", "Italy", 5456454184555214, "2026-09-" + str(monthLengths(9, 2026)),None , None)]

    #Fundraiser Info: Owner Email, Title, Description, tag, image, Goal, Creation Date, Timeframe
    FundInfo = [("kansasgirl@gmail.com", "Journey Home", "Dorothy wants to get off the Wizard's Wild Ride and get back home to Kansas.", "Travel", "PowerfulReasons_hero.jpeg", 1500, "2022-04-16 10-31-22", "2022-10-1 23-59-59"),
                ("Tinman@gmail.com", "Aid Ukraine", "Sending relief funds for civilians impacted by the war. All Proceeds go towards food, water, and evacuations. Any help is much appreciated", "Emergencies", "Ukraine_Image.jpeg", 20000, "2022-07-20 12-31-22", "2023-07-20 10-31-22"),
                ("clownin@yahoo.com", "Misfit Academy", "Help fund this academy for impoverished children.", "Community", "30virus-pediatrics-01-mobileMasterAt3x-v2.jpeg", 2000, "2022-06-10 09-42-02", "2023-07-11 10-28-40"),
                ("workingfromhome@gmail.com", "Investment Opportunity Going Fast!!", "Be the hottest invester you know! With me! Trusted by Warren Buffett himself! 10% monthly return guaranteed!! !", "Business", "Growing_Graph_Plant-780x438.jpeg" , 100000, "2022-10-31 10-00-00", "2025-12-31 23-59-59"),
                ("nbonaparte@yahoo.com", "Hurricane Disaster", "Raising funds for hurricane relief in Florida", "Emergencies", "hurricane-house.jpeg" , 10000, "2022-07-04 13-14-36", "2023-01-01 00-00-00"),
                ("white@gmail.com", 'Going to Europe', 'Looking to fulfill my lifelong dream of going to Europe. Please any little goes a long way.', 'Travel', 'Industryyyy.jpeg', 3000, '2022-11-22 21:02:12', '2024-03-06 00:00:00'),
                ("kirayoshikage@aol.com", 'School Supplies', 'Please help contribute to this classroom. We are in desperate need of school supplies. This will benefit the students learning experience.', 'Education', 'Growing_Graph_Plant-780x438.jpeg', 350,'2022-11-22 12:56:18', '2024-01-01 00:00:00'),
                ("Jlopez@gmail.com", "Xbox Woes" ,'I really need to buy a new Xbox 360 so that I can play with all of my friends', 'Wishes', 'kidsWish.jpeg', 500, '2022-11-22 12:56:18', '2024-01-01 00:00:00'),
                ("venividivici@outlook.com", "I DO!!", "Help John and Kate realize their dream wedding!", "Newlyweds", "bride-groom-getting-married-illustrated.jpeg" , 15000, "2022-05-05 15-55-13", "2023-08-05 00-00-00"),
                ("personalcomputer@outlook.com", "The Super Computer", "I will achieve my goal of building the greatest super computer AI of this generation. I just need a small donation of...", "Other", "supercomputer_servers_data_center.jpeg", 50000, "2022-04-16 10-31-22", "2022-10-1 23-59-59"),
                ("2ofakind@gmail.com", "Youth Sports", "I need help funding a youth sports center. Proceeds will go towards towards equipment and field upkeep. Coaches and Refs are volunteers.", "Sports", "youthSports.jpeg", 4000, "2022-07-20 12-31-22", "2023-07-20 10-31-22"),
                ("clownin@yahoo.com", "Medical Bills", "Raising funds to help pay for my mothers medical bills. The unexpected hospital stay has put my mother in peril of losing her house.", "Medical", "medicalBills.png", 85000, "2022-06-10 09-42-02", "2023-07-11 10-28-40"),
                ("lopez@gmail.com", "Tech Start Up", "Please fund my new start up, i'm making something like GoFundMe, but its not GoFundMe...", "Business", "32899395526_bf271c8fa9_b.jpeg", 10000, "2022-10-31 10-00-00", "2022-12-01 23-59-59"),
                ("2ofakind@gmail.com", "Tornado Disaster", "Please help us rebuild this community that was destroyed by a tornado.", "Emergencies", "gettyimages-1237246621-3b7c952eadb66cc8d43b0a4fc5bdc302eb1f80fd.jpeg", 15000, "2022-07-04 13-14-36", "2023-01-01 00-00-00"),
                ("white@gmail.com", 'Animal Shelter', 'Collecting funds for this local animal shelter, this all volunteer shelter will out the proceeds to keeping the building lights on and the animals fed and cared for.', 'Animals', 'animalShelter.jpeg', 5000, '2022-11-22 21:02:12', '2024-03-06 00:00:00'),
                ("kirayoshikage@aol.com", 'Support Buying Back Items', 'My car was recently broken into, I need to repair a broken window and I also need help buying back a toddle car seat that was stolen. Thank you', 'Other', 'community.jpeg', 450, '2022-11-22 12:56:18', '2024-01-01 00:00:00'),
                ("DenverNotColorodo@gmail.com", "House Fire", 'My house recently burned down in the forest fire along with most of my possessions. Anything right now would go a long way.', 'Environment', 'r.jpeg', 20000, '2022-11-22 12:56:18', '2024-01-01 00:00:00'),
                ("kansasgirl@gmail.com", "Car Troubles", "The only car I have recently broke down, I really need it fixed so the I can get to work and take care of my family.", "Emergencies","carTroubles.jpeg", 1000, "2022-05-05 15-55-13","2023-08-05 00-00-00")]

    #Transaction Info: Transaction ID, Fundraiser ID, Donor Email, Donation Amount, Transaction Date
    TranInfo = [(1001, "DenverNotColorodo@gmail.com", 150, "2022-06-23 14-50-33"),
                (1002, "nbonaparte@yahoo.com", 100, "2022-08-02 03-22-40"),
                (1003, "Tinman@gmail.com", 300, "2022-08-05 08-00-00"),
                (1004, "clownin@yahoo.com", 1, "2022-08-15 17-08-55"),
                (1005, "clownin@yahoo.com", 10, "2022-08-15 19-03-49"),
                (1006, "venividivici@outlook.com", 500, "2022-09-13 13-14-09"),
                (1007, "2ofakind@gmail.com", 241.56, "2022-09-15 14-38-01"),
                (1008, "DenverNotColorodo@gmail.com", 100, "2022-09-27 09-45-25"),
                (1009, "personalcomputer@outlook.com", 1000, "2022-09-30 04-35-09"),
                (1010, "nbonaparte@yahoo.com", 200, "2022-10-03 09-38-23"),
                (1011, "venividivici@outlook.com", 500, "2022-10-04 08-10-49"),
                (1012, "personalcomputer@outlook.com", 1000, "2022-10-09 10-55-10"),
                (1013, "kirayoshikage@aol.com", 30, "2022-10-15 09-33-13"),
                (1014, "kirayoshikage@aol.com", 100, "2022-11-02 14-44-21"),
                (1015, "2ofakind@gmail.com", 933.13, "2022-11-05 04-27-12"),
                (1016, "DenverNotColorodo@gmail.com", 150, "2022-06-23 14-50-33"),
                (1017, "nbonaparte@yahoo.com", 100, "2022-08-02 03-22-40"),
                (1018, "Tinman@gmail.com", 300, "2022-08-05 08-00-00"),
                (1001, "clownin@yahoo.com", 1, "2022-08-15 17-08-55"),
                (1007, "clownin@yahoo.com", 10, "2022-08-15 19-03-49"),
                (1003, "venividivici@outlook.com", 500, "2022-09-13 13-14-09"),
                (1012, "2ofakind@gmail.com", 241.56, "2022-09-15 14-38-01"),
                (1017, "DenverNotColorodo@gmail.com", 100, "2022-09-27 09-45-25"),
                (1009, "personalcomputer@outlook.com", 1000, "2022-09-30 04-35-09"),
                (1001, "nbonaparte@yahoo.com", 200, "2022-10-03 09-38-23"),
                (1014, "venividivici@outlook.com", 500, "2022-10-04 08-10-49"),
                (1013, "personalcomputer@outlook.com", 1000, "2022-10-09 10-55-10"),
                (1003, "kirayoshikage@aol.com", 30, "2022-10-15 09-33-13"),
                (1018, "kirayoshikage@aol.com", 100, "2022-11-02 14-44-21"),
                (1004, "2ofakind@gmail.com", 933.13, "2022-11-05 04-27-12")
                ]

    #Some basic strings that can be executed by the mySQL cursor when passed the right arguments: cursor.execute(statement, tuple)
    userInsert = 'INSERT INTO user (Username, Password, Email, Name, PhoneNumber, ZipCode, StreetAddress, City, State, Country, CardNumber, ExpirationDate, RouteNo, AccountNo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    fundraiserInsert = 'INSERT INTO fundraiser (Title, Description, Tag, ImagePath, Goal, CreationDate, Timeframe) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    donationInsert = 'INSERT INTO donation (TransactionDate, DonationAmount) VALUES (%s, %s)'
    ownsInsert = 'INSERT INTO owns (EmailAddress, FundNo) VALUES (%s, %s)'
    donatesInsert = 'INSERT INTO donates (EmailAddress, FundNo, DonationsToFund) VALUES (%s, %s, %s)'
    givesInsert = 'INSERT INTO gives (EmailAddress, TransactionNo) VALUES (%s, %s)'
    fundsInsert = 'INSERT INTO funds (TransactionNo, FundNo) VALUES (%s, %s)'
    donatesUpdate = 'UPDATE donates SET DonationsToFund = %s WHERE FundNo = %s AND EmailAddress = %s'

    checkDonor = 'SELECT DonationsToFund FROM donates WHERE EmailAddress = %s AND FundNo = %s'
    checkTableAI = 'SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s'

    for u in userInfo:
        dbCursor.execute(userInsert, u)

    for f in FundInfo:
        dbCursor.execute(checkTableAI, ("test", "fundraiser"))
        fundID = dbCursor.fetchone()[0]
        dbCursor.execute(fundraiserInsert, f[1:])
        dbCursor.execute(ownsInsert, (f[0], fundID))

    for t in TranInfo:
        dbCursor.execute(checkTableAI, ("test", "donation"))
        tranID = dbCursor.fetchone()[0]
        dbCursor.execute(donationInsert, (t[3], t[2]))
        dbCursor.execute(givesInsert, (t[1], tranID))
        dbCursor.execute(fundsInsert, (tranID, t[0]))
        dbCursor.execute(checkDonor, (t[1], t[0]))
        currentDonateAmount = dbCursor.fetchone()
        if currentDonateAmount is None:
            dbCursor.execute(donatesInsert, (t[1], t[0], t[2]))
        else:
            dbCursor.execute(donatesUpdate, (t[2] + currentDonateAmount[0], t[0], t[1]))
        dbCursor.execute("UPDATE FUNDRAISER SET Balance = Balance + %d WHERE FundID = %d" % (t[2], t[0]))

    dbConnection.commit()

    dbCursor.close()
    dbConnection.close()

if __name__ == "__main__":
    main()
