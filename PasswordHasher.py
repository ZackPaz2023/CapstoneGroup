from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password):
    hashed_password = ph.hash(password)

    return hashed_password


def verify_password(password, hashedPassword):

    try:
        correctPassword = ph.verify(hashedPassword, password)
    except:
        correctPassword = False

    return correctPassword

def check_for_rehash(hash):
    return ph.check_needs_rehash(hash)
