-- Return all the donations a User has given
SET @user_email = '';

SELECT DonationsToFund
FROM DONATES INNER JOIN USER ON EmailAddress = Email
WHERE Email = user_email;

-- Return the top 5 donations of a fundraiser
SET @fid = 0;

SELECT DonationAmount
FROM DONATION
INNER JOIN FUNDRAISER ON DONATION.TransactionID = fid AND 
FUNDRAISER.FundID = fid
ORDER BY DonationAmount DESC
LIMIT 5;

-- Return the 5 most recent donations of a fundraiser
SELECT DonationAmount
FROM DONATION
INNER JOIN FUNDRAISER ON DONATION.TransactionID = fid AND 
FUNDRAISER.FundID = fid
ORDER BY TransactionDate DESC
LIMIT 5;

-- Return all the donations of a given fundraiser
SET @fund = 0;

SELECT DonationsToFund
FROM DONATES INNER JOIN FUNDRAISER ON FundNo = FundID
WHERE FundID = fund;

-- Return the user's profile info
SET @user_email = "";

SELECT Email, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country
FROM USER
WHERE Email = user_email;

-- Return the total of all the donations of a given fundraiser
SELECT SUM(DonationAmount) 
FROM DONATION
INNER JOIN FUNDS ON DONATION.TransactionID = FUNDS.TransactionNo;

-- Return the title of all fundraisers
SELECT Title
FROM FUNDRAISER;

-- Return the list of all fundraisers a user has created
SET @user_email = "";

SELECT Title
FROM OWNS INNER JOIN FUNDRAISER 
ON OWNS.FundNo = FUNDRAISER.FundID
WHERE EmailAddress = user_email;

-- Return a list of all fundraisers who has reached its goal
SELECT Title
FROM FUNDRAISER
WHERE Balance >= Goal;

-- Return the list of all fundraisers created before some date
SET @target_date = '';

SELECT Title
FROM FUNDRAISER
WHERE target_date > CreationDate;

-- Return all donations in a fundraiser that are greater than some amount
SET @target_amount = 0;

SELECT *
FROM DONATES INNER JOIN FUNDRAISER ON DONATES.FundNo = FUNDRAISER.FundID
WHERE target_amount > DonationsToFund;
