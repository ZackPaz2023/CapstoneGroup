def valid_email(email):
    # Acceptable ASCII ranges: 48-57, 64-90, 97-122, 45, 95
    if (email[0] == "." or email[0] == "_" or email[0] == "-" or email[0] == "@"):
        return False

    has_at = False
    has_address_period = False
    prev_char_period_or_dash = False
    for char in email:
        # First, determine whether or not the character is valid
        valid_char = False
        ascii_code = ord(char)
        if (ascii_code == 45):
            valid_char = True
        if (ascii_code == 46):
            valid_char = True
        elif (ascii_code == 95):
            valid_char = True
        elif (48 <= ascii_code <= 57):
            valid_char = True
        elif (64 <= ascii_code <= 90):
            valid_char = True
        elif (97 <= ascii_code <= 122):
            valid_char = True

        if (valid_char == False):
            return False

        # Second, determine if the character is in the correct position
        if (char != "." and char != "_" and char != "-"):
            prev_char_period_or_dash = False

        if (char == '@' and has_at == False):
            has_at = True
        elif (char == '@' and has_at == True):
            return False
        elif (char == "." and has_address_period == False):
            if (has_at):
                has_address_period = True
                prev_char_period_or_dash = True
            else:
                if (prev_char_period_or_dash):
                    return False
                else:
                    prev_char_period_or_dash = True
        elif (char == "." and has_address_period == True):
            return False
        elif (char == "-" or char == "_"):
            if (prev_char_period_or_dash):
                return False
            else:
                prev_char_period_or_dash = True

    if (prev_char_period_or_dash):
        return False

    if (len(email.split(".")[-1]) < 2):
        return False

    return True


def reformat_phone_num(phoneNum):
    formattedNum = ""
    area_code_formatted = False
    prefix_formatted = False
    digits = 0
    for char in phoneNum:
        valid_char = False
        ascii_code = ord(char)
        if (40 <= ascii_code <= 41):
            valid_char = True
        elif (48 <= ascii_code <= 57):
            valid_char = True
            if (digits < 3):
                formattedNum += char
                digits += 1
            elif (digits >= 3):
                if (area_code_formatted == False or prefix_formatted == False):
                    digits = 1
                    formattedNum += "-"
                    formattedNum += char
                    if (area_code_formatted == False):
                        area_code_formatted = True
                    elif (prefix_formatted == False):
                        prefix_formatted = True
                else:
                    formattedNum += char


        elif (ascii_code == 45):
            valid_char = True
            formattedNum += char
            digits = 0
            if (area_code_formatted == False):
                area_code_formatted = True
            elif (prefix_formatted == False):
                prefix_formatted = True

        if (valid_char == False):
            return phoneNum

    return formattedNum


def valid_phone_num(phoneNum):
    for char in phoneNum:
        valid_char = False
        ascii_code = ord(char)
        if (40 <= ascii_code <= 41):
            valid_char = True
        elif (48 <= ascii_code <= 57):
            valid_char = True
        elif (ascii_code == 45):
            valid_char = True

        if (valid_char == False):
            return False

    if (len(phoneNum) == 12):
        return True
    else:
        return False


def valid_password(password):
    if not (8 <= len(password) <= 20):
        return False
    has_upper_case = False
    for char in password:
        ascii_code = ord(char)
        if (65 <= ascii_code <= 90):
            has_upper_case = True

    if (has_upper_case):
        return True
    else:
        return False


def valid_zip_code(zipCode):
    has_dash = False
    for char in zipCode:
        ascii_code = ord(char)
        if ((48 <= ascii_code <= 57) or ascii_code == 45) == False:
            return False
        if (ascii_code == 45):
            has_dash = True

    if (has_dash):
        zipCode = zipCode.split('-')
        if (len(zipCode[0]) != 5 or len(zipCode[1]) != 4 or len(zipCode) != 2):
            return False
    else:
        if (len(zipCode) != 5):
            return False

    return True


def valid_card_number(cardNum):

    try:
        int(cardNum)
    except ValueError:
        return False

    if len(cardNum) != 16:
        return False

    return True


def valid_routing_number(routingNum):
    if (len(routingNum) != 9):
        return False
    try:
        int(routingNum)
    except ValueError:
        return False

    total = 0
    for x in range(9):
        if x % 3 == 0:
            total += int(routingNum) * 3
        if x % 3 == 1:
            total += int(routingNum) * 7
        if x % 3 == 2:
            total += int(routingNum) * 1

    if (total % 10 != 0):
        return False
    else:
        return True


def valid_length(data, correctLength):
    if (len(data) == correctLength):
        return True
    else:
        return False


def valid_new_user_input(form_input, payment_type):
    valid_input = True
    flags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    # Check each field
    if not (5 <= len(form_input["Name"]) <= 40):
        valid_input = False
        flags[0] = 0
    if not valid_email(form_input["Email"]):
        valid_input = False
        flags[1] = 0
    if not (5 <= len(form_input["UserName"]) <= 20):
        valid_input = False
        flags[2] = 0
    if not valid_password(form_input["Password"]):
        valid_input = False
        flags[3] = 0
    if not valid_phone_num(reformat_phone_num(form_input["PhoneNumber"])):
        valid_input = False
        flags[4] = 0
    if len(form_input["StreetAddress"]) < 8:
        valid_input = False
        flags[5] = 0
    if len(form_input["City"]) < 2:
        valid_input = False
        flags[6] = 0
    if len(form_input["State"]) < 2:
        valid_input = False
        flags[7] = 0
    if not valid_zip_code(form_input["ZipCode"]):
        valid_input = False
        flags[8] = 0
    if len(form_input["Country"]) < 5:
        valid_input = False
        flags[9] = 0

    # If payment type is creditCard
    if (payment_type == "creditCard"):
        if not valid_card_number(form_input["CardNumber"]):
            valid_input = False
            flags[10] = 0
        if len(form_input["cvv"]) != 3:
            valid_input = False
            flags[11] = 0
    # If payment type is bankInfo
    if (payment_type == "bankInfo"):
        if not (5 <= len(form_input["AccountNumber"]) <= 17):
            valid_input = False
            flags[12] = 0
        if not valid_routing_number(form_input["RoutingNumber"]):
            valid_input = False
            flags[13] = 0

    return (valid_input, flags)


def valid_new_fundraiser_input(form_input):
    valid_input = True

    if (len(form_input["title"]) < 1):
        valid_input = False
    try:
        if (int(form_input["goal"]) <= 50):
            valid_input = False
    except ValueError:
        valid_input = False

    return valid_input


def valid_new_donation_input(form_input, is_guest):
    valid_input = True

    try:
        if (int(form_input["amount"]) < 1):
            valid_input = False
    except ValueError:
        valid_input = False

    if (is_guest):
        if not valid_zip_code(form_input["ZipCode"]):
            valid_input = False
        if len(form_input["StreetAddress"]) < 8:
            valid_input = False
        if len(form_input["State"]) < 2:
            valid_input = False
        if len(form_input["City"]) < 2:
            valid_input = False
        if len(form_input["Country"]) < 5:
            valid_input = False

        if not valid_card_number(form_input["CardNumber"]):
            valid_input = False
        if len(form_input["cvv"]) != 3:
            valid_input = False

        if not (5 <= len(form_input["AccountNumber"]) <= 17):
            valid_input = False
        if not valid_routing_number(form_input["RoutingNumber"]):
            valid_input = False
    else:
        if len(form_input["cvv"]) != 3:
            valid_input = False
        if not valid_routing_number(form_input["RoutingNumber"]):
            valid_input = False

    return valid_input
