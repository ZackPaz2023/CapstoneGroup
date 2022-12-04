import unittest
import PasswordHasher


class HasherTest(unittest.TestCase):

    def test_hash(self):
        password = "Password%^78"
        hashedPassword = PasswordHasher.hash_password(password)
        self.assertNotEqual(password, hashedPassword)

    def test_verify_password(self):
        password = "Password%^78"
        hashedPassword = PasswordHasher.hash_password(password)
        self.assertTrue(PasswordHasher.verify_password(password, hashedPassword))

    def test_incorrect_password(self):
        password = "Password%^78"
        hashedPassword = PasswordHasher.hash_password(password)
        self.assertFalse(PasswordHasher.verify_password("badpassword", hashedPassword))


if __name__ == '__main__':
    unittest.main()
