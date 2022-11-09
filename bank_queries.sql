-- TESTED
-- Return all the donations a User has given
SET @user_email = '';

SELECT *
FROM DONATION
WHERE TransactionID IN
	(SELECT TransactionNo
	FROM GIVES INNER JOIN USER ON EmailAddress = Email
	WHERE Email = user_email);

-- NOT TESTED
-- Return the top 5 donations of a fundraiser
SET @fid = 0;

SELECT DonationAmount
FROM DONATION
WHERE TransactionID IN 
	(SELECT TransactionNo
	FROM FUNDS
	INNER JOIN FUNDRAISER ON FundNo = fid AND FundID = fid)
ORDER BY DonationAmount DESC
LIMIT 5;

-- TESTED
-- Return the 5 most recent donations of a fundraiser
SELECT DonationAmount, TransactionDate
FROM DONATION
WHERE TransactionID IN 
	(SELECT TransactionNo
	FROM FUNDS
	INNER JOIN FUNDRAISER ON FundNo = fid AND FundID = fid)
ORDER BY TransactionDate DESC
LIMIT 5;

-- TESTED
-- Return all the donations of a given fundraiser
SET @fund = 0;

SELECT DonationAmount, TransactionDate
FROM DONATION
WHERE TransactionID IN
	(SELECT TransactionNo
	FROM FUNDS INNER JOIN FUNDRAISER ON FundNo = FundID
	WHERE FundID = fund);

-- TESTED
-- Return the user's profile info
SET @user_email = "";

SELECT Email, Name, PhoneNumber, ZipCode, StreetAddress, State, City, Country
FROM USER
WHERE Email = user_email;

-- TESTED
-- Return the total of all the donations of a given fundraiser
SELECT SUM(DonationAmount) 
FROM DONATION
INNER JOIN FUNDS ON DONATION.TransactionID = FUNDS.TransactionNo
WHERE FundNo = fund;

-- TESTED
-- Return the title of all fundraisers
SELECT Title
FROM FUNDRAISER;

-- TESTED
-- Balance returns NULL, since we never update value after inputting the donations from the fundraiser
-- Return the list of all fundraisers a user has created
SET @user_email = "";

SELECT Title, Description, Goal, Balance, CreationDate, Timeframe
FROM OWNS INNER JOIN FUNDRAISER 
ON OWNS.FundNo = FUNDRAISER.FundID
WHERE EmailAddress = user_email;

-- NOT TESTED (This should work once Balance works)
-- Return a list of all fundraisers who has reached its goal
SELECT Title
FROM FUNDRAISER
WHERE Balance >= Goal;

-- TESTED
-- Return the list of all fundraisers created before some date
SET @target_date = '';

SELECT Title
FROM FUNDRAISER
WHERE target_date < CreationDate;

-- TESTED
-- Returns a table of TransactionNo, These are the unique keys
-- of the donations.
-- fund = Fundraiser key
-- Return all donations in a fundraiser that are greater than some amount
SET @target_amount = 0;

SELECT TransactionNo
FROM FUNDS INNER JOIN FUNDRAISER ON FUNDS.FundNo = FUNDRAISER.FundID
WHERE FundNo = fund AND TransactionNo IN
	(SELECT TransactionID
    FROM DONATION
    WHERE target_amount < DonationAmount);
    
-- TESTED
-- Return all the fundraisers a user has donated to
SELECT Title, DonationsToFund
FROM DONATES INNER JOIN FUNDRAISER ON FundNo = FundID
WHERE EmailAddress = user_email;

-- TESTED
-- Return all the fundraisers a user owns
SELECT Title
FROM OWNS INNER JOIN FUNDRAISER ON FundNo = FundID
WHERE EmailAddress = user_email;

-- NOT TESTED
-- Return all fundraisers with a certain tag
SET @target_tag = "";

SELECT Title
FROM TAGS INNER JOIN FUNDRAISER ON TAGS.FundNo = FUNDRAISER.FundID
WHERE Tag = target_tag;
