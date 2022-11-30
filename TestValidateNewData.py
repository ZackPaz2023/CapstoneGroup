import ValidateNewData
import unittest


class ValidationTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_phone_num_reformat(self):
        self.assertEqual(ValidateNewData.reformat_phone_num("(816)-604-0506"), "816-604-0506")

    def test_good_phone_num(self):
        self.assertTrue(ValidateNewData.valid_phone_num("816-604-0506"))

    def test_bad_phone_num1(self):
        self.assertFalse(ValidateNewData.valid_phone_num("816-604-05077"))

    def test_bad_phone_num2(self):
        self.assertFalse(ValidateNewData.valid_phone_num("816-604-050a"))

    def test_bad_phone_num3(self):
        self.assertFalse(ValidateNewData.valid_phone_num("816-604"))

    def test_bad_phone_num4(self):
        self.assertFalse(ValidateNewData.valid_phone_num("816-604-050#"))

    def test_good_routing_num(self):
        self.assertTrue(ValidateNewData.valid_routing_number("110110110"))

    def test_bad_routing_num1(self):
        self.assertFalse(ValidateNewData.valid_routing_number("111111111"))

    def test_bad_routing_num2(self):
        self.assertFalse(ValidateNewData.valid_routing_number("11111111"))

    def test_bad_routing_num3(self):
        self.assertFalse(ValidateNewData.valid_routing_number("11111111a"))

    def test_valid_password1(self):
        self.assertTrue(ValidateNewData.valid_password("aPPledOg74^#"))

    def test_valid_password2(self):
        self.assertTrue(ValidateNewData.valid_password("aPPledOg74<<"))

    def test_valid_password3(self):
        self.assertTrue(ValidateNewData.valid_password("aPPledOg74||"))

    def test_bad_password1(self):
        self.assertFalse(ValidateNewData.valid_password("Badpassword"))

    def test_bad_password2(self):
        self.assertFalse(ValidateNewData.valid_password("1@Thispasswordiswaaaaaaytoolong"))

    def test_bad_password3(self):
        self.assertFalse(ValidateNewData.valid_password("password"))

    def test_bad_password4(self):
        self.assertFalse(ValidateNewData.valid_password("password%"))

    def test_bad_password5(self):
        self.assertFalse(ValidateNewData.valid_password("Badpassword2"))

    def test_card_num(self):
        self.assertTrue(ValidateNewData.valid_card_number("1111222233334444"))

    def test_bad_card_num1(self):
        self.assertFalse(ValidateNewData.valid_card_number("111122223333444a"))

    def test_bad_card_num2(self):
        self.assertFalse(ValidateNewData.valid_card_number("111122223333444a"))

    def test_good_email1(self):
        self.assertTrue(ValidateNewData.valid_email("validemail59@gmail.com"))

    def test_good_email2(self):
        self.assertTrue(ValidateNewData.valid_email("valid.email59@gmail.com"))

    def test_bad_email1(self):
        self.assertFalse(ValidateNewData.valid_email("invalidemail59@gmail"))

    def test_bad_email2(self):
        self.assertFalse(ValidateNewData.valid_email("invalidemail59@gmail.c"))

    def test_bad_email3(self):
        self.assertFalse(ValidateNewData.valid_email("invalidemail59"))

    def test_bad_email4(self):
        self.assertFalse(ValidateNewData.valid_email("invali@demail59@gmail"))

    def test_bad_email5(self):
        self.assertFalse(ValidateNewData.valid_email(".invalidemail59@gmail.com"))

    def test_valid_zip_code1(self):
        self.assertTrue(ValidateNewData.valid_zip_code("64112"))

    def test_valid_zip_code2(self):
        self.assertTrue(ValidateNewData.valid_zip_code("64112-4499"))

    def test_invalid_zip_code1(self):
        self.assertFalse(ValidateNewData.valid_zip_code("64112-449"))

    def test_invalid_zip_code2(self):
        self.assertFalse(ValidateNewData.valid_zip_code("64112-44559"))

    def test_invalid_zip_code3(self):
        self.assertFalse(ValidateNewData.valid_zip_code("64112-445a"))

    def test_invalid_zip_code4(self):
        self.assertFalse(ValidateNewData.valid_zip_code("64112-4455-111"))

    def test_invalid_zip_code5(self):
        self.assertFalse(ValidateNewData.valid_zip_code("6411"))

    def test_invalid_zip_code6(self):
        self.assertFalse(ValidateNewData.valid_zip_code("6411%"))


if __name__ == '__main__':
    unittest.main()
