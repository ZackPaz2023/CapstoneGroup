CREATE TABLE USER
	(Username char(30) NOT NULL,
	 Password char(30) NOT NULL,
	 Email char(50) NOT NULL,
	 Name char(30) NOT NULL,
	 PhoneNumber char(15) NOT NULL,
	 ZipCode Mediumint,
	 StreetAddress char(50),
	 State char(10),
	 City char(20),
	 Country char(20),
	 CardNumber Bigint,
	 ExpirationDate Date,
	 RouteNo int,
	 AccountNo Bigint,
	 PRIMARY KEY (Email));
     
CREATE TABLE FUNDRAISER
	(Title char(50) NOT NULL,
	 Description TEXT(1000),
	 Goal decimal(15, 2) NOT NULL CHECK (Goal > 0),
	 Balance decimal(15, 2) DEFAULT 0.00,
	 CreationDate Datetime CHECK (CreationDate >= '2022-01-01 00:00:00'),
	 Timeframe Datetime,
	 FundID int NOT NULL AUTO_INCREMENT,
	 PRIMARY KEY (FundID));
     
ALTER TABLE FUNDRAISER AUTO_INCREMENT=1001;
     
ALTER TABLE FUNDRAISER
	ADD CONSTRAINT timeframe_CHECK
		CHECK (Timeframe >= CreationDate);
        
CREATE TABLE DONATION
	(DonationAmount decimal(15, 2) CHECK (DonationAmount > 0),
	 TransactionID int NOT NULL AUTO_INCREMENT,
	 TransactionDate Datetime NOT NULL CHECK (TransactionDate >= '2022-01-01 00:00:00'),
	 PRIMARY KEY (TransactionID));
     
ALTER TABLE DONATION AUTO_INCREMENT=1;
     
CREATE TABLE OWNS
	(EmailAddress char(50) NOT NULL,
	 FundNo int NOT NULL,
	 PRIMARY KEY (EmailAddress, FundNo),
	 FOREIGN KEY (EmailAddress) REFERENCES USER (Email),
	 FOREIGN KEY (FundNo) REFERENCES FUNDRAISER (FundID));

CREATE TABLE DONATES
	(EmailAddress char(50) NOT NULL,
	 FundNo int NOT NULL,
	 DonationsToFund decimal(15, 2) CHECK (DonationsToFund > 0),
	 PRIMARY KEY (EmailAddress, FundNo),
	 FOREIGN KEY (EmailAddress) REFERENCES USER (Email),
	 FOREIGN KEY (FundNo) REFERENCES FUNDRAISER (FundID));
     
CREATE TABLE GIVES
	(EmailAddress char(50) NOT NULL,
	 TransactionNo int NOT NULL,
	 PRIMARY KEY (EmailAddress, TransactionNo),
	 FOREIGN KEY (EmailAddress) REFERENCES USER (Email),
	 FOREIGN KEY (TransactionNo) REFERENCES DONATION (TransactionID));


CREATE TABLE FUNDS
	(TransactionNo int NOT NULL,
	 FundNo int NOT NULL,
	 PRIMARY KEY (TransactionNo, FundNo),
	 FOREIGN KEY (TransactionNo) REFERENCES DONATION (TransactionID),
	 FOREIGN KEY (FundNo) REFERENCES FUNDRAISER (FundID));
